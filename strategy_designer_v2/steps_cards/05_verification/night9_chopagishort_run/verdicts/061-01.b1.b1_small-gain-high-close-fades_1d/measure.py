import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    CL_THR = 0.8
    MIN_CASES = 30
    MIN_DAYS = 30
    RAW_COL = "debug_info.components.small_gain.last_history_value"
    EPS = 1e-9

    def prep(df):
        d = df.copy()
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
        d = d.sort_values("timestamp").reset_index(drop=True)
        return d

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = prep(df)
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            hi = d["high"].astype(float).values
            lo = d["low"].astype(float).values
            cl = d["close"].astype(float).values
            rng = hi - lo
            with np.errstate(divide="ignore", invalid="ignore"):
                loc = np.where(rng > 0, (cl - lo) / rng, np.nan)
            active = f != 0
            in_sit = np.where(np.isnan(loc), False, loc >= CL_THR - EPS)
            n_active += int(active.sum())
            n_agree += int((active & in_sit & (f < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean unusual 5-bar move per short bet, in the short direction"
    main_thr = "confirm: mean > 0 with day-pooled t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2"
    sup_name = "mean unusual move of smaller-gain half minus larger-gain half (split at median raw gain)"
    reading = ("Situation checked as close location (close-low)/(high-low) >= 0.8 on the short side only, since the "
               "profile's 365-day volatility percentile and 60-bar trend cannot be rebuilt from the recorded windows; "
               "a case is the first short bet (forecast falling >= 2 points below its least-short level since the last "
               "bet, reset to 0 after a flat or long bar) in each 5-bar grid cell from the window's first row with a "
               "full 5-bar return inside the window; the day-pooled t uses per-day sums of deviations with a D/(D-1) "
               "correction; the median split puts cases strictly below the median in the smaller-gain half and "
               "strictly above it in the larger-gain half, cases at the median and without a raw value left out.")

    if agreement is None or not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars whose close sits at 0.8 "
                           "or more of the day's range, as the plan's Fidelity requires"
                           if agreement is not None else "No bar has a non-zero forecast."),
            "reading": reading,
        }

    # ---------- 2. normal drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = prep(df)["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]):
                    rets.append(c[i + H] / c[i] - 1.0)
        if rets:
            drift[coin] = float(np.mean(rets))

    # ---------- 3. cases ----------
    cases = []
    for coin, wins in bars.items():
        if coin not in drift:
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = prep(df)
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            c = d["close"].astype(float).values
            raw = (pd.to_numeric(d[RAW_COL], errors="coerce").values
                   if RAW_COL in d.columns else np.full(len(d), np.nan))
            ts = d["timestamp"]
            ref = 0.0
            prev_short = False
            used_cells = set()
            for i in range(len(d)):
                fi = f[i]
                if fi >= 0:
                    ref = 0.0
                    prev_short = False
                    continue
                if not prev_short:
                    ref = 0.0
                prev_short = True
                if fi <= ref - BAND + EPS:
                    ref = fi
                    cell = i // H
                    if cell in used_cells:
                        continue
                    used_cells.add(cell)
                    if i + H < len(d) and c[i] > 0 and np.isfinite(c[i + H]):
                        r = c[i + H] / c[i] - 1.0
                        u = -(r - drift[coin])
                        cases.append({
                            "coin": coin,
                            "day": ts.iloc[i].floor("D"),
                            "u": u,
                            "raw": float(raw[i]) if np.isfinite(raw[i]) else np.nan,
                        })
                else:
                    ref = max(ref, fi)

    n_cases = len(cases)
    cdf = pd.DataFrame(cases) if cases else pd.DataFrame(columns=["coin", "day", "u", "raw"])
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    mean_u = float(cdf["u"].mean()) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        dev = cdf["u"] - mean_u
        s_day = dev.groupby(cdf["day"]).sum().values
        D = len(s_day)
        var = (D / (D - 1)) * float(np.sum(s_day ** 2)) / (n_cases ** 2)
        se = np.sqrt(var)
        t_val = float(mean_u / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    sub = cdf.dropna(subset=["raw"]) if n_cases else cdf
    if len(sub) >= 2:
        med = float(sub["raw"].median())
        small = sub.loc[sub["raw"] < med, "u"]
        large = sub.loc[sub["raw"] > med, "u"]
        if len(small) > 0 and len(large) > 0:
            sup_val = float(small.mean() - large.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"cases": int(n_cases), "distinct days": int(n_days)}
    main = {"name": main_name, "value": mean_u,
            "statistic": {"name": "t of the mean, cases of one day pooled", "value": t_val} if t_val is not None else None,
            "threshold": main_thr}
    supporting = {"name": sup_name, "value": sup_val, "passed": sup_pass}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = (f"The plan's minimum of {MIN_CASES} cases on {MIN_DAYS} distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The day-pooled t cannot be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 and the smaller-gain minus larger-gain difference is above 0."
        else:
            status = "inconclusive"
            decided = "The mean unusual move is positive with t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The day-pooled t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
