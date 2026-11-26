import numpy as np
import pandas as pd

RAW = "debug_info.components.rise_sd.last_history_value"


def _prep(df):
    df = df.sort_values("timestamp").reset_index(drop=True).copy()
    df["ts"] = pd.to_datetime(df["timestamp"], utc=True)
    df["day"] = df["ts"].dt.floor("D")
    c = df["close"].astype(float)
    df["ret1"] = c / c.shift(1) - 1.0
    sd = df["ret1"].rolling(30, min_periods=30).std(ddof=1)
    df["rise_sd_px"] = df["ret1"] / sd.replace(0, np.nan)
    df["hi20"] = c.rolling(20, min_periods=20).max()
    df["dist20"] = c / df["hi20"] - 1.0
    df["fwd5"] = c.shift(-5) / c - 1.0
    df["f"] = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
    raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
    df["raw"] = raw
    df["rise_any"] = raw.where(raw.notna(), df["rise_sd_px"])
    df["cell"] = np.arange(len(df)) // 5
    return df


def _bets(f, band=2.0):
    out = np.zeros(len(f), dtype=bool)
    low = 0.0
    for i, v in enumerate(f):
        if v <= 0:
            low = 0.0
            continue
        if v - low >= band:
            out[i] = True
            low = v
        else:
            low = min(low, v)
    return out


def _clustered_slope(x, y, g):
    x = np.asarray(x, float); y = np.asarray(y, float)
    X = np.column_stack([np.ones_like(x), x])
    n, k = X.shape
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    u = y - X @ beta
    meat = np.zeros((k, k))
    groups = pd.Series(np.arange(n)).groupby(pd.Series(g).values)
    G = 0
    for _, idx in groups:
        idx = idx.values
        s = X[idx].T @ u[idx]
        meat += np.outer(s, s)
        G += 1
    if G < 2 or n <= k:
        return float(beta[1]), None
    corr = (G / (G - 1.0)) * ((n - 1.0) / (n - k))
    V = corr * XtX_inv @ meat @ XtX_inv
    se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
    t = float(beta[1] / se) if np.isfinite(se) and se > 0 else None
    return float(beta[1]), t


def measure(bars):
    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    prepped = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = _prep(df)
            prepped[(coin, w)] = d
            act = d["f"] != 0
            ok = act & d["hi20"].notna() & d["rise_any"].notna()
            sit = (d["close"].astype(float) >= d["hi20"] * (1 - 1e-9)) & (d["rise_any"] > 0)
            if "regime" in d.columns:
                sit = sit & (d["regime"].astype(str) != "chop")
            n_active += int(ok.sum())
            n_agree += int((ok & sit & (d["f"] > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation = close equal to the highest of the last 20 closes (today included, bars with fewer than 20 "
               "closes in the window left out) with a positive raw rise_sd (recomputed from prices where not recorded) "
               "outside the 'chop' profile regime, side long; a case is the first bet (forecast rise >= 2 from its low on "
               "the long side since the last bet) in each 5-bar grid cell of a window, with its 5-bar return from that bar; "
               "the coin's mean 5-day return uses the non-overlapping grid of all its windows; t uses day-clustered "
               "sandwich errors with the CR1 small-sample factor; the far-below rises are, inside non-'chop' bars, "
               "positive rises with recomputed 30-day-std size within [min, max] of the cases' raw sizes and close <= 95% "
               "of the 20-day closing high, read once per grid cell; the plan's 'fewer than 30 cases/days' is reported "
               "as not observable.")

    if agreement is not None and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "OLS slope of 5-day excess return on case forecast", "value": None,
                             "statistic": None, "threshold": "slope > 0 with day-clustered t >= 2"},
            "supporting_check": None,
            "counts": {"cases": None, "distinct days": None},
            "decided_by": "Fewer than 90% of active bars are long bars on a 20-day closing high with a rise, which the "
                          "plan's Fidelity says the book should be on.",
            "reading": reading,
        }

    # ---------- coin mean 5-day return ----------
    coin_rets = {}
    for (coin, w), d in prepped.items():
        grid = d.iloc[::5]["fwd5"].dropna()
        coin_rets.setdefault(coin, []).extend(grid.tolist())
    coin_mean = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in coin_rets.items()}

    # ---------- cases ----------
    cases = []
    for (coin, w), d in prepped.items():
        b = _bets(d["f"].values)
        d = d.assign(bet=b)
        sel = d[d["bet"]].groupby("cell").head(1)
        for _, r in sel.iterrows():
            if pd.isna(r["fwd5"]) or not np.isfinite(coin_mean.get(coin, np.nan)):
                continue
            cases.append({"coin": coin, "day": r["day"], "f": float(r["f"]),
                          "ex": float(r["fwd5"] - coin_mean[coin]),
                          "size": float(r["rise_any"]) if pd.notna(r["rise_any"]) else np.nan})
    cdf = pd.DataFrame(cases, columns=["coin", "day", "f", "ex", "size"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    slope, t = (None, None)
    if n_cases >= 3 and cdf["f"].nunique() > 1:
        slope, t = _clustered_slope(cdf["f"].values, cdf["ex"].values, cdf["day"].astype(str).values)

    # ---------- supporting check ----------
    diff = None
    n_far = 0
    sizes = cdf["size"].dropna() if n_cases else pd.Series(dtype=float)
    if n_cases and len(sizes):
        lo, hi = float(sizes.min()), float(sizes.max())
        far = []
        for (coin, w), d in prepped.items():
            if not np.isfinite(coin_mean.get(coin, np.nan)):
                continue
            m = (d["ret1"] > 0) & d["rise_sd_px"].between(lo, hi) & (d["dist20"] <= -0.05) & d["fwd5"].notna()
            if "regime" in d.columns:
                m = m & (d["regime"].astype(str) != "chop")
            s = d[m].groupby("cell").head(1)
            far.extend((s["fwd5"] - coin_mean[coin]).tolist())
        n_far = len(far)
        if n_far:
            diff = float(cdf["ex"].mean() - np.mean(far))
    sup_passed = None if diff is None else bool(diff > 0)

    counts = {"cases": n_cases, "distinct days": n_days, "far-below rises": n_far}
    main = {"name": "OLS slope of 5-day excess return on case forecast",
            "value": slope,
            "statistic": {"name": "day-clustered t", "value": t} if t is not None else None,
            "threshold": "confirm: slope > 0 with t >= 2 (and supporting difference > 0); reject: slope < 0 with t <= -2"}
    sup = {"name": "mean 5-day excess: cases minus far-below rises", "value": diff, "passed": sup_passed}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = "The plan's minimum of 30 cases on 30 distinct days is not reached."
    elif t is None or slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the supporting difference is greater than 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting difference is not greater than 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's |t| is below 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
