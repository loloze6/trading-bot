import numpy as np
import pandas as pd


def measure(bars):
    H = 18
    BAND = 2.0
    LB = 180
    COMP = "debug_info.components.streak_loss.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            raw = (pd.to_numeric(df[COMP], errors="coerce").values
                   if COMP in df.columns else np.full(n, np.nan))
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * n)
            prev_close = np.r_[np.nan, close[:-1]]
            ret30 = np.full(n, np.nan)
            if n > LB:
                ret30[LB:] = close[LB:] / close[:-LB] - 1.0
            for i in range(n):
                if f[i] == 0:
                    continue
                n_active += 1
                # gate: 30-day return > 0, recomputed from prices; the regime column where 180 past bars are not in the window
                if np.isfinite(ret30[i]):
                    gate = ret30[i] > 0
                else:
                    gate = regime[i] == "mean_reversion"
                # down-streak: the bar closed down (vs previous close in the window) and the streak loss is non-zero
                if np.isfinite(prev_close[i]):
                    down = close[i] < prev_close[i]
                else:
                    down = True
                streak = np.isfinite(raw[i]) and raw[i] != 0
                if gate and down and streak and f[i] > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean unusual 18-bar move after bets (return minus coin's normal 18-bar drift), pooled"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 independent cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 cases"
    sup_name = "mean unusual move, upper half minus lower half of 180-bar return at signal bar"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "independent cases": None},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars of a down-streak in a coin with a positive 30-day return, as the plan's situation requires.",
            "reading": "Situation = forecast > 0 on a bar that closed below the previous close with a non-zero streak_loss raw value and a positive 180-bar return (the regime column used where 180 past bars are not in the window).",
        }

    # ---------- 2. criterion ----------
    cases = []  # (unusual move, ret180)
    for coin, wins in bars.items():
        # coin's normal drift: mean 18-bar return on the non-overlapping grid of all its windows
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(close) - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            # bets: a rise of the long forecast of >= BAND from its lowest level since the last bet (0 after flat)
            bets = []
            low = 0.0
            for i in range(n):
                fi = f[i]
                if fi <= 0:
                    low = 0.0
                    continue
                if fi - low >= BAND:
                    bets.append(i)
                    low = fi
                else:
                    low = min(low, fi)
            seen = set()
            for i in bets:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                r180 = close[i] / close[i - LB] - 1.0 if i >= LB else np.nan
                cases.append((r - drift, r180))

    n_cases = len(cases)
    counts = {"independent cases": int(n_cases)}
    reading = ("A bet is the holding-period bet (long forecast rising >= 2 from its lowest level since the last bet, reset at flat), "
               "the first bet per 18-bar cell of each window is kept, cases without 18 bars ahead in the window are dropped, "
               "the supporting split puts cases with 180-bar return above the median in the upper half (others lower) and leaves out cases without 180 past bars in the window, "
               "and the situation's gate uses the regime column where the 180-bar return cannot be computed.")

    if n_cases == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": "Fewer than 30 independent cases (none).",
            "reading": reading,
        }

    um = np.array([c[0] for c in cases], dtype=float)
    r180 = np.array([c[1] for c in cases], dtype=float)
    mean = float(np.mean(um))
    if n_cases > 1 and np.std(um, ddof=1) > 0:
        t = float(mean / (np.std(um, ddof=1) / np.sqrt(n_cases)))
    else:
        t = float("nan")

    ok = np.isfinite(r180)
    sup_val = None
    sup_pass = None
    if ok.sum() >= 2:
        med = np.median(r180[ok])
        up = um[ok][r180[ok] > med]
        lo = um[ok][r180[ok] <= med]
        if len(up) > 0 and len(lo) > 0:
            sup_val = float(np.mean(up) - np.mean(lo))
            sup_pass = bool(sup_val > 0)
    counts["cases with 180-bar return"] = int(ok.sum())

    if n_cases < 30:
        status = "not observable"
        decided = f"Fewer than 30 independent cases ({n_cases})."
    elif np.isfinite(t) and mean > 0 and t >= 2:
        if sup_pass is True:
            status = "confirmed"
            decided = "The mean unusual move is above 0 with t >= 2 over at least 30 independent cases and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "A confirm-sized main result whose supporting check fails."
    elif np.isfinite(t) and mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2 over at least 30 independent cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": {"name": "t of the mean", "value": t if np.isfinite(t) else None},
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
