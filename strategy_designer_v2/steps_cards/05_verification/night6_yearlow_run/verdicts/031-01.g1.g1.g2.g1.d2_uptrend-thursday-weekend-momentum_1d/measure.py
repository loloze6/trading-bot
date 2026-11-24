import numpy as np
import pandas as pd


def measure(bars):
    H = 2
    FC = "forecast"
    PPV = "debug_info.components.rise14.post_pipeline_value"

    def to_utc(ts):
        t = pd.to_datetime(ts, utc=True, errors="coerce")
        return t

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    frames = {}
    for coin, wins in bars.items():
        frames[coin] = {}
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["_ts"] = to_utc(d["timestamp"])
            d["_close"] = pd.to_numeric(d["close"], errors="coerce")
            d["_fc"] = pd.to_numeric(d[FC], errors="coerce") if FC in d.columns else np.nan
            # Thursday-close bar: the bar opening on Thursday (UTC), the next bar is a Friday
            d["_thu"] = d["_ts"].dt.dayofweek == 3
            # close 60 days earlier, looked up by timestamp inside the same window
            m = pd.Series(d["_close"].values, index=d["_ts"].values)
            m = m[~m.index.duplicated(keep="last")]
            past_ts = (d["_ts"] - pd.Timedelta(days=60)).values
            past = m.reindex(past_ts).values
            d["_past60"] = past
            d["_up60"] = d["_close"].values > past
            d["_up60_known"] = ~pd.isna(past)
            frames[coin][w] = d

            act = d["_fc"].notna() & (d["_fc"] != 0)
            known = act & d["_up60_known"]
            n_active_uncomputable += int((act & ~d["_up60_known"]).sum())
            n_active += int(known.sum())
            ok = known & d["_thu"] & d["_up60"] & (d["_fc"] > 0)
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("Thursday-close bars are the bars whose UTC start is a Thursday (next bar a Friday); the 60-day uptrend "
               "is close above the close of the bar 60 days earlier in the same window, and active bars where that "
               "bar is not in the window are left out of the agreement; the coin's mean 2-bar return uses the "
               "non-overlapping grid 0,2,4,... of every window; cases are pooled over all coins with an OLS slope "
               "(with intercept) whose t uses a cluster-by-day robust variance with the usual G/(G-1)(N-1)/(N-K) "
               "correction; the plan's minimum counts, read on cases with forecast above 0, give 'not observable' "
               "when unmet.")

    main_name = "OLS slope of 2-bar excess return on rise14 post_pipeline_value, uptrend Thursday cases"
    threshold = "slope t >= 2 (with forecast-weighted mean excess > 0) confirms; slope t <= -2 rejects"
    sup_name = "forecast-weighted mean 2-bar excess return > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long on Thursday-close bars "
                           "above their close of 60 days earlier, so the config does not trade the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in frames.items():
        # coin's mean 2-bar return over all windows, non-overlapping grid
        grid_rets = []
        for w, d in wins.items():
            c = d["_close"].values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        if len(grid_rets) == 0:
            continue
        mu = float(np.mean(grid_rets))
        for w, d in wins.items():
            fwd = d["_close"].shift(-H) / d["_close"] - 1.0
            reg = d["regime"].astype(str) == "trending" if "regime" in d.columns else pd.Series(False, index=d.index)
            sel = d["_thu"] & reg
            x = pd.to_numeric(d[PPV], errors="coerce") if PPV in d.columns else pd.Series(np.nan, index=d.index)
            sub = pd.DataFrame({
                "day": d["_ts"].dt.normalize(),
                "x": x,
                "y": fwd - mu,
                "f": d["_fc"],
            })[sel]
            sub = sub.dropna(subset=["x", "y", "f", "day"])
            if len(sub):
                rows.append(sub)

    if rows:
        C = pd.concat(rows, ignore_index=True)
    else:
        C = pd.DataFrame(columns=["day", "x", "y", "f"])

    n_cases = int(len(C))
    pos = C[C["f"] > 0] if n_cases else C
    n_pos = int(len(pos))
    n_pos_days = int(pos["day"].nunique()) if n_pos else 0
    n_days_all = int(C["day"].nunique()) if n_cases else 0

    counts = {
        "uptrend Thursday cases with forecast above 0": n_pos,
        "distinct Thursdays of those cases": n_pos_days,
        "uptrend Thursday cases (all, incl. forecast 0)": n_cases,
        "distinct days (clusters)": n_days_all,
    }

    # slope with cluster-by-day t
    slope = None
    tval = None
    if n_cases >= 3 and C["x"].nunique() > 1 and n_days_all >= 2:
        X = np.column_stack([np.ones(n_cases), C["x"].values.astype(float)])
        y = C["y"].values.astype(float)
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in C.groupby("day").indices.items():
            s = X[idx].T @ u[idx]
            meat += np.outer(s, s)
        G = n_days_all
        N, K = n_cases, 2
        corr = (G / (G - 1.0)) * ((N - 1.0) / (N - K)) if N > K else np.nan
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        tval = float(slope / se) if np.isfinite(se) and se > 0 else None

    # forecast-weighted mean excess
    wmean = None
    if n_cases:
        sf = float(C["f"].sum())
        if sf != 0:
            wmean = float((C["y"] * C["f"]).sum() / sf)
    sup_pass = None if wmean is None else bool(wmean > 0)

    main = {"name": main_name, "value": slope,
            "statistic": None if tval is None else {"name": "slope t, clustered by day", "value": tval},
            "threshold": threshold}
    sup = {"name": sup_name, "value": wmean, "passed": sup_pass}
    sc = {"agreement": None if agreement is None else float(agreement), "passed": True}

    if n_pos < 100 or n_pos_days < 60:
        status = "not observable"
        decided = (f"The plan's minimum is not reached: {n_pos} uptrend Thursday cases with a forecast above 0 "
                   f"(100 needed) over {n_pos_days} distinct Thursdays (60 needed).")
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm rule met: the slope's t is 2 or more and the forecast-weighted mean excess return is above 0."
    elif tval >= 2:
        status = "inconclusive"
        decided = ("Inconclusive rule met: the slope's t is 2 or more but the forecast-weighted mean excess return "
                   "is 0 or below.")
    elif tval <= -2:
        status = "rejected"
        decided = "Reject rule met: the slope's t is -2 or less."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule met: the slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
