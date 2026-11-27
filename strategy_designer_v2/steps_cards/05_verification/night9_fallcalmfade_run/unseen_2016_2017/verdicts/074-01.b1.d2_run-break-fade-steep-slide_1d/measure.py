import numpy as np
import pandas as pd


def measure(bars):
    # ---------- 1. Situation check ----------
    n_active_checkable = 0
    n_agree = 0
    n_active_total = 0

    # ---------- 2. Data for the criterion ----------
    case_rows = []

    for coin, windows in bars.items():
        coin_rets = []
        per_window = []
        for w, df in windows.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").astype(float)
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")

            # next-day return inside the window only
            nxt = close.shift(-1) / close - 1.0
            coin_rets.append(nxt.dropna().values)
            per_window.append((ts, close, fc, nxt))

            # situation from prices: 60-day return below -10 % and an up close
            # ending a run of at least 2 down closes
            trend60 = (close / close.shift(60) - 1.0) * 100.0
            up = close > close.shift(1)
            down1 = close.shift(1) < close.shift(2)
            down2 = close.shift(2) < close.shift(3)
            run_ok = up & down1 & down2
            computable = trend60.notna() & close.shift(3).notna()
            situation = run_ok & (trend60 < -10.0)

            active = fc.notna() & (fc != 0)
            n_active_total += int(active.sum())
            chk = active & computable
            n_active_checkable += int(chk.sum())
            n_agree += int((chk & situation & (fc < 0)).sum())

        all_r = np.concatenate(coin_rets) if coin_rets else np.array([])
        mu = float(np.mean(all_r)) if len(all_r) else np.nan

        for ts, close, fc, nxt in per_window:
            mask = (fc < 0) & nxt.notna()
            for i in np.where(mask.values)[0]:
                case_rows.append({
                    "coin": coin,
                    "day": ts.iloc[i].normalize(),
                    "absf": abs(float(fc.iloc[i])),
                    "x": -(float(nxt.iloc[i]) - mu),
                })

    agreement = (n_agree / n_active_checkable) if n_active_checkable > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    reading = ("The situation is rebuilt from closes (60-day return = close[t]/close[t-60]-1 in %, below -10; "
               "an up close after two consecutive down closes) and checked only on active bars where 60 prior bars "
               "exist inside the window; the coin's mean daily return pools all its windows' next-day returns; "
               "cases are bars with forecast < 0 that have a next-day return in the same window; the day-clustered t "
               "sums deviations per UTC day with a G/(G-1) correction; the larger half is cases with absolute "
               "forecast above the median, the smaller half those at or below it.")

    main_name = "mean next-day excess short return (return minus coin mean, sign flipped)"
    threshold = "confirm: mean > 0 with t >= 2 and check > 0; reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active_total, "active bars checkable": n_active_checkable},
            "decided_by": ("Fewer than 90 % of the checkable active bars are short bars of the plan's situation "
                           "(60-day return below -10 % and an up close ending at least 2 down closes)"
                           if agreement is not None else
                           "No active bar has enough history in its window to check the plan's situation."),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows, columns=["coin", "day", "absf", "x"])
    n = len(cases)
    n_days = int(cases["day"].nunique()) if n else 0

    mean_x = float(cases["x"].mean()) if n else None
    t_val = None
    if n >= 2:
        dev = cases["x"] - mean_x
        S = dev.groupby(cases["day"]).sum().values
        G = len(S)
        var = float(np.sum(S ** 2)) / (n ** 2)
        if G > 1:
            var *= G / (G - 1)
        se = np.sqrt(var)
        t_val = float(mean_x / se) if se > 0 else None

    diff = None
    check_passed = None
    if n >= 2:
        med = float(cases["absf"].median())
        hi = cases.loc[cases["absf"] > med, "x"]
        lo = cases.loc[cases["absf"] <= med, "x"]
        if len(hi) > 0 and len(lo) > 0:
            diff = float(hi.mean() - lo.mean())
            check_passed = bool(diff > 0)
        else:
            check_passed = False

    counts = {"cases (bars with forecast < 0)": int(n), "days with cases": n_days}

    if n < 100:
        status = "not observable"
        decided_by = f"Only {n} cases (bars with forecast < 0) across the coins, below the plan's minimum of 100."
    elif t_val is not None and mean_x > 0 and t_val >= 2 and check_passed:
        status = "confirmed"
        decided_by = "The mean excess short return is above 0 with t >= 2 and the larger-minus-smaller forecast half difference is above 0."
    elif t_val is not None and mean_x < 0 and t_val <= -2:
        status = "rejected"
        decided_by = "The mean excess short return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        if t_val is not None and mean_x > 0 and t_val >= 2:
            decided_by = "The mean excess short return is above 0 with t >= 2 but the supporting check difference is not above 0."
        else:
            decided_by = "The t of the mean excess short return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_x,
            "statistic": ({"name": "t of the mean, cases of the same day taken together", "value": t_val}
                          if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess, larger-|forecast| half minus smaller half",
            "value": diff,
            "passed": check_passed,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
