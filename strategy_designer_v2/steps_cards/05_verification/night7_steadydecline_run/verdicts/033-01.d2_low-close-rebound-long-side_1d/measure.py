import numpy as np
import pandas as pd


def measure(bars):
    rows = []
    all_rets = {}
    for coin, wins in bars.items():
        coin_rets = []
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float)
            high = d["high"].astype(float)
            low = d["low"].astype(float)
            rng = high - low
            cl = (close - low) / rng.where(rng > 0)
            nxt = close.shift(-1) / close - 1.0  # inside this window only
            coin_rets.append(nxt.dropna().values)
            part = pd.DataFrame({
                "coin": coin, "window": w,
                "day": ts.dt.floor("D"),
                "forecast": pd.to_numeric(d["forecast"], errors="coerce"),
                "regime": d["regime"].astype(str),
                "cl": cl, "ret": nxt,
            })
            rows.append(part)
        all_rets[coin] = np.concatenate(coin_rets) if coin_rets else np.array([])
    data = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()

    # ---------- situation check ----------
    active = data[data["forecast"].fillna(0) != 0]
    n_active = len(active)
    if n_active > 0:
        ok = (active["cl"] < 0.5) & (active["forecast"] > 0)
        agreement = float(ok.fillna(False).mean())
    else:
        agreement = 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    reading = ("Situation computed from prices as (close-low)/(high-low) < 0.5 (zero-range bars count as outside it), long side; "
               "the slope is a pooled OLS with intercept of excess next-day return on forecast over regime bars of all coins and windows, "
               "with day-clustered (CR1) standard errors; the coin's mean daily return is the mean of all its next-bar returns over all windows; "
               "the t of the forecast>=2 excess return in the reject rule is the ordinary t of the mean; counts are regime bars with a next-day return.")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars with the close in the lower half of the day's range "
                           "(the plan's situation and side)."),
            "reading": reading,
        }

    # ---------- main measure ----------
    reg = data[data["regime"] == "mean_reversion"].copy()
    reg["mu"] = reg["coin"].map({c: (float(np.mean(r)) if len(r) else np.nan) for c, r in all_rets.items()})
    reg["ex"] = reg["ret"] - reg["mu"]
    reg = reg.dropna(subset=["ex", "forecast"])
    n_reg = int(len(reg))
    n_days = int(reg["day"].nunique())

    slope, t_slope = None, None
    if n_reg >= 3:
        x = reg["forecast"].values.astype(float)
        y = reg["ex"].values.astype(float)
        X = np.column_stack([np.ones_like(x), x])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) == 2:
            XtX_inv = np.linalg.inv(XtX)
            beta = XtX_inv @ X.T @ y
            e = y - X @ beta
            groups = reg["day"].values
            meat = np.zeros((2, 2))
            gdf = pd.DataFrame({"g": groups, "a": X[:, 0] * e, "b": X[:, 1] * e})
            sums = gdf.groupby("g")[["a", "b"]].sum().values
            for s in sums:
                meat += np.outer(s, s)
            G = sums.shape[0]
            N, K = X.shape
            corr = (G / (G - 1)) * ((N - 1) / (N - K)) if G > 1 and N > K else 1.0
            V = corr * XtX_inv @ meat @ XtX_inv
            slope = float(beta[1])
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            t_slope = float(slope / se) if se and np.isfinite(se) else None

    # ---------- supporting check ----------
    hi = reg[reg["forecast"] >= 2]["ex"].values.astype(float)
    n_hi = int(len(hi))
    mean_hi = float(np.mean(hi)) if n_hi > 0 else None
    t_hi = None
    if n_hi > 1:
        sd = float(np.std(hi, ddof=1))
        if sd > 0:
            t_hi = float(mean_hi / (sd / np.sqrt(n_hi)))
    sup_pass = (mean_hi is not None and mean_hi > 0)

    counts = {"regime bars": n_reg, "distinct days": n_days, "forecast >= 2 regime bars": n_hi}

    if n_reg < 300 or n_days < 200:
        status = "not observable"
        decided = f"The plan's minimum of 300 regime bars on 200 distinct days is not reached ({n_reg} bars on {n_days} days)."
    elif slope is None or t_slope is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the mean excess next-day return on forecast >= 2 bars is above 0."
    elif (slope < 0 and t_slope <= -2) or (mean_hi is not None and mean_hi < 0 and t_hi is not None and t_hi <= -2):
        status = "rejected"
        if slope < 0 and t_slope <= -2:
            decided = "The slope is negative with t <= -2."
        else:
            decided = "The excess next-day return on forecast >= 2 bars is negative with t <= -2."
    else:
        status = "inconclusive"
        if slope > 0 and t_slope >= 2:
            decided = "The slope is positive with t >= 2 but the supporting check fails."
        else:
            decided = "The slope t lies between -2 and 2 and no reject rule is met."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of excess next-day return on forecast, regime bars",
            "value": slope,
            "statistic": {"name": "t, standard errors clustered by day", "value": t_slope} if t_slope is not None else None,
            "threshold": "confirm: slope > 0 with t >= 2 (and check passes); reject: slope < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "mean excess next-day return on regime bars with forecast >= 2, above 0",
            "value": mean_hi,
            "passed": bool(sup_pass) if mean_hi is not None else False,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
