import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.wide_high_close.last_history_value"
    EPS = 1e-9

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            if len(df) == 0 or "forecast" not in df:
                continue
            hi = df["high"].astype(float)
            lo = df["low"].astype(float)
            cl = df["close"].astype(float)
            rng = hi - lo
            # close location in range, from low
            close_loc = np.where(rng > 0, (cl - lo) / rng.replace(0, np.nan), np.nan)
            close_loc = pd.Series(close_loc, index=df.index)
            # range multiple from prices (20-bar mean bar range incl. current), inside the window
            mean_rng = rng.rolling(20, min_periods=20).mean()
            range_mult = rng / mean_rng
            # where the component is recorded: value = (close-low)/mean range -> range_mult = value*range/(close-low)
            if LHV in df.columns:
                v = pd.to_numeric(df[LHV], errors="coerce")
                cml = cl - lo
                derived = pd.Series(np.where((cml > 0) & v.notna(), v * rng / cml.replace(0, np.nan), np.nan),
                                    index=df.index)
                range_mult = derived.where(derived.notna(), range_mult)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            situ = (range_mult >= 1.0 - EPS) & (close_loc >= 0.5 - EPS) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ.fillna(False)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean 1-day short-direction unusual move on forecast<0 bars"
    main_thr = "t >= 2 confirms (with supporting difference > 0); t <= -2 rejects"
    sup_name = "unusual move of larger-|forecast| half minus smaller half"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with range >= its "
                           "20-day mean bar range and close in the upper half of the range"
                           if n_active > 0 else "The record has no active bar to compare with the plan's situation."),
            "reading": "The situation is checked on the range and close-location conditions and the short side; the "
                       "agitated-profile veto is the code's, not recomputed.",
        }

    # ---------- 2. criterion ----------
    cases = []
    for coin, wins in bars.items():
        all_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            if len(df) < 2:
                continue
            cl = df["close"].astype(float).values
            r = cl[1:] / cl[:-1] - 1.0
            all_rets.append(r)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values[:-1]
            ts = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D").values[:-1]
            for i in range(len(r)):
                if fc[i] < 0 and np.isfinite(r[i]):
                    coin_cases.append((ts[i], fc[i], r[i]))
        if not all_rets:
            continue
        rr = np.concatenate(all_rets)
        rr = rr[np.isfinite(rr)]
        if len(rr) == 0:
            continue
        drift = float(rr.mean())
        for d, f, r in coin_cases:
            cases.append({"day": d, "absf": abs(f), "u": -(r - drift)})

    cdf = pd.DataFrame(cases, columns=["day", "absf", "u"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    mean_u = float(cdf["u"].mean()) if n_cases else None
    t = None
    if n_cases and n_days > 1:
        dev = cdf["u"] - mean_u
        sums = dev.groupby(cdf["day"]).sum().values
        var = (n_days / (n_days - 1)) * np.sum(sums ** 2) / (n_cases ** 2)
        if var > 0:
            t = float(mean_u / np.sqrt(var))

    diff = None
    if n_cases >= 2:
        s = cdf.sort_values("absf", ascending=False, kind="mergesort").reset_index(drop=True)
        k = n_cases // 2
        diff = float(s["u"].iloc[:k].mean() - s["u"].iloc[n_cases - k:].mean())
    sup_pass = (diff > 0) if diff is not None else None

    counts = {"distinct days of cases": n_days, "cases": n_cases}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct days of cases, under the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean short-direction unusual move has a t of 2 or more and the supporting difference is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "The mean short-direction unusual move has a t of -2 or less: these days rise more than the drift."
    elif t >= 2:
        status = "inconclusive"
        decided = "A confirming t with the supporting difference at or below 0 is inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": {"name": "t of the mean, deviations summed per day", "value": t} if t is not None else None,
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are every bar with forecast < 0 and a next bar in the same window (the 1-bar grid is every "
                    "bar), the drift is the coin's mean 1-day return over all its windows, the day-clustered variance "
                    "uses a D/(D-1) correction, the halves are the top and bottom floor(n/2) cases by |forecast| "
                    "(middle case dropped if n is odd), and the plan's 30-day minimum maps to 'not observable'."),
    }
