import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    LHV = "debug_info.components.fall30.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            # 30-day return: the recorded raw value, or rebuilt from the window's prices where missing
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce").values.astype(float)
            else:
                raw = np.full(len(df), np.nan)
            rebuilt = np.full(len(df), np.nan)
            if len(df) > 30:
                rebuilt[30:] = close[30:] / close[:-30] - 1.0
            raw = np.where(np.isnan(raw), rebuilt, raw)
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array(["unknown"] * len(df))
            active = f != 0
            situation = (raw < 0) & (regime == "unknown")
            agree = active & situation & (f < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean signed excess 10-bar return, weighted by -forecast/10, short side"
    threshold = "mean > 0 with t >= 2 (confirm), mean < 0 with t <= -2 (reject), on at least 30 distinct days"
    reading = ("Situation bars are those with a negative 30-day return (recorded fall30 raw value, rebuilt from closes "
               "where missing) in the regime 'unknown' the profile leaves open, on the short side; grid bars are "
               "positions 0,10,20,... of each window with a close 10 bars later in the same window; the normal drift is "
               "the mean of all the coin's grid 10-bar returns over all its windows; the t sums the cases' deviations "
               "per UTC day (clustered standard error); the halves are the n//2 cases with the largest and smallest "
               "|forecast| (stable sort), the middle case left out when n is odd; the 30-distinct-day minimum gives "
               "'not observable' when not reached.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are short bars after a 30-day fall "
                           "inside the choppy agitated profile, as the Fidelity's situation and side require."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    vals, unw, absf, days = [], [], [], []
    for coin, wins in bars.items():
        grid_rows = []
        for w in sorted(wins.keys(), key=lambda s: (len(str(s)), str(s))):
            df = wins[w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            f = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df) - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                grid_rows.append((c1 / c0 - 1.0, f[i], ts.iloc[i].strftime("%Y-%m-%d")))
        if not grid_rows:
            continue
        drift = float(np.mean([r[0] for r in grid_rows]))
        for r, fc, d in grid_rows:
            if np.isfinite(fc) and fc < 0:
                ex = -(r - drift)
                vals.append((-fc / 10.0) * ex)
                unw.append(ex)
                absf.append(abs(fc))
                days.append(d)

    vals = np.array(vals, dtype=float)
    unw = np.array(unw, dtype=float)
    absf = np.array(absf, dtype=float)
    n_cases = int(len(vals))
    n_days = int(len(set(days)))

    mean = float(vals.mean()) if n_cases > 0 else None
    tstat = None
    if n_cases > 1 and n_days > 1:
        dev = pd.Series(vals - vals.mean()).groupby(pd.Series(days)).sum().values
        var = (n_days / (n_days - 1.0)) * float(np.sum(dev ** 2)) / (n_cases ** 2)
        se = np.sqrt(var)
        if se > 0:
            tstat = float(mean / se)

    sup_val, sup_pass = None, None
    if n_cases >= 2:
        order = np.argsort(-absf, kind="mergesort")
        k = n_cases // 2
        top = unw[order[:k]]
        bot = unw[order[-k:]]
        sup_val = float(top.mean() - bot.mean())
        sup_pass = bool(sup_val > 0)

    counts = {"distinct case days": n_days, "cases": n_cases}

    if n_days < 30:
        status = "not observable"
        decided = f"The cases fall on {n_days} distinct days, fewer than the plan's minimum of 30."
    elif tstat is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed (zero spread), so neither confirm nor reject holds."
    elif mean > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean above 0 with t >= 2 on at least 30 distinct days, and the larger-|forecast| half beats the smaller half."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting check fails (larger-|forecast| half not above the smaller half), which the plan calls inconclusive."
    elif mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "Mean below 0 with t <= -2 on at least 30 distinct days."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2 (or its sign disagrees with the mean's), meeting neither confirm nor reject."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": ({"name": "t of the mean, cases of one day summed", "value": tstat} if tstat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "unweighted mean signed excess, largest-|forecast| half minus smallest half",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
