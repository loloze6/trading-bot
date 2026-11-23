import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FALL = "debug_info.components.fall.last_history_value"
    VOLR = "debug_info.components.volume.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            # recomputed from prices inside the window (fallback)
            ret_p = close / close.shift(1) - 1.0
            vr_p = vol / vol.shift(1).rolling(20, min_periods=20).mean()
            ret_raw = pd.to_numeric(df[FALL], errors="coerce") if FALL in df.columns else pd.Series(np.nan, index=df.index)
            vr_raw = pd.to_numeric(df[VOLR], errors="coerce") if VOLR in df.columns else pd.Series(np.nan, index=df.index)
            ret = ret_raw.where(ret_raw.notna(), ret_p)
            vr = vr_raw.where(vr_raw.notna(), vr_p)
            situation = (ret < 0) & (vr >= 1.0 - 1e-12)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    threshold_txt = "confirm: mean > 0 with t >= 2 and slope t >= 1; reject: mean < 0 with t <= -2"
    main_name = "mean next-day excess return on forecast > 0 bars"
    sup_name = "OLS slope of next-day excess return on forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars are long bars on a down day with volume at or above its prior 20-day mean, as the Fidelity's situation requires.",
            "reading": "Situation computed from the recorded raw ret1 (fall) and volume-ratio values, recomputed from prices within the window where missing.",
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        rets_all = []
        per_win = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            rets_all.append(nxt.dropna().values)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            per_win.append((fc, nxt))
        allr = np.concatenate(rets_all) if rets_all else np.array([])
        if allr.size == 0:
            continue
        mu = float(np.mean(allr))
        for fc, nxt in per_win:
            m = (fc > 0) & nxt.notna()
            xs.extend(fc[m].values.tolist())
            ys.extend((nxt[m] - mu).values.tolist())

    x = np.asarray(xs, float)
    y = np.asarray(ys, float)
    n = int(y.size)

    mean_ex = float(np.mean(y)) if n > 0 else None
    t_mean = None
    if n > 1:
        sd = float(np.std(y, ddof=1))
        t_mean = float(mean_ex / (sd / np.sqrt(n))) if sd > 0 else 0.0

    slope = None
    t_slope = None
    if n > 2 and np.std(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr > 0 else 0.0
    slope_pass = None if t_slope is None else bool(slope > 0 and t_slope >= 1.0)

    reading = ("Active bars counted as bars with forecast > 0 and a next-day close in the same window; "
               "the coin's mean daily return is over all its close-to-close returns in all windows; "
               "the plan's 'fewer than 200 is inconclusive' is reported as 'not observable' per the workflow.")

    out = {
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_ex,
                         "statistic": None if t_mean is None else {"name": "ordinary t of the mean", "value": t_mean},
                         "threshold": threshold_txt},
        "supporting_check": {"name": sup_name, "value": t_slope, "passed": slope_pass},
        "counts": {"active bars": n},
        "reading": reading,
    }

    if n < 200:
        out["status"] = "not observable"
        out["decided_by"] = f"Only {n} active bars, below the plan's minimum of 200."
        return out

    if mean_ex > 0 and t_mean >= 2:
        if slope_pass:
            out["status"] = "confirmed"
            out["decided_by"] = "Mean next-day excess return above 0 with t >= 2 and a positive slope with t >= 1."
        else:
            out["status"] = "inconclusive"
            out["decided_by"] = "Mean next-day excess return has t >= 2 but the slope check fails (slope not positive with t >= 1)."
    elif mean_ex < 0 and t_mean <= -2:
        out["status"] = "rejected"
        out["decided_by"] = "Mean next-day excess return below 0 with t <= -2."
    else:
        out["status"] = "inconclusive"
        out["decided_by"] = "The t of the mean next-day excess return lies between -2 and 2."
    return out
