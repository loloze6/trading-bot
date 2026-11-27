import numpy as np
import pandas as pd


def _to_day(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        mx = float(np.nanmax(s.values)) if len(s) else 0.0
        unit = "ms" if mx > 1e11 else "s"
        t = pd.to_datetime(s, unit=unit, utc=True)
    else:
        t = pd.to_datetime(s, utc=True)
    return t.dt.floor("D").dt.strftime("%Y-%m-%d").values


def _cluster_slope_t(x, y, groups):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    n = len(y)
    if n < 3:
        return np.nan, np.nan
    X = np.column_stack([np.ones(n), x])
    XtX = X.T @ X
    try:
        bread = np.linalg.inv(XtX)
    except np.linalg.LinAlgError:
        return np.nan, np.nan
    beta = bread @ (X.T @ y)
    u = y - X @ beta
    g = pd.Series(groups)
    uniq = pd.unique(g)
    G = len(uniq)
    if G < 2:
        return float(beta[1]), np.nan
    meat = np.zeros((2, 2))
    codes = pd.factorize(g)[0]
    for k in range(G):
        m = codes == k
        s = X[m].T @ u[m]
        meat += np.outer(s, s)
    k_par = 2
    c = (G / (G - 1.0)) * ((n - 1.0) / (n - k_par)) if n > k_par else np.nan
    V = c * bread @ meat @ bread
    se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
    t = beta[1] / se if se and np.isfinite(se) and se > 0 else np.nan
    return float(beta[1]), float(t)


def measure(bars):
    H = 7
    RAW = "debug_info.components.month_move.last_history_value"
    PROFILE_REGIME = "unknown"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            raw = (pd.to_numeric(df[RAW], errors="coerce").values
                   if RAW in df.columns else np.full(len(df), np.nan))
            # fallback: recompute the 30-bar percent return from prices inside the window
            rec = np.full(len(df), np.nan)
            if len(df) > 30:
                rec[30:] = (close[30:] - close[:-30]) / close[:-30] * 100.0
            raw = np.where(np.isfinite(raw), raw, rec)
            regime = df["regime"].astype(str).values
            in_profile = regime == PROFILE_REGIME
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active += 1
                r = raw[i]
                if in_profile[i] and np.isfinite(r) and r != 0 and np.sign(fc[i]) == np.sign(r):
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast lie in the choppy calm profile "
                           "(regime 'unknown') with the forecast's sign equal to the sign of the 30-bar return."),
            "reading": ("The choppy calm profile is read as the detector's non-chop regime 'unknown'; the side is "
                        "long above the close of 30 bars earlier and short below it."),
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin in sorted(bars):
        coin_rets = []
        coin_cases = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            days = _to_day(df["timestamp"])
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    continue
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                r = close[i + H] / close[i] - 1.0
                coin_rets.append(r)
                f = fc[i]
                if np.isfinite(f) and f != 0:
                    coin_cases.append((r, float(f), days[i]))
        if not coin_rets:
            continue
        mu = float(np.mean(coin_rets))
        for r, f, d in coin_cases:
            rows.append({"coin": coin, "excess": r - mu, "forecast": f, "day": d})

    cases = pd.DataFrame(rows, columns=["coin", "excess", "forecast", "day"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    long_c = cases[cases["forecast"] > 0]
    short_c = cases[cases["forecast"] < 0]
    n_long, n_short = int(len(long_c)), int(len(short_c))

    slope, t = (np.nan, np.nan)
    if n_cases >= 3:
        slope, t = _cluster_slope_t(cases["forecast"].values, cases["excess"].values, cases["day"].values)

    mean_long = float(long_c["excess"].mean()) if n_long else None
    mean_short = float(short_c["excess"].mean()) if n_short else None
    long_ok = (mean_long is not None) and mean_long > 0
    short_ok = (mean_short is not None) and mean_short < 0
    support_passed = bool(long_ok and short_ok) if (n_long and n_short) else None

    counts = {"cases": n_cases, "days": n_days, "long cases": n_long, "short cases": n_short,
              "active bars": int(n_active)}

    t_val = float(t) if np.isfinite(t) else None

    if n_cases < 100:
        status, decided = "not observable", "Fewer than 100 cases: the plan's minimum count is not reached."
    elif n_days < 60:
        status, decided = "not observable", "The cases fall on fewer than 60 days: the plan's minimum count is not reached."
    elif n_long < 30 or n_short < 30:
        status, decided = "not observable", "Fewer than 30 cases on one side: the plan's minimum count is not reached."
    elif t_val is None:
        status, decided = "inconclusive", "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and support_passed:
        status, decided = "confirmed", "The slope's t is 2 or more with at least 100 cases on at least 60 days, and the mean excess return is above 0 on long cases and below 0 on short cases."
    elif t_val >= 2:
        status, decided = "inconclusive", "The slope's t is 2 or more but one side fails the supporting check."
    elif t_val <= -2:
        status, decided = "rejected", "The slope's t is -2 or less with at least 100 cases on at least 60 days."
    else:
        status, decided = "inconclusive", "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": passed},
        "main_measure": {
            "name": "slope of 7-bar excess return on forecast",
            "value": (float(slope) if np.isfinite(slope) else None),
            "statistic": ({"name": "slope t, day-clustered", "value": t_val} if t_val is not None else None),
            "threshold": "confirm if t >= 2 (with supporting check), reject if t <= -2, with at least 100 cases on at least 60 days",
        },
        "supporting_check": {
            "name": "mean excess return >0 on long cases and <0 on short cases",
            "value": {"long_mean_excess": mean_long, "short_mean_excess": mean_short} and (
                (mean_long if mean_long is not None else 0.0) - (mean_short if mean_short is not None else 0.0)
                if (mean_long is not None and mean_short is not None) else None),
            "passed": support_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The choppy calm profile is the detector's non-chop regime 'unknown' and the side is the sign of the "
                    "30-bar return. The slope's t uses OLS with an intercept and day-clustered (CR1) standard errors, "
                    "clustering cases by their grid bar's UTC day. The coin's mean is over every valid non-overlapping "
                    "7-bar grid return in all its windows. The minimums (100 cases, 60 days, 30 per side) gate the "
                    "result as 'not observable'. The supporting check's value is the long mean excess minus the short "
                    "mean excess."),
    }
