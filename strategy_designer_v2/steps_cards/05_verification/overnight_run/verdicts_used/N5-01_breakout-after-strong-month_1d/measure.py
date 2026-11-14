import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    LB = 20
    NW_LAG = 9
    MIN_EVENTS = 100
    fc_col = "forecast"

    # ---------- per coin: forward returns, coin mean over all windows pooled ----------
    frames = []
    for coin, wins in bars.items():
        coin_parts = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True).copy()
            close = pd.to_numeric(d["close"], errors="coerce")
            fwd = close.shift(-H) / close - 1.0
            prior_max = close.shift(1).rolling(LB, min_periods=LB).max()
            computable = prior_max.notna() & close.notna()
            newhigh = close > prior_max
            reg = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            # situation: new 20-day high from prices; where fewer than 20 prior closes exist
            # in the window, fall back on the detector's decision (regime == trending)
            situation = np.where(computable, newhigh, reg.str.lower() == "trending")
            f = pd.to_numeric(d[fc_col], errors="coerce")
            part = pd.DataFrame({
                "coin": coin,
                "window": w,
                "pos": np.arange(len(d)),
                "forecast": f.values,
                "fwd": fwd.values,
                "situation": situation.astype(bool),
            })
            coin_parts.append(part)
        if not coin_parts:
            continue
        cp = pd.concat(coin_parts, ignore_index=True)
        coin_mean = cp["fwd"].mean(skipna=True)
        cp["excess"] = cp["fwd"] - coin_mean
        frames.append(cp)

    reading = ("Situation = close above each of its prior 20 closes in the same window "
               "(regime == 'trending' used where fewer than 20 prior closes exist), expected side long; "
               "coin mean = mean of all 10-bar forward returns of that coin pooled over windows; "
               "Newey-West lag 9 applied to pairs of new-high bars of the same coin-window at most 9 bars apart "
               "(Bartlett weights); thirds by forecast quantiles 1/3 and 2/3; non-overlapping events counted "
               "greedily per coin-window, an event at least 10 bars after the previous counted one.")

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "slope of 10-bar forward excess return on forecast",
                             "value": None, "statistic": None,
                             "threshold": "slope > 0 with Newey-West t >= 2 (confirm); slope < 0 with t <= -2 (reject)"},
            "supporting_check": None,
            "counts": {"non-overlapping new-high events": 0},
            "decided_by": "No bars in the record.",
            "reading": reading,
        }

    all_df = pd.concat(frames, ignore_index=True)

    # ---------- situation check ----------
    active = all_df["forecast"].notna() & (all_df["forecast"] != 0)
    n_active = int(active.sum())
    if n_active == 0:
        agreement = None
    else:
        ok = active & all_df["situation"] & (all_df["forecast"] > 0)
        agreement = float(ok.sum() / n_active)

    if agreement is not None and agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "slope of 10-bar forward excess return on forecast",
                             "value": None, "statistic": None,
                             "threshold": "slope > 0 with Newey-West t >= 2 (confirm); slope < 0 with t <= -2 (reject)"},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of nonzero-forecast bars are long bars at a new 20-day close high, "
                           "so the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    # ---------- sample: new-high bars (forecast > 0) with a forward return ----------
    s = all_df[(all_df["forecast"] > 0) & all_df["excess"].notna()].copy()
    s = s.sort_values(["coin", "window", "pos"]).reset_index(drop=True)

    # non-overlapping events count
    n_events = 0
    for _, g in s.groupby(["coin", "window"], sort=False):
        last = None
        for p in g["pos"].values:
            if last is None or p - last >= H:
                n_events += 1
                last = p
    counts = {"non-overlapping new-high events": int(n_events), "new-high bars": int(len(s))}

    threshold_txt = "slope > 0 with Newey-West t >= 2 (confirm); slope < 0 with t <= -2 (reject)"

    # ---------- regression with Newey-West ----------
    slope = None
    tstat = None
    if len(s) >= 3 and s["forecast"].nunique() > 1:
        x = s["forecast"].values.astype(float)
        y = s["excess"].values.astype(float)
        X = np.column_stack([np.ones_like(x), x])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ (X.T @ y)
        e = y - X @ beta
        S = np.zeros((2, 2))
        for _, g in s.groupby(["coin", "window"], sort=False):
            idx = g.index.values
            pos = g["pos"].values.astype(float)
            u = X[idx] * e[idx][:, None]
            dmat = np.abs(pos[:, None] - pos[None, :])
            wmat = np.where(dmat <= NW_LAG, 1.0 - dmat / (NW_LAG + 1.0), 0.0)
            S += u.T @ wmat @ u
        V = XtX_inv @ S @ XtX_inv
        slope = float(beta[1])
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        tstat = float(slope / se) if se and np.isfinite(se) and se > 0 else None

    # ---------- supporting check ----------
    diff = None
    if len(s) >= 3:
        q1, q2 = np.quantile(s["forecast"].values, [1.0 / 3.0, 2.0 / 3.0])
        top = s.loc[s["forecast"] >= q2, "excess"]
        bot = s.loc[s["forecast"] <= q1, "excess"]
        if len(top) > 0 and len(bot) > 0:
            diff = float(top.mean() - bot.mean())
    supp_passed = None if diff is None else bool(diff > 0)

    main = {"name": "slope of 10-bar forward excess return on forecast (new-high bars)",
            "value": slope,
            "statistic": None if tstat is None else {"name": "Newey-West t (lag 9)", "value": tstat},
            "threshold": threshold_txt}
    supp = {"name": "mean 10-bar excess return, top third minus bottom third of forecasts",
            "value": diff, "passed": supp_passed}

    # ---------- decision ----------
    if n_events < MIN_EVENTS:
        status = "not observable"
        decided = (f"Only {n_events} new-high events not overlapping within 10 bars, below the plan's "
                   f"minimum of {MIN_EVENTS}.")
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope or its t-stat could not be computed, so neither confirm nor reject is met."
    elif slope > 0 and tstat >= 2 and diff is not None and diff > 0:
        status = "confirmed"
        decided = "Slope positive with t >= 2 and top-minus-bottom-third difference positive (confirm rule)."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "Slope negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        if -2 < tstat < 2:
            decided = "Slope t-stat between -2 and 2 (inconclusive rule)."
        else:
            decided = ("Slope positive with t >= 2 but the top-minus-bottom-third difference is not positive, "
                       "so neither confirm nor reject is met.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True if agreement is not None else False},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
