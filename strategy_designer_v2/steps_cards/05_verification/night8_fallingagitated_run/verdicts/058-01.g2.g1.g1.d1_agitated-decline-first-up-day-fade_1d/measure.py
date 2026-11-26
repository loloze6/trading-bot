import numpy as np
import pandas as pd


def measure(bars):
    # ---------- 1. Situation check ----------
    # Situation: first up day after a non-up day (up-close streak exactly 1); expected side: short.
    n_active = 0
    n_agree = 0
    n_undetermined = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce")
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            up_today = c > c.shift(1)
            not_up_prev = c.shift(1) <= c.shift(2)
            determinable = c.shift(2).notna() & c.shift(1).notna() & c.notna()
            situation = up_today & not_up_prev
            active = f != 0
            for i in np.where(active.values)[0]:
                if not determinable.iloc[i]:
                    n_undetermined += 1
                    continue
                n_active += 1
                if bool(situation.iloc[i]) and f.iloc[i] < 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading_sc = ("situation recomputed from closes within each window as close[t]>close[t-1] and "
                  "close[t-1]<=close[t-2] with a short forecast; active bars on a window's first two rows "
                  "(streak not computable) are left out; the falling-agitated profile (365-day volatility "
                  "percentile) cannot be rebuilt from the record's windows and is not re-checked")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active), "active bars not determinable": int(n_undetermined)},
            "decided_by": ("fewer than 90% of the bars with a nonzero forecast are short first-up-days "
                           "(up-close streak exactly 1) as the plan's situation requires"
                           if n_active > 0 else "no active bars on which the plan's situation could be checked"),
            "reading": reading_sc,
        }

    # ---------- 2. Criterion ----------
    # coin's mean daily return over all windows
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce")
            r = (c.shift(-1) / c - 1.0).dropna()
            rets.append(r.values)
        coin_mu[coin] = float(np.mean(np.concatenate(rets))) if rets and sum(len(x) for x in rets) > 0 else np.nan

    rows = []
    for coin in sorted(bars.keys()):
        wins = bars[coin]
        for w in sorted(wins.keys(), key=lambda s: (len(str(s)), str(s))):
            df = wins[w]
            if df is None or len(df) < 2:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce")
            f = pd.to_numeric(d["forecast"], errors="coerce")
            r1 = c.shift(-1) / c - 1.0
            ts = pd.to_datetime(d["timestamp"], utc=True)
            for i in range(len(d)):
                fi = f.iloc[i]
                if pd.isna(fi) or fi == 0:
                    continue
                ri = r1.iloc[i]
                if pd.isna(ri) or not np.isfinite(coin_mu[coin]):
                    continue
                x = -(ri - coin_mu[coin])  # short-signed excess return
                rows.append({"coin": coin, "ts": ts.iloc[i], "day": ts.iloc[i].floor("D"),
                             "absf": abs(float(fi)), "x": float(x)})

    cases = pd.DataFrame(rows, columns=["coin", "ts", "day", "absf", "x"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean = None
    t = None
    if n_cases >= 2:
        mean = float(cases["x"].mean())
        dev = cases["x"] - mean
        S = dev.groupby(cases["day"]).sum().values
        D = len(S)
        if D > 1:
            var = (D / (D - 1.0)) * float(np.sum(S ** 2)) / (n_cases ** 2)
            se = np.sqrt(var)
            t = float(mean / se) if se > 0 else None
    elif n_cases == 1:
        mean = float(cases["x"].mean())

    diff = None
    sup_passed = None
    if n_cases >= 2:
        s = cases.sort_values(["absf", "ts", "coin"], kind="mergesort").reset_index(drop=True)
        half = n_cases // 2
        bottom = s.iloc[:n_cases - half]
        top = s.iloc[n_cases - half:]
        if len(top) > 0 and len(bottom) > 0:
            diff = float(top["x"].mean() - bottom["x"].mean())
            sup_passed = bool(diff > 0)

    if n_cases < 100:
        status = "not observable"
        decided_by = f"the plan needs at least 100 cases and the record has {n_cases}"
    elif mean is not None and t is not None and mean > 0 and t >= 2 and sup_passed:
        status = "confirmed"
        decided_by = "the main mean is positive with t >= 2 and the top-minus-bottom difference is positive (confirm rule)"
    elif mean is not None and t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided_by = "the main mean is negative with t <= -2 (reject rule)"
    else:
        status = "inconclusive"
        if t is not None and mean is not None and mean > 0 and t >= 2:
            decided_by = "t >= 2 but the top-minus-bottom difference is not positive (inconclusive rule)"
        else:
            decided_by = "the main t lies between -2 and 2 (inconclusive rule)"

    reading = (reading_sc + "; the t clusters cases by UTC day (deviations from the mean summed per day, "
               "with a D/(D-1) correction); the top and bottom halves split the cases sorted by |forecast| "
               "(ties ordered by time then coin), the bottom half taking the extra case when the count is odd; "
               "fewer than 100 cases is reported as not observable")

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean next-day short-signed return beyond the coin's mean daily return",
            "value": mean,
            "statistic": {"name": "t of the mean, cases of one day taken together", "value": t} if t is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "top-half minus bottom-half |forecast| short-signed excess return",
            "value": diff,
            "passed": sup_passed,
        },
        "counts": {"cases": n_cases, "days": n_days},
        "decided_by": decided_by,
        "reading": reading,
    }
