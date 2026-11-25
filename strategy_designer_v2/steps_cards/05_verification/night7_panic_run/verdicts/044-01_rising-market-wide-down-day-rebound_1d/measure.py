import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    BAND = 2.0
    FC = "forecast"
    PPV = "debug_info.components.range_std.post_pipeline_value"

    # ---------- 1. situation check: down close (close < prior close), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df[FC].astype(float).fillna(0.0).values
            prev = np.r_[np.nan, close[:-1]]
            for i in range(len(df)):
                if fc[i] == 0 or np.isnan(prev[i]):
                    continue
                n_active += 1
                if close[i] < prev[i] and fc[i] > 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    sit_passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean excess 3-day return of bet cases (coin return minus coin's mean 3-day return)"
    main_thr = "confirm: mean > 0 with day-clustered t >= 2 over >= 100 cases and slope check passes; reject: mean < 0 with t <= -2 over >= 100 cases"
    sup_name = "OLS slope of excess 3-day return on range_std post_pipeline_value (positive, t >= 1)"
    reading = ("The situation is checked as a close below the prior close within the window on long bars (the rising "
               "profile is applied by code not recorded, so it is not recomputed, and each window's first bar, having "
               "no prior close, is left out); a case is the first bet (forecast rise >= 2 points from its lowest level "
               "since the last bet, reset at 0 after a flat) in each 3-bar grid cell from each window's first row; the "
               "coin's mean 3-day return is over the same non-overlapping grid pooled across all its windows; the "
               "day-clustered t uses the sum of deviations per signal day with a G/(G-1) correction.")

    if agreement is None:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": {"cases": 0, "days": 0},
            "decided_by": "No active bar in the record, so fewer than 100 cases: the minimum count is not reached.",
            "reading": reading,
        }

    if not sit_passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active_bars": int(n_active), "agreeing_bars": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long bets on a down close, "
                           "so the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        # coin's mean 3-day return over all windows, non-overlapping grid
        grid_rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = df[FC].astype(float).fillna(0.0).values
            ppv = df[PPV].astype(float).values if PPV in df.columns else np.full(len(df), np.nan)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            # bets on the long side
            bet = np.zeros(len(df), dtype=bool)
            ref = 0.0
            for i in range(len(df)):
                f = fc[i]
                if f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    bet[i] = True
                    ref = f
                else:
                    ref = min(ref, f)
            # one case per grid cell
            for start in range(0, len(df), H):
                idx = [j for j in range(start, min(start + H, len(df))) if bet[j]]
                if not idx:
                    continue
                s = idx[0]
                if s + H >= len(df):
                    continue
                if not (np.isfinite(c[s]) and np.isfinite(c[s + H]) and c[s] > 0):
                    continue
                r = c[s + H] / c[s] - 1.0
                rows.append({
                    "coin": coin,
                    "day": ts.iloc[s].floor("D"),
                    "excess": r - drift,
                    "fc": ppv[s],
                })

    cases = pd.DataFrame(rows, columns=["coin", "day", "excess", "fc"])
    n = int(len(cases))
    n_days = int(cases["day"].nunique()) if n else 0

    mean_ex = float(cases["excess"].mean()) if n else None
    t_main = None
    if n >= 2:
        dev = cases["excess"] - mean_ex
        g = dev.groupby(cases["day"]).sum().values
        G = len(g)
        if G >= 2:
            var = (G / (G - 1.0)) * np.sum(g ** 2) / (n ** 2)
            if var > 0:
                t_main = float(mean_ex / np.sqrt(var))

    slope = None
    t_slope = None
    sup_passed = None
    sub = cases.dropna(subset=["excess", "fc"])
    if len(sub) >= 3 and np.var(sub["fc"].values) > 0:
        res = stats.linregress(sub["fc"].values, sub["excess"].values)
        slope = float(res.slope)
        if res.stderr and res.stderr > 0:
            t_slope = float(res.slope / res.stderr)
            sup_passed = bool(slope > 0 and t_slope >= 1.0)
        else:
            sup_passed = False
    elif n > 0:
        sup_passed = False

    if n < 100:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 100 cases."
    elif t_main is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_ex > 0 and t_main >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "Mean excess 3-day return > 0 with t >= 2 over at least 100 cases, and the slope check passes."
        else:
            status = "inconclusive"
            decided = "Main t >= 2 but the slope check fails, which the plan calls inconclusive."
    elif mean_ex < 0 and t_main <= -2:
        status = "rejected"
        decided = "Mean excess 3-day return < 0 with t <= -2 over at least 100 cases."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "t of the mean, clustered by day", "value": t_main} if t_main is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": sup_name,
            "value": slope,
            "passed": sup_passed,
        },
        "counts": {"cases": n, "days": n_days},
        "decided_by": decided,
        "reading": reading,
    }
