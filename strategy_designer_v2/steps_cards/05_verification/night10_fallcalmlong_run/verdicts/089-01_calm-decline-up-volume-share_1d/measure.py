import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.up_vol_share.last_history_value"
    PROFILE = "unknown"   # the regime that is not vetoed to "chop" = the falling calm profile

    def recompute_raw(df):
        # The component's exact output: up-close volume share of the last 20 bars minus 0.5.
        c = df["close"].astype(float)
        v = df["volume"].astype(float)
        up = (c.diff() > 0).astype(float)
        up[c.diff().isna()] = np.nan
        upv = (v * up).rolling(20, min_periods=20).sum()
        tot = v.rolling(20, min_periods=20).sum()
        return upv / tot.replace(0, np.nan) - 0.5

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            raw = raw.where(raw.notna(), recompute_raw(df))
            in_prof = df["regime"].astype(str) == PROFILE
            active = f != 0
            sit = in_prof & (raw > 0) & (f > 0)
            n_active += int(active.sum())
            n_agree += int((active & sit).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90 % of the bars with a non-zero forecast are long bars inside the falling calm "
                          "profile (regime not vetoed) with the up-day volume share above one half.",
            "reading": "The profile is read from the recorded regime ('unknown' = not vetoed to chop), the share from "
                       "the recorded raw value (recomputed from prices where missing).",
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    case_moves, case_days = [], []

    for coin, wins in bars.items():
        # coin's normal drift: mean 5-bar return on the non-overlapping grid of all its windows
        all_grid = []
        prepared = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = c[H:] / c[: n - H] - 1.0
            grid = np.arange(0, n, H)
            g = fwd[grid]
            all_grid.extend(list(g[~np.isnan(g)]))
            prepared.append((df, fwd, grid))
        if len(all_grid) == 0:
            continue
        drift = float(np.mean(all_grid))

        for df, fwd, grid in prepared:
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            in_prof = (df["regime"].astype(str) == PROFILE).values
            # main-measure sample
            for t in grid:
                if in_prof[t] and not np.isnan(fwd[t]) and not np.isnan(f[t]):
                    xs.append(float(f[t]))
                    ys.append(float(fwd[t] - drift))
            # cases: long-side rises of the forecast of at least the band, one per grid cell
            days = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D").astype(str).values
            low = 0.0
            used_cells = set()
            for t in range(len(df)):
                ft = f[t]
                if np.isnan(ft) or ft <= 0:
                    low = 0.0
                    continue
                if ft - low >= BAND:
                    low = ft
                    cell = t // H
                    if cell not in used_cells and not np.isnan(fwd[t]):
                        used_cells.add(cell)
                        case_moves.append(float(fwd[t] - drift))
                        case_days.append(days[t])
                else:
                    low = min(low, ft)

    xs = np.array(xs)
    ys = np.array(ys)
    n_grid = int(len(xs))
    n_pos = int((xs > 0).sum()) if n_grid else 0

    slope = None
    t_slope = None
    if n_grid >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr > 0 else None

    n_cases = len(case_moves)
    mean_case = float(np.mean(case_moves)) if n_cases else None
    case_t = None
    n_case_days = len(set(case_days))
    if n_cases >= 2:
        d = pd.Series(np.array(case_moves) - mean_case).groupby(np.array(case_days)).sum()
        se = np.sqrt(float((d ** 2).sum())) / n_cases
        case_t = float(mean_case / se) if se > 0 else None
    sup_passed = None if mean_case is None else bool(mean_case > 0)

    counts = {
        "in-profile grid bars": n_grid,
        "in-profile grid bars with forecast above 0": n_pos,
        "cases": n_cases,
        "case days": n_case_days,
    }

    threshold = "confirm if slope t >= 2 and cases' mean unusual move > 0; reject if slope t <= -2; else inconclusive"
    main = {
        "name": "OLS slope of drift-adjusted 5-bar forward return on forecast (in-profile grid bars)",
        "value": slope,
        "statistic": None if t_slope is None else {"name": "OLS t of slope", "value": t_slope},
        "threshold": threshold,
    }
    supporting = {
        "name": "mean unusual 5-bar move over long-side cases (day-clustered t %s)"
                % ("n/a" if case_t is None else "%.2f" % case_t),
        "value": mean_case,
        "passed": sup_passed,
    }
    reading = ("In-profile means regime 'unknown' (not vetoed to chop); grid bars count only where the 5-bar forward "
               "return exists inside the window; the drift is the coin's mean 5-bar return on the grid of all its "
               "windows; cases are long-side forecast rises of >= 2 points from the lowest level since the last bet "
               "(reset at flat), first per grid cell; the plan's 'too few -> inconclusive' is reported as 'not observable'.")
    if agreement is None:
        reading += " No bar had a non-zero forecast, so the situation check passed vacuously."

    if n_grid < 150 or n_pos < 60:
        status = "not observable"
        decided_by = ("Minimum count not reached: %d in-profile grid bars (need 150) and %d with forecast above 0 "
                      "(need 60)." % (n_grid, n_pos))
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope t could not be computed (no spread in the forecast), so neither rule is met."
    elif t_slope >= 2 and sup_passed:
        status = "confirmed"
        decided_by = "Confirm: slope t %.2f is 2 or more and the cases' mean unusual move is above 0." % t_slope
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "Reject: slope t %.2f is -2 or less." % t_slope
    elif t_slope >= 2:
        status = "inconclusive"
        decided_by = ("Inconclusive: slope t %.2f is 2 or more but the cases' mean unusual move is 0 or below "
                      "(or there are no cases)." % t_slope)
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: slope t %.2f lies between -2 and 2." % t_slope

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
