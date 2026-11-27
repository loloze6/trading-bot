import json
import numpy as np
import pandas as pd


def _to_dt(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype(float)
        med = np.nanmedian(np.abs(v.values)) if len(v) else 0.0
        unit = "ms" if med > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def _component_raw(df, cid):
    flat = "debug_info.components.%s.last_history_value" % cid
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    if "debug_info.components" in df.columns:
        out = []
        for x in df["debug_info.components"].values:
            val = np.nan
            d = x
            if isinstance(d, str):
                try:
                    d = json.loads(d)
                except Exception:
                    d = None
            if isinstance(d, dict):
                c = d.get(cid)
                if isinstance(c, dict):
                    v = c.get("last_history_value")
                    try:
                        val = float(v) if v is not None else np.nan
                    except Exception:
                        val = np.nan
            out.append(val)
        return pd.Series(out, index=df.index, dtype=float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def _cluster_slope_t(x, y, groups):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    n = len(x)
    if n < 3 or np.var(x) == 0:
        return None, None
    X = np.column_stack([np.ones(n), x])
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    resid = y - X @ beta
    g = pd.Series(groups).astype(str).values
    uniq = np.unique(g)
    G = len(uniq)
    if G < 2:
        return float(beta[1]), None
    meat = np.zeros((2, 2))
    for u in uniq:
        m = g == u
        s = X[m].T @ resid[m]
        meat += np.outer(s, s)
    k = 2
    corr = (G / (G - 1.0)) * ((n - 1.0) / (n - k)) if n > k else 1.0
    V = corr * XtX_inv @ meat @ XtX_inv
    se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
    if not np.isfinite(se) or se == 0:
        return float(beta[1]), None
    return float(beta[1]), float(beta[1] / se)


def measure(bars):
    reading = ("The situation is a positive one-day scaled return (the recorded scaled_rise raw value > 0, "
               "or the day's close-to-close return > 0 where it is not recorded) on the long side; "
               "the horizon of 1 bar makes every bar its own grid cell; the coin's mean daily return pools all "
               "its windows' 1-day returns; the regression is OLS with an intercept and day-clustered (CR1) "
               "standard errors; the plan's 'fewer than 100 cases on at least 50 distinct days' minimum is "
               "reported as not observable, as the workflow requires.")

    active_total = 0
    active_agree = 0
    case_rows = []

    for coin, wins in bars.items():
        # coin mean daily return over all windows
        all_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            ret_today = close / close.shift(1) - 1.0
            ret_next = close.shift(-1) / close - 1.0
            all_rets.append(ret_next.dropna().values)
            raw = _component_raw(d, "scaled_rise")
            days = _to_dt(d["timestamp"]).dt.floor("D").dt.strftime("%Y-%m-%d").values
            prepared.append((fc, raw, ret_today, ret_next, days))
        if all_rets:
            cat = np.concatenate(all_rets)
            coin_mean = float(np.mean(cat)) if len(cat) else np.nan
        else:
            coin_mean = np.nan

        for fc, raw, ret_today, ret_next, days in prepared:
            # situation check
            act = fc.notna() & (fc != 0)
            sit = pd.Series(np.where(raw.notna(), raw > 0, ret_today > 0), index=fc.index).astype(bool)
            sit_unknown = raw.isna() & ret_today.isna()
            agree = act & sit & ~sit_unknown & (fc > 0)
            active_total += int(act.sum())
            active_agree += int(agree.sum())

            # cases
            m = (fc > 0) & ret_next.notna()
            if np.isfinite(coin_mean):
                for i in np.where(m.values)[0]:
                    case_rows.append((float(fc.iloc[i]),
                                      float(ret_next.iloc[i] - coin_mean),
                                      days[i]))

    agreement = (active_agree / active_total) if active_total > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "slope t of next-day excess return on forecast, day-clustered"
    threshold = "confirm: slope t >= 2 with mean excess > 0; reject: slope t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(active_total), "active bars in situation on long side": int(active_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on a day whose "
                           "volatility-scaled one-day return is positive, so the config does not trade the plan's "
                           "situation on its side."),
            "reading": reading,
        }

    n_cases = len(case_rows)
    if n_cases:
        x = np.array([r[0] for r in case_rows])
        y = np.array([r[1] for r in case_rows])
        g = np.array([r[2] for r in case_rows])
        n_days = int(len(np.unique(g)))
    else:
        x = y = g = np.array([])
        n_days = 0

    slope, tstat = (None, None)
    mean_excess = float(np.mean(y)) if n_cases else None
    if n_cases >= 3:
        slope, tstat = _cluster_slope_t(x, y, g)

    sup_pass = None if mean_excess is None else bool(mean_excess > 0)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided = ("Minimum not reached: the plan needs at least 100 cases on at least 50 distinct days; "
                   "there are %d cases on %d days." % (n_cases, n_days))
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm: slope t >= 2 and the mean excess next-day return over the cases is above 0."
    elif tstat <= -2:
        status = "rejected"
        decided = "Reject: slope t <= -2."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "Inconclusive: slope t >= 2 but the mean excess next-day return is at or below 0."
    else:
        status = "inconclusive"
        decided = "Inconclusive: slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": None if slope is None else float(slope),
            "statistic": None if tstat is None else {"name": "day-clustered slope t", "value": float(tstat)},
            "threshold": threshold,
        },
        "supporting_check": {"name": "mean excess next-day return over cases > 0",
                             "value": mean_excess, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
