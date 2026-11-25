import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LH = "debug_info.components.low_close.last_history_value"
    PP = "debug_info.components.low_close.post_pipeline_value"

    reading = ("The detector's MeanBarRangeRatio is recomputed from prices as the 90-bar mean of (high-low)/close "
               "over its 30-bar mean, inside each window, and where fewer than 90 bars of the window exist the "
               "recorded regime stands in for it; the close sits low when (high-close)/(high-low) > 0; the coin's "
               "mean daily return is the mean of all its 1-bar returns over all windows; the slope's t is the OLS "
               "slope with standard errors clustered by UTC day; regime bars are those with regime "
               "'mean_reversion' and a next-day return in the window; thirds are cut by forecast rank.")

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    rows = []
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            all_rets.append((c.shift(-1) / c - 1).iloc[:-1].dropna())
        coin_mean = float(pd.concat(all_rets).mean()) if all_rets else np.nan

        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            h = df["high"].astype(float)
            l = df["low"].astype(float)
            c = df["close"].astype(float)
            rng = h - l
            loc_px = np.where(rng > 0, (h - c) / rng.replace(0, np.nan), 0.0)
            loc_px = pd.Series(loc_px, index=df.index).fillna(0.0)
            if LH in df.columns:
                loc = df[LH].astype(float).where(df[LH].notna(), loc_px)
            else:
                loc = loc_px
            rel = rng / c
            ratio = rel.rolling(90, min_periods=90).mean() / rel.rolling(30, min_periods=30).mean()
            reg_rec = df["regime"].astype(str) == "mean_reversion"
            wide = np.where(ratio.notna(), ratio < 1.0, reg_rec)
            situ = pd.Series(wide, index=df.index).astype(bool) & (loc > 0)

            fc = df["forecast"].astype(float).fillna(0.0)
            act = fc != 0
            n_active += int(act.sum())
            n_agree += int((act & situ & (fc > 0)).sum())

            nxt = c.shift(-1) / c - 1
            if PP in df.columns:
                f = df[PP].astype(float)
            else:
                f = pd.Series(np.nan, index=df.index)
            day = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D")
            sub = pd.DataFrame({
                "coin": coin, "window": w, "ts": pd.to_datetime(df["timestamp"], utc=True),
                "day": day, "f": f, "y": nxt - coin_mean, "reg": reg_rec,
            })
            sub = sub[sub["reg"] & sub["f"].notna() & sub["y"].notna()]
            rows.append(sub)

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    sit = {"agreement": float(agreement), "passed": passed}

    main_name = "OLS slope of next-day excess return on low_close forecast, regime bars"
    thr = "confirm: slope > 0 with t >= 2 and top-minus-bottom third > 0; reject: slope < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of the active bars are long bars of the plan's situation (close below "
                           "the high in a 30-day range wider than the 90-day one), under the 90 % needed."),
            "reading": reading,
        }

    data = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(columns=["f", "y", "day"])
    n_bars = int(len(data))
    n_days = int(data["day"].nunique()) if n_bars else 0
    counts = {"regime bars": n_bars, "distinct days": n_days}

    if n_bars < 300 or n_days < 150:
        return {
            "status": "not observable",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "The plan's minimum of 300 regime bars on at least 150 distinct days is not reached.",
            "reading": reading,
        }

    x = data["f"].to_numpy(float)
    y = data["y"].to_numpy(float)
    X = np.column_stack([np.ones_like(x), x])
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    e = y - X @ beta
    codes, _ = pd.factorize(data["day"])
    G = int(codes.max()) + 1
    scores = np.zeros((G, 2))
    np.add.at(scores, codes, X * e[:, None])
    meat = scores.T @ scores
    N, K = X.shape
    corr = (G / (G - 1)) * ((N - 1) / (N - K)) if G > 1 and N > K else 1.0
    V = corr * XtX_inv @ meat @ XtX_inv
    se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
    slope = float(beta[1])
    t = float(slope / se) if se and np.isfinite(se) and se > 0 else 0.0

    d = data.sort_values(["f", "coin", "window", "ts"], kind="mergesort").reset_index(drop=True)
    terc = pd.qcut(np.arange(len(d)), 3, labels=False)
    top = d.loc[terc == 2, "y"].mean()
    bot = d.loc[terc == 0, "y"].mean()
    diff = float(top - bot)
    sup_pass = bool(diff > 0)
    sup = {"name": "mean excess next-day return, top third minus bottom third of forecasts",
           "value": diff, "passed": sup_pass}

    if slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        dec = "The slope is positive with t >= 2 and the top-minus-bottom-third difference is above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        dec = "The slope is negative with t <= -2."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        dec = "The slope is positive with t >= 2 but the top-minus-bottom-third difference is 0 or below."
    else:
        status = "inconclusive"
        dec = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "t of OLS slope, SE clustered by day", "value": t},
                         "threshold": thr},
        "supporting_check": sup,
        "counts": counts,
        "decided_by": dec,
        "reading": reading,
    }
