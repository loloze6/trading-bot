import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.oc_drop.last_history_value"
    PROFILE_REGIME = "unknown"  # the regime that is not vetoed: trend < -10 and vol percentile > 0.5

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    coin_frames = {}
    for coin, wins in bars.items():
        frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            d["window"] = str(w)
            d["fwd"] = d["close"].shift(-1) / d["close"] - 1.0  # inside the window only
            frames.append(d)
        if not frames:
            continue
        coin_frames[coin] = frames
        for d in frames:
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            in_prof = d["regime"].astype(str) == PROFILE_REGIME
            drop_price = np.where(d["close"] < d["open"],
                                  (d["open"] - d["close"]) / d["open"] * 100.0, 0.0)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                drop = raw.where(raw.notna(), pd.Series(drop_price, index=d.index))
            else:
                drop = pd.Series(drop_price, index=d.index)
            situation = in_prof & (drop > 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "OLS slope of next-day excess return on forecast (day-clustered t)"
    thr = "confirm: t >= 2 with forecast-weighted mean excess > 0; reject: t <= -2"
    sup_name = "forecast-weighted mean excess return of cases > 0"
    reading_base = ("Profile bars are those with regime 'unknown' (not vetoed to chop); the drop is the "
                    "recorded raw oc_drop value, recomputed from open/close where missing; the coin's mean "
                    "daily return is the mean of all its within-window 1-bar returns; cluster-robust SE "
                    "uses the usual G/(G-1)*(N-1)/(N-K) correction; days are UTC dates of the bar; the "
                    "plan's minimum counts give 'not observable' when unmet.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are in-profile down days "
                           "with a long forecast, as the plan's situation requires."),
            "reading": reading_base,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, frames in coin_frames.items():
        allret = pd.concat([d["fwd"] for d in frames]).dropna()
        mu = float(allret.mean()) if len(allret) else np.nan
        for d in frames:
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            in_prof = d["regime"].astype(str) == PROFILE_REGIME
            m = in_prof & (fc > 0) & d["fwd"].notna()
            if m.any():
                sub = pd.DataFrame({
                    "f": fc[m].astype(float).values,
                    "ex": (d.loc[m, "fwd"] - mu).astype(float).values,
                    "day": d.loc[m, "timestamp"].dt.strftime("%Y-%m-%d").values,
                })
                rows.append(sub)
    cases = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(columns=["f", "ex", "day"])
    cases = cases.dropna()
    n = int(len(cases))
    n_days = int(cases["day"].nunique()) if n else 0
    counts = {"cases": n, "distinct days": n_days}

    slope = None
    tval = None
    wmean = None
    if n >= 3 and cases["f"].nunique() > 1:
        X = np.column_stack([np.ones(n), cases["f"].values])
        y = cases["ex"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in cases.groupby("day").indices.items():
            s = X[idx].T @ u[idx]
            meat += np.outer(s, s)
        G = n_days
        k = 2
        corr = (G / (G - 1)) * ((n - 1) / (n - k)) if G > 1 and n > k else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        tval = float(slope / se) if se and np.isfinite(se) and se > 0 else None
    if n > 0 and cases["f"].sum() > 0:
        wmean = float((cases["ex"] * cases["f"]).sum() / cases["f"].sum())
    sup_pass = None if wmean is None else bool(wmean > 0)

    if n < 100 or n_days < 50:
        status = "not observable"
        decided = (f"The plan's minimum counts are not reached ({n} cases, need 100; "
                   f"{n_days} distinct days, need 50).")
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope has a t of 2 or more and the forecast-weighted mean excess return is above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope has a t of -2 or less."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope t is 2 or more but the forecast-weighted mean excess return is 0 or below."
    else:
        status = "inconclusive"
        decided = "The slope t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tval is None else {"name": "day-clustered t of the slope", "value": tval},
            "threshold": thr,
        },
        "supporting_check": {"name": sup_name, "value": wmean, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
