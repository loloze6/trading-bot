import numpy as np
import pandas as pd


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        mx = float(np.nanmax(np.abs(s.values))) if len(s) else 0.0
        unit = "ns" if mx > 1e17 else ("us" if mx > 1e14 else ("ms" if mx > 1e11 else "s"))
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    RAW = "debug_info.components.scaled_fall.last_history_value"
    rows = []
    coin_rets = {}

    for coin, wins in bars.items():
        rets_all = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            ret_prev = close / close.shift(1) - 1.0          # inside this window only
            ret_next = close.shift(-1) / close - 1.0         # inside this window only
            rets_all.append(ret_next.dropna().values)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            # the one-day fall: sign of the recorded vol-scaled 1-bar return, else the price return
            fall = np.where(raw.notna(), raw < 0, ret_prev < 0)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)
            day = _to_utc(d["timestamp"]).dt.floor("D").dt.strftime("%Y-%m-%d").values
            rows.append(pd.DataFrame({
                "coin": coin, "window": w, "day": day,
                "forecast": fc.values, "ret_next": ret_next.values,
                "fall": fall.astype(bool),
                "profile": (regime == "unknown").values,
            }))
        if rets_all:
            allr = np.concatenate(rets_all)
            coin_rets[coin] = float(np.nanmean(allr)) if len(allr) else np.nan

    if not rows:
        data = pd.DataFrame(columns=["coin", "window", "day", "forecast", "ret_next", "fall", "profile"])
    else:
        data = pd.concat(rows, ignore_index=True)

    main_name = "slope of excess next-day return on the forecast, bars with forecast > 0"
    thr = "confirm if slope t >= 2 and top-third check passes; reject if slope t <= -2"
    stat_name = "t of the OLS slope, day-clustered (CR1)"
    reading = ("The falling, agitated profile is read as the bars whose regime is 'unknown' (both chop vetoes off), "
               "the fall as the recorded raw scaled return (else the price return) below zero, the expected side long; "
               "cases are bars with forecast > 0 and a next-day close in the same window; the coin's mean daily return is "
               "the pooled mean of all its in-window close-to-close returns; the slope's t uses a CR1 day-clustered "
               "standard error; the top third is the positive forecasts at or above their 2/3 quantile; the plan's "
               "minimum counts, when not reached, give 'not observable'.")

    # ---- situation check
    active = data[(data["forecast"].fillna(0) != 0)]
    n_active = len(active)
    if n_active > 0:
        ok = active["profile"] & active["fall"] & (active["forecast"] > 0)
        agreement = float(ok.mean())
        passed = agreement >= 0.9
    else:
        agreement, passed = None, True

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are long bars on a one-day fall inside the falling, "
                           "agitated profile (regime 'unknown'), as the Fidelity requires."),
            "reading": reading,
        }

    # ---- cases
    cases = data[(data["forecast"] > 0) & data["ret_next"].notna()].copy()
    cases["excess"] = cases["ret_next"] - cases["coin"].map(coin_rets)
    cases = cases[cases["excess"].notna()]
    n_bars = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_bars else 0
    counts = {"bars with forecast > 0": n_bars, "distinct days": n_days}

    slope = None
    t_slope = None
    if n_bars >= 3 and cases["forecast"].nunique() > 1:
        x = cases["forecast"].values.astype(float)
        y = cases["excess"].values.astype(float)
        X = np.column_stack([np.ones_like(x), x])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in pd.Series(np.arange(n_bars)).groupby(cases["day"].values):
            g = X[idx.values].T @ e[idx.values]
            meat += np.outer(g, g)
        G = n_days
        k = 2
        corr = (G / (G - 1.0)) * ((n_bars - 1.0) / (n_bars - k)) if G > 1 and n_bars > k else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        slope = float(beta[1])
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        t_slope = float(slope / se) if np.isfinite(se) and se > 0 else None

    top_mean = None
    top_pass = None
    if n_bars > 0:
        q = cases["forecast"].quantile(2.0 / 3.0)
        top = cases[cases["forecast"] >= q]
        if len(top):
            top_mean = float(top["excess"].mean())
            top_pass = bool(top_mean > 0)
    counts["bars in top third"] = int(len(top)) if n_bars > 0 else 0

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": stat_name, "value": t_slope} if t_slope is not None else None),
            "threshold": thr}
    supp = {"name": "mean excess next-day return, top third of positive forecasts",
            "value": top_mean, "passed": top_pass}

    if n_bars < 30 or n_days < 20:
        status = "not observable"
        decided = (f"The plan's minimum of 30 bars with forecast > 0 on at least 20 distinct days is not reached "
                   f"({n_bars} bars, {n_days} days).")
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and top_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the top-third mean excess return is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the top-third check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
