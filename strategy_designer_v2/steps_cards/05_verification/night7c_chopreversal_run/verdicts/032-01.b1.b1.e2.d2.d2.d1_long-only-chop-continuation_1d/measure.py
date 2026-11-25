import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    ER_N = 30
    COL_F = "forecast"

    def _ts(df):
        return pd.to_datetime(df["timestamp"], utc=True, errors="coerce")

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_fallback = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").astype(float)
            f = pd.to_numeric(df[COL_F], errors="coerce").fillna(0.0).astype(float)
            net = (c - c.shift(ER_N)).abs()
            path = c.diff().abs().rolling(ER_N, min_periods=ER_N).sum()
            er = net / path.replace(0.0, np.nan)
            ret30 = c / c.shift(ER_N) - 1.0
            ret7 = c / c.shift(H) - 1.0
            computable = er.notna() & ret30.notna() & ret7.notna()
            sit = (er <= 0.30 + 1e-9) & (ret30 > 0) & (ret7 > 0)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            active = f != 0
            for i in np.where(active.values)[0]:
                n_active += 1
                if bool(computable.iloc[i]):
                    in_sit = bool(sit.iloc[i])
                else:
                    n_fallback += 1
                    in_sit = regime.iloc[i] == "chop"
                if in_sit and f.iloc[i] > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    reading = ("Situation recomputed per window from closes (ER30 = |close[t]-close[t-30]| / sum of 30 absolute daily "
               "changes, 30- and 7-bar simple returns), with the recorded regime=='chop' used only on active bars lacking "
               "30 bars of in-window history; the coin's mean 7-day return is the mean over its non-overlapping grid "
               "returns of all windows; terciles split the forecast-sorted cases into three near-equal groups "
               "(np.array_split); the day-clustered t uses per-day summed deviations with a D/(D-1) correction; "
               "below the minimum counts the status is 'not observable'.")

    main_name = "mean unusual 7-day move on positive-forecast grid bars"
    main_thr = "confirm: mean > 0 with t >= 2 (and tercile difference > 0); reject: t <= -2"
    sup_name = "top minus bottom forecast tercile mean unusual move"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of the {n_active} active bars are long bars of the plan's situation "
                           "(ER30 <= 0.30, 30-bar return > 0, 7-bar return > 0), below the 90% required."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").astype(float).values
            f = pd.to_numeric(df[COL_F], errors="coerce").astype(float).values
            ts = _ts(df)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                coin_rets.append(r)
                if np.isfinite(f[i]) and f[i] > 0:
                    d = ts.iloc[i]
                    day = d.floor("D") if pd.notna(d) else pd.NaT
                    coin_cases.append((r, float(f[i]), day))
        if len(coin_rets) == 0:
            continue
        drift = float(np.mean(coin_rets))
        for r, fv, day in coin_cases:
            rows.append({"coin": coin, "u": r - drift, "f": fv, "day": day})

    cases = pd.DataFrame(rows, columns=["coin", "u", "f", "day"])
    cases = cases.dropna(subset=["u", "f", "day"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"grid cases with a positive forecast": n_cases, "distinct days": n_days}

    mean_u = float(cases["u"].mean()) if n_cases else None
    t = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["u"] - mean_u
        s = dev.groupby(cases["day"]).sum().values
        D = len(s)
        var = (D / (D - 1.0)) * np.sum(s ** 2) / (n_cases ** 2)
        se = np.sqrt(var)
        t = float(mean_u / se) if se > 0 else None

    diff = None
    if n_cases >= 3:
        srt = cases.sort_values("f", kind="mergesort")
        parts = np.array_split(srt["u"].values, 3)
        if len(parts[0]) > 0 and len(parts[2]) > 0:
            diff = float(np.mean(parts[2]) - np.mean(parts[0]))
    sup_pass = None if diff is None else bool(diff > 0)

    main = {"name": main_name, "value": mean_u,
            "statistic": None if t is None else {"name": "day-clustered t of the mean", "value": t},
            "threshold": main_thr}
    sup = {"name": sup_name, "value": diff, "passed": sup_pass}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = (f"Minimum not reached: {n_cases} positive-forecast grid cases on {n_days} distinct days, "
                   "the plan needs at least 30 cases on at least 30 distinct days.")
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed (zero standard error)."
    elif mean_u > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2 and top-minus-bottom tercile difference above 0 (confirm rule)."
    elif t <= -2:
        status = "rejected"
        decided = "Mean unusual move has t <= -2 (reject rule)."
    elif t >= 2:
        status = "inconclusive"
        decided = "Main t >= 2 but the top-minus-bottom tercile difference is not above 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
