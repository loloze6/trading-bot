import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    VD = "debug_info.components.dryup.last_history_value"
    RT = "debug_info.components.slide.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            # fallback recomputation inside the window when a raw value is missing
            ret5_px = close / close.shift(5) - 1.0
            m_recent = vol.rolling(30, min_periods=30).mean()
            m_prior = m_recent.shift(30)
            with np.errstate(divide="ignore", invalid="ignore"):
                vdry_px = np.log(m_recent / m_prior)
            vdry = pd.to_numeric(df[VD], errors="coerce") if VD in df else pd.Series(np.nan, index=df.index)
            ret5 = pd.to_numeric(df[RT], errors="coerce") if RT in df else pd.Series(np.nan, index=df.index)
            vdry = vdry.where(vdry.notna(), vdry_px)
            ret5 = ret5.where(ret5.notna(), ret5_px)
            situ = (vdry < 0) & (ret5 < 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean short-side excess 5-bar return on non-overlapping grid bars with forecast < 0"
    main_thr = "confirm: mean > 0 with t >= 2 (and supporting check > 0); reject: mean < 0 with t <= -2"
    sup_name = "mean short-side excess return, |forecast| above median minus at/below median"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "distinct days with cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars where the 30-day "
                           "volume log-ratio < 0 and the 5-day return < 0, as the plan's situation requires."),
            "reading": ("The situation is checked as volume log-ratio < 0 and 5-day return < 0 with a short forecast, "
                        "from the recorded raw values (recomputed from prices when missing)."),
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_all = []
        coin_cases = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                grid_all.append(r)
                if fc[i] < 0:
                    coin_cases.append((ts.iloc[i].normalize(), r, abs(fc[i])))
        if len(grid_all) == 0:
            continue
        mu = float(np.mean(grid_all))
        for d, r, af in coin_cases:
            rows.append({"day": d, "x": -(r - mu), "absf": af})

    cases = pd.DataFrame(rows, columns=["day", "x", "absf"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean = None
    t = None
    if n_cases > 0:
        mean = float(cases["x"].mean())
        if n_days > 1:
            dev = (cases["x"] - mean).groupby(cases["day"]).sum().values
            var = (dev ** 2).sum() * n_days / (n_days - 1)
            se = np.sqrt(var) / n_cases
            t = float(mean / se) if se > 0 else None

    sup_val = None
    if n_cases > 0:
        med = cases["absf"].median()
        big = cases.loc[cases["absf"] > med, "x"]
        small = cases.loc[cases["absf"] <= med, "x"]
        if len(big) > 0 and len(small) > 0:
            sup_val = float(big.mean() - small.mean())
    sup_pass = None if sup_val is None else bool(sup_val > 0)

    reading = ("Cases are the bars at positions 0, 5, 10, ... of each window with forecast < 0 and a full 5-bar "
               "return inside the window; the coin's mean 5-day return is taken over the same grid of all its "
               "windows; t is the mean over its standard error with case deviations summed per UTC day; the "
               "'larger half' is |forecast| strictly above the median and the 'smaller half' at or below it; "
               "the plan's 30-day minimum is applied as 'not observable' per the workflow rules.")

    if n_days < 30 or mean is None or t is None:
        status = "not observable"
        decided = f"Only {n_days} distinct days with cases, below the plan's minimum of 30."
    elif mean > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Main-measure mean > 0 with t >= 2 and the supporting check > 0 (confirm rule)."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "Main-measure mean < 0 with t <= -2 (reject rule)."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check is not > 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name,
                         "value": mean,
                         "statistic": None if t is None else {"name": "t of the mean, cases summed per day", "value": t},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": {"distinct days with cases": n_days, "short cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
