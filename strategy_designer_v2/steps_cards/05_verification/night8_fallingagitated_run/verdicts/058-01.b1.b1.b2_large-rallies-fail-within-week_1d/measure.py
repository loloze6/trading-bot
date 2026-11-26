import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.scaled_rise.last_history_value"
    PROFILE_REGIME = "unknown"  # the regime left when neither 'chop' veto fires: falling (trend < -10) and agitated (vol pct > 0.5)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # fallback where the component is not recorded: the sign of the 3-day return from the prices
            ret3 = close / close.shift(3) - 1.0
            rise = raw.where(raw.notna(), ret3)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)
            active = fc.notna() & (fc != 0)
            situ = (regime == PROFILE_REGIME) & (rise > 0) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of 5-bar excess return (minus coin's normal 5-bar drift) on forecast, cases forecast < 0"
    threshold = "confirm: slope > 0 with t >= 2 (and supporting check); reject: slope < 0 with t <= -2; else inconclusive"
    reading_base = ("The falling-agitated profile is read as regime == 'unknown' (the detector's recorded decision, the only "
                    "regime with a strategy), the situation as a positive raw scaled 3-day rise (prices' 3-day return where not "
                    "recorded) with forecast < 0; the drift is the coin's mean 5-bar return on all its windows' grids; the "
                    "plan's 'fewer than 30 distinct days' is treated as its minimum count (not observable); clustered t uses the "
                    "CR1 small-sample correction.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement) if agreement is not None else None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "distinct days of cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars inside the falling-agitated "
                           "profile after a scaled 3-day rise, so the config does not do what the Fidelity says."
                           if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": reading_base,
        }

    # ---------- 2. criterion ----------
    rows = []
    drift_rets = {}
    for coin, wins in bars.items():
        all_r = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_r.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    rows.append((coin, fc[i], r, ts.iloc[i].floor("D")))
        drift_rets[coin] = float(np.mean(all_r)) if all_r else np.nan

    cases = pd.DataFrame(rows, columns=["coin", "f", "r", "day"])
    if len(cases):
        cases["drift"] = cases["coin"].map(drift_rets)
        cases["x"] = cases["r"] - cases["drift"]
        cases = cases.dropna(subset=["f", "x"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"distinct days of cases": n_days, "cases": n_cases}

    slope = None
    t = None
    if n_cases >= 3 and n_days >= 2 and cases["f"].nunique() > 1:
        X = np.column_stack([np.ones(n_cases), cases["f"].to_numpy()])
        y = cases["x"].to_numpy()
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        codes = pd.factorize(cases["day"])[0]
        for g in np.unique(codes):
            m = codes == g
            s = X[m].T @ u[m]
            meat += np.outer(s, s)
        G = len(np.unique(codes))
        K = 2
        corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - K))
        V = corr * XtX_inv @ meat @ XtX_inv
        slope = float(beta[1])
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        t = float(slope / se) if np.isfinite(se) and se > 0 else None

    short_mean = float((-cases["x"]).mean()) if n_cases else None
    sup_pass = (short_mean > 0) if short_mean is not None else None

    main = {"name": main_name, "value": slope,
            "statistic": {"name": "t clustered by day", "value": t} if t is not None else None,
            "threshold": threshold}
    sup = {"name": "mean 5-bar excess return in the short direction > 0", "value": short_mean,
           "passed": bool(sup_pass) if sup_pass is not None else None}

    if n_days < 30:
        status = "not observable"
        decided = f"The cases fall on {n_days} distinct days, fewer than the plan's minimum of 30."
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the mean short-direction excess return is above 0 (confirm rule)."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 (reject rule)."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the mean short-direction excess return is not above 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The slope's clustered t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
