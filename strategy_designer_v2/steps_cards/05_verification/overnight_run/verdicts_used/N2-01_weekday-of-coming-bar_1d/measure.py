import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    AL = "postRebalance_current_allocation"
    MIN_ACTIVE = 300

    def t_of_mean(x):
        x = np.asarray(x, dtype=float)
        n = len(x)
        if n < 2:
            return float(np.mean(x)) if n else None, None
        m = float(np.mean(x))
        sd = float(np.std(x, ddof=1))
        if sd == 0 or not np.isfinite(sd):
            return m, None
        return m, float(m / (sd / np.sqrt(n)))

    # Situation check
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or FC not in df.columns:
                continue
            ts = pd.to_datetime(df["timestamp"])
            fc = pd.to_numeric(df[FC], errors="coerce")
            active = fc.notna() & (fc != 0)
            coming_sat = ((ts + pd.Timedelta(days=1)).dt.weekday == 5)
            ok = active & coming_sat & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean of allocation x (next-bar return minus coin all-window mean daily return) over forecast>0 bars"
    threshold = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; at least 300 active Saturday bars pooled"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active Saturday bars": n_active},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars whose coming bar is a Saturday "
                           "(Friday-dated bars), so the config does not trade the plan's Saturday situation on its long side."
                           if n_active > 0 else "No bar has a non-zero forecast, so the situation cannot be matched."),
            "reading": "The situation is a bar whose timestamp plus one day falls on a Saturday (the Friday-dated bar), held long.",
        }

    main_vals = []
    sat_vals = []
    for coin, wins in bars.items():
        # coin mean daily return over all windows together (within-window returns only)
        rets_all = []
        frames = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            r = close.shift(-1) / close - 1
            rets_all.append(r.dropna().values)
            frames.append((df.reset_index(drop=True), r))
        if not rets_all:
            continue
        allr = np.concatenate(rets_all)
        allr = allr[np.isfinite(allr)]
        if len(allr) == 0:
            continue
        mu = float(np.mean(allr))
        for df, r in frames:
            ts = pd.to_datetime(df["timestamp"])
            coming_sat = ((ts + pd.Timedelta(days=1)).dt.weekday == 5)
            fc = pd.to_numeric(df[FC], errors="coerce")
            al = pd.to_numeric(df[AL], errors="coerce") if AL in df.columns else pd.Series(np.nan, index=df.index)
            m = (fc > 0) & r.notna() & al.notna() & np.isfinite(r)
            if m.any():
                main_vals.extend((al[m] * (r[m] - mu)).tolist())
            s = coming_sat & r.notna() & np.isfinite(r)
            if s.any():
                sat_vals.extend((r[s] - mu).tolist())

    n_main = len(main_vals)
    mean_main, t_main = t_of_mean(main_vals) if n_main else (None, None)
    mean_sat, t_sat = t_of_mean(sat_vals) if sat_vals else (None, None)

    counts = {"active Saturday bars": n_main, "Saturday bars": len(sat_vals)}

    if n_main < MIN_ACTIVE:
        status = "not observable"
        decided = f"Only {n_main} active Saturday bars pooled over coins and windows, below the plan's minimum of 300."
    elif t_main is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_main > 0 and t_main >= 2:
        status = "confirmed"
        decided = "The pooled main-measure mean is positive with t >= 2 (confirm rule)."
    elif mean_main < 0 and t_main <= -2:
        status = "rejected"
        decided = "The pooled main-measure mean is negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The pooled main-measure t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_main,
            "statistic": ({"name": "t of the mean", "value": t_main} if t_main is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean Saturday return minus coin all-window mean daily return (t = %s)" % (
                "nan" if t_sat is None else "%.4f" % t_sat),
            "value": mean_sat,
            "passed": None,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("A Saturday bar is the return from a Friday-dated bar's close to the next bar's close, active bars are "
                    "forecast > 0 bars with a valid next return weighted by postRebalance_current_allocation, the coin mean is the "
                    "mean of all within-window one-bar returns pooled over its windows, the plan's 'fewer than 300 is inconclusive' "
                    "minimum is reported as not observable, and the supporting check has no pass rule in the plan so its passed is null."),
    }
