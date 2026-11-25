import numpy as np
import pandas as pd


def _component_col(df, cid, field="last_history_value"):
    name = "debug_info.components.%s.%s" % (cid, field)
    if name in df.columns:
        return pd.to_numeric(df[name], errors="coerce")
    if "debug_info.components" in df.columns:
        def get(x):
            try:
                if isinstance(x, dict):
                    v = x.get(cid, {})
                    if isinstance(v, dict):
                        return v.get(field, np.nan)
            except Exception:
                pass
            return np.nan
        return pd.to_numeric(df["debug_info.components"].map(get), errors="coerce")
    return pd.Series(np.nan, index=df.index)


def _short_bets(f):
    """Bars where the short forecast deepens by >= 2 points from its shallowest level since the last bet."""
    bets = np.zeros(len(f), dtype=bool)
    ref = 0.0
    for i, v in enumerate(f):
        if not np.isfinite(v) or v >= 0:
            ref = 0.0
            continue
        m = -v
        ref = min(ref, m)
        if m - ref >= 2.0 - 1e-12:
            bets[i] = True
            ref = m
    return bets


def measure(bars):
    H = 7
    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            ret = close.pct_change()
            vol = ret.rolling(30, min_periods=30).std()
            volr = vol / vol.rolling(60, min_periods=60).mean()
            diff_abs = close.diff().abs().rolling(30, min_periods=30).sum()
            er = (close - close.shift(30)).abs() / diff_abs
            computed = volr.notna() & er.notna()
            reg_from_prices = (volr >= 1.0) & (er >= 0.3)
            reg_recorded = df["regime"].astype(str).eq("mean_reversion") if "regime" in df.columns \
                else pd.Series(False, index=df.index)
            regime_on = np.where(computed, reg_from_prices, reg_recorded)
            rise = _component_col(df, "rise")
            rise_ok = rise.isna() | (rise > 0)
            active = fc != 0
            agree = active & pd.Series(regime_on, index=df.index).astype(bool) & (fc < 0) & rise_ok
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    reading = ("Situation recomputed from prices (30-day std of daily returns, ddof 1, over its 60-bar mean including "
               "the bar, >= 1, and 30-day Kaufman ER >= 0.3), falling back to the recorded regime on bars whose history "
               "lacks the warm-up, with a short forecast and a positive raw rise where recorded; a case is the first short "
               "bet (forecast deepening >= 2 points from its shallowest level since the last bet) in each 7-bar grid cell, "
               "its return taken from that bar's close over 7 bars inside the window, drift = mean of non-overlapping "
               "7-bar grid returns over all the coin's windows, t clustered by calendar day.")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars in the plan's agitated, "
                          "steady-progress regime (30-day vol >= its 60-day mean and ER >= 0.3).",
            "reading": reading,
        }

    # ---------- criterion ----------
    rows = []
    for coin in sorted(bars):
        grid_rets = []
        coin_cases = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            bets = _short_bets(fc)
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bets[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                coin_cases.append((ts.iloc[i].floor("D"), r, abs(fc[i])))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for d, r, af in coin_cases:
            rows.append((d, -(r - drift), af))

    n_cases = len(rows)
    days = len(set(r[0] for r in rows))
    counts = {"cases": n_cases, "days": days}
    mean_u = None
    t = None
    slope = None
    if n_cases > 0:
        cdf = pd.DataFrame(rows, columns=["day", "u", "af"])
        mean_u = float(cdf["u"].mean())
        dev = cdf["u"] - mean_u
        s = dev.groupby(cdf["day"]).sum().values
        D = len(s)
        if D > 1:
            var = (D / (D - 1.0)) * float(np.sum(s ** 2)) / (n_cases ** 2)
            se = np.sqrt(var)
            t = float(mean_u / se) if se > 0 else None
        if n_cases > 1 and cdf["af"].var() > 0:
            slope = float(np.polyfit(cdf["af"].values, cdf["u"].values, 1)[0])

    slope_pass = None if slope is None else bool(slope > 0)
    main = {
        "name": "mean unusual 7-bar move of short cases (short direction)",
        "value": mean_u,
        "statistic": {"name": "t of the mean, cases summed per day", "value": t} if t is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 over >= 30 cases (and slope > 0); reject: mean < 0 with t <= -2 over >= 30 cases",
    }
    support = {"name": "OLS slope of unusual move on |forecast|", "value": slope, "passed": slope_pass}

    if n_cases < 30:
        status = "not observable"
        decided = "Fewer than 30 cases (the plan's minimum count) were found."
    elif t is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t >= 2 and slope_pass:
        status = "confirmed"
        decided = "Mean unusual move positive with t >= 2 over at least 30 cases, and the slope on |forecast| is positive."
    elif mean_u > 0 and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope of the unusual move on |forecast| is not positive."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
