import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    RAW = "debug_info.components.dist_above_high.last_history_value"

    def to_days(ts):
        s = pd.Series(ts)
        if pd.api.types.is_numeric_dtype(s):
            mx = float(np.nanmax(s.values)) if len(s) else 0.0
            unit = "ms" if mx > 1e11 else "s"
            d = pd.to_datetime(s, unit=unit, utc=True)
        else:
            d = pd.to_datetime(s, utc=True)
        return d.dt.strftime("%Y-%m-%d").values

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values.astype(float)
            raw = (pd.to_numeric(df[RAW], errors="coerce").values.astype(float)
                   if RAW in df.columns else np.full(len(df), np.nan))
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active += 1
                # close above the prior 20-day closing high
                if np.isfinite(raw[i]):
                    above = raw[i] > 0
                elif i >= 20 and np.all(np.isfinite(close[i - 20:i])):
                    above = close[i] > np.max(close[i - 20:i])
                else:
                    above = False
                # rising market (60-bar price evolution), checked only where computable in the window
                if i >= 60 and np.isfinite(close[i - 60]) and close[i - 60] > 0:
                    rising = close[i] / close[i - 60] - 1.0 > 0
                else:
                    rising = True
                if above and rising and fc[i] > 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation = raw distance above prior 20-day closing high > 0 (recomputed from closes where not "
               "recorded) and, where 60 bars of the window exist, a positive 60-bar price change as the rising "
               "profile, side long; the plan's 'fewer than 30 cases on distinct days' is applied as a minimum count "
               "(not observable), the weighted-mean t pools each day's weighted deviations, and the slope is an "
               "ordinary least-squares slope of excess return on forecast over all cases.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars with the close above its "
                           "prior 20-day closing high in a rising market, as the Fidelity's situation requires."
                           if n_active > 0 else "No active bar in the record."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    f_list, e_list, d_list = [], [], []
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            days = to_days(df["timestamp"])
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    coin_cases.append((fc[i], r, days[i]))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for f, r, d in coin_cases:
            f_list.append(f)
            e_list.append(r - drift)
            d_list.append(d)

    f = np.array(f_list, dtype=float)
    e = np.array(e_list, dtype=float)
    days = np.array(d_list, dtype=object)
    n_cases = int(len(f))
    n_days = int(len(set(days.tolist()))) if n_cases else 0

    m = None
    t = None
    slope = None
    if n_cases > 0 and f.sum() > 0:
        m = float(np.sum(f * e) / np.sum(f))
        dev = f * (e - m) / np.sum(f)
        per_day = pd.Series(dev).groupby(pd.Series(days)).sum().values
        k = len(per_day)
        if k > 1:
            var = np.sum(per_day ** 2) * k / (k - 1)
            se = float(np.sqrt(var))
            if se > 0:
                t = float(m / se)
    if n_cases >= 2 and np.var(f) > 0:
        slope = float(np.polyfit(f, e, 1)[0])
    slope_pos = (slope > 0) if slope is not None else None

    counts = {"cases": n_cases, "cases on distinct days": n_days}
    main = {
        "name": "forecast-weighted mean 3-bar excess return",
        "value": m,
        "statistic": {"name": "t of weighted mean, same-day cases pooled", "value": t} if t is not None else None,
        "threshold": "confirm: above 0 with t >= 2 (and slope > 0); reject: below 0 with t <= -2",
    }
    supp = {"name": "OLS slope of 3-bar excess return on forecast", "value": slope,
            "passed": (bool(slope_pos) if slope_pos is not None else None)}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, fewer than the plan's minimum of 30 cases on distinct days."
    elif t is None or m is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif m > 0 and t >= 2 and slope_pos:
        status = "confirmed"
        decided = "The forecast-weighted mean excess return is above 0 with t >= 2 and the slope on the forecast is positive."
    elif m < 0 and t <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess return is below 0 with t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope on the forecast is not positive, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
