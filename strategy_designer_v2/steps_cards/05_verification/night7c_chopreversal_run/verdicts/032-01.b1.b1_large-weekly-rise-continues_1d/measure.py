import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    RAW = "debug_info.components.rise.last_history_value"
    THRESH = 2.0

    def to_days(ts):
        s = pd.Series(ts)
        if pd.api.types.is_numeric_dtype(s):
            mx = float(np.nanmax(s.values)) if len(s) else 0.0
            unit = "ms" if mx > 1e11 else "s"
            dt = pd.to_datetime(s, unit=unit, utc=True)
        else:
            dt = pd.to_datetime(s, utc=True)
        return dt.dt.strftime("%Y-%m-%d").values

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float).reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").reset_index(drop=True)
            r1 = close.pct_change()
            ret7 = close / close.shift(H) - 1.0
            vol = r1.rolling(30).std()
            z_re = ret7 / (vol * np.sqrt(H))
            if RAW in df.columns:
                z_rec = pd.to_numeric(df[RAW], errors="coerce").reset_index(drop=True)
                z = z_rec.where(z_rec.notna(), z_re)
            else:
                z = z_re
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            ok = active & (fc > 0) & z.notna() & (z >= THRESH - 1e-9)
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean unusual 7-bar move of the long cases (return minus the coin's mean 7-bar return)"
    thr = "confirm: mean > 0 with day-clustered t >= 2 and slope > 0; reject: mean < 0 with t <= -2"
    sup_name = "least-squares slope of the unusual move on the forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in the situation on the long side": int(n_agree)},
            "decided_by": ("No active bars in the record." if n_active == 0 else
                           "Fewer than 90% of the bars with a non-zero forecast are long bars with the 7-day return "
                           "over (30-day daily std x sqrt(7)) at least 2, as the plan's situation requires."),
            "reading": "The situation is read from the recorded raw value of 'rise' (recomputed from prices where missing).",
        }

    # ---------- 2. criterion ----------
    cases_ret, cases_fc, cases_day, cases_coin = [], [], [], []
    drift = {}
    for coin, wins in bars.items():
        all_grid = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            days = to_days(df["timestamp"].values)
            n = len(close)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                all_grid.append(r)
                if np.isfinite(fc[t]) and fc[t] > 0:
                    cases_ret.append(r)
                    cases_fc.append(float(fc[t]))
                    cases_day.append(days[t])
                    cases_coin.append(coin)
        drift[coin] = float(np.mean(all_grid)) if all_grid else np.nan

    x = np.array([cases_ret[i] - drift[cases_coin[i]] for i in range(len(cases_ret))], dtype=float)
    f = np.array(cases_fc, dtype=float)
    d = np.array(cases_day)
    keep = np.isfinite(x) & np.isfinite(f)
    x, f, d = x[keep], f[keep], d[keep]
    n_cases = int(len(x))
    n_days = int(len(np.unique(d))) if n_cases else 0

    mean = float(np.mean(x)) if n_cases else None
    tval = None
    if n_cases >= 2 and n_days >= 2:
        dev = pd.Series(x - mean).groupby(d).sum().values
        var = (dev ** 2).sum() / (n_cases ** 2) * (n_days / (n_days - 1))
        se = np.sqrt(var)
        if se > 0:
            tval = float(mean / se)
    slope = None
    if n_cases >= 2 and np.std(f) > 0:
        slope = float(np.polyfit(f, x, 1)[0])
    slope_ok = None if slope is None else bool(slope > 0)

    counts = {"cases": n_cases, "distinct days": n_days}

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = (f"Minimum count not reached: {n_cases} cases (need 30) and {n_days} distinct days (need 20).")
    elif tval is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and tval >= 2 and slope_ok:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 and the slope on the forecast is above 0."
    elif mean < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2."
    elif tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope of the unusual move on the forecast is at or below 0 (or undefined)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": None if tval is None else {"name": "t of the mean, cases of one day taken together", "value": tval},
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": slope, "passed": slope_ok},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are grid bars (positions 0, 7, 14, ... of each window, with a full 7-bar return inside the window) "
                    "with forecast > 0, the drift is the coin's mean 7-bar return on that grid over all its windows, the t uses "
                    "day-clustered deviations with a D/(D-1) correction, and the plan's 'fewer than 30 cases or 20 days' is "
                    "treated as the minimum count giving 'not observable'."),
    }
