import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.day_fall.last_history_value"
    PROFILE_REGIME = "unknown"

    def _num(df, col):
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        return pd.Series(np.nan, index=df.index)

    # ---------- coin mean daily return over all windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = _num(d, "close")
            r = (c.shift(-1) / c - 1.0).iloc[:-1]
            rets.append(r.dropna())
        allr = pd.concat(rets) if rets else pd.Series(dtype=float)
        coin_mean[coin] = float(allr.mean()) if len(allr) else np.nan

    # ---------- collect rows ----------
    n_active = 0
    n_agree = 0
    case_rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = _num(d, "close")
            fc = _num(d, "forecast").fillna(0.0)
            raw = _num(d, RAW)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)
            day_ret = close / close.shift(1) - 1.0
            nxt = close.shift(-1) / close - 1.0
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            day = ts.dt.floor("D")

            # the situation: inside the falling agitated profile (the detector's decision, regime 'unknown'),
            # on a down day (raw one-day return < 0; recomputed from closes when the raw value is missing)
            down = raw < 0
            down = down.where(raw.notna(), day_ret < 0).fillna(False).astype(bool)
            situation = (regime == PROFILE_REGIME) & down

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

            for i in range(len(d)):
                if fc.iloc[i] > 0 and pd.notna(nxt.iloc[i]) and pd.notna(day.iloc[i]):
                    case_rows.append((coin, day.iloc[i], float(fc.iloc[i]),
                                      float(nxt.iloc[i]) - coin_mean.get(coin, np.nan)))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("The profile is read from the recorded regime (the detector's components are not recorded and their "
               "60- and 365-bar warm-ups lie outside the windows) and a down day from the raw one-day return < 0; "
               "the slope is a pooled OLS with intercept of the next-day excess return (fraction) on the forecast "
               "across all coins, with CR1 standard errors clustered by UTC day, and the cases are every bar with "
               "forecast > 0 (a 1-bar horizon makes every bar its own grid cell).")

    threshold = "confirm: slope > 0 with t >= 2 and weighted mean > 0; reject: slope < 0 with t <= -2; min 100 cases on 60 distinct days"
    main_name = "slope of next-day excess return on forecast (return per forecast point)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on down days inside the "
                           "falling agitated profile (regime 'unknown'), so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows, columns=["coin", "day", "f", "y"]).dropna()
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    slope = None
    tstat = None
    wmean = None
    if n_cases >= 3:
        X = np.column_stack([np.ones(n_cases), cases["f"].values])
        y = cases["y"].values
        XtX_inv = np.linalg.pinv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in cases.groupby("day").indices.items():
            s = X[idx].T @ u[idx]
            meat += np.outer(s, s)
        G = n_days
        k = 2
        corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - k)) if G > 1 and n_cases > k else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        slope = float(beta[1])
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        tstat = float(slope / se) if se and np.isfinite(se) and se > 0 else None
        sf = cases["f"].sum()
        wmean = float((cases["y"] * cases["f"]).sum() / sf) if sf > 0 else None

    sup_passed = None if wmean is None else bool(wmean > 0)

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = (f"The plan's minimum of 100 cases on at least 60 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tstat >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the forecast-weighted mean excess return is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the forecast-weighted mean excess return is not above 0."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "t clustered by day", "value": tstat} if tstat is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "forecast-weighted mean next-day excess return above 0",
                             "value": wmean, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
