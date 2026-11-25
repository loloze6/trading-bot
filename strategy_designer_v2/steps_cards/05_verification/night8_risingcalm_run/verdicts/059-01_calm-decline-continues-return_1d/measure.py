import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.scaled_decline.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            f = pd.to_numeric(d["forecast"], errors="coerce")
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            reg = d["regime"].astype(str) if "regime" in d.columns else pd.Series("unknown", index=d.index)
            active = f.notna() & (f != 0)
            calm = reg != "chop"
            situ = raw.notna() & (raw < 0) & calm
            agree = active & situ & (f < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The calm profile is taken as the recorded regime not being 'chop' (the volatility-percentile veto), "
               "the coin's mean 5-bar return is the mean of its non-overlapping 5-bar grid returns over all its windows, "
               "the regression pools all coins' grid bars with forecast < 0, and the one case per grid cell is the first "
               "short bet (rise of at least 2 points in short size from its lowest level since the last bet) in that cell "
               "with a full 5-bar forward return.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are bars where the 14-day vol-scaled return is below zero "
                           "in the calm profile with a short forecast (agreement %.3f)." % agreement),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    case_moves = []
    for coin, wins in bars.items():
        prepared = []
        grid_rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(d)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            grid = np.arange(0, n, H)
            for g in grid:
                if np.isfinite(fwd[g]):
                    grid_rets.append(fwd[g])
            prepared.append((close, f, fwd, grid, n))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for close, f, fwd, grid, n in prepared:
            # main measure: grid bars with forecast < 0
            for g in grid:
                if np.isfinite(f[g]) and f[g] < 0 and np.isfinite(fwd[g]):
                    xs.append(f[g])
                    ys.append(fwd[g] - drift)
            # short bets
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                fi = f[i]
                if not np.isfinite(fi) or fi >= 0:
                    ref = 0.0
                    continue
                m = -fi
                if m - ref >= BAND - 1e-12:
                    bet[i] = True
                    ref = m
                else:
                    ref = min(ref, m)
            for g in grid:
                for i in range(g, min(g + H, n)):
                    if bet[i] and np.isfinite(fwd[i]):
                        case_moves.append(-(fwd[i] - drift))
                        break

    n_grid = len(xs)
    n_cases = len(case_moves)

    slope = None
    tval = None
    if n_grid >= 3 and np.std(xs) > 0:
        lr = stats.linregress(np.array(xs), np.array(ys))
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    mean_move = float(np.mean(case_moves)) if n_cases > 0 else None
    check_pass = (mean_move > 0) if mean_move is not None else None

    counts = {"grid bars with forecast < 0": int(n_grid), "cases": int(n_cases)}

    if n_grid < 100 or n_cases < 30:
        status = "not observable"
        decided_by = ("Minimum count not reached: %d grid bars with forecast < 0 (need 100) and %d cases (need 30)."
                      % (n_grid, n_cases))
    elif tval is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and check_pass:
        status = "confirmed"
        decided_by = "The slope's t is 2 or more and the cases' mean unusual move in the short direction is positive."
    elif tval >= 2:
        status = "inconclusive"
        decided_by = "The slope's t is 2 or more but the supporting check fails (mean unusual move not above 0)."
    elif tval <= -2:
        status = "rejected"
        decided_by = "The slope's t is -2 or less: deeper declines are followed by relatively higher returns."
    else:
        status = "inconclusive"
        decided_by = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "OLS slope of 5-bar excess forward return on forecast, grid bars with forecast < 0",
            "value": slope,
            "statistic": {"name": "OLS t of slope", "value": tval} if tval is not None else None,
            "threshold": "confirm if t >= 2 (with supporting check), reject if t <= -2",
        },
        "supporting_check": {
            "name": "mean unusual move of short cases (>= 2 points) in short direction",
            "value": mean_move,
            "passed": check_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
