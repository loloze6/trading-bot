import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10

    # ---------- helpers ----------
    def comp_series(df, cid, field):
        col = f"debug_info.components.{cid}.{field}"
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        if "debug_info.components" in df.columns:
            def ext(v):
                try:
                    if isinstance(v, dict):
                        c = v.get(cid)
                        if isinstance(c, dict):
                            x = c.get(field)
                            return float(x) if x is not None else np.nan
                except Exception:
                    return np.nan
                return np.nan
            return df["debug_info.components"].apply(ext).astype(float)
        return pd.Series(np.nan, index=df.index)

    def is_trending(df):
        return df["regime"].astype(str).str.strip().str.lower() == "trending"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = f != 0
            if not active.any():
                continue
            trend = is_trending(df)
            # graded range position (centred, positive near the 20-day high)
            rng = comp_series(df, "range20", "post_pipeline_value")
            rng_raw = comp_series(df, "range20", "last_history_value")
            rng = rng.where(rng.notna(), rng_raw)
            # extension penalty (>= 0, subtracted)
            ext = comp_series(df, "ext30", "post_pipeline_value")
            ext = ext.fillna(0.0).clip(lower=0.0)
            score = 1.0 * rng - 0.5 * ext
            # expected side: long where the graded score is positive (near highs, not extended)
            exp_sign = np.sign(score)
            agree = trend & rng.notna() & (np.sign(f) == exp_sign) & (exp_sign != 0)
            n_active += int(active.sum())
            n_agree += int((agree & active).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of active bars are trending-regime bars whose forecast sign matches "
                           "the graded situation (long near the 20-day high, cut by the 30-day extension), "
                           "so the config does not do what the Fidelity says."
                           if n_active > 0 else "No active bars: the forecast is never non-zero."),
            "reading": ("Situation = regime 'trending' (close >= 200-day SMA) and sign of the graded score "
                        "range20 - 0.5*ext30 (post-pipeline values, raw as fallback) gives the expected side."),
        }

    # ---------- 2. main measure ----------
    xs, ys_raw, coins_rows = [], [], []
    coin_grid_rets = {}
    for coin, wins in bars.items():
        all_r = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            trend = is_trending(df).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                all_r.append(r)
                if trend[i] and np.isfinite(f[i]):
                    xs.append(float(f[i]))
                    ys_raw.append(r)
                    coins_rows.append(coin)
        coin_grid_rets[coin] = float(np.mean(all_r)) if all_r else np.nan

    ys = np.array([ys_raw[k] - coin_grid_rets[coins_rows[k]] for k in range(len(ys_raw))], dtype=float)
    xs = np.array(xs, dtype=float)
    ok = np.isfinite(xs) & np.isfinite(ys)
    xs, ys = xs[ok], ys[ok]
    n_cases = int(len(xs))

    slope, t_slope = None, None
    if n_cases >= 3 and np.std(xs) > 0:
        res = stats.linregress(xs, ys)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    # ---------- 3. supporting check: timing gain ----------
    coin_mean_daily = {}
    for coin, wins in bars.items():
        rr = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            r = (c / c.shift(1) - 1.0).dropna()
            rr.extend(r.tolist())
        coin_mean_daily[coin] = float(np.mean(rr)) if rr else np.nan

    book_parts, mkt_parts = [], []
    for coin, wins in bars.items():
        mu = coin_mean_daily[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            day = ts.dt.floor("D")
            v = pd.to_numeric(df["postRebalance_total_value"], errors="coerce")
            a = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            tmp = pd.DataFrame({"day": day, "v": v, "a": a})
            g = tmp.groupby("day", sort=True).last()
            br = g["v"] / g["v"].shift(1) - 1.0
            mg = g["a"].shift(1) * mu
            d = pd.DataFrame({"book": br, "mkt": mg}).dropna()
            if len(d):
                d["coin"] = coin
                book_parts.append(d)
    timing = None
    if book_parts:
        allb = pd.concat(book_parts)
        daily = allb.groupby(level=0)[["book", "mkt"]].mean()
        timing = float(daily["book"].mean() - daily["mkt"].mean())
    timing_pass = (timing is not None and timing > 0)

    # ---------- 4. decision ----------
    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} independent trending-bar cases, fewer than the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed with at least 100 cases."
    elif t_slope >= 2 and timing_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more with at least 100 independent cases, and the timing gain is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less with at least 100 independent cases."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the timing gain is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "OLS slope of forward 10-bar return minus coin mean on forecast, trending bars",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": "t >= 2 confirms (with timing gain > 0), t <= -2 rejects, with at least 100 independent cases",
        },
        "supporting_check": {
            "name": "timing gain (book mean daily return minus market-rise gain), before costs",
            "value": timing,
            "passed": (bool(timing_pass) if timing is not None else None),
        },
        "counts": {"independent cases": n_cases},
        "decided_by": decided,
        "reading": ("Trending bars are those with regime 'trending' at grid positions 0,10,20,... of each window "
                    "with a full 10-bar forward return inside the window; the coin's mean 10-bar return is the mean "
                    "over the same non-overlapping grid of all bars in all windows; the slope's t is the OLS t with an "
                    "intercept on pooled coins; the side check uses the sign of range20 - 0.5*ext30 on trending bars."),
    }
