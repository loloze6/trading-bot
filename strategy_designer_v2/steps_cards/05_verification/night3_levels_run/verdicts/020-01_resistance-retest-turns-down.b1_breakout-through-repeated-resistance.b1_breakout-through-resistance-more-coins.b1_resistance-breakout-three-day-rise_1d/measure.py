import numpy as np
import pandas as pd
from scipy import stats

RAW = "debug_info.components.res_break.last_history_value"
POST = "debug_info.components.res_break.post_pipeline_value"
H = 3
BAND = 2.0
MIN_CASES = 30


def _long_bets(fc):
    """Bars where the forecast rises on the long side by at least BAND,
    measured from its lowest long level since the last bet (0 after flat/short)."""
    bets = np.zeros(len(fc), dtype=bool)
    base = 0.0
    for i, f in enumerate(fc):
        if not np.isfinite(f) or f <= 0:
            base = 0.0
            continue
        if f - base >= BAND:
            bets[i] = True
            base = f
        else:
            base = min(base, f)
    return bets


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(float)
            else:
                raw = np.full(len(df), np.nan)
            prev = np.r_[np.nan, close[:-1]]
            # a fresh upward cross through the level: raw break value > 0, and the
            # close rose from the day before (close[t-1] <= level < close[t])
            price_ok = np.where(np.isfinite(prev), close > prev, True)
            situation = np.isfinite(raw) & (raw > 0) & price_ok
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean excess 3-bar return over cases (return minus coin's 3-bar drift), pooled"
    thr = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; at least 30 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of a fresh "
                           "close above a 90-day swing-high level (raw break value > 0 after a rise from "
                           "the prior close), so the config does not trade the plan's situation."),
            "reading": "Situation bars are bars with a positive raw component value and a close above the previous close; the expected side is long.",
        }

    # ---------- 2. criterion ----------
    excess_all = []
    size_all = []
    for coin, wins in bars.items():
        # coin drift: mean non-overlapping 3-bar return over all windows
        grid_rets = []
        per_window = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            n = len(close)
            for s in range(0, n - H, H):
                r = close[s + H] / close[s] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            per_window.append(df)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for df in per_window:
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(float)
            post = (pd.to_numeric(df[POST], errors="coerce").to_numpy(float)
                    if POST in df.columns else np.full(len(df), np.nan))
            n = len(close)
            bets = _long_bets(fc)
            for s in range(0, n, H):
                idx = np.where(bets[s:min(s + H, n)])[0]
                if len(idx) == 0:
                    continue
                t = s + int(idx[0])
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                excess_all.append(r - drift)
                size_all.append(post[t])

    ex = np.asarray(excess_all, float)
    sz = np.asarray(size_all, float)
    n_cases = int(len(ex))

    mean_ex = float(np.mean(ex)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(ex, ddof=1))
        t_stat = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    slope = None
    m = np.isfinite(sz) & np.isfinite(ex)
    if m.sum() >= 3 and np.ptp(sz[m]) > 0:
        slope = float(stats.linregress(sz[m], ex[m]).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif mean_ex > 0 and t_stat >= 2 and slope_pass:
        status = "confirmed"
        decided = "The mean excess 3-bar return is positive with t >= 2 and the supporting slope is positive."
    elif mean_ex > 0 and t_stat >= 2:
        status = "inconclusive"
        decided = "The mean excess 3-bar return is positive with t >= 2 but the slope is 0 or below (or undefined)."
    elif mean_ex < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean excess 3-bar return is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess 3-bar return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
            "threshold": thr,
        },
        "supporting_check": {
            "name": "OLS slope of excess 3-bar return on post_pipeline_value at case bar",
            "value": slope,
            "passed": slope_pass,
        },
        "counts": {"cases": n_cases, "active bars": int(n_active)},
        "decided_by": decided,
        "reading": ("Cases are long-side forecast rises of at least 2 points (from the lowest long level since the last bet, "
                    "0 after flat), the first per 3-bar grid cell of each window, dropped when the 3-bar return leaves the window; "
                    "drift is the coin's mean non-overlapping 3-bar return over all its windows."),
    }
