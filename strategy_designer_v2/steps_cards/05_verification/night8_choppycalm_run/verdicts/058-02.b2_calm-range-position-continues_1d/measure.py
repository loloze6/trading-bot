import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.range_pos.last_history_value"
    PROFILE_REGIME = "unknown"  # the only regime with a strategy: the choppy calm profile

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce")
            hi = pd.to_numeric(df["high"], errors="coerce")
            lo = pd.to_numeric(df["low"], errors="coerce")
            # recomputed range position (current bar included), used where the raw value is missing
            hh = hi.rolling(20, min_periods=20).max()
            ll = lo.rolling(20, min_periods=20).min()
            mid = (hh + ll) / 2.0
            half = (hh - ll) / 2.0
            pos_re = ((close - mid) / half.replace(0, np.nan)).values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            raw = np.where(np.isnan(raw), pos_re, raw)
            regime = df["regime"].astype(str).values
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active += 1
                in_profile = regime[i] == PROFILE_REGIME
                r = raw[i]
                if in_profile and not np.isnan(r) and r != 0 and np.sign(r) == np.sign(fc[i]):
                    n_agree += 1

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "slope of 5-bar excess return on forecast", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirms, t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"grid cases inside the profile": 0, "distinct days": 0},
            "decided_by": "No bar has a non-zero forecast, so fewer than 30 grid cases inside the profile.",
            "reading": "none",
        }

    agreement = n_agree / n_active
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "slope of 5-bar excess return on forecast", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirms, t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"grid cases inside the profile": None, "distinct days": None},
            "decided_by": ("Fewer than 90 % of the active bars are choppy calm profile bars whose forecast sign "
                           "equals the sign of the close's position around the middle of its 20-day high-low range."),
            "reading": "Profile bars are those with regime 'unknown' (the only regime given a strategy); the side is the sign of the raw range position.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        all_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] != 0:
                    coin_rows.append((ts.iloc[i].floor("D"), float(fc[i]), r))
        if len(all_rets) == 0:
            continue
        drift = float(np.mean(all_rets))
        for d, f, r in coin_rows:
            rows.append((d, f, r - drift))

    n_cases = len(rows)
    days = [r[0] for r in rows]
    n_days = len(set(days))
    counts = {"grid cases inside the profile": int(n_cases), "distinct days": int(n_days)}
    reading = ("Profile bars are those with regime 'unknown'; the drift is the coin's mean 5-bar return over all "
               "grid cells of all its windows; 'taken together by day' is a day-clustered (CR1) standard error of the OLS slope; "
               "the plan's minimum counts, when not reached, give 'not observable'.")
    mm_name = "OLS slope of the 5-bar excess return on the forecast"
    thr = "slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects; otherwise inconclusive"

    if n_cases < 30 or n_days < 20:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": ("Fewer than 30 grid cases inside the profile" if n_cases < 30
                           else "Fewer than 20 distinct days") + ": the plan's minimum count is not reached.",
            "reading": reading,
        }

    d = pd.DataFrame(rows, columns=["day", "x", "y"])
    x = d["x"].values
    y = d["y"].values
    xm, ym = x.mean(), y.mean()
    sxx = float(np.sum((x - xm) ** 2))
    if sxx == 0:
        return {
            "status": "inconclusive",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "The forecast does not vary over the cases, so no slope or t can be computed.",
            "reading": reading,
        }
    beta = float(np.sum((x - xm) * (y - ym)) / sxx)
    alpha = ym - beta * xm
    e = y - alpha - beta * x
    d["s"] = (x - xm) * e
    g = d.groupby("day")["s"].sum().values
    G = len(g)
    N = len(d)
    k = 2
    corr = (G / (G - 1.0)) * ((N - 1.0) / (N - k)) if G > 1 else 1.0
    var_b = corr * float(np.sum(g ** 2)) / sxx ** 2
    se = np.sqrt(var_b) if var_b > 0 else np.nan
    t = float(beta / se) if np.isfinite(se) and se > 0 else float("nan")

    if np.isfinite(t) and beta > 0 and t >= 2:
        status = "confirmed"
        dec = "The slope is positive with t >= 2: higher in the range is followed by a larger 5-day excess rise."
    elif np.isfinite(t) and beta < 0 and t <= -2:
        status = "rejected"
        dec = "The slope is negative with t <= -2: higher in the range is followed by a smaller excess rise (reversion)."
    else:
        status = "inconclusive"
        dec = "The t of the slope lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": mm_name, "value": beta,
                         "statistic": {"name": "t of slope, cases clustered by day",
                                       "value": t if np.isfinite(t) else None},
                         "threshold": thr},
        "supporting_check": None,
        "counts": counts,
        "decided_by": dec,
        "reading": reading,
    }
