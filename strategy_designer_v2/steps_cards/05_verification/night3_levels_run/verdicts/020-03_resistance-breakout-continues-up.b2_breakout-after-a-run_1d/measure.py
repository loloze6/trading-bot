import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    BRK = "debug_info.components.break.last_history_value"
    RUN = "debug_info.components.runup.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            active = f != 0
            n_act = int(active.sum())
            if n_act == 0:
                continue
            n_active += n_act
            brk = pd.to_numeric(df[BRK], errors="coerce").values if BRK in df.columns else np.full(len(df), np.nan)
            run = pd.to_numeric(df[RUN], errors="coerce").values if RUN in df.columns else np.full(len(df), np.nan)
            close = pd.to_numeric(df["close"], errors="coerce").values
            # 20-day return: recorded raw value, or recomputed from closes inside the window when missing
            run_px = np.full(len(df), np.nan)
            if len(df) > 20:
                run_px[20:] = close[20:] / close[:-20] - 1.0
            run_use = np.where(np.isnan(run), run_px, run)
            with np.errstate(invalid="ignore"):
                situ = (brk > 0) & (run_use > 0)
            agree = active & situ & (f > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "mean unusual 5-bar move of long cases (return from signal close minus coin's normal 5-bar drift)"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases and slope > 0; reject: mean < 0 with t <= -2 over >= 30 cases"
    slope_name = "OLS slope of unusual move on forecast at entry"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the close has just "
                           "broken above a 90-day swing-high level (break reading > 0) after a rising 20-day return; "
                           "the config's forecast does not follow the plan's situation and side."),
            "reading": "Situation taken as break raw value > 0 and 20-day return > 0 with a positive forecast.",
        }

    # ---------- 2. criterion ----------
    unusual = []
    f_entry = []
    for coin in sorted(bars):
        # normal drift: mean of non-overlapping 5-bar returns over all windows of the coin
        grid_rets = []
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                r = c[i + H] / c[i] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w in sorted(bars[coin]):
            df = bars[coin][w]
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            # bets on the long side: rise of the forecast >= band from its lowest level since last bet
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for t in range(n):
                ft = f[t]
                if ft <= 0:
                    ref = 0.0
                    continue
                if t == 0 or f[t - 1] <= 0:
                    ref = 0.0
                ref = min(ref, ft)
                if ft - ref >= BAND:
                    bet[t] = True
                    ref = ft
            # one case per 5-bar grid cell: the first bet bar in the cell
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
                unusual.append(r - drift)
                f_entry.append(f[t])

    u = np.asarray(unusual, dtype=float)
    x = np.asarray(f_entry, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_stat = None
    if n_cases >= 2:
        sd = float(np.std(u, ddof=1))
        if sd > 0:
            t_stat = float(mean_u / (sd / np.sqrt(n_cases)))
    slope = None
    if n_cases >= 2 and np.unique(x).size >= 2:
        slope = float(stats.linregress(x, u).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif t_stat is not None and mean_u > 0 and t_stat >= 2 and slope_pass is True:
        status = "confirmed"
        decided = "Mean unusual move positive with t >= 2 over at least 30 cases and supporting slope above 0."
    elif t_stat is not None and mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        if t_stat is not None and t_stat >= 2:
            decided = "t of 2 or more but the supporting slope is at or below 0 (or undefined): inconclusive."
        else:
            decided = "t between -2 and 2 over at least 30 cases: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
            "threshold": threshold,
        },
        "supporting_check": {"name": slope_name, "value": slope, "passed": slope_pass},
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": ("A case is the first long bet bar (forecast rise >= 2 from its low since the last bet) in each "
                    "non-overlapping 5-bar grid cell of a window, its return taken from that bar's close over 5 bars "
                    "within the window, minus the coin's mean grid 5-bar return over all its windows."),
    }
