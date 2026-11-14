import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    AL = "postRebalance_current_allocation"

    n_active = 0
    n_agree = 0
    main_vals = []
    sat_vals = []

    for coin, wins in bars.items():
        # The coin's mean daily return over all its windows together (returns inside each window only).
        all_rets = []
        prepared = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            ret_next = close.shift(-1) / close - 1.0
            ts = pd.to_datetime(df["timestamp"])
            coming_sat = ((ts + pd.Timedelta(days=1)).dt.weekday == 5).values
            fc = pd.to_numeric(df[FC], errors="coerce") if FC in df.columns else pd.Series(np.nan, index=df.index)
            al = pd.to_numeric(df[AL], errors="coerce") if AL in df.columns else pd.Series(np.nan, index=df.index)
            all_rets.append(ret_next.dropna().values)
            prepared.append((ret_next, coming_sat, fc, al))
        all_rets = np.concatenate(all_rets) if all_rets else np.array([])
        if all_rets.size == 0:
            continue
        coin_mean = float(np.mean(all_rets))

        for ret_next, coming_sat, fc, al in prepared:
            # Situation check: active bars must be bars whose coming bar is Saturday, and long.
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & pd.Series(coming_sat, index=fc.index) & (fc > 0)).sum())

            # Main measure: forecast > 0, allocation x (next-bar return - coin mean).
            m = (fc > 0) & ret_next.notna() & al.notna()
            if m.any():
                main_vals.extend((al[m] * (ret_next[m] - coin_mean)).tolist())

            # Supporting check: every Saturday bar (return from Friday close to Saturday close).
            s = pd.Series(coming_sat, index=ret_next.index) & ret_next.notna()
            if s.any():
                sat_vals.extend((ret_next[s] - coin_mean).tolist())

    def mean_t(x):
        x = np.asarray(x, dtype=float)
        n = x.size
        if n == 0:
            return None, None
        mu = float(np.mean(x))
        if n < 2:
            return mu, None
        sd = float(np.std(x, ddof=1))
        if sd == 0 or not np.isfinite(sd):
            return mu, None
        return mu, float(mu / (sd / np.sqrt(n)))

    reading = ("Saturday bars are the Friday-dated decision bars whose next bar is Saturday "
               "(timestamp + 1 day has weekday 5), the allocation is postRebalance_current_allocation, "
               "'the coin's mean daily return over all 24 windows' is read as the mean of all within-window "
               "one-bar returns of that coin over every window present in the record, the 300-bar minimum counts "
               "forecast>0 bars with a valid next return, and the supporting check, which has no threshold in "
               "the plan, is marked passed when its mean is positive with t >= 2 like the confirm rule.")

    threshold_txt = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; otherwise inconclusive; at least 300 active Saturday bars"
    main_name = "mean of allocation x (next-bar return - coin mean daily return) on forecast>0 bars"

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active Saturday bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are long positions taken on a Friday bar before a "
                           "Saturday session, which the plan's situation requires."),
            "reading": reading,
        }

    mu, t = mean_t(main_vals)
    smu, st = mean_t(sat_vals)
    sup_passed = None
    if smu is not None and st is not None:
        sup_passed = bool(smu > 0 and st >= 2)

    n_main = len(main_vals)
    counts = {"active Saturday bars": int(n_main), "Saturday bars": int(len(sat_vals))}

    if n_main < 300:
        status = "not observable"
        decided = f"Only {n_main} active Saturday bars pooled over coins and windows, below the plan's minimum of 300."
    elif mu is not None and t is not None and mu > 0 and t >= 2:
        status = "confirmed"
        decided = "The main-measure mean is positive with t >= 2, pooled over the coins."
    elif mu is not None and t is not None and mu < 0 and t <= -2:
        status = "rejected"
        decided = "The main-measure mean is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The main-measure t lies between -2 and 2 (or is undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": None if mu is None else float(mu),
            "statistic": None if t is None else {"name": "t of the mean", "value": float(t)},
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "mean Saturday return minus coin all-window mean daily return (t of the mean)",
            "value": None if smu is None else float(smu),
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
