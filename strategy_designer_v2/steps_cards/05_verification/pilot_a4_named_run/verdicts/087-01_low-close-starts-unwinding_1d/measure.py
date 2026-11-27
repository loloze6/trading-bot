import json
import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    BAND = 2.0
    CL_THR = 0.8
    MIN_CASE_DAYS = 30
    comp_col = "debug_info.components.low_close.last_history_value"

    def _get_comp(df):
        if comp_col in df.columns:
            return pd.to_numeric(df[comp_col], errors="coerce").values
        if "debug_info.components" in df.columns:
            out = []
            for v in df["debug_info.components"].values:
                val = np.nan
                try:
                    d = v
                    if isinstance(d, str):
                        d = json.loads(d)
                    if isinstance(d, dict):
                        c = d.get("low_close")
                        if isinstance(c, dict) and c.get("last_history_value") is not None:
                            val = float(c["last_history_value"])
                except Exception:
                    val = np.nan
                out.append(val)
            return np.array(out, dtype=float)
        return np.full(len(df), np.nan)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            hi = df["high"].astype(float).values
            lo = df["low"].astype(float).values
            cl = df["close"].astype(float).values
            rng = hi - lo
            with np.errstate(divide="ignore", invalid="ignore"):
                cl_price = np.where(rng > 0, (hi - cl) / rng, np.nan)
            comp = _get_comp(df)
            clv = np.where(np.isfinite(comp), comp, cl_price)
            act = f != 0
            sit = np.isfinite(clv) & (clv >= CL_THR - 1e-9)
            n_active += int(act.sum())
            n_agree += int((act & sit & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean unusual 3-day move of short cases (drift removed, sign flipped)"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 case-days and check passes; reject: mean < 0 with t <= -2 over >= 30 case-days"
    reading = ("Situation checked as close location from the high (raw component, or recomputed from prices where not recorded) >= 0.8 "
               "with a short forecast, the profile being code-added and not rebuilt; a case is the first short bet (rise of |forecast| "
               "by >= 2 from its low since the last bet) in each 3-bar grid cell of a window with a full 3-bar return in it; drift is the "
               "coin's mean non-overlapping 3-bar return over all its windows; t is clustered by signal day; the median split puts "
               "|forecast| > median in the larger half.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the active bars are short bars with the close in the bottom fifth of the day's range "
                           "(close location from the high >= 0.8), as the Fidelity's situation and side require."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin drift
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df.sort_values("timestamp")["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]):
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (day, unusual, absf)
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = df["close"].astype(float).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                m = max(-f[i], 0.0)
                if m <= 0:
                    ref = 0.0
                    continue
                if m - ref >= BAND - 1e-12:
                    bet[i] = True
                    ref = m
                else:
                    ref = min(ref, m)
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n or not (c[t] > 0) or not np.isfinite(c[t + H]):
                    continue
                r = c[t + H] / c[t] - 1.0
                u = -(r - drift[coin])
                cases.append((ts.iloc[t].strftime("%Y-%m-%d"), u, abs(f[t])))

    n_cases = len(cases)
    days = sorted(set(d for d, _, _ in cases))
    n_days = len(days)
    counts = {"case-days": n_days, "cases": n_cases}

    mean_u = float(np.mean([u for _, u, _ in cases])) if n_cases else None
    tval = None
    if n_cases > 0 and n_days > 1:
        dev = pd.Series([u - mean_u for _, u, _ in cases], index=[d for d, _, _ in cases])
        S = dev.groupby(level=0).sum().values
        var = (n_days / (n_days - 1)) * float(np.sum(S ** 2)) / (n_cases ** 2)
        se = np.sqrt(var)
        tval = float(mean_u / se) if se > 0 else None

    sup_val, sup_pass = None, None
    if n_cases >= 2:
        absf = np.array([a for _, _, a in cases])
        uu = np.array([u for _, u, _ in cases])
        med = np.median(absf)
        big = uu[absf > med]
        small = uu[absf <= med]
        if len(big) > 0 and len(small) > 0:
            sup_val = float(big.mean() - small.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {"name": main_name, "value": mean_u,
            "statistic": {"name": "t of the mean, cases clustered by day", "value": tval} if tval is not None else None,
            "threshold": threshold}
    supporting = {"name": "mean unusual move, larger |forecast| half minus smaller half", "value": sup_val, "passed": sup_pass}

    if n_days < MIN_CASE_DAYS:
        status = "not observable"
        decided = f"Only {n_days} case-days, fewer than the plan's minimum of 30."
    elif tval is not None and mean_u > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move positive with t >= 2 over at least 30 case-days, and the larger-|forecast| half beats the smaller half."
        else:
            status = "inconclusive"
            decided = "The main measure confirms (positive, t >= 2) but the supporting check fails."
    elif tval is not None and mean_u < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2 over at least 30 case-days."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
