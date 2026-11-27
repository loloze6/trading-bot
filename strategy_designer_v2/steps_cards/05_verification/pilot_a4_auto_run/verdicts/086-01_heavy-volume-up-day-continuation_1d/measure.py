import json
import numpy as np
import pandas as pd
from scipy import stats

H = 5
BAND = 2.0
MIN_CASES = 30
COMP = "heavy_vol"


def _parse_comp(x):
    if isinstance(x, dict):
        return x
    if isinstance(x, str):
        try:
            v = json.loads(x)
            return v if isinstance(v, dict) else {}
        except Exception:
            return {}
    return {}


def _raw_heavy(df):
    flat = "debug_info.components.%s.last_history_value" % COMP
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce").reset_index(drop=True)
    if "debug_info.components" in df.columns:
        vals = []
        for x in df["debug_info.components"].tolist():
            d = _parse_comp(x).get(COMP, {})
            v = d.get("last_history_value") if isinstance(d, dict) else None
            try:
                vals.append(float(v) if v is not None else np.nan)
            except Exception:
                vals.append(np.nan)
        return pd.Series(vals, dtype=float)
    return pd.Series(np.nan, index=range(len(df)), dtype=float)


def _prep(df):
    df = df.sort_values("timestamp").reset_index(drop=True)
    close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
    vol = pd.to_numeric(df["volume"], errors="coerce").reset_index(drop=True)
    fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).reset_index(drop=True)
    raw = _raw_heavy(df)
    regime = df["regime"].astype(str).reset_index(drop=True) if "regime" in df.columns else pd.Series([""] * len(df))
    ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce").reset_index(drop=True)
    return close, vol, fc, raw, regime, ts


def measure(bars):
    # ---------- situation check ----------
    n_active = 0
    n_ok = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            close, vol, fc, raw, regime, ts = _prep(df)
            up = close > close.shift(1)
            up_known = close.shift(1).notna() & close.notna()
            vr_pc = vol / vol.shift(1).rolling(20, min_periods=20).mean() - 1.0
            heavy = raw.where(raw.notna(), vr_pc)
            heavy_known = heavy.notna()
            heavy_ok = heavy > 0
            trending = regime == "trending"
            for i in range(len(df)):
                f = fc.iloc[i]
                if f == 0:
                    continue
                n_active += 1
                if up_known.iloc[i] and heavy_known.iloc[i]:
                    sit = bool(up.iloc[i]) and bool(heavy_ok.iloc[i])
                else:
                    sit = bool(trending.iloc[i])
                if sit and f > 0:
                    n_ok += 1
    agreement = (n_ok / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean unusual move per case over 5 bars (long, minus the coin's normal 5-bar drift)"
    thr = "confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2; at least 30 cases"
    reading = ("The situation is checked as 'close above the previous close and volume above its prior 20-bar mean' "
               "on the long side (the falling-calm profile is added by code and not recomputed), using the recorded "
               "heavy_vol raw value (ratio minus 1) where present, else the volume recomputed inside the window, else "
               "the detector's 'trending' regime on bars without a previous close; cases are bets (forecast rises of at "
               "least 2 points from its lowest level since the last bet, from 0 after a flat), the first per 5-bar "
               "grid cell of each window, equally weighted, the t clusters cases by UTC day, and fewer than 30 cases "
               "gives 'not observable' as the workflow requires.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are long bars of the plan's situation "
                           "(an up close on volume above its prior 20-day mean): the config's forecast and the "
                           "Fidelity disagree."),
            "reading": reading,
        }

    # ---------- normal drift per coin ----------
    drift = {}
    for coin in sorted(bars):
        rets = []
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            close = _prep(df)[0].values
            for t in range(0, len(close) - H, H):
                if np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0:
                    rets.append(close[t + H] / close[t] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    unusual, rawv, days = [], [], []
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            close, vol, fc, raw, regime, ts = _prep(df)
            c = close.values
            f = fc.values
            ref = 0.0
            used_cells = set()
            for i in range(len(f)):
                fi = f[i]
                if fi <= 0:
                    ref = 0.0
                    continue
                ref = min(ref, fi)
                if fi - ref >= BAND:
                    ref = fi
                    cell = i // H
                    if cell in used_cells:
                        continue
                    used_cells.add(cell)
                    if i + H >= len(c):
                        continue
                    if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                        continue
                    if not np.isfinite(drift.get(coin, np.nan)):
                        continue
                    r = c[i + H] / c[i] - 1.0
                    unusual.append(r - drift[coin])
                    rawv.append(raw.iloc[i])
                    d = ts.iloc[i]
                    days.append(d.strftime("%Y-%m-%d") if pd.notna(d) else "%s_%s_%d" % (coin, w, i))

    n = len(unusual)
    n_days = len(set(days))
    counts = {"cases": int(n), "days": int(n_days)}

    mean_u = float(np.mean(unusual)) if n > 0 else None
    t_val = None
    if n > 1:
        u = np.array(unusual)
        dev = pd.Series(u - u.mean()).groupby(pd.Series(days)).sum().values
        G = len(dev)
        if G > 1:
            var = (dev ** 2).sum() / n ** 2 * G / (G - 1)
            if var > 0:
                t_val = float(u.mean() / np.sqrt(var))

    rho = None
    if n > 2:
        x = np.array(rawv, dtype=float)
        y = np.array(unusual, dtype=float)
        m = np.isfinite(x) & np.isfinite(y)
        if m.sum() > 2 and np.nanstd(x[m]) > 0 and np.nanstd(y[m]) > 0:
            rho = float(stats.spearmanr(x[m], y[m]).correlation)
    sup_pass = None if rho is None else bool(rho > 0)

    main = {"name": main_name, "value": mean_u,
            "statistic": {"name": "t of the mean, cases of one day clustered",
                          "value": t_val} if t_val is not None else None,
            "threshold": thr}
    sup = {"name": "Spearman of heavy_vol raw value vs unusual move", "value": rho, "passed": sup_pass}

    if n < MIN_CASES:
        status = "not observable"
        decided = "Fewer than the plan's minimum of 30 cases over the coins and windows (%d)." % n
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so it meets neither the confirm nor the reject rule."
    elif mean_u > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is above 0 with t >= 2 and the Spearman correlation is above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the Spearman correlation is at or below 0 (or not computable): inconclusive by the plan."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
