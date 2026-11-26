import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RUN_COL = "debug_info.components.run_len.last_history_value"
    MIN_TOTAL = 100
    MIN_GROUP = 20

    # ---------- coin drift: mean 1-day return over all windows of the coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) >= 2:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        drift[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- situation check and case collection ----------
    n_active = 0
    n_agree = 0
    cases = []  # (day, unusual move, run length)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if RUN_COL in df.columns:
                run = pd.to_numeric(df[RUN_COL], errors="coerce").to_numpy(dtype=float)
            else:
                run = np.full(len(df), np.nan)
            regime = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            days = ts.dt.floor("D").astype(str).to_numpy()
            n = len(df)
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                # situation: run-break day (raw run >= 1, an up close when the prior close is in the window),
                # inside the falling-calm profile (detector regime mean_reversion, i.e. not vetoed), short side
                in_run = np.isfinite(run[t]) and run[t] >= 1
                up_ok = True
                if t >= 1 and np.isfinite(close[t]) and np.isfinite(close[t - 1]):
                    up_ok = close[t] > close[t - 1]
                in_profile = regime[t] == "mean_reversion"
                if in_run and up_ok and in_profile and f < 0:
                    n_agree += 1
            # cases: forecast below 0, next-day return inside the window
            for t in range(n - 1):
                f = fc[t]
                if not np.isfinite(f) or f >= 0:
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + 1]) and close[t] > 0):
                    continue
                if not np.isfinite(drift[coin]):
                    continue
                r = close[t + 1] / close[t] - 1.0
                u = -(r - drift[coin])
                cases.append((days[t], float(u), float(run[t]) if np.isfinite(run[t]) else np.nan))

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90

    reading = ("Cases are all coin-day bars with forecast below 0 and a next-day close in the same window, each counted "
               "as one case-day toward the minimums (100 total, 20 per run group, groups by the recorded run length: "
               ">=3 vs 1-2); the falling-calm profile in the situation check is read from the detector's recorded regime "
               "(mean_reversion = not vetoed) since its profile components are not recorded; the day-clustered t uses "
               "deviations summed per UTC day with a D/(D-1) correction.")

    main_name = "mean next-day unusual move on short cases (short direction, minus coin mean daily return)"
    main_thr = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2"
    sup_name = "unusual move, run >= 3 minus run 1-2 (Welch t)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short run-break days "
                           "(run >= 1 on an up close) inside the falling-calm profile, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    u = np.array([c[1] for c in cases], dtype=float)
    runs = np.array([c[2] for c in cases], dtype=float)
    dayk = np.array([c[0] for c in cases])
    n_cases = int(len(u))
    long_mask = np.isfinite(runs) & (runs >= 3)
    short_mask = np.isfinite(runs) & (runs >= 1) & (runs < 3)
    n_long = int(long_mask.sum())
    n_short = int(short_mask.sum())
    n_days = int(len(np.unique(dayk))) if n_cases else 0

    # main measure with day-clustered t
    mean_u = float(np.mean(u)) if n_cases else None
    t_main = None
    if n_cases >= 2 and n_days >= 2:
        dev = u - mean_u
        s = pd.Series(dev).groupby(dayk).sum().to_numpy()
        D = len(s)
        var_mean = (D / (D - 1.0)) * np.sum(s ** 2) / (n_cases ** 2)
        if var_mean > 0:
            t_main = float(mean_u / np.sqrt(var_mean))

    # supporting check
    diff = None
    t_diff = None
    if n_long >= 2 and n_short >= 2:
        a = u[long_mask]
        b = u[short_mask]
        diff = float(np.mean(a) - np.mean(b))
        tt = stats.ttest_ind(a, b, equal_var=False)
        if np.isfinite(tt.statistic):
            t_diff = float(tt.statistic)

    counts = {"case-days in total": n_cases, "case-days with run >= 3": n_long,
              "case-days with run 1-2": n_short, "distinct days with cases": n_days}

    sup_passed = None
    if diff is not None and t_diff is not None:
        sup_passed = bool(diff > 0 and t_diff >= 2)

    main = {"name": main_name, "value": mean_u,
            "statistic": {"name": "t of the mean, cases summed per day", "value": t_main} if t_main is not None else None,
            "threshold": main_thr}
    sup = {"name": sup_name, "value": diff, "passed": sup_passed}
    if t_diff is not None:
        sup["welch_t"] = t_diff

    if n_cases < MIN_TOTAL or n_long < MIN_GROUP or n_short < MIN_GROUP:
        status = "not observable"
        missing = []
        if n_cases < MIN_TOTAL:
            missing.append(f"{n_cases} case-days in total (< 100)")
        if n_long < MIN_GROUP:
            missing.append(f"{n_long} case-days with run >= 3 (< 20)")
        if n_short < MIN_GROUP:
            missing.append(f"{n_short} case-days with run 1-2 (< 20)")
        decided = "Minimum count not reached: " + "; ".join(missing) + "."
    else:
        main_reject = mean_u is not None and t_main is not None and mean_u < 0 and t_main <= -2
        diff_reject = t_diff is not None and t_diff <= -2
        main_confirm = mean_u is not None and t_main is not None and mean_u > 0 and t_main >= 2
        if main_reject:
            status = "rejected"
            decided = "Reject rule: the main mean unusual move is negative with t <= -2."
        elif diff_reject:
            status = "rejected"
            decided = "Reject rule: the long-run minus short-run difference has Welch t <= -2."
        elif main_confirm and sup_passed:
            status = "confirmed"
            decided = ("Confirm rule: the main mean unusual move is positive with t >= 2 and the long-run minus "
                       "short-run difference is positive with Welch t >= 2.")
        elif main_confirm:
            status = "inconclusive"
            decided = ("Inconclusive: the main measure meets the confirm rule but the supporting check "
                       "(long-run minus short-run positive with t >= 2) fails.")
        else:
            status = "inconclusive"
            decided = "Inconclusive rule: the main t is between -2 and 2 (or undefined) and no reject rule is met."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
