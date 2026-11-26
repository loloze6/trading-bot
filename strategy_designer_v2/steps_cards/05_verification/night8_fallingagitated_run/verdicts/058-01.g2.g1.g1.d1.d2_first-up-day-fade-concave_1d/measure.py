import numpy as np
import pandas as pd


def measure(bars):
    MIN_CASE_DAYS = 100
    T_THR = 2.0
    RET_COL = "close"

    # ---------- coin mean daily return over all its windows (within-window returns only) ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df[RET_COL], errors="coerce").to_numpy(dtype=float)
            if len(c) >= 2:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- situation check + case collection ----------
    n_active = 0
    n_agree = 0
    case_rows = []  # (day, unusual, |forecast|)

    for coin, wins in bars.items():
        mu = coin_mu[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            regime = df["regime"].astype(str).to_numpy()
            n = len(df)
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            day = ts.dt.floor("D").to_numpy()

            # up-close streak of exactly 1, recomputed from closes inside the window
            streak1 = np.full(n, np.nan)
            for i in range(2, n):
                if np.isfinite(close[i]) and np.isfinite(close[i - 1]) and np.isfinite(close[i - 2]):
                    up_t = close[i] > close[i - 1]
                    up_prev = close[i - 1] > close[i - 2]
                    streak1[i] = 1.0 if (up_t and not up_prev) else 0.0

            in_profile_regime = regime == "mean_reversion"

            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                if np.isnan(streak1[i]):
                    continue  # streak not computable inside the window: left out of the check
                n_active += 1
                if in_profile_regime[i] and streak1[i] == 1.0 and f < 0:
                    n_agree += 1

            # cases: in the regime (and profile) with forecast below 0, next close in the same window
            for i in range(n - 1):
                f = fc[i]
                if not (np.isfinite(f) and f < 0 and in_profile_regime[i]):
                    continue
                if not (np.isfinite(close[i]) and np.isfinite(close[i + 1]) and np.isfinite(mu)):
                    continue
                r = close[i + 1] / close[i] - 1.0
                unusual = -(r - mu)
                case_rows.append((day[i], unusual, abs(f)))

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual next-day fall on case bars, summed per day"
    thr_words = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; at least 100 case-days"
    reading_base = ("The falling-agitated profile is taken from the recorded regime (its detector components are not recorded "
                    "and their 365-bar lookback cannot be rebuilt inside a window) while the streak of exactly 1 is recomputed "
                    "from closes (first two bars of each window left out); the supporting check splits individual cases strictly "
                    "above and below the cases' median |forecast|, cases equal to it left out.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_words},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "case-days": None},
            "decided_by": ("Fewer than 90% of the active bars are first-up-day bars (up-close streak exactly 1) inside the "
                           "falling agitated profile with a short forecast."),
            "reading": reading_base,
        }

    cases = pd.DataFrame(case_rows, columns=["day", "unusual", "absf"])
    n_cases = int(len(cases))
    if n_cases:
        per_day = cases.groupby("day")["unusual"].sum()
        n_days = int(len(per_day))
    else:
        per_day = pd.Series(dtype=float)
        n_days = 0

    mean_val = float(per_day.mean()) if n_days else None
    t_val = None
    if n_days >= 2:
        sd = float(per_day.std(ddof=1))
        if sd > 0:
            t_val = float(mean_val / (sd / np.sqrt(n_days)))

    supp_val = None
    supp_pass = None
    if n_cases >= 2:
        med = float(cases["absf"].median())
        hi = cases.loc[cases["absf"] > med, "unusual"]
        lo = cases.loc[cases["absf"] < med, "unusual"]
        if len(hi) and len(lo):
            supp_val = float(hi.mean() - lo.mean())
            supp_pass = bool(supp_val > 0)
        else:
            supp_pass = False

    counts = {"case-days": n_days, "cases": n_cases, "active bars": int(n_active)}

    if n_days < MIN_CASE_DAYS:
        status = "not observable"
        decided = f"Only {n_days} case-days, fewer than the plan's minimum of 100."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (no spread across days), so neither rule is met."
    elif mean_val > 0 and t_val >= T_THR:
        if supp_pass:
            status = "confirmed"
            decided = "Mean unusual fall above 0 with t >= 2 and the high-|forecast| minus low-|forecast| difference above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif mean_val < 0 and t_val <= -T_THR:
        status = "rejected"
        decided = "Mean unusual fall below 0 with t <= -2: these days are followed by a rise."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": ({"name": "t of the mean across days", "value": t_val} if t_val is not None else None),
            "threshold": thr_words,
        },
        "supporting_check": {
            "name": "mean unusual fall, |forecast| above median minus below median",
            "value": supp_val,
            "passed": supp_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
