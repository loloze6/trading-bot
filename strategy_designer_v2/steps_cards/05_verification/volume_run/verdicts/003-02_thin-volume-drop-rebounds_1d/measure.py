import json
import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RET_THR = -2.0
    VR_THR = 0.5
    MIN_EVENTS = 20
    EPS = 1e-9

    def _parse_cell(cell):
        if isinstance(cell, dict):
            return cell
        if isinstance(cell, str):
            try:
                v = json.loads(cell)
                return v if isinstance(v, dict) else None
            except Exception:
                return None
        return None

    def get_component(df, cid, field="last_history_value"):
        flat = f"debug_info.components.{cid}.{field}"
        if flat in df.columns:
            return pd.to_numeric(df[flat], errors="coerce").to_numpy(dtype=float)
        if "debug_info.components" in df.columns:
            out = np.full(len(df), np.nan)
            for i, cell in enumerate(df["debug_info.components"].to_numpy()):
                d = _parse_cell(cell)
                if not d:
                    continue
                c = d.get(cid)
                if isinstance(c, dict):
                    v = c.get(field)
                    try:
                        out[i] = float(v) if v is not None else np.nan
                    except Exception:
                        out[i] = np.nan
            return out
        return np.full(len(df), np.nan)

    def recompute_ret(close):
        r = close.pct_change()
        vol = r.rolling(20, min_periods=20).std()
        return (r / vol).to_numpy(dtype=float)

    def recompute_vr(volume):
        avg = volume.rolling(30, min_periods=30).mean()
        return (volume / avg).to_numpy(dtype=float)

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            active = np.isfinite(fc) & (fc != 0)
            if not active.any():
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            ret = get_component(df, "fall")
            vr = get_component(df, "volume")
            ret_fb = recompute_ret(close)
            vr_fb = recompute_vr(vol)
            ret = np.where(np.isfinite(ret), ret, ret_fb)
            vr = np.where(np.isfinite(vr), vr, vr_fb)
            with np.errstate(invalid="ignore"):
                sit = np.isfinite(ret) & np.isfinite(vr) & (ret <= RET_THR + EPS) & (vr <= VR_THR + EPS)
            agree = active & sit & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean excess 5-bar forward return after forecast>0 bars (vs coin's mean 5-bar return)"
    threshold = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; at least 20 independent events"
    reading = ("Raw fall size and volume ratio are read from the recorded 'fall' and 'volume' components' last_history_value "
               "(recomputed from prices only if missing); the coin's mean 5-bar return is taken on the non-overlapping grid "
               "(positions 0,5,10,... of each window) pooled over all windows; an event is dropped when it lies fewer than 5 bars "
               "after the previous counted event in the same window, and events without a full 5-bar forward return inside "
               "their window are left out.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of non-zero forecast bars are long bars with a 1-day vol-scaled return <= -2 "
                           "and a 30-bar volume ratio <= 0.5, so the config does not trade the plan's situation."),
            "reading": reading,
        }

    # ---------- coin mean 5-bar returns (non-overlapping grid, all windows) ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for p in range(0, len(c) - H, H):
                a, b = c[p], c[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- events ----------
    ex_list = []
    fc_list = []
    n_raw = 0
    for coin, wins in bars.items():
        cm = coin_mean.get(coin, np.nan)
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            last = None
            for p in range(len(df)):
                if not (np.isfinite(fc[p]) and fc[p] > 0):
                    continue
                n_raw += 1
                if p + H >= len(df):
                    continue
                a, b = c[p], c[p + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0 and np.isfinite(cm)):
                    continue
                if last is not None and p - last < H:
                    continue
                last = p
                ex_list.append(b / a - 1.0 - cm)
                fc_list.append(fc[p])

    ex = np.asarray(ex_list, dtype=float)
    fcs = np.asarray(fc_list, dtype=float)
    n = len(ex)

    mean = float(np.mean(ex)) if n > 0 else None
    t = None
    if n >= 2:
        sd = np.std(ex, ddof=1)
        if sd > 0:
            t = float(mean / (sd / np.sqrt(n)))
    slope = None
    if n >= 2 and np.std(fcs) > 0:
        slope = float(stats.linregress(fcs, ex).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    counts = {"independent events": int(n), "bars with forecast above 0": int(n_raw)}

    if n < MIN_EVENTS:
        status = "not observable"
        decided = f"Only {n} independent events, fewer than the plan's minimum of 20."
    elif t is not None and mean > 0 and t >= 2 and slope_pass:
        status = "confirmed"
        decided = "Mean excess return above 0 with t >= 2 and a positive slope on the forecast, with at least 20 independent events."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean excess return below 0 with t <= -2, with at least 20 independent events."
    elif t is not None and mean > 0 and t >= 2:
        status = "inconclusive"
        decided = "Confirming mean (t >= 2) but the slope of excess return on the forecast is 0 or below (or undefined)."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2 (or is undefined), meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": None if t is None else {"name": "one-sample t", "value": t},
            "threshold": threshold,
        },
        "supporting_check": {"name": "OLS slope of excess 5-bar return on forecast", "value": slope, "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
