import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.scaled_fall.last_history_value"

    rows = []
    active_total = 0
    active_agree = 0

    for coin, wins in bars.items():
        # Coin's mean daily return over all its windows (never across windows)
        all_rets = []
        prepared = []
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            if "timestamp" in d.columns:
                d = d.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fwd = close.shift(-1) / close - 1.0
            back = close / close.shift(1) - 1.0
            all_rets.append(fwd.dropna().values)
            prepared.append((wname, d, close, fwd, back))
        if len(all_rets) == 0:
            continue
        cat = np.concatenate(all_rets) if len(all_rets) else np.array([])
        coin_mean = float(np.mean(cat)) if cat.size else np.nan

        for wname, d, close, fwd, back in prepared:
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            # Down day: day's 1-bar return < 0 from prices; on a window's first bar
            # (no previous close in the window) fall back to the sign of the raw component.
            down = back < 0
            first_missing = back.isna()
            down = down.where(~first_missing, raw < 0)
            down = down.fillna(False).astype(bool)

            active = fc != 0
            active_total += int(active.sum())
            active_agree += int((active & down & (fc > 0)).sum())

            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            day = ts.dt.floor("D")
            sel = (fc > 0) & fwd.notna() & ts.notna()
            for i in np.where(sel.values)[0]:
                rows.append((coin, day.iloc[i], float(fc.iloc[i]), float(fwd.iloc[i] - coin_mean)))

    agreement = (active_agree / active_total) if active_total > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "pooled slope of next-day excess return on forecast, down-day bars"
    thr = "confirm: slope > 0 with day-clustered t >= 2 (and top-quintile mean > 0); reject: slope < 0 with t <= -2"
    sup_name = "mean next-day excess return, top quintile of forecast on down-day bars"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"down-day cases": len(rows),
                       "distinct days": int(len(set(r[1] for r in rows)))},
            "decided_by": ("Fewer than 90 % of the active bars are down days with a long (positive) forecast, "
                           "so the config does not trade the plan's situation (down day, long) on its side."
                           if agreement is not None else "No active bars: the config never trades the plan's situation."),
            "reading": "Down day read from the 1-bar close-to-close return inside the window, from the raw component's sign on a window's first bar.",
        }

    df = pd.DataFrame(rows, columns=["coin", "day", "x", "y"])
    n_cases = int(len(df))
    n_days = int(df["day"].nunique()) if n_cases else 0
    counts = {"down-day cases": n_cases, "distinct days": n_days}

    reading = ("Down day from the 1-bar close return inside each window (raw component sign on a window's first bar); "
               "excess = next-day return minus the coin's mean 1-bar return over all its windows; slope by pooled OLS with "
               "a day-clustered (CR1, G/(G-1)) standard error; top quintile = down-day bars with forecast at or above the "
               "pooled 80th percentile; its t is the ordinary t of the mean, as the plan does not name one.")

    if n_cases < 300 or n_days < 150:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Minimum not reached: the plan needs at least 300 down-day cases on at least 150 distinct days (have {n_cases} on {n_days}).",
            "reading": reading,
        }

    x = df["x"].values
    y = df["y"].values
    xbar, ybar = x.mean(), y.mean()
    xc = x - xbar
    sxx = float(np.sum(xc ** 2))
    if sxx > 0:
        slope = float(np.sum(xc * (y - ybar)) / sxx)
        a = ybar - slope * xbar
        e = y - a - slope * x
        g = pd.Series(xc * e).groupby(df["day"].values).sum().values
        G = len(g)
        var = (G / (G - 1)) * float(np.sum(g ** 2)) / sxx ** 2 if G > 1 else np.nan
        se = np.sqrt(var) if np.isfinite(var) else np.nan
        t_slope = float(slope / se) if se and np.isfinite(se) and se > 0 else np.nan
    else:
        slope, t_slope = np.nan, np.nan

    q80 = float(np.quantile(x, 0.8))
    top = y[x >= q80]
    nt = int(top.size)
    top_mean = float(top.mean()) if nt else np.nan
    if nt > 1:
        sd = float(np.std(top, ddof=1))
        t_top = float(top_mean / (sd / np.sqrt(nt))) if sd > 0 else np.nan
    else:
        t_top = np.nan
    counts["top-quintile cases"] = nt

    sup_pass = bool(np.isfinite(top_mean) and top_mean > 0)

    rej_slope = np.isfinite(slope) and np.isfinite(t_slope) and slope < 0 and t_slope <= -2
    rej_top = np.isfinite(top_mean) and np.isfinite(t_top) and top_mean < 0 and t_top <= -2
    conf = np.isfinite(slope) and np.isfinite(t_slope) and slope > 0 and t_slope >= 2 and sup_pass

    if rej_slope:
        status = "rejected"
        decided = f"Reject rule: the slope is negative with day-clustered t = {t_slope:.2f} <= -2."
    elif rej_top:
        status = "rejected"
        decided = f"Reject rule: the top-quintile mean excess next-day return is negative with t = {t_top:.2f} <= -2."
    elif conf:
        status = "confirmed"
        decided = f"Confirm rule: the slope is positive with t = {t_slope:.2f} >= 2 and the top-quintile mean excess return is above 0."
    else:
        status = "inconclusive"
        if np.isfinite(slope) and slope > 0 and np.isfinite(t_slope) and t_slope >= 2 and not sup_pass:
            decided = "Inconclusive rule: a positive slope with t >= 2 but a top-quintile mean at or below 0."
        else:
            decided = f"Inconclusive rule: any other result (slope t = {t_slope:.2f}, |t| < 2, and no reject condition met)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name,
                         "value": None if not np.isfinite(slope) else float(slope),
                         "statistic": {"name": "OLS slope t, day-clustered",
                                       "value": None if not np.isfinite(t_slope) else float(t_slope)},
                         "threshold": thr},
        "supporting_check": {"name": sup_name,
                             "value": None if not np.isfinite(top_mean) else float(top_mean),
                             "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
