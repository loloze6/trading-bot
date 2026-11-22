import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LHV = "debug_info.components.vol_rise.last_history_value"
    H = 10
    BAND = 2.0
    MIN_CASES = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values.astype(float)
            n = len(df)
            # regime: 90-bar return above 0, from prices where the window holds 90 prior bars,
            # else the detector's recorded decision (its rule is ret90 > 0)
            ret90 = np.full(n, np.nan)
            if n > 90:
                ret90[90:] = close[90:] / close[:-90] - 1.0
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * n)
            regime_ok = np.where(np.isnan(ret90), reg == "trending", ret90 > 0)
            # the rise: the day's volatility-scaled return above 0 (raw component value)
            if LHV in df.columns:
                lhv = pd.to_numeric(df[LHV], errors="coerce").values.astype(float)
            else:
                lhv = np.full(n, np.nan)
            r1 = np.full(n, np.nan)
            if n > 1:
                r1[1:] = close[1:] / close[:-1] - 1.0
            rise = np.where(np.isnan(lhv), r1 > 0, lhv > 0)
            situation = regime_ok & rise
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    reading = ("Regime ret90>0 recomputed from closes where the window holds 90 prior bars, else the recorded "
               "regime=='trending'; the rise is last_history_value>0 (day's return>0 if missing); cases are "
               "long bets per the holding rule (forecast rise >=2 from its lowest level since the last bet, from 0 "
               "after a flat), the first per 10-bar grid cell from each window's first row; drift is the coin's mean "
               "10-bar grid return over all windows; the median split puts cases above the median in the upper half "
               "and at or below it in the lower half.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of active bars are long bars where the 90-bar return is above 0 and "
                           "the day's volatility-scaled return is a rise, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin drift: mean 10-bar return on the non-overlapping grid of all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            for p in range(0, len(c) - H, H):
                r = c[p + H] / c[p] - 1.0
                if np.isfinite(r):
                    rets.append(r)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    case_moves = []
    case_fc = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values.astype(float)
            n = len(df)
            ref = 0.0
            seen_cells = set()
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    ref = f
                    cell = t // H
                    if cell in seen_cells:
                        continue
                    seen_cells.add(cell)
                    if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and np.isfinite(drift[coin]):
                        r = c[t + H] / c[t] - 1.0
                        case_moves.append(r - drift[coin])
                        case_fc.append(f)
                else:
                    ref = min(ref, f)

    moves = np.array(case_moves, dtype=float)
    fcs = np.array(case_fc, dtype=float)
    n_cases = int(len(moves))

    mean_move = float(moves.mean()) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = moves.std(ddof=1)
        t_stat = float(mean_move / (sd / np.sqrt(n_cases))) if sd > 0 else None

    diff = None
    n_up = n_lo = 0
    if n_cases > 0:
        med = float(np.median(fcs))
        up = moves[fcs > med]
        lo = moves[fcs <= med]
        n_up, n_lo = int(len(up)), int(len(lo))
        if n_up > 0 and n_lo > 0:
            diff = float(up.mean() - lo.mean())
    sup_pass = (diff is not None and diff > 0)

    main = {
        "name": "mean 10-bar unusual move over cases (before costs)",
        "value": mean_move,
        "statistic": {"name": "t of the mean", "value": t_stat} if t_stat is not None else None,
        "threshold": "confirm t >= 2 over at least 30 cases; reject t <= -2 over at least 30 cases",
    }
    support = {
        "name": "upper-half minus lower-half mean unusual move (median forecast split)",
        "value": diff,
        "passed": bool(sup_pass) if n_cases > 0 else None,
    }
    counts = {"cases": n_cases, "upper half cases": n_up, "lower half cases": n_lo}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif t_stat is not None and t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "t >= 2 over at least 30 cases with the upper-minus-lower difference above 0 (confirm rule)."
    elif t_stat is not None and t_stat <= -2:
        status = "rejected"
        decided = "t <= -2 over at least 30 cases (reject rule)."
    elif t_stat is not None and t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the upper-minus-lower difference is at 0 or below (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 over at least 30 cases (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
