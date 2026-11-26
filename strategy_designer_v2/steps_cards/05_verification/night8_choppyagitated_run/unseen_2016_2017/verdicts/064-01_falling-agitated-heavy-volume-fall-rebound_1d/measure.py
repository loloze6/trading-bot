import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    HV_RAW = "debug_info.components.heavy_volume.last_history_value"

    # ---------- coin mean daily return over all its windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").astype(float)
            r = (c.shift(-1) / c - 1.0).dropna()
            rets.append(r.values)
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if allr.size else np.nan

    # ---------- situation check + collect cases ----------
    n_active = 0
    n_agree = 0
    case_rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").astype(float)
            v = pd.to_numeric(df["volume"], errors="coerce").astype(float)
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).astype(float)
            regime = df["regime"].astype(str)

            ret1 = c / c.shift(1) - 1.0
            vr_price = v / v.shift(1).rolling(20, min_periods=20).mean()
            if HV_RAW in df.columns:
                hv = pd.to_numeric(df[HV_RAW], errors="coerce").astype(float)
                vr = (hv + 1.0).where(hv.notna(), vr_price)
            else:
                vr = vr_price
            profile_ok = regime == "mean_reversion"  # vetoes send outside-profile bars to chop

            active = fc != 0
            known = ret1.notna() & vr.notna()
            situ = (ret1 < 0) & (vr > 1.0) & profile_ok
            use = active & known
            n_active += int(use.sum())
            n_agree += int((use & situ & (fc > 0)).sum())

            nxt = c.shift(-1) / c - 1.0
            is_case = (fc > 0) & (regime == "mean_reversion") & nxt.notna()
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in np.where(is_case.values)[0]:
                case_rows.append({
                    "coin": coin, "window": w,
                    "day": ts.iloc[i].floor("D"),
                    "x": float(fc.iloc[i]),
                    "y": float(nxt.iloc[i]) - coin_mean[coin],
                })

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "slope of excess next-day return on forecast, within windows"
    threshold = "confirm: slope t >= 2 and mean excess > 0; reject: slope t <= -2 or mean excess t <= -2"
    reading = ("Situation profile taken from the recorded regime 'mean_reversion' (the detector's profile components are "
               "not recorded) with ret1 from closes and volume ratio from heavy_volume raw value + 1 (prices when missing); "
               "bars whose situation cannot be computed are left out; the slope uses forecast and excess return demeaned within "
               "each coin-window, and both t's use day-clustered standard errors (deviations summed per UTC day, factor G/(G-1)); "
               "the plan's 100 distinct case days is treated as the minimum count.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are long bars on a down day with volume above its prior 20-day mean "
                           "inside the falling agitated profile."),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows)
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"distinct case days": n_days, "cases": n_cases}

    if n_days < 100:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean excess next-day return > 0", "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Only {n_days} distinct case days, fewer than the plan's 100.",
            "reading": reading,
        }

    # ---------- slope within windows, day-clustered t ----------
    g = cases.groupby(["coin", "window"])
    xt = cases["x"] - g["x"].transform("mean")
    yt = cases["y"] - g["y"].transform("mean")
    sxx = float((xt ** 2).sum())
    slope, slope_t = None, None
    if sxx > 0:
        slope = float((xt * yt).sum() / sxx)
        e = yt - slope * xt
        sc = (xt * e).groupby(cases["day"]).sum()
        G = len(sc)
        var = float((sc ** 2).sum()) / sxx ** 2 * (G / (G - 1) if G > 1 else 1.0)
        slope_t = float(slope / np.sqrt(var)) if var > 0 else None

    # ---------- mean excess, day-clustered t ----------
    m = float(cases["y"].mean())
    d = (cases["y"] - m).groupby(cases["day"]).sum()
    G = len(d)
    var_m = float((d ** 2).sum()) / n_cases ** 2 * (G / (G - 1) if G > 1 else 1.0)
    mean_t = float(m / np.sqrt(var_m)) if var_m > 0 else None
    sup_pass = bool(m > 0)

    st = slope_t if slope_t is not None else 0.0
    mt = mean_t if mean_t is not None else 0.0
    if st <= -2 or mt <= -2:
        status = "rejected"
        decided = (f"Reject rule met: slope t {st:.2f} <= -2" if st <= -2
                   else f"Reject rule met: mean excess t {mt:.2f} <= -2 (heavy-volume falls keep falling)")
    elif st >= 2 and sup_pass:
        status = "confirmed"
        decided = f"Confirm rule met: slope t {st:.2f} >= 2 and mean excess {m:.5f} > 0."
    else:
        status = "inconclusive"
        if st >= 2:
            decided = f"Slope t {st:.2f} >= 2 but mean excess {m:.5f} <= 0 with t {mt:.2f} > -2: inconclusive."
        else:
            decided = f"Slope t {st:.2f} between -2 and 2 and mean excess t {mt:.2f} > -2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "slope t, day-clustered", "value": slope_t}
                                       if slope_t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean excess next-day return > 0 (t day-clustered: %s)" %
                                     (None if mean_t is None else round(mean_t, 3)),
                             "value": m, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
