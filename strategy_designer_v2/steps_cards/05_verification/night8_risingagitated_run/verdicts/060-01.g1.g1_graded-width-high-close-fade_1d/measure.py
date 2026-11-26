import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    reading = ("The profile part of the situation (falling agitated) cannot be rebuilt from prices inside ~120-bar windows "
               "(365-bar lookback), so it is read from the recorded regime not being the veto result 'chop', while the "
               "upper-half close is recomputed from prices as (close-low)/(high-low) > 0.5; cases on the same UTC day are "
               "summed and the t uses a day-clustered standard error of the case mean; the supporting check splits cases "
               "strictly above and strictly below the median of |forecast| (ties at the median left out); the last bar of "
               "each window has no next-day return and is left out.")

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    case_rows = []
    for coin, wins in bars.items():
        # coin's mean daily return over all its windows together
        all_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            if len(c) > 1:
                all_rets.append(c[1:] / c[:-1] - 1.0)
        if all_rets:
            allr = np.concatenate(all_rets)
            allr = allr[np.isfinite(allr)]
            mu = float(np.mean(allr)) if len(allr) else np.nan
        else:
            mu = np.nan

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            hi = df["high"].astype(float).values
            lo = df["low"].astype(float).values
            cl = df["close"].astype(float).values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            rng = hi - lo
            with np.errstate(divide="ignore", invalid="ignore"):
                cloc = np.where(rng > 0, (cl - lo) / rng, np.nan)
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            in_profile = regime != "chop"
            situation = (cloc > 0.5) & in_profile

            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            ts = pd.to_datetime(df["timestamp"], utc=True)
            day = ts.dt.floor("D").values
            nxt = np.full(len(cl), np.nan)
            if len(cl) > 1:
                nxt[:-1] = cl[1:] / cl[:-1] - 1.0
            for i in range(len(df)):
                if np.isfinite(fc[i]) and fc[i] < 0 and np.isfinite(nxt[i]) and np.isfinite(mu):
                    case_rows.append((day[i], -(nxt[i] - mu), abs(fc[i])))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    sit = {"agreement": float(agreement), "passed": passed}

    main_name = "mean excess next-day fall on short cases (short direction, vs coin drift)"
    thr = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: t <= -2; else inconclusive; >= 100 cases on >= 50 days"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are short bars with an upper-half close inside the falling "
                           "agitated profile, so the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows, columns=["day", "x", "absf"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    def clustered(sub):
        n = len(sub)
        if n == 0:
            return np.nan, np.nan
        m = float(sub["x"].mean())
        g = sub.groupby("day")["x"].agg(["sum", "count"])
        D = len(g)
        if D < 2:
            return m, np.nan
        dev = g["sum"].values - g["count"].values * m
        se = np.sqrt(np.sum(dev ** 2) * D / (D - 1)) / n
        t = m / se if se > 0 else np.nan
        return m, float(t)

    mean_x, t_x = clustered(cases)

    if n_cases:
        med = float(cases["absf"].median())
        above = cases[cases["absf"] > med]["x"]
        below = cases[cases["absf"] < med]["x"]
        diff = float(above.mean() - below.mean()) if len(above) and len(below) else np.nan
    else:
        diff = np.nan
    sup_pass = bool(np.isfinite(diff) and diff > 0) if np.isfinite(diff) else None

    counts = {"cases": n_cases, "distinct days": n_days}
    mm = {"name": main_name,
          "value": float(mean_x) if np.isfinite(mean_x) else None,
          "statistic": {"name": "t of the mean, cases summed per day",
                        "value": float(t_x) if np.isfinite(t_x) else None},
          "threshold": thr}
    sc = {"name": "above-median |forecast| mean excess fall minus below-median",
          "value": float(diff) if np.isfinite(diff) else None,
          "passed": sup_pass}

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided = (f"The plan's minimum of 100 cases over 50 distinct days is not reached "
                   f"({n_cases} cases, {n_days} days).")
    elif not np.isfinite(t_x):
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_x >= 2 and mean_x > 0 and sup_pass:
        status = "confirmed"
        decided = "The mean excess next-day fall is positive with t >= 2 and wider days fall more than narrower days."
    elif t_x <= -2:
        status = "rejected"
        decided = "The mean excess next-day fall has t <= -2: the coin rises more than its drift after upper-half closes."
    elif t_x >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the wide-day cases fall no more than the narrow-day cases, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": mm,
        "supporting_check": sc,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
