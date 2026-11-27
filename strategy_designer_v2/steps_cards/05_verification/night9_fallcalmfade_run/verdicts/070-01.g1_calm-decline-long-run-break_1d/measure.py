import numpy as np
import pandas as pd


def _to_day(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype(float)
        med = np.nanmedian(v.values) if len(v) else 0.0
        unit = "ms" if med > 1e11 else "s"
        dt = pd.to_datetime(v, unit=unit, utc=True)
    else:
        dt = pd.to_datetime(s, utc=True)
    return dt.dt.floor("D").astype("int64").values


def measure(bars):
    RAW = "debug_info.components.run_break.last_history_value"

    # ---------- coin mean daily return over all windows ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(allr)) if len(allr) else np.nan

    n_active = 0
    n_agree = 0
    case_r, case_w, case_day = [], [], []
    grp_long, grp_single = [], []

    for coin, wins in bars.items():
        mu = coin_mu[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            regime = df["regime"].astype(str).values
            raw = (pd.to_numeric(df[RAW], errors="coerce").values
                   if RAW in df.columns else np.full(n, np.nan))
            days = _to_day(df["timestamp"])
            profile = regime == "unknown"  # not vetoed: falling (trend < -10) and calm (vol pct <= 0.5)

            prev = np.full(n, np.nan)
            prev[1:] = c[:-1]
            up = c > prev
            down = c < prev
            # down-run length ending at t-1, and whether its start was seen in the window
            runlen = np.zeros(n, dtype=int)
            run_known = np.zeros(n, dtype=bool)
            for t in range(1, n):
                k = 0
                j = t - 1
                while j >= 1 and down[j]:
                    k += 1
                    j -= 1
                runlen[t] = k
                # run start seen if bar j (the one before the run) is in window with a known direction
                run_known[t] = (j >= 1) or (k == 0)
            nxt = np.full(n, np.nan)
            nxt[:-1] = c[1:] / c[:-1] - 1.0

            # ---------- situation check ----------
            for t in range(n):
                if not np.isfinite(fc[t]) or fc[t] == 0:
                    continue
                n_active += 1
                ok = profile[t] and np.isfinite(raw[t]) and raw[t] > 0 and fc[t] < 0
                if ok and t >= 1:
                    ok = bool(up[t])
                if ok and t >= 2:
                    ok = bool(down[t - 1])
                if ok:
                    n_agree += 1

            # ---------- main measure cases ----------
            for t in range(n - 1):
                if np.isfinite(fc[t]) and fc[t] < 0 and np.isfinite(nxt[t]) and np.isfinite(mu):
                    case_r.append(-(nxt[t] - mu))
                    case_w.append(abs(fc[t]))
                    case_day.append(days[t])

            # ---------- supporting check (rebuilt from prices, falling calm bars) ----------
            for t in range(1, n - 1):
                if not (profile[t] and up[t] and np.isfinite(nxt[t]) and np.isfinite(mu)):
                    continue
                k = runlen[t]
                if k == 0:
                    continue
                ex = nxt[t] - mu
                if k >= 2:
                    grp_long.append(ex)
                elif k == 1 and run_known[t]:
                    grp_single.append(ex)

    agreement = (n_agree / n_active) if n_active > 0 else None
    sit_passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "abs(forecast)-weighted mean short-side next-day excess move"
    thr = "confirm: > 0 with t >= 2 over >= 30 case-days; reject: < 0 with t <= -2 over >= 30 case-days"
    reading = ("Falling calm is taken as the detector's 'unknown' (not vetoed) regime on each bar, both for the "
               "situation check and for the supporting check's profile (the 60-bar trend and 365-bar vol percentile "
               "cannot be rebuilt inside a window), run lengths are rebuilt from window closes with single-day breaks "
               "kept only when the run's start is seen, the t clusters weighted deviations by calendar day with a "
               "G/(G-1) correction, and case-days are the distinct days with a short forecast.")

    if not sit_passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short run-breaking up closes "
                           "(down run of 2+) in the falling calm regime, as the Fidelity requires."),
            "reading": reading,
        }

    r = np.array(case_r, float)
    wts = np.array(case_w, float)
    dd = np.array(case_day)
    n_days = int(len(np.unique(dd))) if len(dd) else 0

    m = None
    tstat = None
    if len(r) > 0 and wts.sum() > 0:
        m = float(np.sum(wts * r) / np.sum(wts))
        dev = pd.Series(wts * (r - m)).groupby(dd).sum().values
        G = len(dev)
        if G > 1:
            var = (G / (G - 1)) * np.sum(dev ** 2) / (np.sum(wts) ** 2)
            se = np.sqrt(var)
            tstat = float(m / se) if se > 0 else None

    if len(grp_long) > 0 and len(grp_single) > 0:
        diff = float(np.mean(grp_long) - np.mean(grp_single))
        sup_passed = bool(diff < 0)
    else:
        diff = None
        sup_passed = None

    counts = {"case-days": n_days, "cases": int(len(r)),
              "breaks of 2+ down days": int(len(grp_long)),
              "breaks of a single down day": int(len(grp_single))}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} case-days, below the plan's minimum of 30."
    elif m is None or tstat is None:
        status = "inconclusive"
        decided = "The main measure's t could not be computed, so neither the confirm nor the reject rule is met."
    elif m > 0 and tstat >= 2:
        if sup_passed is True:
            status = "confirmed"
            decided = "Main measure positive with t >= 2 over at least 30 case-days and the supporting difference below 0."
        else:
            status = "inconclusive"
            decided = "Main measure meets the confirm rule but the supporting check is not below 0 (or not computable)."
    elif m < 0 and tstat <= -2:
        status = "rejected"
        decided = "Main measure negative with t <= -2 over at least 30 case-days: rises follow the breaks."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": m,
                         "statistic": None if tstat is None else {"name": "t of the weighted mean, clustered by day",
                                                                  "value": tstat},
                         "threshold": thr},
        "supporting_check": {"name": "mean next-day excess return, breaks of 2+ down days minus breaks of 1",
                             "value": diff, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
