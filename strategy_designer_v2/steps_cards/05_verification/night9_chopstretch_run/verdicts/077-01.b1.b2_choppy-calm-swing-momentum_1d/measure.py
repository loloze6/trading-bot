import numpy as np
import pandas as pd


def _to_time(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype(float)
        med = np.nanmedian(np.abs(v.values)) if len(v) else 0
        unit = "ms" if med > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def _recompute_raw(close, period=14, vol_period=30):
    ret = close.pct_change()
    vol = ret.rolling(vol_period, min_periods=vol_period).std()
    mv = close / close.shift(period) - 1.0
    den = vol * np.sqrt(period)
    out = mv / den
    out[(den == 0) | den.isna()] = np.nan
    return out


def measure(bars):
    H = 7
    RAW = "debug_info.components.swing_move.last_history_value"

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            raw = raw.where(raw.notna(), _recompute_raw(close))
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            active = fc != 0
            in_profile = regime == "unknown"
            side_ok = np.sign(fc) == np.sign(raw)
            n_active += int(active.sum())
            n_agree += int((active & in_profile & side_ok & raw.notna()).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90
    situation = {"agreement": agreement, "passed": bool(passed)}

    main_name = "OLS slope of 7-bar forward excess return (minus coin's normal 7-bar drift) on the forecast, grid bars with nonzero forecast"
    threshold = "confirm: t >= 2 with both sides passing; reject: t <= -2; else inconclusive"
    reading = ("Profile taken from the recorded regime ('unknown' = choppy-calm, the only regime with a strategy) and side from the sign of "
               "the raw swing-scaled 14-day move (recomputed from prices where unrecorded); the slope is an OLS slope with intercept whose t uses "
               "day-clustered standard errors (scores summed per UTC day, G/(G-1) correction); the normal drift is the mean of each coin's "
               "non-overlapping 7-bar grid returns over all its windows; fewer than the plan's minimum cases is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on expected side": int(n_agree)},
            "decided_by": ("Fewer than 90% of bars with a nonzero forecast are choppy-calm (regime 'unknown') bars whose forecast sign matches "
                           "the sign of the swing-scaled 14-day move, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(close)
            for i in range(0, n - H, H):
                a, b = close[i], close[i + H]
                if np.isfinite(a) and np.isfinite(b) and a != 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    rows = []
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            days = _to_time(df["timestamp"]).dt.floor("D").values
            n = len(df)
            for i in range(0, n - H, H):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                a, b = close[i], close[i + H]
                if not (np.isfinite(a) and np.isfinite(b)) or a == 0:
                    continue
                rows.append((days[i], float(f), b / a - 1.0 - drift[coin]))

    cases = pd.DataFrame(rows, columns=["day", "f", "y"])
    n_cases = int(len(cases))
    n_long = int((cases["f"] > 0).sum()) if n_cases else 0
    n_short = int((cases["f"] < 0).sum()) if n_cases else 0
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"grid cases with a nonzero forecast": n_cases, "long cases": n_long,
              "short cases": n_short, "days (clusters)": n_days}

    slope = None
    t = None
    if n_cases >= 3 and cases["f"].nunique() > 1:
        x = cases["f"].values
        y = cases["y"].values
        X = np.column_stack([np.ones(n_cases), x])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        resid = y - X @ beta
        scores = X * resid[:, None]
        sc = pd.DataFrame(scores).groupby(cases["day"].values).sum().values
        G = sc.shape[0]
        meat = sc.T @ sc
        corr = G / (G - 1) if G > 1 else np.nan
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t = float(slope / se) if np.isfinite(se) and se > 0 else None

    mean_long = float(cases.loc[cases["f"] > 0, "y"].mean()) if n_long else None
    mean_short = float(cases.loc[cases["f"] < 0, "y"].mean()) if n_short else None
    long_ok = mean_long is not None and mean_long > 0
    short_ok = mean_short is not None and mean_short < 0
    support_pass = bool(long_ok and short_ok) if (n_long and n_short) else None
    supporting = {
        "name": "mean excess forward return: long > 0 and short < 0",
        "value": None if mean_long is None or mean_short is None else float(mean_long - mean_short),
        "passed": support_pass,
        "long_mean_excess": mean_long,
        "short_mean_excess": mean_short,
    }

    main = {"name": main_name, "value": slope,
            "statistic": None if t is None else {"name": "slope t (day-clustered)", "value": t},
            "threshold": threshold}

    if n_cases < 100 or n_long < 30 or n_short < 30:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} grid cases (need 100), {n_long} long and {n_short} short (need 30 each).")
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and support_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess return is above 0 on long cases and below 0 on short cases."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but one side fails the supporting check."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger swing-scaled moves are followed by reversals."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": situation,
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
