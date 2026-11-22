import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.bounce_near_low.last_history_value"

    def _num(df, col):
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
        return np.full(len(df), np.nan)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = _num(df, "close")
            fc = _num(df, "forecast")
            raw = _num(df, RAW)
            regime = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))
            n = len(df)
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                # falling-coin condition: 90-bar return < 0, from prices when the window holds 90 prior bars,
                # otherwise the detector's recorded decision (its component is not recorded)
                if t >= 90 and np.isfinite(close[t]) and np.isfinite(close[t - 90]) and close[t - 90] > 0:
                    falling = (close[t] / close[t - 90] - 1.0) < 0
                else:
                    falling = regime[t] == "mean_reversion"
                # graded rise: raw value (rise in usual moves x proximity, clipped at 0) > 0
                if np.isfinite(raw[t]):
                    rising = raw[t] > 0
                elif t >= 1 and np.isfinite(close[t]) and np.isfinite(close[t - 1]) and close[t - 1] > 0:
                    rising = close[t] / close[t - 1] - 1.0 > 0
                else:
                    rising = False
                if falling and rising and f < 0:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean unusual 5-bar move of the short bets, short direction"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases and slope > 0; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("The 90-bar return is recomputed from closes inside the window where 90 prior bars exist and taken from the "
               "recorded regime otherwise; a case is the first short bet (forecast falling >= 2 points below its least "
               "negative level since the last bet, from 0 after flat or a side change) in each 5-bar grid cell from each "
               "window's first row, cases whose 5-bar return leaves the window are dropped, and the drift is the coin's "
               "mean non-overlapping 5-bar return over all its windows.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars on a positive graded rise "
                           "in a coin with a negative 90-bar return, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    unusual = []
    absf = []
    for coin, wins in bars.items():
        # normal drift over all windows of the coin
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = _num(df, "close")
            fc = _num(df, "forecast")
            prepared.append((close, fc))
            for t in range(0, len(df) - H, H):
                c0, c1 = close[t], close[t + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    grid_rets.append(c1 / c0 - 1.0)
        if not prepared:
            continue
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan

        for close, fc in prepared:
            n = len(close)
            side = 0
            ref = 0.0
            bet_bars = []
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f):
                    continue
                s = int(np.sign(f))
                if s == 0:
                    side, ref = 0, 0.0
                    continue
                if s != side:
                    side, ref = s, 0.0
                a = abs(f)
                if a - ref >= BAND - 1e-12:
                    if s < 0:
                        bet_bars.append(t)
                    ref = a
                else:
                    ref = min(ref, a)
            seen_cells = set()
            for t in bet_bars:
                cell = t // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if t + H >= n:
                    continue
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0 and np.isfinite(drift)):
                    continue
                r = c1 / c0 - 1.0
                unusual.append(-(r - drift))
                absf.append(abs(fc[t]))

    unusual = np.asarray(unusual, dtype=float)
    absf = np.asarray(absf, dtype=float)
    n_cases = int(len(unusual))

    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    t_stat = None
    if n_cases >= 2:
        sd = float(np.std(unusual, ddof=1))
        if sd > 0:
            t_stat = float(mean_u / (sd / np.sqrt(n_cases)))
    slope = None
    if n_cases >= 3 and np.unique(absf).size >= 2:
        slope = float(stats.linregress(absf, unusual).slope)

    slope_passed = None if slope is None else bool(slope > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif t_stat is not None and mean_u > 0 and t_stat >= 2:
        if slope_passed:
            status = "confirmed"
            decided_by = "The mean unusual move is positive with t >= 2 over at least 30 cases and the slope on |forecast| is above 0."
        else:
            status = "inconclusive"
            decided_by = "The mean unusual move meets the confirm rule but the slope on |forecast| is not above 0."
    elif t_stat is not None and mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided_by = "The mean unusual move is negative with t <= -2 over at least 30 cases: prices rise after these bounces beyond drift."
    else:
        status = "inconclusive"
        decided_by = "With at least 30 cases, the t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "slope of unusual move (short) on |forecast|",
            "value": slope,
            "passed": slope_passed,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided_by,
        "reading": reading,
    }
