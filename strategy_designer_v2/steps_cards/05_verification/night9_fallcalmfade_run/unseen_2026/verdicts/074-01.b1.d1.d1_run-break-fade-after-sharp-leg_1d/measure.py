import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    sit_total = 0
    sit_ok = 0
    sit_fallback_used = False
    case_rows = []  # (day, unusual, absf)

    # ---- coin means over all windows (next-day returns inside windows) ----
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(allr)) if allr.size else np.nan

    undetermined_active = []
    for coin, wins in bars.items():
        mu = coin_mu[coin]
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df[FC], errors="coerce").to_numpy(dtype=float)
            reg = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(c)
            for t in range(n):
                ft = f[t]
                # ---- situation check ----
                if np.isfinite(ft) and ft != 0:
                    run_ok = None
                    if t >= 3:
                        up = c[t] > c[t - 1]
                        run2 = (c[t - 1] < c[t - 2]) and (c[t - 2] < c[t - 3])
                        run_ok = bool(up and run2)
                    fall_ok = None
                    if t >= 60 and np.isfinite(c[t - 60]) and c[t - 60] > 0:
                        fall_ok = bool((c[t] / c[t - 60] - 1.0) * 100.0 < -10.0)
                    if run_ok is None or fall_ok is None:
                        undetermined_active.append((run_ok, fall_ok, reg[t], ft))
                    else:
                        sit_total += 1
                        if run_ok and fall_ok and ft < 0:
                            sit_ok += 1
                # ---- cases ----
                if np.isfinite(ft) and ft < -2 and t + 1 < n:
                    r = c[t + 1] / c[t] - 1.0
                    if np.isfinite(r) and np.isfinite(mu):
                        case_rows.append((ts.iloc[t].date().isoformat(), -(r - mu), abs(ft)))

    if sit_total == 0 and undetermined_active:
        sit_fallback_used = True
        for run_ok, fall_ok, rg, ft in undetermined_active:
            sit_total += 1
            r_ok = run_ok if run_ok is not None else True
            f_ok = fall_ok if fall_ok is not None else (rg != "chop")
            if r_ok and f_ok and ft < 0:
                sit_ok += 1

    agreement = float(sit_ok / sit_total) if sit_total > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("Falling market read as the 60-bar close change below -10 % and the situation as an up close after at least "
               "2 consecutive down closes, both from closes inside each window, with active bars whose 60-bar or 3-bar "
               "history is not in the window left out of the agreement"
               + (" (none were computable, so the recorded regime stood in for the falling-market test)" if sit_fallback_used else "")
               + "; the top half of the split is |forecast| above the median and the bottom half the rest; the day-pooled "
               "t uses per-day summed deviations with a D/(D-1) correction; the plan's 50 cases / 50 days minimum is "
               "reported as not observable.")

    mm_name = "mean short-side unusual next-day move of bars with forecast below -2"
    mm_thr = "confirm: mean > 0 with day-pooled t >= 2; reject: t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": mm_thr},
            "supporting_check": None,
            "counts": {"active bars checked": int(sit_total)},
            "decided_by": ("Fewer than 90 % of the active bars are short bars on an up close ending a run of 2+ down closes "
                           "in a falling market (60-bar change below -10 %)."),
            "reading": reading,
        }

    n_cases = len(case_rows)
    days = sorted(set(d for d, _, _ in case_rows))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    mean_u = None
    tval = None
    if n_cases > 0:
        u = np.array([x[1] for x in case_rows], dtype=float)
        mean_u = float(np.mean(u))
        if n_days > 1:
            dev = pd.Series(u - mean_u, index=[x[0] for x in case_rows]).groupby(level=0).sum().to_numpy()
            var = (n_days / (n_days - 1.0)) * np.sum(dev ** 2) / (n_cases ** 2)
            se = float(np.sqrt(var))
            tval = float(mean_u / se) if se > 0 else None

    supp_val = None
    supp_pass = None
    if n_cases > 0:
        absf = np.array([x[2] for x in case_rows], dtype=float)
        u = np.array([x[1] for x in case_rows], dtype=float)
        med = np.median(absf)
        top = u[absf > med]
        bot = u[absf <= med]
        if top.size > 0 and bot.size > 0:
            supp_val = float(np.mean(top) - np.mean(bot))
            supp_pass = bool(supp_val > 0)

    main = {"name": mm_name, "value": mean_u,
            "statistic": {"name": "t of the mean, cases of one day pooled", "value": tval} if tval is not None else None,
            "threshold": mm_thr}
    supp = {"name": "mean unusual move of top half minus bottom half by |forecast|", "value": supp_val, "passed": supp_pass}
    sc = {"agreement": agreement, "passed": True}

    if n_cases < 50 or n_days < 50:
        status = "not observable"
        decided = f"The plan's minimum of 50 cases on 50 distinct days is not reached ({n_cases} cases, {n_days} days)."
    elif tval is None:
        status = "inconclusive"
        decided = "The day-pooled t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and tval >= 2:
        if supp_pass:
            status = "confirmed"
            decided = "The mean short-side unusual move is above 0 with a t of 2 or more and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "The t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    elif tval <= -2:
        status = "rejected"
        decided = "The mean short-side unusual move has a t of -2 or less."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
