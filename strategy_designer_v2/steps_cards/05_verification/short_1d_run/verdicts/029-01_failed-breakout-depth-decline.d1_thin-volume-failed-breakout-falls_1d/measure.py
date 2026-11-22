import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    PERIOD = 20
    FAILW = 3          # fail_window 4: breakout close 1 to 3 bars before the bar
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.thin_failed_breakout.last_history_value"

    total_active = 0
    agree_active = 0
    case_rows = []  # (short-direction unusual move, abs forecast on signal bar)

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        # coin's normal 5-bar drift: non-overlapping grid over all its windows
        grid_rets = []
        for w in sorted(wins.keys()):
            df = wins[w]
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan

        for w in sorted(wins.keys()):
            df = wins[w].reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(n, np.nan)

            # prior 20-day closing high at each bar, and breakout flags
            prior_high = np.full(n, np.nan)
            for j in range(PERIOD, n):
                seg = c[j - PERIOD:j]
                if np.all(np.isfinite(seg)):
                    prior_high[j] = seg.max()
            breakout = np.isfinite(prior_high) & np.isfinite(c) & (c > prior_high)

            # situation per bar
            situation = np.zeros(n, dtype=bool)
            for t in range(n):
                thin = np.isfinite(raw[t]) and raw[t] > 0
                computable = (t - FAILW) >= PERIOD
                if computable:
                    failed = False
                    for j in range(t - FAILW, t):
                        if breakout[j] and np.isfinite(c[t]) and c[t] < prior_high[j]:
                            failed = True
                            break
                    situation[t] = failed and thin
                else:
                    # not enough recorded history to rebuild from prices: rely on the raw value
                    situation[t] = thin

            active = f != 0
            total_active += int(active.sum())
            agree_active += int((active & situation & (f < 0)).sum())

            # bets on the short side: rise in short size of >= band from lowest level since last bet
            ref = 0.0
            prev_short = False
            bet = np.zeros(n, dtype=bool)
            for t in range(n):
                if f[t] < 0:
                    mag = -f[t]
                    if not prev_short:
                        ref = 0.0
                    if mag - ref >= BAND - 1e-12:
                        bet[t] = True
                        ref = mag
                    else:
                        ref = min(ref, mag)
                    prev_short = True
                else:
                    prev_short = False
                    ref = 0.0

            # one case per non-overlapping 5-bar grid cell
            seen_cells = set()
            for t in range(n):
                if not bet[t]:
                    continue
                cell = t // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0 and np.isfinite(drift)):
                    continue
                r = c[t + H] / c[t] - 1.0
                case_rows.append((-(r - drift), abs(f[t])))

    agreement = (agree_active / total_active) if total_active > 0 else 0.0
    passed = total_active > 0 and agreement >= 0.90

    threshold_txt = "mean short-direction unusual move > 0 with t >= 2 over at least 30 cases (reject: < 0 with t <= -2)"
    reading = ("Cases are the first short-side forecast rise of at least 2 points in each 5-bar grid cell "
               "(positions 0,5,10,... of each window) with a full 5-bar return inside the window; the larger half is "
               "abs(forecast) strictly above the median and the smaller half at or below it; situation bars in the first "
               "23 bars of a window, where the 20-day high cannot be rebuilt from recorded prices, are judged by raw value > 0.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean short-direction unusual 5-bar move", "value": None,
                             "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"cases": len(case_rows), "active bars": int(total_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are short bars of a thin-volume failed "
                           "breakout (close back below the prior 20-day closing high broken 1 to 3 bars earlier)."),
            "reading": reading,
        }

    moves = np.array([m for m, _ in case_rows], dtype=float)
    absf = np.array([a for _, a in case_rows], dtype=float)
    n_cases = int(len(moves))

    mean = float(np.mean(moves)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(moves, ddof=1))
        if sd > 0:
            t_stat = float(mean / (sd / np.sqrt(n_cases)))

    diff = None
    n_large = n_small = 0
    if n_cases > 0:
        med = float(np.median(absf))
        large = moves[absf > med]
        small = moves[absf <= med]
        n_large, n_small = int(len(large)), int(len(small))
        if n_large > 0 and n_small > 0:
            diff = float(np.mean(large) - np.mean(small))
    supp_pass = None if diff is None else bool(diff > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    elif t_stat is not None and mean > 0 and t_stat >= 2 and supp_pass:
        status = "confirmed"
        decided = "Mean short-direction unusual move above 0 with t >= 2 over at least 30 cases, and the larger-minus-smaller half difference above 0."
    elif t_stat is not None and mean < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean short-direction unusual move below 0 with t <= -2 over at least 30 cases."
    elif t_stat is not None and mean > 0 and t_stat >= 2:
        status = "inconclusive"
        decided = "The main measure meets the confirm rule but the supporting check difference is 0 or below (or not measurable)."
    else:
        status = "inconclusive"
        decided = "The t of the mean short-direction unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "mean short-direction unusual 5-bar move", "value": mean,
                         "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
                         "threshold": threshold_txt},
        "supporting_check": {"name": "larger-half minus smaller-half mean unusual move (by abs forecast)",
                             "value": diff, "passed": supp_pass},
        "counts": {"cases": n_cases, "larger half cases": n_large, "smaller half cases": n_small},
        "decided_by": decided,
        "reading": reading,
    }
