import numpy as np
import pandas as pd


def measure(bars):
    COMP = "debug_info.components.scaled_rise.last_history_value"
    EPS = 1e-12

    def to_day(ts):
        return pd.to_datetime(ts, utc=True).dt.floor("D")

    def clustered_mean_t(vals, days):
        vals = np.asarray(vals, dtype=float)
        n = len(vals)
        if n < 2:
            return (float(np.mean(vals)) if n else None), None
        m = vals.mean()
        dev = pd.Series(vals - m).groupby(np.asarray(days)).sum().values
        se = np.sqrt(np.sum(dev ** 2)) / n
        if not np.isfinite(se) or se <= 0:
            return float(m), None
        return float(m), float(m / se)

    def clustered_slope_t(x, y, days):
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        n = len(x)
        if n < 3:
            return None, None
        X = np.column_stack([np.ones(n), x])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) < 2:
            return None, None
        XtX_inv = np.linalg.inv(XtX)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        scores = pd.DataFrame(X * e[:, None]).groupby(np.asarray(days)).sum().values
        meat = scores.T @ scores
        V = XtX_inv @ meat @ XtX_inv
        se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
        if not np.isfinite(se) or se <= 0:
            return float(beta[1]), None
        return float(beta[1]), float(beta[1] / se)

    # ---- assemble rows per coin, returns strictly inside each window ----
    frames = []
    for coin, wins in bars.items():
        coin_frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            d["close"] = pd.to_numeric(d["close"], errors="coerce")
            d["next_ret"] = d["close"].shift(-1) / d["close"] - 1.0
            d["prev_ret"] = d["close"] / d["close"].shift(1) - 1.0
            d["coin"] = coin
            d["window"] = w
            d["day"] = to_day(d["timestamp"])
            if COMP not in d.columns:
                d[COMP] = np.nan
            coin_frames.append(d[["coin", "window", "day", "close", "next_ret", "prev_ret",
                                  "forecast", "regime", "postRebalance_current_allocation", COMP]])
        if not coin_frames:
            continue
        cdf = pd.concat(coin_frames, ignore_index=True)
        coin_mean = cdf["next_ret"].dropna().mean()  # coin's mean daily return over all windows
        cdf["excess"] = cdf["next_ret"] - coin_mean
        frames.append(cdf)

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean timing gain of position vs coin drift, next day",
                             "value": None, "statistic": None,
                             "threshold": "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2"},
            "supporting_check": None,
            "counts": {"distinct days with a nonzero position": 0},
            "decided_by": "No bars in the record: fewer than 100 distinct days with a nonzero position.",
            "reading": "none",
        }

    allb = pd.concat(frames, ignore_index=True)
    allb["forecast"] = pd.to_numeric(allb["forecast"], errors="coerce").fillna(0.0)
    allb["pos"] = pd.to_numeric(allb["postRebalance_current_allocation"], errors="coerce")
    raw = pd.to_numeric(allb[COMP], errors="coerce")

    # ---- situation check: falling calm profile (regime 'unknown') and an up day, side short ----
    in_profile = allb["regime"].astype(str) == "unknown"
    up_day = raw.where(raw.notna(), allb["prev_ret"]) > 0
    situation = in_profile & up_day
    active = allb["forecast"].abs() > EPS
    n_active = int(active.sum())
    if n_active > 0:
        agree = float((situation & (allb["forecast"] < 0))[active].mean())
        passed = agree >= 0.9
    else:
        agree = None
        passed = True

    main_name = "mean timing gain: position x (next-day return - coin mean daily return)"
    main_thr = "confirm: mean > 0 with t >= 2 (and slope check passes); reject: mean < 0 with t <= -2"
    reading = ("The falling calm profile is read from the recorded regime ('unknown' = neither veto fired), an up day "
               "from the raw scaled rise > 0; a nonzero position is postRebalance_current_allocation != 0; 'cases of one "
               "day summed together' is read as day-clustered standard errors (deviations / scores summed per day) for "
               "both the mean and the slope; the 100-day minimum counts all bars with a nonzero position.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agree, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of bars with a nonzero forecast are short on an up day inside the falling "
                           "calm profile, so the config does not trade the plan's situation and side."),
            "reading": reading,
        }

    # ---- main measure ----
    haspos = allb["pos"].notna() & (allb["pos"].abs() > EPS)
    n_days_pos = int(allb.loc[haspos, "day"].nunique())
    m = allb[haspos & allb["excess"].notna()]
    gains = (m["pos"] * m["excess"]).values
    main_mean, main_t = clustered_mean_t(gains, m["day"].values) if len(m) else (None, None)

    # ---- supporting check ----
    s = allb[(allb["forecast"] < 0) & allb["excess"].notna()]
    slope, slope_t = clustered_slope_t(s["forecast"].values, s["excess"].values, s["day"].values)
    sup_pass = bool(slope is not None and slope_t is not None and slope > 0 and slope_t >= 2)

    counts = {
        "distinct days with a nonzero position": n_days_pos,
        "position bars with next-day return": int(len(m)),
        "days of position cases": int(m["day"].nunique()) if len(m) else 0,
        "forecast-below-0 bars in regression": int(len(s)),
        "days in regression": int(s["day"].nunique()) if len(s) else 0,
    }

    if n_days_pos < 100:
        status = "not observable"
        decided = f"Only {n_days_pos} distinct days with a nonzero position, fewer than the plan's 100."
    elif main_mean is None or main_t is None:
        status = "inconclusive"
        decided = "The main t-statistic could not be computed: any other result is inconclusive."
    elif main_mean > 0 and main_t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Main mean above 0 with t >= 2 and the slope on the forecast positive with t >= 2."
    elif main_mean < 0 and main_t <= -2:
        status = "rejected"
        decided = "Main mean below 0 with t <= -2: positions lose against the coin's drift after scaled rises."
    elif main_mean > 0 and main_t >= 2:
        status = "inconclusive"
        decided = "Main t >= 2 but the supporting slope's t is under 2 (or slope not positive): inconclusive."
    else:
        status = "inconclusive"
        decided = "Main t between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agree, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": main_mean,
            "statistic": ({"name": "t of the mean, day-clustered", "value": main_t} if main_t is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "slope of next-day excess return on forecast (forecast < 0), day-clustered t >= 2",
            "value": slope_t,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
