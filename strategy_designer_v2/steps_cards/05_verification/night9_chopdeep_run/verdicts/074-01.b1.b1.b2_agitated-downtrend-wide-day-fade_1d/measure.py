import numpy as np
import pandas as pd


def measure(bars):
    W_RAW = "debug_info.components.width.last_history_value"
    BAND = 2.0
    MIN_DAYS = 30

    n_active = 0
    n_agree = 0
    case_rows = []  # (day, excess_short, abs_forecast)

    for coin, windows in bars.items():
        # Per-coin normal drift: mean 1-bar return over all windows (returns inside each window only)
        all_rets = []
        prepared = []
        for wname, df in windows.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            fwd = close.shift(-1) / close - 1.0
            all_rets.append(fwd.dropna().values)
            prepared.append((d, fwd))
        if not prepared:
            continue
        rets_concat = np.concatenate(all_rets) if all_rets else np.array([])
        drift = float(np.mean(rets_concat)) if len(rets_concat) > 0 else np.nan

        for d, fwd in prepared:
            close = d["close"].astype(float)
            high = d["high"].astype(float)
            low = d["low"].astype(float)
            fc = d["forecast"].astype(float).fillna(0.0).values

            # --- situation: up day and range above its 20-bar mean range (day included) ---
            up = (close > close.shift(1)).values
            up_known = close.shift(1).notna().values
            rng = high - low
            width_px = (rng / rng.rolling(20, min_periods=20).mean()).values
            if W_RAW in d.columns:
                width_rec = pd.to_numeric(d[W_RAW], errors="coerce").values
            else:
                width_rec = np.full(len(d), np.nan)
            width = np.where(np.isfinite(width_rec), width_rec, width_px)
            situation = up_known & up & np.isfinite(width) & (width > 1.0)

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            # --- cases: short bets (rise of |forecast| on the short side of at least the band) ---
            side = 0
            ref = 0.0
            ts = d["timestamp"].values
            fwd_v = fwd.values
            for i in range(len(d)):
                f = fc[i]
                s = int(np.sign(f))
                if s != side:
                    side = s
                    ref = 0.0
                if s == 0:
                    continue
                m = abs(f)
                is_bet = (m - ref) >= BAND
                if is_bet:
                    ref = m
                else:
                    ref = min(ref, m)
                if is_bet and s < 0 and np.isfinite(fwd_v[i]) and np.isfinite(drift):
                    excess_short = -(fwd_v[i] - drift)
                    day = pd.Timestamp(ts[i]).tz_convert("UTC").normalize() if pd.Timestamp(ts[i]).tzinfo else pd.Timestamp(ts[i]).normalize()
                    case_rows.append((day, float(excess_short), float(m)))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9) if n_active > 0 else True

    threshold_txt = "confirm: mean > 0 with t >= 2 (and |forecast|-weighted mean > unweighted mean); reject: mean < 0 with t <= -2"
    main_name = "mean excess next-day return in the short direction (vs coin's mean daily return)"
    reading = ("Situation checked as up day (close above the previous close in the same window) with high-low range over "
               "its 20-bar mean range (recorded width where present, else recomputed from prices; first bar of a window "
               "counted as not in the situation), side short, the profile not rechecked; cases are short bets on the 1-bar "
               "grid, the per-day t uses the sums of each day's deviations from the mean with a D/(D-1) correction, and the "
               "plan's 'fewer than 30 distinct days' minimum gives 'not observable'.")

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short forecasts on up days whose range "
                           "exceeds its 20-bar mean range, so the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    n_cases = len(case_rows)
    if n_cases > 0:
        cdf = pd.DataFrame(case_rows, columns=["day", "x", "w"])
        n_days = int(cdf["day"].nunique())
        mean = float(cdf["x"].mean())
        dev = cdf["x"] - mean
        S = dev.groupby(cdf["day"]).sum().values
        D = len(S)
        if D > 1 and np.sum(S ** 2) > 0:
            se = np.sqrt(np.sum(S ** 2) * D / (D - 1)) / n_cases
            t = float(mean / se)
        else:
            t = None
        wsum = cdf["w"].sum()
        wmean = float((cdf["x"] * cdf["w"]).sum() / wsum) if wsum > 0 else None
    else:
        n_days, mean, t, wmean = 0, None, None, None

    sup_pass = (wmean > mean) if (wmean is not None and mean is not None) else None
    sup_diff = (wmean - mean) if (wmean is not None and mean is not None) else None

    counts = {"distinct days with cases": int(n_days), "cases": int(n_cases)}
    sit = {"agreement": float(agreement) if agreement is not None else None, "passed": bool(passed)}
    main = {"name": main_name, "value": mean,
            "statistic": {"name": "t of the mean, deviations summed per day", "value": t} if t is not None else None,
            "threshold": threshold_txt}
    sup = {"name": "|forecast|-weighted mean minus unweighted mean of the excess fall",
           "value": float(sup_diff) if sup_diff is not None else None,
           "passed": bool(sup_pass) if sup_pass is not None else None}

    if n_days < MIN_DAYS or t is None:
        status = "not observable"
        decided = f"Only {n_days} distinct days with cases, below the plan's minimum of 30."
    elif mean > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean excess next-day fall above 0 with t >= 2 and the |forecast|-weighted mean exceeds the unweighted mean."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean excess next-day return in the short direction below 0 with t <= -2: wide up days are followed by excess rises."
    elif mean > 0 and t >= 2:
        status = "inconclusive"
        decided = "The main measure confirms (mean > 0, t >= 2) but the |forecast|-weighted mean is not larger than the unweighted mean."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
