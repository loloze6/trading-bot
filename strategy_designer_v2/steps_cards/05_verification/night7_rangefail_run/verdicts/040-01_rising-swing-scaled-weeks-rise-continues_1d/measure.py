import numpy as np
import pandas as pd


def measure(bars):
    H = 14
    RAW = "debug_info.components.swing_rise.last_history_value"
    STRAT_REGIME = "unknown"  # the only regime with a strategy: not vetoed to chop = rising profile

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            in_profile = df["regime"].astype(str) == STRAT_REGIME
            situation = in_profile & raw.notna() & (raw > 0)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of 14-bar excess return on forecast (forecast > 0, in profile, 14-bar grid)"
    threshold = "confirm: slope > 0 with t >= 2 and mean excess > 0; reject: slope < 0 with t <= -2"
    reading_base = ("Rising profile read as regime == 'unknown' (the 60-day price-evolution veto not firing), "
                    "the situation as profile bars with the raw 20-day swing-scaled return > 0 on the long side; "
                    "the coin's mean 14-bar return is taken over all its non-overlapping grid cases in all windows; "
                    "the slope's t uses day-clustered errors (each day's x-deviation times residual summed per day); "
                    "days are the UTC dates of the case bars.")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean excess 14-bar return of forecast > 0 cases > 0",
                                 "value": None, "passed": None},
            "counts": {"grid cases with forecast > 0": 0, "distinct days": 0},
            "decided_by": "No bar has a non-zero forecast, so fewer than 100 grid cases with forecast > 0 exist.",
            "reading": reading_base,
        }

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are rising-profile bars with a positive "
                           "20-day swing-scaled return and a long forecast, as the Fidelity's situation and side require."),
            "reading": reading_base,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_all = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for p in range(0, n, H):
                if p + H >= n:
                    break
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_all.append(r)
                if reg[p] == STRAT_REGIME and np.isfinite(fc[p]) and fc[p] > 0:
                    coin_cases.append((r, float(fc[p]), ts.iloc[p].strftime("%Y-%m-%d")))
        if len(coin_all) == 0:
            continue
        mu = float(np.mean(coin_all))
        for r, f, d in coin_cases:
            rows.append((coin, r - mu, f, d))

    n_cases = len(rows)
    days = sorted(set(r[3] for r in rows))
    n_days = len(days)
    counts = {"grid cases with forecast > 0": int(n_cases), "distinct days": int(n_days)}

    slope = None
    t = None
    mean_ex = None
    if n_cases >= 2:
        y = np.array([r[1] for r in rows], dtype=float)
        x = np.array([r[2] for r in rows], dtype=float)
        d = np.array([r[3] for r in rows])
        mean_ex = float(np.mean(y))
        xd = x - x.mean()
        sxx = float(np.sum(xd ** 2))
        if sxx > 0:
            slope = float(np.sum(xd * (y - y.mean())) / sxx)
            a = y.mean() - slope * x.mean()
            e = y - a - slope * x
            s = pd.Series(xd * e).groupby(d).sum().values
            var_b = float(np.sum(s ** 2)) / (sxx ** 2)
            if var_b > 0:
                t = float(slope / np.sqrt(var_b))
    elif n_cases == 1:
        mean_ex = float(rows[0][1])

    sup_pass = None if mean_ex is None else bool(mean_ex > 0)
    supporting = {"name": "mean excess 14-bar return of forecast > 0 cases > 0",
                  "value": mean_ex, "passed": sup_pass}
    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "t of slope (day-clustered)", "value": t} if t is not None else None),
            "threshold": threshold}

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} grid cases with forecast > 0 (need 100) "
                   f"on {n_days} distinct days (need 50).")
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed (no spread in the forecast), so neither rule is met."
    elif slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the mean excess return is above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the mean excess return is <= 0."
    else:
        status = "inconclusive"
        decided = "The slope's |t| is below 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
