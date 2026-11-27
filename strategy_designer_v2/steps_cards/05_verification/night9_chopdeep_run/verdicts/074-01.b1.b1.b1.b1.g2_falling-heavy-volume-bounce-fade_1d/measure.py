import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    HV = "debug_info.components.heavy_volume.last_history_value"
    BAND = 2.0
    MIN_CASES = 30
    MIN_DAYS = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    coin_rets = {}
    windows = []
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True).copy()
            close = d["close"].astype(float)
            high = d["high"].astype(float)
            low = d["low"].astype(float)
            vol = d["volume"].astype(float)
            fc = d[FC].astype(float).fillna(0.0)

            ret1 = close / close.shift(1) - 1.0
            rng = high - low
            width = rng / rng.rolling(20, min_periods=20).mean()
            volr = vol / vol.shift(1).rolling(20, min_periods=20).mean()
            trend = (close / close.shift(60) - 1.0) * 100.0

            up_c = ret1 > 0
            width_c = width > 1.0
            vol_c = volr > 1.0
            falling_c = trend < -10.0

            reg_mr = d["regime"].astype(str) == "mean_reversion" if "regime" in d.columns else pd.Series(False, index=d.index)
            hv = d[HV].astype(float) if HV in d.columns else pd.Series(np.nan, index=d.index)

            # Where a condition cannot be computed inside the window, fall back on the record:
            # vol from heavy_volume's raw value (centred ratio > 0); the others from the detector's regime.
            up_s = np.where(ret1.notna(), up_c, reg_mr)
            width_s = np.where(width.notna(), width_c, reg_mr)
            vol_s = np.where(volr.notna(), vol_c, np.where(hv.notna(), hv > 0, reg_mr))
            fall_s = np.where(trend.notna(), falling_c, reg_mr)
            situ = up_s & width_s & vol_s & fall_s

            active = fc.values != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc.values < 0)).sum())

            fwd = close.shift(-1) / close - 1.0
            rets.append(fwd.dropna().values)
            windows.append((coin, d, fc, fwd))
        coin_rets[coin] = np.concatenate(rets) if rets else np.array([])

    agreement = n_agree / n_active if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean short-direction unusual 1-day move per case"
    thr = "mean > 0 with day-pooled t >= 2 confirms; mean < 0 with t <= -2 rejects"
    sup_name = "heavier-half minus lighter-half mean unusual move (split at median |forecast|)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars on an up, wide, heavy-volume day in a falling market (60-day evolution below -10%), as the Fidelity requires.",
            "reading": "Conditions not computable inside a window were taken from the record (heavy_volume raw value > 0 for volume, regime 'mean_reversion' for the others); the 60-bar price evolution is read in percent.",
        }

    # ---------- 2. cases: short bets (forecast rises on the short side by >= band) ----------
    mean_ret = {c: (float(np.mean(r)) if len(r) else np.nan) for c, r in coin_rets.items()}
    rows = []
    for coin, d, fc, fwd in windows:
        ref = 0.0
        side = 0
        for i in range(len(d)):
            f = fc.iloc[i]
            s = 1 if f > 0 else (-1 if f < 0 else 0)
            if s != side:
                ref = 0.0
                side = s
            if s == 0:
                continue
            m = abs(f)
            if m - ref >= BAND:
                ref = m
                if s < 0 and not np.isnan(fwd.iloc[i]) and not np.isnan(mean_ret[coin]):
                    um = -(fwd.iloc[i] - mean_ret[coin])
                    day = pd.Timestamp(d["timestamp"].iloc[i])
                    if day.tzinfo is not None:
                        day = day.tz_convert("UTC").tz_localize(None)
                    rows.append((coin, day.normalize(), float(um), float(m)))
            else:
                ref = min(ref, m)

    cases = pd.DataFrame(rows, columns=["coin", "day", "um", "absf"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_um = float(cases["um"].mean()) if n_cases else None
    t = None
    if n_cases > 1:
        dev = cases["um"] - mean_um
        S = dev.groupby(cases["day"]).sum()
        se = np.sqrt(float((S ** 2).sum())) / n_cases
        t = float(mean_um / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        med = cases["absf"].median()
        heavy = cases.loc[cases["absf"] > med, "um"]
        light = cases.loc[cases["absf"] <= med, "um"]
        if len(heavy) and len(light):
            sup_val = float(heavy.mean() - light.mean())
            sup_pass = bool(sup_val > 0)

    reading = ("Cases are the short bets (forecast rising >= 2 points on the short side from its lowest level since the last bet) with a next bar in the window; "
               "the coin's mean is its mean 1-day return over all its windows; the day-pooled t uses the per-day sums of deviations without small-sample correction; "
               "the heavier half is |forecast| strictly above the median; situation conditions not computable inside a window were taken from the record "
               "(heavy_volume raw > 0, regime 'mean_reversion') and the 60-bar evolution is read in percent.")

    main = {"name": main_name, "value": mean_um,
            "statistic": {"name": "t of the mean, cases of one day pooled", "value": t} if t is not None else None,
            "threshold": thr}
    sup = {"name": sup_name, "value": sup_val, "passed": sup_pass}
    sc = {"agreement": float(agreement), "passed": True}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": sup, "counts": counts,
                "decided_by": f"Minimum not reached: {n_cases} cases (need 30) and {n_days} distinct days (need 30).",
                "reading": reading}

    if t is not None and mean_um > 0 and t >= 2:
        if sup_pass:
            status, by = "confirmed", "The mean unusual move is above 0 with t >= 2 and the heavier half beats the lighter half."
        else:
            status, by = "inconclusive", "The main measure meets the confirm rule but the supporting check fails."
    elif t is not None and mean_um < 0 and t <= -2:
        status, by = "rejected", "The mean unusual move is below 0 with t <= -2."
    else:
        status, by = "inconclusive", "The t lies between -2 and 2 (or cannot be computed)."

    return {"status": status, "situation_check": sc, "main_measure": main,
            "supporting_check": sup, "counts": counts, "decided_by": by, "reading": reading}
