import numpy as np
import pandas as pd


def _to_time(s):
    if pd.api.types.is_numeric_dtype(s):
        v = pd.to_numeric(s, errors="coerce")
        unit = "ms" if v.dropna().abs().median() > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True, errors="coerce")


def _cluster_ols_t(x, y, groups):
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
    e = y - X @ beta
    g = pd.Series(groups).astype(str).values
    uniq = np.unique(g)
    G = len(uniq)
    if G < 2:
        return float(beta[1]), np.nan
    meat = np.zeros((2, 2))
    for u in uniq:
        m = g == u
        s = X[m].T @ e[m]
        meat += np.outer(s, s)
    k = 2
    c = (G / (G - 1.0)) * ((n - 1.0) / (n - k))
    V = c * bread @ meat @ bread
    se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
    return float(beta[1]), float(beta[1] / se) if se and np.isfinite(se) else np.nan


def measure(bars):
    raw_col = "debug_info.components.scaled_rise.last_history_value"

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    # ---------- data for criterion ----------
    case_rows = []
    coin_means = {}

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        all_rets = []
        prepared = []
        for w in sorted(wins.keys(), key=lambda k: (len(str(k)), str(k))):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.copy()
            if "timestamp" in df.columns:
                df["_ts"] = _to_time(df["timestamp"])
                df = df.sort_values("_ts").reset_index(drop=True)
            else:
                df["_ts"] = pd.NaT
            close = pd.to_numeric(df["close"], errors="coerce")
            ret_prev = close / close.shift(1) - 1.0
            ret_next = close.shift(-1) / close - 1.0
            all_rets.append(ret_prev.dropna().values)
            df["_ret_prev"] = ret_prev
            df["_ret_next"] = ret_next
            prepared.append(df)

        if all_rets:
            cat = np.concatenate(all_rets) if len(all_rets) else np.array([])
            coin_means[coin] = float(np.mean(cat)) if len(cat) else np.nan
        else:
            coin_means[coin] = np.nan

        for df in prepared:
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            in_profile = regime.str.lower() == "unknown"
            if raw_col in df.columns:
                raw = pd.to_numeric(df[raw_col], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            up = raw > 0
            up = up.where(raw.notna(), df["_ret_prev"] > 0).fillna(False).astype(bool)
            situation = in_profile & up
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            mu = coin_means[coin]
            sel = (fc < 0) & df["_ret_next"].notna()
            for i in np.where(sel.values)[0]:
                ts = df["_ts"].iloc[i]
                day = str(ts.normalize().date()) if pd.notna(ts) else f"{coin}_{i}"
                case_rows.append((abs(float(fc.iloc[i])),
                                  float(df["_ret_next"].iloc[i]) - mu,
                                  day))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    threshold_txt = "confirm if slope t <= -2 (with mean excess < 0); reject if slope t >= +2"
    main_name = "slope of next-day excess return on abs(forecast), forecast<0 bars"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are up days inside the "
                           "falling-agitated profile (regime 'unknown') with a short forecast, as the Fidelity states."),
            "reading": ("The profile is read from the recorded regime ('unknown' = both vetoes passed, i.e. 60-bar "
                        "evolution < -10 and volatility percentile > 0.5) and an up day from the raw scaled return > 0."),
        }

    reading = ("Profile read from regime 'unknown' and up day from raw scaled return > 0; the slope t uses an OLS "
               "of excess return on abs(forecast) with day-clustered (CR1) standard errors; the coin's mean daily "
               "return is the mean of all its within-window close-to-close returns; days are UTC calendar days of the "
               "bar's timestamp.")

    n_cases = len(case_rows)
    days = sorted(set(r[2] for r in case_rows))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    if n_cases >= 3:
        x = np.array([r[0] for r in case_rows])
        y = np.array([r[1] for r in case_rows])
        g = [r[2] for r in case_rows]
        slope, t = _cluster_ols_t(x, y, g)
        mean_ex = float(np.mean(y))
    else:
        slope, t, mean_ex = np.nan, np.nan, (float(np.mean([r[1] for r in case_rows])) if case_rows else np.nan)

    slope_v = float(slope) if np.isfinite(slope) else None
    t_v = float(t) if np.isfinite(t) else None
    mean_v = float(mean_ex) if np.isfinite(mean_ex) else None
    sup_pass = (mean_v < 0) if mean_v is not None else None

    main = {"name": main_name, "value": slope_v,
            "statistic": {"name": "OLS slope t, day-clustered", "value": t_v} if t_v is not None else None,
            "threshold": threshold_txt}
    sup = {"name": "mean next-day excess return on forecast<0 bars below 0", "value": mean_v,
           "passed": sup_pass}

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases (need 100) and {n_days} distinct days (need 60).")
    elif t_v is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_v <= -2 and sup_pass:
        status = "confirmed"
        decided = "The slope has t <= -2 and the mean next-day excess return is below 0 (confirm rule)."
    elif t_v >= 2:
        status = "rejected"
        decided = "The slope has t >= +2 (reject rule)."
    elif t_v <= -2:
        status = "inconclusive"
        decided = "The slope has t <= -2 but the mean excess return is not below 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and +2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
