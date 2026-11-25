import numpy as np
import pandas as pd


def measure(bars):
    comp = "debug_info.components.low_close_wide_day.last_history_value"

    # ---------- gather rows, per coin and window (never across windows) ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            d["ret1"] = close.shift(-1) / close - 1.0  # inside the window only
            d["coin"] = coin
            d["window"] = w
            d["day"] = d["timestamp"].dt.floor("D")
            if comp not in d.columns:
                d[comp] = np.nan
            rows.append(d[["coin", "window", "timestamp", "day", "high", "close",
                           "forecast", comp, "ret1"]])
    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "slope of next-day excess return on forecast", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirms (with check), t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"bars with a forecast": 0, "distinct days": 0, "bars in the top fifth": 0},
            "decided_by": "no bars in the record",
            "reading": "none",
        }
    allb = pd.concat(rows, ignore_index=True)
    allb["forecast"] = allb["forecast"].astype(float)
    allb[comp] = allb[comp].astype(float)

    # ---------- situation check ----------
    # Situation (kept): close below the day's high on a graded scale, (high - close) / prior 30-day mean range > 0;
    # the outcome is a rise, so the expected side is long.
    active = allb[allb["forecast"].notna() & (allb["forecast"] != 0)]
    if len(active) > 0:
        raw = active[comp]
        in_sit = raw.notna() & (raw > 0) & (active["high"].astype(float) > active["close"].astype(float))
        on_side = active["forecast"] > 0
        agreement = float((in_sit & on_side).mean())
    else:
        agreement = 0.0
    passed = agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "slope of next-day excess return on forecast", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirms (with check), t <= -2 rejects"},
            "supporting_check": None,
            "counts": {},
            "decided_by": ("fewer than 90 % of the active bars are long bars where the close sits below the high "
                           "with a positive raw (high - close) / prior 30-day mean range, as the Fidelity requires"
                           if len(active) > 0 else "the record has no active (non-zero forecast) bars"),
            "reading": "situation = raw component > 0 and high > close, expected side long.",
        }

    # ---------- main measure ----------
    # Coin mean daily return over all its windows (every bar's next-day return, inside windows).
    coin_mean = allb.groupby("coin")["ret1"].mean()
    allb["excess"] = allb["ret1"] - allb["coin"].map(coin_mean)
    s = allb[allb["excess"].notna() & allb["forecast"].notna()].copy()

    n = len(s)
    with_fc = s[s["forecast"] != 0]
    n_fc = int(len(with_fc))
    n_days_fc = int(with_fc["day"].nunique())

    slope = None
    tval = None
    if n >= 3 and s["forecast"].var() > 0:
        x = s["forecast"].values
        y = s["excess"].values
        X = np.column_stack([np.ones(n), x])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ (X.T @ y)
        e = y - X @ beta
        sc = pd.DataFrame(X * e[:, None], columns=["a", "b"])
        sc["day"] = s["day"].values
        G_scores = sc.groupby("day")[["a", "b"]].sum().values
        G = G_scores.shape[0]
        meat = G_scores.T @ G_scores
        V = XtX_inv @ meat @ XtX_inv
        if G > 1:
            V = V * G / (G - 1)
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        tval = float(slope / se) if se and np.isfinite(se) and se > 0 else None

    # ---------- supporting check: top fifth of the forecast ----------
    if n > 0:
        q80 = float(s["forecast"].quantile(0.8))
        top = s[s["forecast"] >= q80]
        if q80 <= 0:
            top = top[top["forecast"] > 0]
    else:
        top = s.iloc[0:0]
    n_top = int(len(top))
    top_mean = float(top["excess"].mean()) if n_top > 0 else None
    check_pass = (top_mean is not None) and (top_mean > 0)

    counts = {"bars with a forecast": n_fc,
              "distinct days of bars with a forecast": n_days_fc,
              "bars in the top fifth": n_top}

    # ---------- decision ----------
    if n_fc < 1000:
        status = "not observable"
        decided = f"fewer than 1,000 bars with a forecast ({n_fc})."
    elif n_days_fc < 500:
        status = "not observable"
        decided = f"bars with a forecast fall on fewer than 500 distinct days ({n_days_fc})."
    elif n_top < 200:
        status = "not observable"
        decided = f"fewer than 200 bars in the top fifth ({n_top})."
    elif tval is None:
        status = "inconclusive"
        decided = "the slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and check_pass:
        status = "confirmed"
        decided = "the slope's t is 2 or more and the top-fifth mean excess return is above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "the slope's t is -2 or less."
    elif tval >= 2:
        status = "inconclusive"
        decided = "the slope's t is 2 or more but the top-fifth mean excess return is not above 0."
    else:
        status = "inconclusive"
        decided = "the slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "slope of next-day return minus coin mean on forecast (pooled, every bar)",
                         "value": slope,
                         "statistic": ({"name": "OLS slope t, clustered by day", "value": tval}
                                       if tval is not None else None),
                         "threshold": "t >= 2 confirms (with the check passing), t <= -2 rejects"},
        "supporting_check": {"name": "mean next-day excess return in the top fifth of the forecast > 0",
                             "value": top_mean, "passed": bool(check_pass)},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Regression with intercept over every bar with a next-day return in its window, t from "
                    "day-clustered (UTC day) standard errors with a G/(G-1) correction; 'bars with a forecast' "
                    "are bars with a non-zero forecast; the top fifth is bars at or above the pooled 80th "
                    "percentile of the forecast (non-zero only if that percentile is 0)."),
    }
