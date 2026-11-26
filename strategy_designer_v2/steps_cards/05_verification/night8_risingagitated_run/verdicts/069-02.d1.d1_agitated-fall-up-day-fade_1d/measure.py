import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    REG = "regime"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp")
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).values
            reg = df[REG].astype(str).values if REG in df.columns else np.array([""] * len(df))
            prev = np.r_[np.nan, close[:-1]]
            up = close > prev
            # The first row of a window has no prior close inside the window:
            # fall back on the regime rule (mean_reversion is only chosen when up_day > 0).
            first_unknown = np.isnan(prev)
            # The profile (falling agitated) comes from the regime detector's vetoes;
            # its components are not recorded, so the recorded regime stands for it.
            in_profile = reg == "mean_reversion"
            up_ok = np.where(first_unknown, in_profile, up)
            situation = up_ok & in_profile
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "least-squares slope of next-day excess return e on depth d = -forecast"
    threshold = "t <= -2 confirms (with mean of -e > 0); t >= +2 rejects; otherwise inconclusive; at least 100 cases on at least 60 distinct days"
    reading = ("Cases are all bars with forecast < 0 that have a next bar in the same window; the coin's mean daily return "
               "is the mean of all its one-bar returns inside windows over all windows; the slope's t is OLS with "
               "standard errors clustered by UTC day (cases of one day taken together, with the usual G/(G-1)*(N-1)/(N-K) "
               "correction); the profile in the situation check is read from the recorded regime (mean_reversion), "
               "since the detector's components are not recorded and the 365-bar percentile cannot be rebuilt inside windows; "
               "the plan's minimum counts, when not reached, give 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": None, "distinct days": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars on an up close "
                           "in the falling agitated profile (agreement %s)." % (agreement,)),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        # coin's mean daily return over all windows
        all_r = []
        per_win = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            r_next = np.r_[close[1:] / close[:-1] - 1.0, np.nan]
            all_r.append(r_next[:-1])
            per_win.append((df, r_next))
        if not all_r:
            continue
        allr = np.concatenate(all_r)
        allr = allr[np.isfinite(allr)]
        if len(allr) == 0:
            continue
        mu = float(np.mean(allr))
        for df, r_next in per_win:
            fc = pd.to_numeric(df[FC], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            day = ts.dt.floor("D").values
            for i in range(len(df)):
                if np.isfinite(fc[i]) and fc[i] < 0 and np.isfinite(r_next[i]):
                    rows.append((coin, day[i], -float(fc[i]), float(r_next[i] - mu)))

    n_cases = len(rows)
    if n_cases > 0:
        cases = pd.DataFrame(rows, columns=["coin", "day", "d", "e"])
        n_days = int(cases["day"].nunique())
    else:
        cases = None
        n_days = 0

    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    slope = None
    tval = None
    mean_short = None
    if cases is not None and n_cases >= 3:
        d = cases["d"].values
        e = cases["e"].values
        X = np.column_stack([np.ones(n_cases), d])
        XtX = X.T @ X
        try:
            XtX_inv = np.linalg.inv(XtX)
            beta = XtX_inv @ (X.T @ e)
            u = e - X @ beta
            slope = float(beta[1])
            groups = cases["day"].values
            meat = np.zeros((2, 2))
            G = 0
            for g, idx in pd.Series(np.arange(n_cases)).groupby(groups):
                ii = idx.values
                s = X[ii].T @ u[ii]
                meat += np.outer(s, s)
                G += 1
            if G > 1:
                corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - 2.0))
                V = corr * XtX_inv @ meat @ XtX_inv
                se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
                tval = float(slope / se) if np.isfinite(se) and se > 0 else None
        except np.linalg.LinAlgError:
            pass
        mean_short = float(np.mean(-e))

    sup_passed = None if mean_short is None else bool(mean_short > 0)
    supporting = {"name": "mean of -e over the cases above 0", "value": mean_short, "passed": sup_passed}
    statistic = {"name": "t of the slope, cases clustered by day", "value": tval} if tval is not None else None

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = ("The plan's minimum of at least 100 cases on at least 60 distinct days is not reached "
                   "(%d cases on %d days)." % (n_cases, n_days))
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval <= -2:
        if sup_passed:
            status = "confirmed"
            decided = "The slope of e on d has t of -2 or less and the mean of -e over the cases is above 0 (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The slope's t is -2 or less but the supporting check (mean of -e above 0) fails (inconclusive rule)."
    elif tval >= 2:
        status = "rejected"
        decided = "The slope of e on d has t of +2 or more (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and +2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope, "statistic": statistic, "threshold": threshold},
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
