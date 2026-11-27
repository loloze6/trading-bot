import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RL = "debug_info.components.run_loss.last_history_value"
    BAND = 2.0

    active_total = 0
    active_agree = 0
    case_rows = []

    # normal drift per coin: mean daily return over all windows (h = 1, every bar is a grid cell)
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            if len(c) > 1:
                rets.append(c[1:] / c[:-1] - 1.0)
        allr = np.concatenate(rets) if rets else np.array([])
        allr = allr[np.isfinite(allr)]
        drift[coin] = float(np.mean(allr)) if len(allr) else np.nan

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * n)
            rl = df[RL].astype(float).values if RL in df.columns else np.full(n, np.nan)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            days = ts.dt.floor("D").astype(str).values

            # situation check
            for t in range(n):
                if fc[t] == 0:
                    continue
                active_total += 1
                # run break: up close ending a down run
                if t >= 2:
                    brk = (close[t] > close[t - 1]) and (close[t - 1] < close[t - 2])
                else:
                    brk = bool(np.isfinite(rl[t]) and rl[t] > 0)
                # falling profile: 60-bar return below -10 %
                if t >= 60:
                    falling = (close[t] / close[t - 60] - 1.0) * 100.0 < -10.0
                else:
                    falling = regime[t] == "mean_reversion"
                if brk and falling and fc[t] < 0:
                    active_agree += 1

            # cases: bets on the short side (rise of |forecast| of at least the band)
            ref = 0.0
            for t in range(n):
                if fc[t] < 0:
                    m = -fc[t]
                    if m - ref >= BAND:
                        if t + 1 < n:
                            r = close[t + 1] / close[t] - 1.0
                            if np.isfinite(r):
                                case_rows.append({
                                    "coin": coin, "day": days[t], "ret": r,
                                    "dev": -(r - drift[coin]), "run_loss": rl[t],
                                })
                        ref = m
                    else:
                        ref = min(ref, m)
                else:
                    ref = 0.0

    agreement = float(active_agree / active_total) if active_total else 0.0
    passed = active_total > 0 and agreement >= 0.9
    reading = ("Cases are the short bets of the workflow (a rise of the forecast's size of at least 2 points from its "
               "lowest level since the last bet), the supporting regression uses the raw next-day return, the main t "
               "uses per-day sums of deviations, the situation's 60-day profile is computed from prices when 60 bars "
               "precede the bar in its window and read from the recorded regime otherwise, and the plan's minimum of "
               "100 cases on 80 days yields 'not observable' when unmet.")
    main_name = "mean next-day return minus drift, short direction"
    main_thr = "mean > 0 with t >= 2 to confirm; t <= -2 rejects"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(active_total)},
            "decided_by": ("Fewer than 90 % of the active bars are short bars on an up close ending a down run in a "
                           "market whose 60-day return is below -10 %."),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows, columns=["coin", "day", "ret", "dev", "run_loss"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_dev = float(cases["dev"].mean()) if n_cases else None
    t_main = None
    if n_days >= 2:
        ds = cases.groupby("day")["dev"].sum().values
        sd = np.std(ds, ddof=1)
        if sd > 0:
            t_main = float(np.mean(ds) / (sd / np.sqrt(len(ds))))

    slope = None
    t_slope = None
    reg = cases.dropna(subset=["run_loss", "ret"])
    if len(reg) >= 3 and np.std(reg["run_loss"].values) > 0:
        lr = stats.linregress(reg["run_loss"].values, reg["ret"].values)
        slope = float(lr.slope)
        if lr.stderr and lr.stderr > 0:
            t_slope = float(lr.slope / lr.stderr)
    sup_pass = None if t_slope is None else bool(slope < 0 and t_slope <= -2)

    counts = {"cases": n_cases, "distinct days": n_days}

    if n_cases < 100 or n_days < 80:
        status = "not observable"
        decided = f"The plan's minimum of 100 cases on 80 distinct days is not reached ({n_cases} cases on {n_days} days)."
    elif (t_main is not None and t_main <= -2) or (t_slope is not None and t_slope >= 2):
        status = "rejected"
        decided = ("Reject rule: the main measure's t is <= -2 or the supporting slope's t is >= +2.")
    elif mean_dev is not None and t_main is not None and mean_dev > 0 and t_main >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm rule: mean above 0 with t >= 2 and a negative slope with t <= -2."
    else:
        status = "inconclusive"
        decided = ("Inconclusive rule: the results meet neither the confirm rule (including its supporting check) "
                   "nor the reject rule.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_dev,
            "statistic": None if t_main is None else {"name": "t of the mean, cases summed per day", "value": t_main},
            "threshold": main_thr,
        },
        "supporting_check": {"name": "t of slope of next-day return on run loss", "value": t_slope, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
