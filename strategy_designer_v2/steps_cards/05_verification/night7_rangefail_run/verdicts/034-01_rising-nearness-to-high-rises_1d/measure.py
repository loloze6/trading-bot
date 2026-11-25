import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    NH_RAW = "debug_info.components.near_high.last_history_value"
    NH_POST = "debug_info.components.near_high.post_pipeline_value"
    PROFILE_REGIME = "unknown"  # the config's only active regime = the "rising" profile (chop is vetoed, null)

    def standardise(raw, window=60, min_periods=20):
        s = pd.Series(raw, dtype=float)
        past = s.abs().shift(1).rolling(window, min_periods=min_periods).mean()
        out = s * 10.0 / past
        out = out.where(past != 0, 0.0)
        out = out.where(past.notna(), np.nan)
        return out.clip(-20, 20)

    # ---------------- situation check ----------------
    n_active = 0
    n_agree = 0
    grid_rows = []
    drift_by_coin = {}

    for coin, wins in bars.items():
        all_grid_returns = []
        for wname, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            regime = df["regime"].astype(str)
            in_prof = regime == PROFILE_REGIME

            # rebuild the expected forecast from the raw nearness value: (std(x) + 10) / 2
            if NH_RAW in df.columns:
                raw = pd.to_numeric(df[NH_RAW], errors="coerce")
                raw_valid = raw.dropna()
                st = pd.Series(np.nan, index=df.index)
                if len(raw_valid) > 0:
                    st.loc[raw_valid.index] = standardise(raw_valid.values).values
                if NH_POST in df.columns:
                    post = pd.to_numeric(df[NH_POST], errors="coerce")
                    st = st.fillna(post)
                expected = ((st + 10.0) / 2.0).clip(-20, 20)
            else:
                expected = pd.Series(np.nan, index=df.index)

            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & in_prof & expected.notna() & (np.sign(expected) == np.sign(fc)) & (expected != 0)
            n_agree += int(agree.sum())

            # ---------------- grid ----------------
            close = pd.to_numeric(df["close"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_grid_returns.append(r)
                grid_rows.append({
                    "coin": coin,
                    "day": ts.iloc[i].floor("D"),
                    "ret": r,
                    "forecast": fc.iloc[i],
                    "in_profile": bool(in_prof.iloc[i]),
                })
        if all_grid_returns:
            drift_by_coin[coin] = float(np.mean(all_grid_returns))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90
    sit = {"agreement": float(agreement), "passed": bool(passed)}

    main_name = "slope of drift-removed 5-day return on forecast (in-profile grid cases)"
    threshold = "slope t >= 2 (with positive supporting difference) confirms; t <= -2 rejects"
    sup_name = "mean drift-removed 5-day return, forecast > 0 minus forecast < 0"
    reading = ("Profile bars are those with regime 'unknown' (the config's only active regime, chop vetoed) and a "
               "non-missing forecast, all such grid bars enter the regression (forecast 0 included), the drift is the "
               "coin's mean 5-day return over all its non-overlapping grid bars, the slope's t uses day-clustered "
               "standard errors (CR1), and too few cases gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on expected side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are rising-profile bars whose forecast "
                           "sign matches the nearness-to-high relative to its usual distance ((std(x)+10)/2)."),
            "reading": reading,
        }

    g = pd.DataFrame(grid_rows)
    if len(g):
        g = g[g["in_profile"] & g["forecast"].notna()].copy()
        g["y"] = g["ret"] - g["coin"].map(drift_by_coin)
        g = g[g["y"].notna()]
    n_cases = int(len(g))
    n_days = int(g["day"].nunique()) if n_cases else 0
    counts = {"independent in-profile grid cases": n_cases, "distinct days": n_days}

    slope = None
    tval = None
    diff = None
    if n_cases >= 3:
        x = g["forecast"].values.astype(float)
        y = g["y"].values.astype(float)
        xm = x.mean()
        xd = x - xm
        sxx = float(np.sum(xd ** 2))
        if sxx > 0:
            b = float(np.sum(xd * (y - y.mean())) / sxx)
            a = y.mean() - b * xm
            e = y - a - b * x
            sc = pd.Series(xd * e).groupby(g["day"].values).sum().values
            G = len(sc)
            N = n_cases
            meat = float(np.sum(sc ** 2))
            corr = (G / (G - 1.0)) * ((N - 1.0) / (N - 2.0)) if G > 1 and N > 2 else 1.0
            var_b = corr * meat / sxx ** 2
            slope = b
            tval = float(b / np.sqrt(var_b)) if var_b > 0 else None
        pos = g.loc[g["forecast"] > 0, "y"]
        neg = g.loc[g["forecast"] < 0, "y"]
        if len(pos) > 0 and len(neg) > 0:
            diff = float(pos.mean() - neg.mean())

    sup_passed = None if diff is None else bool(diff > 0)
    main = {"name": main_name, "value": slope,
            "statistic": None if tval is None else {"name": "slope t (day-clustered)", "value": tval},
            "threshold": threshold}
    sup = {"name": sup_name, "value": diff, "passed": sup_passed}

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} in-profile grid cases (need 100) and "
                   f"{n_days} distinct days (need 50).")
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_passed:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the supporting difference is positive."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting difference is not positive."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
