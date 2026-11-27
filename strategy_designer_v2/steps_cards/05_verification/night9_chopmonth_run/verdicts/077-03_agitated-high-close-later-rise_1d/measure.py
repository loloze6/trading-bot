import numpy as np
import pandas as pd


def measure(bars):
    H = 6
    BAND = 2.0
    CL_COL = "debug_info.components.high_close.last_history_value"

    # ---------- per coin / window preparation ----------
    n_active = 0
    n_agree = 0
    cases = []  # dicts: ret, coin, day, cl
    drift = {}

    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            # non-overlapping 6-bar returns on the window's grid (normal drift)
            for p in range(0, n - H, H):
                if close[p] > 0 and np.isfinite(close[p]) and np.isfinite(close[p + H]):
                    grid_rets.append(close[p + H] / close[p] - 1.0)
        drift[coin] = float(np.mean(grid_rets)) if len(grid_rets) > 0 else np.nan

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = df["close"].astype(float).values
            high = df["high"].astype(float).values
            low = df["low"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)

            # lagged close location from prices (bar t-1), inside the window
            rng = high - low
            with np.errstate(divide="ignore", invalid="ignore"):
                cl_raw = np.where(rng > 0, (close - low) / rng, np.nan)
            cl_lag = np.full(n, np.nan)
            cl_lag[1:] = cl_raw[:-1]
            # prefer the recorded raw component value where present
            if CL_COL in df.columns:
                rec = pd.to_numeric(df[CL_COL], errors="coerce").values
                cl = np.where(np.isfinite(rec), rec, cl_lag)
            else:
                cl = cl_lag

            # ---------- situation check ----------
            active = fc != 0
            situ = np.isfinite(cl) & (cl >= 0.8)
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())

            # ---------- bets (rise of the long forecast of at least the band) ----------
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            prev_pos = False
            for t in range(n):
                f = fc[t]
                if f > 0:
                    if not prev_pos:
                        ref = 0.0
                    if f - ref >= BAND:
                        bet[t] = True
                        ref = f
                    else:
                        ref = min(ref, f)
                    prev_pos = True
                else:
                    prev_pos = False
                    ref = 0.0

            # one case per grid cell of the horizon: the first bet in the cell
            d = drift.get(coin, np.nan)
            for start in range(0, n, H):
                idx = [t for t in range(start, min(start + H, n)) if bet[t]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n or not np.isfinite(d):
                    continue
                if not (close[t] > 0 and np.isfinite(close[t + H])):
                    continue
                r = close[t + H] / close[t] - 1.0
                cases.append({
                    "u": r - d,
                    "coin": coin,
                    "day": ts.iloc[t].strftime("%Y-%m-%d"),
                    "cl": float(cl[t]) if np.isfinite(cl[t]) else np.nan,
                })

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean unusual 6-bar move per case, long, from the signal bar's close"
    thr = "above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject"
    reading = ("The situation is the lagged close location >= 0.8 (recorded raw value, else from prices) on the long side, "
               "the agitated profile being the config's veto; a case is the first long-forecast rise of at least 2 points "
               "in each 6-bar grid cell of a window, its day the signal bar's UTC date, the day-clustered standard error is "
               "sqrt(sum over days of squared summed deviations)/n without small-sample correction, and an empty "
               "close-location group makes the supporting check fail.")

    if agreement is not None and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": len(cases), "distinct days": len(set(c["day"] for c in cases))},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are long bars whose previous-day close "
                           "location is 0.8 or more, as the plan's situation requires."),
            "reading": reading,
        }

    n_cases = len(cases)
    n_days = len(set(c["day"] for c in cases))
    counts = {"cases": n_cases, "distinct days": n_days}

    if n_cases == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": passed},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "No case was observed: the minimum of 100 cases on at least 50 distinct days is not reached.",
            "reading": reading,
        }

    u = np.array([c["u"] for c in cases], dtype=float)
    days = np.array([c["day"] for c in cases])
    clv = np.array([c["cl"] for c in cases], dtype=float)
    mean_u = float(np.mean(u))
    dev = pd.Series(u - mean_u).groupby(days).sum()
    se = float(np.sqrt(np.sum(dev.values ** 2)) / n_cases)
    t_stat = float(mean_u / se) if se > 0 else None

    hi = u[np.isfinite(clv) & (clv >= 0.9)]
    lo = u[np.isfinite(clv) & (clv >= 0.8) & (clv < 0.9)]
    if len(hi) > 0 and len(lo) > 0:
        sup_val = float(np.mean(hi) - np.mean(lo))
        sup_pass = bool(sup_val > 0)
    else:
        sup_val = None
        sup_pass = False
    counts["cases with close location >= 0.9"] = int(len(hi))
    counts["cases with close location 0.8 to 0.9"] = int(len(lo))

    main = {"name": main_name, "value": mean_u,
            "statistic": {"name": "t of the mean, cases of one day taken together", "value": t_stat},
            "threshold": thr}
    supp = {"name": "mean unusual move (close location >= 0.9) minus (0.8 to 0.9), above 0",
            "value": sup_val, "passed": sup_pass}

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided = (f"The minimum of 100 cases on at least 50 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif t_stat is not None and mean_u > 0 and t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main measure is above 0 with t >= 2 and the supporting check is above 0."
    elif t_stat is not None and mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The main measure is below 0 with t <= -2."
    else:
        status = "inconclusive"
        if t_stat is not None and mean_u > 0 and t_stat >= 2 and not sup_pass:
            decided = "The main measure is above 0 with t >= 2 but the supporting check fails, which the plan calls inconclusive."
        else:
            decided = "The t lies between -2 and 2 (or is undefined), meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
