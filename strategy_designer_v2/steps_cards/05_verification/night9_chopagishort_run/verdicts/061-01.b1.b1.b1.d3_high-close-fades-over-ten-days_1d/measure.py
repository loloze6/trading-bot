import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    LOC_COL = "debug_info.components.high_close.last_history_value"

    def to_days(ts):
        s = pd.Series(ts)
        if pd.api.types.is_numeric_dtype(s):
            mx = float(s.max()) if len(s) else 0.0
            unit = "ms" if mx > 1e11 else "s"
            dt = pd.to_datetime(s, unit=unit, utc=True)
        else:
            dt = pd.to_datetime(s, utc=True)
        return dt.dt.strftime("%Y-%m-%d").values

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            hi = pd.to_numeric(df["high"], errors="coerce").values
            lo = pd.to_numeric(df["low"], errors="coerce").values
            cl = pd.to_numeric(df["close"], errors="coerce").values
            rng = hi - lo
            with np.errstate(divide="ignore", invalid="ignore"):
                loc_px = np.where(rng > 0, (cl - lo) / rng, np.nan)
            if LOC_COL in df.columns:
                raw = pd.to_numeric(df[LOC_COL], errors="coerce").values
                loc = np.where(np.isnan(raw), loc_px, raw)
            else:
                loc = loc_px
            reg = df["regime"].astype(str).values
            active = f != 0
            situ = (loc >= 0.8) & (reg == "mean_reversion") & (f < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean unusual 10-bar move per short case, in the short direction"
    main_thr = "confirm: mean > 0 with day-pooled t >= 2 over >= 30 case-days (and check passes); reject: mean < 0 with t <= -2 over >= 30 case-days"

    reading_base = ("The profile part of the situation is read from the recorded regime (mean_reversion is only reached when no "
                    "chop veto of the profile fires) since the detector's components are not recorded, the close location from "
                    "the raw value or else the prices; a case is the first short bet (rise of |forecast| on the short side of at "
                    "least 2 from its lowest level since the last bet) in each 10-bar grid cell of a window, the t uses day-clustered "
                    "deviations, the stronger half is |forecast| above the case median, and fewer than 30 case-days gives "
                    "'not observable' per the workflow's minimum-count rule.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with a close location of 0.8 or more "
                           "in the choppy agitated profile (mean_reversion regime)." if n_active > 0 else
                           "The record has no active bars, so the forecast never shows the plan's short situation."),
            "reading": reading_base,
        }

    # ---------- 2. criterion ----------
    # normal drift per coin
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            cl = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(cl) - H, H):
                a, b = cl[p], cl[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (day, unusual, |forecast|)
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            cl = pd.to_numeric(df["close"], errors="coerce").values
            days = to_days(df["timestamp"].values)
            n = len(f)
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                m = -f[i] if f[i] < 0 else 0.0
                if m <= 0:
                    ref = 0.0
                    continue
                if m - ref >= BAND:
                    bet[i] = True
                    ref = m
                else:
                    ref = min(ref, m)
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                a, b = cl[t], cl[t + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                r = b / a - 1.0
                u = -(r - drift[coin])
                cases.append((days[t], u, abs(f[t])))

    n_cases = len(cases)
    case_days = len(set(c[0] for c in cases))
    mean_u = None
    tval = None
    if n_cases > 0:
        u = np.array([c[1] for c in cases])
        d = np.array([c[0] for c in cases])
        mean_u = float(u.mean())
        dev = pd.Series(u - mean_u).groupby(d).sum().values
        D = len(dev)
        if D > 1:
            var = (dev ** 2).sum() * D / (D - 1)
            se = np.sqrt(var) / n_cases
            tval = float(mean_u / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        u = np.array([c[1] for c in cases])
        a = np.array([c[2] for c in cases])
        med = np.median(a)
        strong = u[a > med]
        weak = u[a <= med]
        if len(strong) > 0 and len(weak) > 0:
            sup_val = float(strong.mean() - weak.mean())
            sup_pass = bool(sup_val > 0)

    counts = {"case-days": int(case_days), "cases": int(n_cases)}

    if case_days < 30:
        status = "not observable"
        decided = f"Only {case_days} case-days, below the plan's minimum of 30 case-days."
    elif tval is not None and mean_u > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move above 0 with t of 2 or more over at least 30 case-days, and the stronger half beats the weaker half."
        else:
            status = "inconclusive"
            decided = "The main measure meets the confirm rule but the supporting check (stronger minus weaker half above 0) fails."
    elif tval is not None and mean_u < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t of -2 or less over at least 30 case-days."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or could not be computed), meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": mean_u,
                         "statistic": ({"name": "t of the mean, cases of one day pooled", "value": tval}
                                       if tval is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": "mean unusual move of stronger |forecast| half minus weaker half",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
