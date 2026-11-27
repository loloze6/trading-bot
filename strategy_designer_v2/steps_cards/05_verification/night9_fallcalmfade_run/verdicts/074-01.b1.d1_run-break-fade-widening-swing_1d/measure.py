import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RUN = "debug_info.components.run_depth.last_history_value"

    situation_flags = []
    active_short = []
    case_rows = []

    for coin, wins in bars.items():
        # coin's mean daily return over all windows (1-bar returns inside windows only)
        all_rets = []
        prepared = []
        for w, df in wins.items():
            d = df.copy()
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            r_next = close.shift(-1) / close - 1.0
            all_rets.append(r_next.dropna().values)
            prepared.append((w, d, close, r_next))
        all_rets = np.concatenate(all_rets) if all_rets else np.array([])
        mu = float(np.mean(all_rets)) if len(all_rets) else np.nan

        for w, d, close, r_next in prepared:
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            # run ending on an up close: raw component where recorded, else prices
            up = close > close.shift(1)
            prev_down = close.shift(1) < close.shift(2)
            run_price = (up & prev_down)
            run_price = run_price.where(close.shift(2).notna(), other=np.nan)
            if RUN in d.columns:
                lhv = pd.to_numeric(d[RUN], errors="coerce")
                run_cond = pd.Series(np.where(lhv.notna(), lhv > 0, run_price), index=d.index)
            else:
                run_cond = run_price
            run_cond = run_cond.fillna(False).astype(bool)
            # falling market: 60-day return below -10 % from prices; detector's regime where 60 bars are not in-window
            ret60 = (close / close.shift(60) - 1.0) * 100.0
            regime_mr = d["regime"].astype(str) == "mean_reversion" if "regime" in d.columns else pd.Series(False, index=d.index)
            fall_cond = pd.Series(np.where(ret60.notna(), ret60 < -10.0, regime_mr), index=d.index).astype(bool)
            situ = run_cond & fall_cond

            act = fc != 0
            for i in np.where(act.values)[0]:
                situation_flags.append(bool(situ.iloc[i] and fc.iloc[i] < 0))

            day = pd.to_datetime(d["timestamp"], utc=True).dt.floor("D")
            for i in np.where((fc < 0).values)[0]:
                rn = r_next.iloc[i]
                if pd.isna(rn) or pd.isna(mu):
                    continue
                case_rows.append({
                    "coin": coin, "window": w, "day": day.iloc[i],
                    "absf": abs(float(fc.iloc[i])),
                    "x": -(float(rn) - mu),
                })

    n_active = len(situation_flags)
    agreement = float(np.mean(situation_flags)) if n_active else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean short-signed next-day return minus coin mean daily return, over forecast<0 bars"
    thr = "confirm: mean > 0 with t >= 2 (day-clustered) and check > 0; reject: mean < 0 with t <= -2"
    reading = ("Situation from run_depth raw value > 0 (prices where unrecorded) and 60-bar in-window price return < -10 % "
               "(detector's regime where 60 bars are not available); cases with no next bar in the window are left out; "
               "top half = the n//2 cases with largest |forecast| (stable sort), bottom half = the rest; "
               "the 100-case minimum is applied as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90 % of nonzero-forecast bars are short bars on an up close ending a down run with 60-day return below -10 %.",
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows)
    n = int(len(cases))
    n_days = int(cases["day"].nunique()) if n else 0

    mean = None
    t = None
    if n >= 2:
        x = cases["x"].values
        mean = float(np.mean(x))
        dev = cases.assign(dev=x - mean).groupby("day")["dev"].sum().values
        D = len(dev)
        if D >= 2:
            var = np.sum(dev ** 2) * D / (D - 1) / (n ** 2)
            se = float(np.sqrt(var))
            t = float(mean / se) if se > 0 else None
    elif n == 1:
        mean = float(cases["x"].iloc[0])

    diff = None
    if n >= 2:
        order = np.argsort(-cases["absf"].values, kind="mergesort")
        k = n // 2
        top = cases["x"].values[order[:k]]
        bot = cases["x"].values[order[k:]]
        if len(top) and len(bot):
            diff = float(np.mean(top) - np.mean(bot))
    check_passed = None if diff is None else bool(diff > 0)

    counts = {"cases across the coins": n, "days with cases": n_days}

    if n < 100:
        status = "not observable"
        decided = f"Only {n} cases across the coins, below the plan's minimum of 100."
    elif mean is None or t is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither confirm nor reject is met."
    elif mean > 0 and t >= 2 and check_passed:
        status = "confirmed"
        decided = "Mean above 0 with t >= 2 and top-minus-bottom |forecast| half difference above 0."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean below 0 with t <= -2."
    elif mean > 0 and t >= 2:
        status = "inconclusive"
        decided = "Main measure meets confirm (mean > 0, t >= 2) but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 (or sign/t not meeting either rule): inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": None if t is None else {"name": "t of the mean, cases grouped by day", "value": t},
            "threshold": thr,
        },
        "supporting_check": {"name": "top-half minus bottom-half |forecast| mean short-signed unusual move",
                             "value": diff, "passed": check_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
