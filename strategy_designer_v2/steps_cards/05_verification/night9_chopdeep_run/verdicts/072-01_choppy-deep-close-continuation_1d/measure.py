import numpy as np
import pandas as pd


DEPTH_RAW = "debug_info.components.depth.last_history_value"
DEPTH_POST = "debug_info.components.depth.post_pipeline_value"
PROFILE_REGIME = "unknown"  # the config's choppy profile: the only regime with a strategy


def _cluster_ols(x, y, groups):
    """OLS y = a + b x, with standard errors clustered by group (Stata small-sample correction)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    if n < 3 or np.unique(x).size < 2:
        return None, None
    X = np.column_stack([np.ones(n), x])
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ (X.T @ y)
    u = y - X @ beta
    g = pd.Series(groups).astype(str).values
    uniq, inv = np.unique(g, return_inverse=True)
    G = uniq.size
    if G < 2:
        return float(beta[1]), None
    scores = np.zeros((G, 2))
    np.add.at(scores, inv, X * u[:, None])
    meat = scores.T @ scores
    k = 2
    corr = (G / (G - 1.0)) * ((n - 1.0) / (n - k)) if n > k else 1.0
    V = corr * XtX_inv @ meat @ XtX_inv
    se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else None
    b = float(beta[1])
    t = b / se if se not in (None, 0.0) else None
    return b, t


def measure(bars):
    frames = []
    for coin in sorted(bars.keys()):
        wins = bars[coin]
        coin_rows = []
        for w in sorted(wins.keys(), key=lambda s: (len(str(s)), str(s))):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            d["coin"] = coin
            d["window"] = w
            close = pd.to_numeric(d["close"], errors="coerce")
            d["next_ret"] = close.shift(-1) / close - 1.0  # inside the window only
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            d["day"] = d["ts"].dt.floor("D").astype(str)
            for col in (DEPTH_RAW, DEPTH_POST):
                if col not in d.columns:
                    d[col] = np.nan
                d[col] = pd.to_numeric(d[col], errors="coerce")
            d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            d["open"] = pd.to_numeric(d["open"], errors="coerce")
            d["close"] = close
            coin_rows.append(d)
        if not coin_rows:
            continue
        cdf = pd.concat(coin_rows, ignore_index=True)
        # the coin's mean daily return over all its windows together
        cdf["coin_mean"] = cdf["next_ret"].dropna().mean()
        frames.append(cdf)

    threshold_txt = "confirm: slope < 0 with clustered t <= -2 (and check passes); reject: slope > 0 with t >= 2"
    reading = ("The choppy profile is read as the bars whose regime is 'unknown' (the config's only regime with a "
               "strategy, flat when the 60-day trend veto says 'chop'), the situation as that regime with a raw depth "
               "below 0 and a short forecast; 'the day closed up/down' is close above/below the same bar's open; the "
               "minimum counts are taken on the regression's sample (non-zero forecast with a next-day return and a "
               "depth value), days being UTC calendar dates.")

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "slope of next-day excess return on abs(depth)", "value": None,
                             "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"in-profile bars": 0, "distinct days": 0},
            "decided_by": "No bars in the record: the minimum of 300 in-profile bars on 150 days is not reached.",
            "reading": reading,
        }

    all_df = pd.concat(frames, ignore_index=True)

    # ---- situation check ----
    active = all_df["forecast"] != 0
    n_active = int(active.sum())
    in_situation = (
        (all_df["regime"].astype(str) == PROFILE_REGIME)
        & all_df[DEPTH_RAW].notna()
        & (all_df[DEPTH_RAW] < 0)
        & (all_df["forecast"] < 0)
    )
    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "slope of next-day excess return on abs(depth)", "value": None,
                             "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"in-profile bars": 0, "distinct days": 0},
            "decided_by": "No bar has a non-zero forecast: the minimum of 300 in-profile bars on 150 days is not reached.",
            "reading": reading,
        }
    agreement = float((in_situation & active).sum()) / n_active
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "slope of next-day excess return on abs(depth)", "value": None,
                             "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"in-profile bars": None, "distinct days": None},
            "decided_by": ("Fewer than 90 % of the active bars are choppy-profile bars with the close below its 20-day "
                           "high and a short forecast, so the forecast does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---- main measure ----
    s = all_df[active].copy()
    s["excess"] = s["next_ret"] - s["coin_mean"]
    s["x"] = s[DEPTH_POST].abs()
    s = s.dropna(subset=["excess", "x", "day"])
    n_bars = int(len(s))
    n_days = int(s["day"].nunique())

    slope, t = _cluster_ols(s["x"].values, s["excess"].values, s["day"].values) if n_bars > 0 else (None, None)

    up = s[s["close"] > s["open"]]
    down = s[s["close"] < s["open"]]
    b_up, _ = _cluster_ols(up["x"].values, up["excess"].values, up["day"].values) if len(up) else (None, None)
    b_dn, _ = _cluster_ols(down["x"].values, down["excess"].values, down["day"].values) if len(down) else (None, None)
    check_pass = (b_up is not None and b_up < 0) and (b_dn is not None and b_dn < 0)
    check_val = None
    vals = [v for v in (b_up, b_dn) if v is not None]
    if vals:
        check_val = float(max(vals))  # the larger of the two subset slopes: both < 0 iff this < 0

    counts = {"in-profile bars": n_bars, "distinct days": n_days,
              "up-day bars": int(len(up)), "down-day bars": int(len(down))}

    main = {
        "name": "slope of next-day return minus coin mean on abs(depth post_pipeline_value)",
        "value": slope,
        "statistic": {"name": "OLS t, SE clustered by day", "value": t} if t is not None else None,
        "threshold": threshold_txt,
    }
    support = {
        "name": "slope below 0 on up-close and on down-close bars (larger of the two slopes shown)",
        "value": check_val,
        "passed": bool(check_pass),
    }

    if n_bars < 300 or n_days < 150:
        status = "not observable"
        decided = (f"The plan's minimum of 300 in-profile bars on 150 distinct days is not reached "
                   f"({n_bars} bars on {n_days} days).")
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope < 0 and t <= -2:
        if check_pass:
            status = "confirmed"
            decided = "The slope is negative with t <= -2 and is below 0 on both up and down days (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The slope is negative with t <= -2 but is not below 0 in one of the up/down subsets (inconclusive rule)."
    elif slope > 0 and t >= 2:
        status = "rejected"
        decided = "The slope is positive with t >= 2: deeper closes are followed by relatively larger rises (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's |t| is below 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
