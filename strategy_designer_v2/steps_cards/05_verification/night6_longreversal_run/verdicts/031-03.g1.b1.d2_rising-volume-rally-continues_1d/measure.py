import numpy as np
import pandas as pd


def _to_dt(s):
    if np.issubdtype(s.dtype, np.number):
        v = float(np.nanmax(np.abs(s.values))) if len(s) else 0.0
        unit = "ms" if v > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 14
    RAW = "debug_info.components.vol_swell.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            ret14 = close / close.shift(14) - 1.0  # inside this window only
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            active = fc != 0
            evaluable = active & ret14.notna()
            situ = (ret14 > 0) & (raw > 0)
            n_active += int(evaluable.sum())
            n_agree += int((evaluable & situ & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "forecast-weighted mean 14-bar excess return over the coin's mean, cases forecast > 0"
    thr = "confirm: mean > 0 with day-clustered t >= 2 and check passes; reject: mean < 0 with t <= -2; at least 30 distinct case days"
    reading = ("The 14-day return is recomputed as close[t]/close[t-14]-1 inside each window and the swell as the recorded "
               "raw vol_swell > 0, active bars whose first 14 rows cannot be evaluated are left out of the agreement; "
               "the coin's mean 14-bar return is the mean over all its windows' non-overlapping grid returns; the t "
               "clusters weighted deviations by UTC day with a G/(G-1) correction; the median split puts cases above "
               "the median forecast in the upper half and the rest (at or below) in the lower half, comparing plain means; "
               "the plan's 30-case-day minimum is applied as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars evaluated": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are bars with a positive 14-day return and a 14-day mean "
                           "volume above the 30-day mean with a long forecast, as the Fidelity's situation and side require."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = _to_dt(df["timestamp"])
            n = len(df)
            for p in range(0, n, H):
                if p + H >= n:
                    break
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                f = fc[p]
                if np.isfinite(f) and f > 0:
                    rows.append((coin, ts.iloc[p].normalize(), float(f), float(r)))
        coin_rets[coin] = float(np.mean(allr)) if allr else np.nan

    cases = pd.DataFrame(rows, columns=["coin", "day", "f", "r"])
    if len(cases):
        cases["x"] = cases["r"] - cases["coin"].map(coin_rets)
        cases = cases.dropna(subset=["x", "f"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"distinct case days": n_days, "cases": n_cases}

    m = None
    t = None
    if n_cases > 0 and cases["f"].sum() > 0:
        W = cases["f"].sum()
        m = float((cases["f"] * cases["x"]).sum() / W)
        dev = cases["f"] * (cases["x"] - m)
        g = dev.groupby(cases["day"]).sum()
        G = len(g)
        if G > 1:
            var = (G / (G - 1)) * float((g ** 2).sum()) / (W ** 2)
            se = np.sqrt(var)
            t = float(m / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        med = cases["f"].median()
        up = cases.loc[cases["f"] > med, "x"]
        lo = cases.loc[cases["f"] <= med, "x"]
        if len(up) and len(lo):
            sup_val = float(up.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)

    main = {"name": main_name, "value": m,
            "statistic": {"name": "day-clustered t of the weighted mean", "value": t} if t is not None else None,
            "threshold": thr}
    sup = {"name": "mean excess upper-half minus lower-half forecast (median split)",
           "value": sup_val, "passed": sup_pass}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, below the plan's minimum of 30."
    elif m is None or t is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif m > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The forecast-weighted mean excess return is above 0 with t >= 2 and the upper-minus-lower check is above 0."
    elif m > 0 and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check failed, which the plan calls inconclusive."
    elif m < 0 and t <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
