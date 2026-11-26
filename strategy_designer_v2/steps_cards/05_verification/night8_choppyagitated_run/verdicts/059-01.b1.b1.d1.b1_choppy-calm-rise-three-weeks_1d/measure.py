import numpy as np
import pandas as pd


def measure(bars):
    H = 21
    RAW = "debug_info.components.scaled_rise.last_history_value"

    def raw_from_prices(close):
        r7 = close / close.shift(7) - 1.0
        base = r7.abs().rolling(30, min_periods=30).mean()
        out = r7 / base
        out[base == 0] = np.nan
        return out

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            raw = raw.where(raw.notna(), raw_from_prices(close))
            calm = df["regime"].astype(str) == "unknown"
            situation = calm & (raw > 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("No active bars to compare with the plan's situation." if n_active == 0 else
                           "Fewer than 90% of the bars with a non-zero forecast are choppy calm bars "
                           "(regime 'unknown') with a positive scaled 7-bar rise and a long forecast."),
            "reading": "The choppy calm profile is read from the recorded regime ('unknown' = no veto fired), "
                       "since the detector's components are not recorded.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        drift_samples = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for p in range(0, n, H):
                if p + H >= n:
                    break
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                fwd = c1 / c0 - 1.0
                drift_samples.append(fwd)
                if np.isfinite(fc[p]) and fc[p] > 0:
                    coin_rows.append((coin, ts.iloc[p].strftime("%Y-%m-%d"), float(fc[p]), fwd))
        if drift_samples and coin_rows:
            drift = float(np.mean(drift_samples))
            for c, d, f, r in coin_rows:
                rows.append({"coin": c, "day": d, "x": f, "y": r - drift})

    cases = pd.DataFrame(rows, columns=["coin", "day", "x", "y"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    slope = None
    t_slope = None
    mean_ex = None
    t_mean = None
    if n_cases >= 2:
        x = cases["x"].values
        y = cases["y"].values
        mean_ex = float(np.mean(y))
        # day-clustered t of the mean
        dev = pd.Series(y - mean_ex).groupby(cases["day"].values).sum().values
        se_m = np.sqrt(np.sum(dev ** 2)) / n_cases
        t_mean = float(mean_ex / se_m) if se_m > 0 else None
        xc = x - x.mean()
        sxx = float(np.sum(xc ** 2))
        if sxx > 0:
            slope = float(np.sum(xc * (y - y.mean())) / sxx)
            a = y.mean() - slope * x.mean()
            e = y - a - slope * x
            sc = pd.Series(xc * e).groupby(cases["day"].values).sum().values
            se_b = np.sqrt(np.sum(sc ** 2)) / sxx
            t_slope = float(slope / se_b) if se_b > 0 else None

    supp_passed = None if mean_ex is None else bool(mean_ex > 0)
    main = {
        "name": "slope of 21-bar excess return on forecast",
        "value": slope,
        "statistic": None if t_slope is None else {"name": "day-clustered slope t", "value": t_slope},
        "threshold": "slope t >= 2 to confirm (with mean excess > 0); slope t <= -2 or mean excess t <= -2 to reject",
    }
    supp = {"name": "mean 21-bar excess return of cases", "value": mean_ex, "passed": supp_passed}
    reading = ("Profile read from the recorded regime ('unknown' = choppy calm); cases are grid bars (0,21,42,... "
               "per window) with forecast > 0 and a full 21-bar forward return in the window; normal drift is the "
               "coin's mean non-overlapping 21-bar return over all its windows; slope and mean t use day-clustered "
               "standard errors (CR0, deviations summed per day) without small-sample correction.")

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = f"Minimum not reached: {n_cases} cases (need 30) over {n_days} distinct days (need 20)."
    elif t_slope is not None and t_slope <= -2:
        status = "rejected"
        decided = "Reject rule: the slope's t is -2 or less."
    elif t_mean is not None and t_mean <= -2:
        status = "rejected"
        decided = "Reject rule: the mean excess return of the cases has a t of -2 or less (a giveback)."
    elif t_slope is not None and t_slope >= 2 and supp_passed:
        status = "confirmed"
        decided = "Confirm rule: the slope's t is 2 or more and the mean excess return is above 0."
    else:
        status = "inconclusive"
        if t_slope is not None and t_slope >= 2:
            decided = "Slope t is 2 or more but the mean excess return is 0 or below: inconclusive."
        else:
            decided = "Slope t is between -2 and 2 and no giveback: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
