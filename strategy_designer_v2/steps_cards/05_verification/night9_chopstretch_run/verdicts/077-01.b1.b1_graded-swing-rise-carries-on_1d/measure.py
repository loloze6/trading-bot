import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    ACTIVE_REGIME = "unknown"
    RAW = "debug_info.components.swing_rise.last_history_value"
    MIN_CASES = 100
    MIN_DAYS = 50

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
            in_profile = df["regime"].astype(str) == ACTIVE_REGIME
            situation = in_profile & raw.notna() & (raw > 0)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = bool(agreement >= 0.9)
    else:
        agreement = None
        passed = True

    main_name = "OLS slope of 7-bar forward return minus normal drift on forecast, in-profile grid bars"
    threshold = "confirm: slope > 0 with t >= 2 and supporting mean > 0; reject: slope < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"grid cases with forecast > 0": None, "distinct days": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are choppy-calm (regime 'unknown') "
                           "bars with a positive 14-day swing-scaled return held long, as the Fidelity states."),
            "reading": "The profile is read from the recorded regime (the config's only active regime, 'unknown').",
        }

    # ---------- 2. Grid, drift, in-profile cases ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_rets.append(r)
                if reg[i] == ACTIVE_REGIME and np.isfinite(fc[i]):
                    coin_rows.append((coin, ts.iloc[i].strftime("%Y-%m-%d"), float(fc[i]), r))
        if len(coin_rets) == 0:
            continue
        drift = float(np.mean(coin_rets))
        for (c, d, f, r) in coin_rows:
            rows.append((c, d, f, r - drift))

    data = pd.DataFrame(rows, columns=["coin", "day", "forecast", "unusual"])
    pos = data[data["forecast"] > 0]
    n_cases = int(len(pos))
    n_days = int(pos["day"].nunique()) if n_cases else 0

    # supporting check
    sup_mean = float(pos["unusual"].mean()) if n_cases else None
    sup_pass = (sup_mean > 0) if sup_mean is not None else None

    # slope with day-clustered t
    slope = None
    t = None
    if len(data) >= 3 and data["forecast"].var() > 0:
        x = data["forecast"].values
        y = data["unusual"].values
        xm = x.mean()
        dx = x - xm
        sxx = float(np.sum(dx ** 2))
        slope = float(np.sum(dx * (y - y.mean())) / sxx)
        intercept = y.mean() - slope * xm
        e = y - intercept - slope * x
        score = pd.Series(dx * e).groupby(data["day"].values).sum().values
        G = len(score)
        if G > 1:
            var = (G / (G - 1)) * float(np.sum(score ** 2)) / sxx ** 2
            if var > 0:
                t = float(slope / np.sqrt(var))

    counts = {"grid cases with forecast > 0": n_cases,
              "distinct days": n_days,
              "in-profile grid bars": int(len(data))}

    reading = ("The profile is the recorded regime 'unknown' (the config's only active regime); the slope is OLS with "
               "intercept over all in-profile grid bars (forecast 0 included), its t from residual-times-deviation "
               "scores summed per UTC day with a G/(G-1) correction; the drift is the coin's mean 7-bar grid return "
               "over all its windows and bars; the plan's 'fewer cases' rule is reported as not observable.")

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} grid cases with forecast > 0 (need 100) "
                   f"on {n_days} distinct days (need 50).")
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the supporting mean unusual move is above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the supporting mean unusual move is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": ({"name": "slope t, deviations summed per day", "value": t}
                                       if t is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean unusual 7-bar move over grid cases with forecast > 0 above 0",
                             "value": sup_mean, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
