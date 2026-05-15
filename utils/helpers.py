import os
import base64
import pandas as pd

def get_base64_bin_file(bin_file):
    if not os.path.exists(bin_file):
        return ""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def safe_pct(val, val_ant):
    if pd.isna(val) or pd.isna(val_ant) or not val_ant or val_ant == 0:
        return None
    return ((val - val_ant) / abs(val_ant)) * 100

def format_delta(delta):
    if delta is None:
        return '<span style="color:#6b7280;font-weight:600;font-size:13px;">N/D</span>'
    if delta > 0:
        return f'<span style="color:#16a34a;font-weight:600;font-size:13px;">↑ {delta:.1f}%</span>'
    elif delta < 0:
        return f'<span style="color:#dc2626;font-weight:600;font-size:13px;">↓ {abs(delta):.1f}%</span>'
    else:
        return '<span style="color:#6b7280;font-weight:600;font-size:13px;">→ 0.0%</span>'

def icon_color(delta):
    if delta is None: return "#6b7280"
    if delta > 0: return "#16a34a"
    elif delta < 0: return "#dc2626"
    else: return "#6b7280"
