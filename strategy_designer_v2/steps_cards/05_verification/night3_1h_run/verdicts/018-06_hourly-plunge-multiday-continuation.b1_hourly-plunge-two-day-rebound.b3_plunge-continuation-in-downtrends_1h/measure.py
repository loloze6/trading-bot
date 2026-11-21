import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 96
    L30 = 720
    BAND = 2.0
    RAW = "debug_info.components.plunge.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            ret30 = close / pd.Series(close).shift(L30).values - 1.0
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            # 30-day return from closes where possible; else the detector's decision on that rule
            down30 = np.where(np.isfinite(ret30), ret30 < 0, regime == "trending")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            ret24 = close / pd.Series(close).shift(24).values - 1.0
            raw = np.where(np.isfinite(raw), raw, ret24)
            plunge = np.isfinite(raw) & (raw < 0)
            active = f != 0
            agree = active & (f < 0) & plunge & down30
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    threshold_txt = ("confirm: mean > 0 with t >= 2 and depth slope < 0; reject: t <= -2, "
                     "or confirm with depth slope > 0 and slope t >= 2; at least 30 cases")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean unusual 96-bar short-direction move", "value": None,
                             "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "independent cases": None},
            "decided_by": ("Fewer than 90% of the active bars are short forecasts on a 24-bar fall while the "
                           "30-day return is negative, as the plan's situation requires."),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    unusual_all = []
    depth_all = []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 96-bar returns over all windows
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                r = c[i + H] / c[i] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                if f[i] >= 0:
                    ref = 0.0
                    continue
                s = -f[i]
                if s - ref >= BAND:
                    bet[i] = True
                    ref = s
                else:
                    ref = min(ref, s)
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r):
                    continue
                unusual_all.append(-(r - drift))
                if t - L30 >= 0 and np.isfinite(c[t - L30]) and c[t - L30] != 0:
                    depth_all.append(c[t] / c[t - L30] - 1.0)
                else:
                    depth_all.append(np.nan)

    u = np.array(unusual_all, dtype=float)
    d = np.array(depth_all, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_u = None
    if n_cases > 1:
        sd = np.std(u, ddof=1)
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    m = np.isfinite(d) & np.isfinite(u)
    n_reg = int(m.sum())
    slope = None
    slope_t = None
    if n_reg >= 3 and np.std(d[m]) > 0:
        lr = stats.linregress(d[m], u[m])
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    sup_passed = None if slope is None else bool(slope < 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} independent cases pooled over coins, fewer than the plan's minimum of 30."
    elif t_u is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither the confirm nor the reject rule is met."
    elif t_u <= -2:
        status = "rejected"
        decided = "Reject rule: the mean unusual short-direction move has t <= -2."
    elif mean_u > 0 and t_u >= 2:
        if slope is not None and slope > 0 and slope_t is not None and slope_t >= 2:
            status = "rejected"
            decided = "Reject rule: the main measure confirms but the depth slope is above 0 with t >= 2."
        elif sup_passed:
            status = "confirmed"
            decided = "Confirm rule: mean unusual short-direction move above 0 with t >= 2 and depth slope below 0."
        else:
            status = "inconclusive"
            decided = "The main measure meets the confirm rule but the depth slope is not below 0 (nor above 0 with t >= 2)."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the t of the mean unusual move lies between -2 and 2 (or the mean is not above 0)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean unusual 96-bar short-direction move",
                         "value": mean_u,
                         "statistic": None if t_u is None else {"name": "t of the mean", "value": t_u},
                         "threshold": threshold_txt},
        "supporting_check": {"name": "slope of unusual short move on 30-day return",
                             "value": slope, "passed": sup_passed},
        "counts": {"independent cases": n_cases, "cases with 30-day return": n_reg,
                   "active bars": int(n_active)},
        "decided_by": decided,
        "reading": ("A case is the first bet bar (short forecast magnitude rising >= 2 above its lowest level since the "
                    "last bet, reset on flat) in each 96-bar grid cell from each window's first row, kept only if its "
                    "96-bar forward return lies in the window; the 30-day return is close[t]/close[t-720]-1 within the "
                    "window (cases without 720 prior bars are left out of the slope); the plan's fewer-than-30-cases "
                    "rule is applied as the minimum count giving 'not observable'."),
    }
