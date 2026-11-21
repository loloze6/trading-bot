import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.support_break.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            # situation: the close sits under a swing-low support level (raw value present and non-zero)
            situation = raw.notna() & (raw != 0)
            # expected side: short
            agree = active & situation & (f < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "t of the mean unusual 5-bar move of short cases, pooled",
                "value": None,
                "statistic": None,
                "threshold": "t >= 2 confirms, t <= -2 rejects",
            },
            "supporting_check": None,
            "counts": {"cases pooled across coins": 0, "active bars": n_active},
            "decided_by": ("Fewer than 90% of active bars are short bars on which the close is below a "
                           "touch-weighted 90-day swing-low support (non-zero raw component value)"
                           if n_active > 0 else "The forecast is never active, so the plan's short situation is never traded"),
            "reading": "Situation = non-zero raw component value (close under a swing-low level); side = forecast < 0.",
        }

    # ---------- 2. Criterion ----------
    unusual = []
    absf = []
    for coin, wins in bars.items():
        # coin's normal drift: mean 5-bar return on non-overlapping grid of all its windows
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            # detect short bets: forecast deepens on the short side by >= BAND
            # from its least-deep short level since the last bet (from 0 after flat / side change)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                fi = f[i]
                if not np.isfinite(fi) or fi >= 0:
                    ref = 0.0
                    continue
                m = -fi
                if m - ref >= BAND:
                    bet[i] = True
                    ref = m
                else:
                    ref = min(ref, m)
            # one case per non-overlapping 5-bar grid cell: first bet in the cell
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H])) or c[t] == 0:
                    continue
                r = c[t + H] / c[t] - 1.0
                unusual.append(-(r - drift))
                absf.append(abs(f[t]))

    unusual = np.array(unusual, dtype=float)
    absf = np.array(absf, dtype=float)
    n_cases = int(len(unusual))

    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    t_stat = None
    if n_cases >= 2:
        sd = float(np.std(unusual, ddof=1))
        t_stat = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    diff = None
    check_passed = None
    n_large = n_small = 0
    if n_cases >= 2:
        med = float(np.median(absf))
        large = absf > med
        small = ~large
        n_large, n_small = int(large.sum()), int(small.sum())
        if n_large > 0 and n_small > 0:
            diff = float(np.mean(unusual[large]) - np.mean(unusual[small]))
            check_passed = bool(diff > 0)
        else:
            check_passed = False

    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = f"Only {n_cases} cases pooled across coins, fewer than the plan's minimum of 30."
    elif t_stat is None:
        status = "inconclusive"
        decided_by = "The t of the mean unusual move could not be computed (zero dispersion), so neither rule is met."
    elif t_stat >= 2 and check_passed:
        status = "confirmed"
        decided_by = "The mean unusual move has t >= 2 and the larger-|forecast| half has a larger mean move than the smaller half."
    elif t_stat >= 2:
        status = "inconclusive"
        decided_by = "t >= 2 but the larger-|forecast| half does not show a larger mean move: inconclusive by the plan."
    elif t_stat <= -2:
        status = "rejected"
        decided_by = "The mean unusual move has t <= -2: after support breaks the price rises more than usual."
    else:
        status = "inconclusive"
        decided_by = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "t of the mean unusual 5-bar move of short cases, pooled",
            "value": mean_u,
            "statistic": {"name": "t of the mean", "value": t_stat} if t_stat is not None else None,
            "threshold": "t >= 2 (with check) confirms, t <= -2 rejects, between is inconclusive; at least 30 cases",
        },
        "supporting_check": {
            "name": "mean unusual move, larger-|forecast| half minus smaller half",
            "value": diff,
            "passed": check_passed,
        },
        "counts": {
            "cases pooled across coins": n_cases,
            "larger half": n_large,
            "smaller half": n_small,
        },
        "decided_by": decided_by,
        "reading": ("A case is the first short bet (forecast deepening >= 2 points from its least-deep short level since the "
                    "last bet, reset at flat) in each 5-bar grid cell from each window's first row, with its 5-bar return "
                    "inside the window; drift is the coin's mean 5-bar return on that grid over all its windows; the "
                    "larger half is |forecast| strictly above the median, the rest the smaller half; the situation is a "
                    "non-zero raw component value and the side is forecast < 0."),
    }
