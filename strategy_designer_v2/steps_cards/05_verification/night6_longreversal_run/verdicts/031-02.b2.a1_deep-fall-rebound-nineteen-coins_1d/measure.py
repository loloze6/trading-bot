import numpy as np
import pandas as pd


def measure(bars):
    H = 30
    FC = "forecast"
    RAW90 = "debug_info.components.fall90.last_history_value"

    # ---------- 1. Situation check: active bars must be r90 <= -1, and long ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or FC not in df.columns:
                continue
            fc = pd.to_numeric(df[FC], errors="coerce")
            active = fc.notna() & (fc != 0)
            if not active.any():
                continue
            if RAW90 in df.columns:
                r90 = pd.to_numeric(df[RAW90], errors="coerce")
            else:
                r90 = pd.Series(np.nan, index=df.index)
            situ = r90.notna() & (r90 <= -1.0)
            ok = active & situ & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if n_active == 0 else (agreement >= 0.90)

    main_name = "mean 30-bar forward return minus the coin's normal 30-bar drift, over grid bars with forecast > 0"
    threshold = "confirm: mean > 0 with t >= 2 and the check's difference > 0; reject: mean < 0 with t <= -2"
    check_name = "mean unusual return of the larger-forecast half minus the smaller-forecast half"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on the long side": int(n_agree)},
            "decided_by": "Fewer than 90 % of the bars with a non-zero forecast are long bars where the 90-day return "
                          "in usual 90-day moves (fall90 raw value) is at or below -1, as the plan's adapted situation requires.",
            "reading": "The situation is read from fall90's raw value (same component and parameters as the detector's r90); "
                       "an active bar without that value counts as outside the situation.",
        }

    # ---------- 2. Criterion ----------
    case_rows = []      # (coin, day, fwd, forecast)
    drift_rets = {}     # coin -> list of grid forward returns (all grid bars)
    for coin, wins in bars.items():
        rets_all = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df[FC], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                j = i + H
                if j >= n:
                    break
                c0, c1 = close[i], close[j]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                rets_all.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    case_rows.append((coin, ts.iloc[i].normalize(), r, float(fc[i])))
        drift_rets[coin] = rets_all

    drift = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in drift_rets.items()}

    if case_rows:
        cases = pd.DataFrame(case_rows, columns=["coin", "day", "fwd", "fc"])
        cases["unusual"] = cases["fwd"] - cases["coin"].map(drift)
        cases = cases[np.isfinite(cases["unusual"])].reset_index(drop=True)
    else:
        cases = pd.DataFrame(columns=["coin", "day", "fwd", "fc", "unusual"])

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = None
    t_val = None
    if n_cases > 0:
        x = cases["unusual"].to_numpy(dtype=float)
        mean_u = float(np.mean(x))
        dev = cases.assign(d=x - mean_u).groupby("day")["d"].sum().to_numpy(dtype=float)
        D = len(dev)
        if D > 1:
            var = (D / (D - 1)) * np.sum(dev ** 2) / (n_cases ** 2)
            se = np.sqrt(var)
            t_val = float(mean_u / se) if se > 0 else None

    # supporting check: larger-forecast half minus smaller-forecast half
    diff = None
    if n_cases >= 2:
        srt = cases.sort_values(["fc", "day", "coin"], kind="mergesort").reset_index(drop=True)
        k = n_cases // 2
        low = srt.iloc[:k]["unusual"].mean()
        high = srt.iloc[n_cases - k:]["unusual"].mean()
        diff = float(high - low)
    check_passed = None if diff is None else bool(diff > 0)

    counts = {"cases": n_cases, "distinct case days": n_days}
    reading = ("Cases are grid bars (positions 0, 30, 60, ... of each window) with forecast > 0 and a close 30 bars later "
               "in the same window; the normal drift is the mean of the coin's 30-bar grid returns over all its windows; "
               "the day-clustered t sums deviations per calendar day with a D/(D-1) correction; the halves are the top and "
               "bottom n//2 cases by forecast (the middle case left out when n is odd); fewer than 30 case days is "
               "reported as 'not observable' as the plan's minimum count.")

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, fewer than the plan's minimum of 30."
    elif mean_u is not None and t_val is not None and mean_u > 0 and t_val >= 2:
        if check_passed:
            status = "confirmed"
            decided = "The main mean is above 0 with t >= 2 and the larger-forecast half beats the smaller one (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The main mean is above 0 with t >= 2 but the supporting check's difference is not above 0 (inconclusive rule)."
    elif mean_u is not None and t_val is not None and mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The main mean is below 0 with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The main mean's t is between -2 and 2 (or undefined), meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t_val}
                          if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": check_name, "value": diff, "passed": check_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
