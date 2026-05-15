import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV

WINDOW_DAYS   = 180
FORECAST_DAYS = 7
RANDOM_STATE  = 42

FEATURES = [
    'dayofweek',
    'day',
    'month',
    'is_weekend',
    'lag_1',
    'lag_2',
    'lag_3',
    'lag_7',
    'rolling_mean_7',
    'rolling_std_7',
]

PARAM_GRID = {
    'n_estimators':      [50, 100, 200],
    'max_depth':         [5, 8, 10],
    'min_samples_split': [2, 5],
    'min_samples_leaf':  [1, 2],
}

def _build_features(df: pd.DataFrame) -> pd.DataFrame:
    """8 features temporales sin data leakage."""
    d    = df.copy()
    base = d['y'].shift(1)
    d['lag_1']          = d['y'].shift(1)
    d['lag_2']          = d['y'].shift(2)
    d['lag_3']          = d['y'].shift(3)
    d['lag_7']          = d['y'].shift(7)
    d['rolling_mean_7'] = base.rolling(7).mean()
    d['rolling_std_7']  = base.rolling(7).std()
    d['dayofweek']      = d['ds'].dt.dayofweek
    d['day']            = d['ds'].dt.day
    d['month']          = d['ds'].dt.month
    d['is_weekend']     = (d['ds'].dt.dayofweek >= 5).astype(int)
    return d

def _predict_step(model, history: list, dt) -> float:
    """Predice un paso con el historial actual."""
    n    = len(history)
    row  = pd.DataFrame([{
        'dayofweek':      dt.dayofweek,
        'day':            dt.day,
        'month':          dt.month,
        'is_weekend':     int(dt.dayofweek >= 5),
        'lag_1':          history[-1],
        'lag_2':          history[-2] if n >= 2 else history[0],
        'lag_3':          history[-3] if n >= 3 else history[0],
        'lag_7':          history[-7] if n >= 7 else history[0],
        'rolling_mean_7': np.mean(history[-7:]) if n >= 7 else np.mean(history),
        'rolling_std_7':  np.std(history[-7:])  if n >= 7 else 0.0,
    }])
    return max(0.0, float(model.predict(row[FEATURES])[0]))

def _recursive_forecast(model, history: list, future_dates: pd.Series) -> np.ndarray:
    """Predicción recursiva actualizando el historial en cada paso."""
    h, preds = history[:], []
    for dt in future_dates:
        p = _predict_step(model, h, dt)
        preds.append(p)
        h.append(p)
    return np.array(preds)

def _mape(y_true, y_pred) -> float:
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    mask = y_true != 0
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100) if mask.any() else 50.0

@st.cache_data(show_spinner=False, ttl=3600)
def train_model(daily_json: str):
    """
    Recibe el DataFrame serializado (para compatibilidad con cache_data).
    Retorna dict con predicciones, métricas y metadata.
    """
    daily       = pd.read_json(StringIO(daily_json))
    daily['ds'] = pd.to_datetime(daily['ds'])
    daily       = daily.sort_values('ds').tail(WINDOW_DAYS + FORECAST_DAYS)

    df_feat = _build_features(daily).dropna(subset=FEATURES)
    if len(df_feat) < 15:
        return None

    # ── Walk-forward validation (sin GridSearch → rápido)
    tscv     = TimeSeriesSplit(n_splits=3, test_size=FORECAST_DAYS)
    wf_mapes = []
    for tr_idx, te_idx in tscv.split(df_feat):
        if len(tr_idx) > WINDOW_DAYS:
            tr_idx = tr_idx[-WINDOW_DAYS:]
        tr = df_feat.iloc[tr_idx]
        te = df_feat.iloc[te_idx]
        if len(tr) < 15:
            continue
        rf_cv = RandomForestRegressor(
            n_estimators=100, max_depth=8,
            min_samples_leaf=2, min_samples_split=5,
            random_state=RANDOM_STATE, n_jobs=-1
        )
        rf_cv.fit(tr[FEATURES], tr['y'])
        h  = tr['y'].tolist()
        ps = []
        for i in range(len(te_idx)):
            p = _predict_step(rf_cv, h, te['ds'].iloc[i])
            ps.append(p)
            h.append(p)
        wf_mapes.append(_mape(te['y'].values, ps))

    mape_wf  = float(np.mean(wf_mapes)) if wf_mapes else 35.0
    mape_std = float(np.std(wf_mapes))  if wf_mapes else 10.0

    # ── GridSearchCV compacto
    tscv_gs = TimeSeriesSplit(n_splits=3)
    gs = GridSearchCV(
        RandomForestRegressor(random_state=RANDOM_STATE),
        param_grid=PARAM_GRID,
        cv=tscv_gs,
        scoring='neg_mean_squared_error',
        n_jobs=-1,
        verbose=0,
    )
    gs.fit(df_feat[FEATURES], df_feat['y'])
    best_rf = gs.best_estimator_

    # ── Forecast a 7 días futuros
    last_date    = daily['ds'].max()
    future_dates = pd.Series([last_date + pd.Timedelta(days=i+1) for i in range(FORECAST_DAYS)])
    preds = _recursive_forecast(best_rf, daily['y'].tolist(), future_dates)

    # ── Importancia de features
    feat_imp = dict(zip(FEATURES, best_rf.feature_importances_))
    feat_imp = dict(sorted(feat_imp.items(), key=lambda x: x[1], reverse=True))

    # ── Confianza: basada en MAPE walk-forward real
    penalty   = min(mape_std / max(mape_wf, 1), 0.2)
    confianza = max(0.0, min(100.0, (1 - (mape_wf / 120) - penalty) * 100))

    return {
        'preds':        preds.tolist(),
        'future_dates': [d.strftime('%Y-%m-%d') for d in future_dates],
        'hist_dates':   daily['ds'].dt.strftime('%Y-%m-%d').tolist(),
        'hist_y':       daily['y'].tolist(),
        'confianza':    confianza,
        'mape_wf':      mape_wf,
        'mape_std':     mape_std,
        'total_pred':   float(np.sum(preds)),
        'best_params':  gs.best_params_,
        'feat_imp':     feat_imp,
    }
