import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    UP = "debug_info.components.move_up.last_history_value"
    DN = "debug_info.components.move_down.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: the 72-bar move is non-zero (either sign). Side: long, so forecast > 0.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(float)
            # Raw 72-bar return: recorded component value, with the prices as fallback.
            price_r = np.full(len(df), np.nan)
            if len(df) > H:
                price_r[H:] = close[H:] / close[:-H] - 1.0
            raw = np.full(len(df), np.nan)
            for col in (UP, DN):
                if col in df.columns:
                    v = pd.to_numeric(df[col], errors="coerce").to_numpy(float)
                    raw = np.where(np.isnan(raw), v, raw)
            raw = np.where(np.isnan(raw), price_r, raw)
            active = np.isfinite(fc) & (fc != 0)
            situ = np.isfinite(raw) & (raw != 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = agreement >= 0.9

    main_name = "slope t of 72-bar forward excess return on forecast (pooled, sampled bars 0,72,...)"
    threshold = "confirm: slope > 0 with t >= 2 and timing part > 0; reject: slope < 0 with t <= -2; else inconclusive; at least 500 sampled cases"
    sup_name = "book mean daily return minus gain from the market's own rise (timing part) > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"independent sampled cases": 0, "active bars": int(n_active)},
            "decided_by": f"only {agreement:.1%} of the active bars (forecast != 0) have a non-zero 72-bar move with a long forecast, below the 90% the plan's long lean on |3-day move| requires.",
            "reading": "situation = non-zero 72-bar return (raw component value, prices as fallback), expected side = long (forecast > 0).",
        }

    # ---------- 2. Main measure ----------
    xs, rets, coins_l = [], [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(float)
            for i in range(0, len(df) - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r) and np.isfinite(fc[i]):
                    xs.append(fc[i]); rets.append(r); coins_l.append(coin)
    samp = pd.DataFrame({"coin": coins_l, "x": xs, "r": rets})
    n_cases = int(len(samp))

    slope, tval = None, None
    if n_cases >= 3:
        samp["ex"] = samp["r"] - samp.groupby("coin")["r"].transform("mean")
        x = samp["x"].to_numpy(float); y = samp["ex"].to_numpy(float)
        if np.var(x) > 0:
            lr = stats.linregress(x, y)
            slope = float(lr.slope)
            tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- 3. Supporting check: timing part of the book ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            date = ts.dt.floor("D")
            val = pd.to_numeric(d["postRebalance_total_value"], errors="coerce").to_numpy(float)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(float)
            alloc = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce").to_numpy(float)
            last_idx = d.groupby(date).tail(1).index.to_numpy()
            last_idx = np.sort(last_idx)
            for k in range(1, len(last_idx)):
                a, b = last_idx[k - 1], last_idx[k]
                book_r = val[b] / val[a] - 1.0
                coin_r = close[b] / close[a] - 1.0
                pos = np.nanmean(alloc[a:b]) if np.isfinite(alloc[a:b]).any() else np.nan
                coin_rows.append((date.iloc[b], book_r, coin_r, pos))
        if coin_rows:
            cdf = pd.DataFrame(coin_rows, columns=["date", "book", "coin_r", "pos"])
            mu = cdf["coin_r"].mean()
            cdf["mkt"] = cdf["pos"] * mu
            cdf["coin"] = coin
            rows.append(cdf)
    timing = None
    if rows:
        alld = pd.concat(rows, ignore_index=True)
        alld = alld.replace([np.inf, -np.inf], np.nan).dropna(subset=["book", "mkt"])
        if len(alld):
            daily = alld.groupby("date")[["book", "mkt"]].mean()
            timing = float(daily["book"].mean() - daily["mkt"].mean())
    sup_pass = (timing > 0) if timing is not None else None

    # ---------- 4. Decision ----------
    if n_cases < 500 or tval is None:
        status = "not observable"
        decided = f"only {n_cases} independent sampled cases, below the plan's minimum of 500."
    elif slope > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "slope positive with t >= 2 and the timing part of the book above 0."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "slope negative with t <= -2."
    elif tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the timing part of the book is at or below 0 (or not measurable)."
    else:
        status = "inconclusive"
        decided = "|t| < 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": timing, "passed": sup_pass},
        "counts": {"independent sampled cases": n_cases},
        "decided_by": decided,
        "reading": "situation = non-zero 72-bar move (raw component value, prices as fallback) on the long side; the coin's mean 72-bar return is the mean of its sampled forward returns over all windows; the position behind each day's market gain is the mean hourly allocation held over that day, and the coin's mean daily return comes from its day-end closes over all windows.",
    }
