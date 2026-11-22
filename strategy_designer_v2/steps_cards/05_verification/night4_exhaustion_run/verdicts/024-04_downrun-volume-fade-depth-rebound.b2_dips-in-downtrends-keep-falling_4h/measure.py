import numpy as np
import pandas as pd
from scipy import stats

H = 18
LOOKBACK = 180
BAND = 2.0
MIN_CASES = 30
RAW = "debug_info.components.streak_loss.last_history_value"


def _short_bets(fc):
    """Bars where the forecast falls (on the short side) by at least BAND from its
    least-short level since the last bet (reset to 0 after a flat or a change of side)."""
    bets = np.zeros(len(fc), dtype=bool)
    ref = 0.0
    prev_side = 0
    for i, f in enumerate(fc):
        side = 1 if f > 0 else (-1 if f < 0 else 0)
        if side != -1:
            ref = 0.0
            prev_side = side
            continue
        if prev_side != -1:
            ref = 0.0
        m = -f
        if m - ref >= BAND - 1e-12:
            bets[i] = True
            ref = m
        else:
            ref = min(ref, m)
        prev_side = -1
    return bets


def measure(bars):
    n_active = 0
    n_agree = 0
    case_rows = []

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        # coin's normal drift and usual move over H bars, non-overlapping, all windows
        grid_rets = []
        for w in sorted(wins.keys()):
            df = wins[w]
            c = df["close"].astype(float).to_numpy()
            for p in range(0, len(c) - H, H):
                if c[p] > 0 and np.isfinite(c[p]) and np.isfinite(c[p + H]):
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        grid_rets = np.asarray(grid_rets, dtype=float)
        if len(grid_rets) >= 2:
            drift = float(np.mean(grid_rets))
            usual = float(np.std(grid_rets, ddof=1))
        else:
            drift, usual = np.nan, np.nan

        for w in sorted(wins.keys()):
            df = wins[w].reset_index(drop=True)
            n = len(df)
            c = df["close"].astype(float).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            regime = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * n)
            raw = (pd.to_numeric(df[RAW], errors="coerce").to_numpy()
                   if RAW in df.columns else np.full(n, np.nan))

            ret30 = np.full(n, np.nan)
            if n > LOOKBACK:
                ret30[LOOKBACK:] = c[LOOKBACK:] / c[:-LOOKBACK] - 1.0

            # situation: month down and the current bar closed down (inside a down streak)
            month_down = np.where(np.isfinite(ret30), ret30 < 0, regime == "trending")
            down_close = np.zeros(n, dtype=bool)
            if n > 1:
                down_close[1:] = c[1:] < c[:-1]
            if n > 0:
                down_close[0] = np.isfinite(raw[0]) and raw[0] != 0
            situation = month_down & down_close

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            # cases: short bets, first one per H-bar grid cell
            bets = _short_bets(fc)
            seen = set()
            for i in np.where(bets)[0]:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                case_rows.append({
                    "coin": coin, "window": w, "r": r, "drift": drift,
                    "usual": usual, "ret30": ret30[i],
                })

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    reading = ("The situation is the bar closing below the previous close while the 180-bar return "
               "recomputed from closes is below 0 (the recorded regime 'trending' where the 180 prior "
               "closes are not in the window), on the short side; cases are the first short bet of each "
               "18-bar grid cell; the slope regresses the unscaled drift-adjusted return on the 30-day "
               "return pooled over coins, and its minimum of 30 cases applies to the cases that have a "
               "30-day return.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are short bars on a down "
                           "close with a negative 180-bar return, as the plan's Fidelity requires."),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows, columns=["coin", "window", "r", "drift", "usual", "ret30"])
    cases = cases[np.isfinite(cases["drift"]) & np.isfinite(cases["usual"]) & (cases["usual"] > 0)]
    strength = (-(cases["r"] - cases["drift"]) / cases["usual"]).to_numpy()
    n_cases = int(len(strength))

    mean_s, t_s = None, None
    if n_cases >= 2:
        mean_s = float(np.mean(strength))
        sd = float(np.std(strength, ddof=1))
        t_s = float(mean_s / (sd / np.sqrt(n_cases))) if sd > 0 else None
    elif n_cases == 1:
        mean_s = float(strength[0])

    sc = cases[np.isfinite(cases["ret30"])]
    n_slope = int(len(sc))
    slope, t_slope = None, None
    if n_slope >= 3 and np.std(sc["ret30"].to_numpy()) > 0:
        y = (sc["r"] - sc["drift"]).to_numpy()
        x = sc["ret30"].to_numpy()
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    slope_pass = None
    if t_slope is not None:
        slope_pass = bool(slope > 0 and t_slope >= 2)

    counts = {"cases": n_cases, "cases with 30-day return": n_slope}

    main = {
        "name": "mean strength of short-side drift-adjusted 18-bar return",
        "value": mean_s,
        "statistic": {"name": "ordinary t", "value": t_s} if t_s is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 30 cases",
    }
    support = {
        "name": "slope of drift-adjusted 18-bar return on 30-day return (t)",
        "value": t_slope,
        "passed": slope_pass,
    }

    if n_cases < MIN_CASES or n_slope < MIN_CASES:
        status = "not observable"
        decided_by = (f"The plan's minimum of 30 cases is not reached ({n_cases} cases, "
                      f"{n_slope} with a 30-day return).")
    elif (mean_s is not None and t_s is not None and mean_s < 0 and t_s <= -2) or \
         (t_slope is not None and t_slope <= -2):
        status = "rejected"
        if t_s is not None and mean_s < 0 and t_s <= -2:
            decided_by = "Reject: the mean strength is below 0 with t <= -2 over at least 30 cases."
        else:
            decided_by = "Reject: the supporting slope has t <= -2 over at least 30 cases."
    elif mean_s is not None and t_s is not None and mean_s > 0 and t_s >= 2:
        if slope_pass:
            status = "confirmed"
            decided_by = ("Confirm: the mean strength is above 0 with t >= 2 over at least 30 cases "
                          "and the supporting slope is positive with t >= 2.")
        else:
            status = "inconclusive"
            decided_by = ("Inconclusive: the main measure meets the confirm rule but the supporting "
                          "slope is not positive with t >= 2.")
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: the main measure's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
