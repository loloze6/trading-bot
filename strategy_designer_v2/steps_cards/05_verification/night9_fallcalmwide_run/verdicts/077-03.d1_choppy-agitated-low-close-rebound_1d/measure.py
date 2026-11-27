import numpy as np
import pandas as pd


def measure(bars):
    BAND = 2.0
    MIN_CASES = 200
    MIN_DAYS = 100
    T_CONF = 2.0

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp")
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            hi = pd.to_numeric(d["high"], errors="coerce").values
            lo = pd.to_numeric(d["low"], errors="coerce").values
            cl = pd.to_numeric(d["close"], errors="coerce").values
            reg = d["regime"].astype(str).str.strip().str.lower().values
            active = f != 0
            # choppy agitated profile = regime detector's non-chop decision ("unknown"),
            # close strictly below the day's mid-range, long side
            situ = (reg == "unknown") & (cl < (hi + lo) / 2.0) & (f > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars inside the "
                           "choppy agitated profile (regime 'unknown') with the close below the day's mid-range"
                           if n_active > 0 else "The record has no bar with a non-zero forecast to compare with the plan's situation"),
            "reading": "The profile is read from the recorded regime ('unknown' = not vetoed to chop), the low close from the prices, the side as long.",
        }

    # ---------- coin mean daily return over all windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            cl = pd.to_numeric(df.sort_values("timestamp")["close"], errors="coerce").values
            r = cl[1:] / cl[:-1] - 1.0
            rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- cases and positive-forecast bars ----------
    case_r, case_w, case_day = [], [], []
    pos_f, pos_r = [], []
    for coin, wins in bars.items():
        mu = coin_mean.get(coin, np.nan)
        if not np.isfinite(mu):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            cl = pd.to_numeric(d["close"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            days = ts.dt.strftime("%Y-%m-%d").values
            n = len(d)
            nxt = np.full(n, np.nan)
            if n > 1:
                nxt[:-1] = cl[1:] / cl[:-1] - 1.0
            ex = nxt - mu
            ref = 0.0
            for i in range(n):
                fi = f[i]
                is_case = False
                if fi <= 0:
                    ref = 0.0
                else:
                    if fi - ref >= BAND:
                        is_case = True
                        ref = fi
                    else:
                        ref = min(ref, fi)
                if fi > 0 and np.isfinite(ex[i]):
                    pos_f.append(fi)
                    pos_r.append(ex[i])
                    if is_case:
                        case_r.append(ex[i])
                        case_w.append(fi)
                        case_day.append(days[i])

    case_r = np.array(case_r, dtype=float)
    case_w = np.array(case_w, dtype=float)
    n_cases = int(len(case_r))
    n_days = int(len(set(case_day)))

    wmean = None
    tstat = None
    if n_cases > 0 and case_w.sum() > 0:
        W = case_w.sum()
        wmean = float(np.sum(case_w * case_r) / W)
        dev = pd.Series(case_w * (case_r - wmean)).groupby(np.array(case_day)).sum().values
        G = len(dev)
        if G > 1:
            var = (G / (G - 1.0)) * np.sum(dev ** 2) / (W ** 2)
            se = np.sqrt(var)
            tstat = float(wmean / se) if se > 0 else None

    slope = None
    pos_f = np.array(pos_f, dtype=float)
    pos_r = np.array(pos_r, dtype=float)
    if len(pos_f) >= 2 and np.var(pos_f) > 0:
        slope = float(np.polyfit(pos_f, pos_r, 1)[0])
    slope_pass = None if slope is None else bool(slope > 0)

    main = {
        "name": "forecast-weighted mean next-day excess return over cases",
        "value": wmean,
        "statistic": None if tstat is None else {"name": "t of weighted mean, cases summed per day", "value": tstat},
        "threshold": "mean > 0 with t >= 2 (confirm, with positive slope); mean < 0 with t <= -2 (reject)",
    }
    support = {"name": "OLS slope of next-day excess return on forecast, forecast > 0",
               "value": slope, "passed": slope_pass}
    counts = {"cases": n_cases, "distinct days": n_days}
    reading = ("A case is a long-side forecast rise of at least 2 points from its lowest level since the last bet "
               "(reset to 0 when flat), on every bar since the horizon is 1; the excess return is the next close-to-close "
               "return minus the coin's pooled mean daily return over all its windows; the t uses the weighted mean's "
               "standard error with weighted deviations summed per UTC day (G/(G-1) factor); the plan's minimum counts "
               "map to 'not observable'; the profile is read from the recorded regime 'unknown'.")

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases (need 200) on {n_days} distinct days (need 100).")
    elif wmean is None or tstat is None:
        status = "inconclusive"
        decided = "The t of the main mean could not be computed, so neither confirm nor reject is met."
    elif wmean > 0 and tstat >= T_CONF:
        if slope_pass:
            status = "confirmed"
            decided = "The main mean is above 0 with t >= 2 and the supporting slope is positive."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting slope is at or below 0 (or not computable): inconclusive."
    elif wmean < 0 and tstat <= -T_CONF:
        status = "rejected"
        decided = "The main mean is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the main mean lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
