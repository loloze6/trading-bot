import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.vol_fall.last_history_value"

    # ---------- collect per coin / window, never across windows ----------
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True).copy()
            close = pd.to_numeric(d["close"], errors="coerce")
            prev_ret = close / close.shift(1) - 1.0
            next_ret = close.shift(-1) / close - 1.0
            all_rets.append(next_ret.dropna().values)
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            fc = pd.to_numeric(d[FC], errors="coerce")
            ts = pd.to_datetime(d["timestamp"], utc=True)
            rows.append(pd.DataFrame({
                "coin": coin, "window": w, "ts": ts, "day": ts.dt.floor("D"),
                "forecast": fc.values, "raw": raw.values,
                "prev_ret": prev_ret.values, "next_ret": next_ret.values,
            }))
        coin_rets[coin] = np.concatenate(all_rets) if all_rets else np.array([])

    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "slope of excess next-day return on forecast", "value": None,
                             "statistic": None, "threshold": "positive with day-clustered t >= 2 to confirm; negative with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"cases with forecast > 0": 0, "distinct days": 0},
            "decided_by": "No bars in the record, so the minimum of 300 cases over 100 days is not reached.",
            "reading": "none",
        }
    data = pd.concat(rows, ignore_index=True)

    # ---------- situation check: a down day (fall on the latest day), long side ----------
    active = data[data["forecast"].notna() & (data["forecast"] != 0)]
    down_price = active["prev_ret"] < 0
    down_raw = active["raw"] > 0
    # prices decide where the previous close is inside the window; else the component's raw value (positive only on down days)
    situation = np.where(active["prev_ret"].notna(), down_price, down_raw)
    on_side = situation & (active["forecast"].values > 0)
    n_active = len(active)
    agreement = float(on_side.sum() / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    threshold_txt = "confirm: slope > 0 with day-clustered t >= 2 and supporting check passes; reject: slope < 0 with t <= -2; otherwise inconclusive"
    reading = ("The situation is a down day (close below the previous close in the same window, or a positive raw component value on a window's first bar) on the long side; "
               "the slope is an OLS fit with intercept whose t uses standard errors clustered by UTC day (with the usual G/(G-1)*(N-1)/(N-K) correction); "
               "the top and bottom fifths are the highest and lowest floor(n/5) cases by forecast, ties broken stably by record order.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "slope of excess next-day return on forecast", "value": None,
                             "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": f"Only {agreement:.1%} of the bars with a non-zero forecast are long bars after a down day, below the 90% the plan's situation (a fall on the latest day, expecting a rise) requires.",
            "reading": reading,
        }

    # ---------- criterion ----------
    coin_mean = {c: (float(np.mean(r)) if len(r) else np.nan) for c, r in coin_rets.items()}
    data["excess"] = data["next_ret"] - data["coin"].map(coin_mean)
    cases = data[(data["forecast"] > 0) & data["excess"].notna() & data["forecast"].notna()].reset_index(drop=True)
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases with forecast > 0": n_cases, "distinct days": n_days}

    slope = None
    t_val = None
    if n_cases >= 3:
        x = cases["forecast"].values.astype(float)
        y = cases["excess"].values.astype(float)
        X = np.column_stack([np.ones(n_cases), x])
        XtX_inv = np.linalg.pinv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        codes = pd.factorize(cases["day"])[0]
        G = int(codes.max() + 1)
        S = np.zeros((G, 2))
        np.add.at(S, codes, X * u[:, None])
        meat = S.T @ S
        V = XtX_inv @ meat @ XtX_inv
        if G > 1 and n_cases > 2:
            V = V * (G / (G - 1)) * ((n_cases - 1) / (n_cases - 2))
        se = float(np.sqrt(max(V[1, 1], 0.0)))
        slope = float(beta[1])
        t_val = float(slope / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 5:
        order = np.argsort(cases["forecast"].values, kind="mergesort")
        k = n_cases // 5
        bottom = cases["excess"].values[order[:k]]
        top = cases["excess"].values[order[-k:]]
        sup_val = float(np.mean(top) - np.mean(bottom))
        sup_pass = bool(sup_val > 0)

    main = {"name": "slope of excess next-day return on forecast (forecast > 0, pooled)",
            "value": slope,
            "statistic": ({"name": "day-clustered OLS t", "value": t_val} if t_val is not None else None),
            "threshold": threshold_txt}
    support = {"name": "mean excess next-day return, top fifth minus bottom fifth of forecasts",
               "value": sup_val, "passed": sup_pass}

    if n_cases < 300 or n_days < 100:
        status = "not observable"
        decided = f"The minimum counts are not reached: {n_cases} cases with forecast > 0 (300 needed) over {n_days} distinct days (100 needed)."
    elif slope is None or t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the top fifth's mean excess return is above the bottom fifth's (confirm rule)."
    elif slope > 0 and t_val >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif slope < 0 and t_val <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
