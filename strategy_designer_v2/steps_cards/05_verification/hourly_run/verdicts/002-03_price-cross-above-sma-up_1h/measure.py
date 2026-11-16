import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    RAW = "debug_info.components.above_sma200.last_history_value"

    # ---------- 1. Situation check: close above SMA200 (raw distance > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (raw > 0) & (f > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    threshold_txt = "confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; otherwise inconclusive"
    main_name = "OLS slope of next 24-bar return minus window mean 24-bar return on forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active_bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are bars where the close is above the "
                           "200-bar SMA with a long (positive) forecast, so the config does not trade the plan's "
                           "situation on its side."),
            "reading": "Situation taken as raw SMA200 distance > 0 with forecast > 0 on every bar with non-zero forecast.",
        }

    # ---------- 2. Criterion ----------
    xs, ys, rets, fpos = [], [], [], []
    windows_with_pos = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(d)
            idx = np.arange(0, n, H)
            idx = idx[idx + H < n]
            if len(idx) == 0:
                continue
            r = close[idx + H] / close[idx] - 1.0
            fi = f[idx]
            ok = np.isfinite(r) & np.isfinite(fi)
            r, fi = r[ok], fi[ok]
            if len(r) == 0:
                continue
            excess = r - r.mean()
            xs.append(fi)
            ys.append(excess)
            rets.append(r)
            fpos.append(fi > 0)
            if np.any(fi > 0):
                windows_with_pos += 1

    if xs:
        X = np.concatenate(xs)
        Y = np.concatenate(ys)
        R = np.concatenate(rets)
        P = np.concatenate(fpos)
    else:
        X = Y = R = np.array([])
        P = np.array([], dtype=bool)

    n_pos = int(P.sum())
    n_all = int(len(R))

    slope, tstat = None, None
    if n_all >= 3 and np.std(X) > 0:
        lr = stats.linregress(X, Y)
        slope = float(lr.slope)
        tstat = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # Supporting check: two-proportion z, share positive among forecast>0 vs all sampled bars
    z = None
    sup_passed = None
    if n_pos > 0 and n_all > 0:
        p1 = float(np.mean(R[P] > 0))
        p2 = float(np.mean(R > 0))
        pp = (p1 * n_pos + p2 * n_all) / (n_pos + n_all)
        se = np.sqrt(pp * (1 - pp) * (1.0 / n_pos + 1.0 / n_all))
        if se > 0:
            z = float((p1 - p2) / se)
            sup_passed = bool(z >= 1.96)

    counts = {
        "non-overlapping sampled cases with forecast > 0 pooled": n_pos,
        "windows containing such cases": int(windows_with_pos),
        "sampled cases pooled": n_all,
    }

    if n_pos < 150 or windows_with_pos < 3:
        status = "inconclusive"
        decided = ("Inconclusive: fewer than 150 pooled non-overlapping sampled cases with forecast > 0, "
                   "or fewer than 3 of the 6 windows contain such cases.")
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "Inconclusive: the slope's t-statistic could not be computed."
    elif slope > 0 and tstat >= 2:
        status = "confirmed"
        decided = "Confirm: the slope is positive with t >= 2."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "Reject: the slope is negative with t <= -2, so moves after price goes above the average tend to reverse."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": tstat} if tstat is not None else None,
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "share of positive 24-bar returns, forecast > 0 vs all sampled bars (two-proportion z)",
            "value": z,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The window's mean 24-bar return is the mean over that window's non-overlapping sampled bars "
                    "(positions 0, 24, 48, ... with a full 24-bar return inside the window), the regression is pooled "
                    "OLS with an intercept, and the supporting check counts as passed when its pooled two-proportion "
                    "z is at least 1.96 since the plan names no threshold for it."),
    }
