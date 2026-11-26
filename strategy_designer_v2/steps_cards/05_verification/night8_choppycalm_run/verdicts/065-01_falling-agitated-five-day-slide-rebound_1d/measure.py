import numpy as np
import pandas as pd


def _to_datetime(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype(float)
        med = np.nanmedian(np.abs(v.values)) if len(v) else 0.0
        if med > 1e17:
            unit = "ns"
        elif med > 1e14:
            unit = "us"
        elif med > 1e11:
            unit = "ms"
        else:
            unit = "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    RAW = "debug_info.components.slide5.last_history_value"
    PPV = "debug_info.components.slide5.post_pipeline_value"
    PROFILE_REGIME = "unknown"

    n_active = 0
    n_agree = 0
    case_frames = []

    for coin in sorted(bars.keys()):
        windows = bars[coin]
        coin_rets = []
        coin_cases = []
        for w in sorted(windows.keys()):
            df = windows[w]
            if df is None or len(df) == 0:
                continue
            df = df.copy()
            df["_ts"] = _to_datetime(df["timestamp"]).values
            df = df.sort_values("_ts").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))

            # 5-bar return: recorded raw value where present, else recomputed from prices (in percent)
            ret5_px = (close / close.shift(5) - 1.0) * 100.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                ret5 = raw.where(raw.notna(), ret5_px)
            else:
                ret5 = ret5_px

            # situation check
            active = fc.notna() & (fc != 0)
            situ = (regime == PROFILE_REGIME) & (ret5 < 0) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

            # next-bar return inside the window
            r1 = close.shift(-1) / close - 1.0
            coin_rets.append(r1.dropna().values)

            ppv = pd.to_numeric(df[PPV], errors="coerce") if PPV in df.columns else pd.Series(np.nan, index=df.index)
            mask = (regime == PROFILE_REGIME) & (fc > 0) & ppv.notna() & r1.notna()
            if mask.any():
                sub = pd.DataFrame({
                    "coin": coin,
                    "day": pd.to_datetime(df.loc[mask, "_ts"]).dt.floor("D").astype(str).values,
                    "x": ppv[mask].values.astype(float),
                    "r": r1[mask].values.astype(float),
                })
                coin_cases.append(sub)
        if coin_cases:
            allr = np.concatenate(coin_rets) if coin_rets else np.array([])
            mu = float(np.mean(allr)) if len(allr) else np.nan
            cc = pd.concat(coin_cases, ignore_index=True)
            cc["ex"] = cc["r"] - mu
            case_frames.append(cc)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "slope of next-day excess return on slide5 forecast (day-clustered)"
    threshold = "confirm: slope > 0 with t >= 2 and weighted mean > 0; reject: slope < 0 with t <= -2"
    reading = ("The profile is the bars whose recorded regime is 'unknown' (the detector's non-vetoed regime); the 5-day "
               "return is the recorded slide5 raw value, recomputed from closes where missing; cases are profile bars with "
               "forecast > 0 and a next bar in the window, regressed on post_pipeline_value with cluster-robust (by UTC day) "
               "standard errors; the plan's minimum counts (200 cases, 50 days) are applied as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars inside the falling, agitated "
                           "profile with a negative five-day return, as the plan's Fidelity requires."),
            "reading": reading,
        }

    cases = pd.concat(case_frames, ignore_index=True) if case_frames else pd.DataFrame(columns=["coin", "day", "x", "r", "ex"])
    cases = cases.dropna(subset=["x", "ex"])
    n = int(len(cases))
    n_days = int(cases["day"].nunique()) if n else 0
    counts = {"cases": n, "distinct days": n_days}

    slope = None
    tval = None
    wmean = None
    if n >= 3 and np.var(cases["x"].values) > 0:
        x = cases["x"].values
        y = cases["ex"].values
        X = np.column_stack([np.ones(n), x])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        meat = np.zeros((2, 2))
        G = 0
        for _, idx in cases.groupby("day").indices.items():
            s = X[idx].T @ e[idx]
            meat += np.outer(s, s)
            G += 1
        k = 2
        corr = (G / (G - 1.0)) * ((n - 1.0) / (n - k)) if G > 1 else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        tval = float(slope / se) if se and np.isfinite(se) and se > 0 else None
    if n > 0 and cases["x"].sum() > 0:
        wmean = float((cases["ex"] * cases["x"]).sum() / cases["x"].sum())

    sup_pass = (wmean > 0) if wmean is not None else None
    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "day-clustered OLS slope t", "value": tval} if tval is not None else None),
            "threshold": threshold}
    sup = {"name": "forecast-weighted mean next-day excess return", "value": wmean, "passed": sup_pass}

    if n < 200 or n_days < 50:
        status = "not observable"
        decided = f"Minimum counts not reached: {n} cases (need 200) on {n_days} distinct days (need 50)."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the forecast-weighted mean excess return is above 0."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope t is >= 2 but the forecast-weighted mean excess return is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
