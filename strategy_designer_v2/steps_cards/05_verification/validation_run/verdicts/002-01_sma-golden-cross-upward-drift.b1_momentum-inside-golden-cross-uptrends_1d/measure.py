import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    XCOL = "debug_info.components.mom20.last_history_value"

    def is_trending(series):
        return series.astype(str).str.strip().str.lower() == "trending"

    # ---------- 1. situation check ----------
    # Situation: regime "trending" (SMA50 > SMA200, the detector's rule) and a 20-bar rise
    # (raw mom20 > 0), on the long side.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if XCOL in df.columns:
                x = pd.to_numeric(df[XCOL], errors="coerce")
            else:
                x = pd.Series(np.nan, index=df.index)
            if "regime" in df.columns:
                trend = is_trending(df["regime"])
            else:
                trend = pd.Series(False, index=df.index)
            situ = trend & x.notna() & (x > 0)
            ok = active & situ & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of excess 10-bar forward return on recorded 20-bar return, in-regime grid bars"
    thr = "confirm if slope t >= 2 and supporting difference > 0; reject if slope t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of the trending regime "
                           "with a positive raw 20-bar return, so the config does not trade the plan's situation."
                           if n_active > 0 else "No bar has a non-zero forecast, so the plan's situation is never traded."),
            "reading": "Situation taken as regime 'trending' plus a raw mom20 last_history_value above 0, side long.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            x = (pd.to_numeric(df[XCOL], errors="coerce").to_numpy(dtype=float)
                 if XCOL in df.columns else np.full(len(df), np.nan))
            trend = (is_trending(df["regime"]).to_numpy()
                     if "regime" in df.columns else np.zeros(len(df), bool))
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                rows.append({"coin": coin, "r": r, "x": x[t], "fc": fc[t], "trend": bool(trend[t])})

    d = pd.DataFrame(rows, columns=["coin", "r", "x", "fc", "trend"])
    if len(d):
        coin_mean = d.groupby("coin")["r"].mean()
        d["ex"] = d["r"] - d["coin"].map(coin_mean)
    else:
        d["ex"] = []
    cases = d[d["trend"] & d["x"].notna() & d["ex"].notna()]
    n_cases = int(len(cases))

    slope = None
    tstat = None
    if n_cases >= 3 and cases["x"].nunique() > 1:
        lr = stats.linregress(cases["x"].to_numpy(float), cases["ex"].to_numpy(float))
        slope = float(lr.slope)
        tstat = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    pos = cases[cases["fc"] > 0]["ex"]
    zero = cases[cases["fc"] == 0]["ex"]
    diff = float(pos.mean() - zero.mean()) if len(pos) > 0 and len(zero) > 0 else None
    sup_pass = (diff > 0) if diff is not None else None

    counts = {
        "independent in-regime cases": n_cases,
        "cases with positive forecast": int(len(pos)),
        "cases with zero forecast": int(len(zero)),
    }

    if n_cases < 50:
        status = "not observable"
        decided = f"Only {n_cases} independent in-regime cases, fewer than the 50 the plan requires."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif tstat >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The slope t is 2 or more and the supporting difference is positive."
    elif tstat <= -2:
        status = "rejected"
        decided = "The slope t is -2 or less."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "The slope t is 2 or more but the supporting difference is 0 or less (or not computable)."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": tstat} if tstat is not None else None,
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean excess 10-bar return, positive-forecast minus zero-forecast cases",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Spread above 0 is read from the regime column being 'trending'. The coin's mean 10-bar return "
                    "is taken over all grid bars of all its windows. The regressor is the raw mom20 "
                    "last_history_value, and the forecast groups use the forecast on the same grid bars."),
    }
