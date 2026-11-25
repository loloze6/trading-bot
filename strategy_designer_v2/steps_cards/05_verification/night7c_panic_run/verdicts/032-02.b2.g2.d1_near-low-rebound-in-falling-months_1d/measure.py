import numpy as np
import pandas as pd


def measure(bars):
    LC = "debug_info.components.low_close.last_history_value"
    F30 = "debug_info.components.fall30.last_history_value"

    # ---------- gather per-coin, per-window frames ----------
    frames = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["coin"] = coin
            d["window"] = w
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d["day"] = d["ts"].dt.floor("D")
            close = d["close"].astype(float)
            high = d["high"].astype(float)
            low = d["low"].astype(float)
            # next-day return inside the window only
            d["ret1"] = close.shift(-1) / close - 1.0
            # recompute regime-detector components from prices (within window)
            rng = (high - low) / close
            mbr = rng.rolling(90, min_periods=90).mean() / rng.rolling(30, min_periods=30).mean()
            ret30_px = close / close.shift(30) - 1.0
            if F30 in d.columns:
                ret30 = pd.to_numeric(d[F30], errors="coerce").where(
                    pd.to_numeric(d[F30], errors="coerce").notna(), ret30_px)
            else:
                ret30 = ret30_px
            d["mbr_calc"] = mbr
            d["ret30_calc"] = ret30
            frames.append(d)

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": None, "supporting_check": None, "counts": {},
            "decided_by": "no bars in the record", "reading": "none"}

    all_bars = pd.concat(frames, ignore_index=True)
    all_bars["forecast"] = pd.to_numeric(all_bars["forecast"], errors="coerce").fillna(0.0)
    regime = all_bars["regime"].astype(str)

    # ---------- situation check ----------
    active = all_bars[all_bars["forecast"] != 0].copy()
    if len(active) == 0:
        agreement = None
        passed = False
    else:
        computable = active["mbr_calc"].notna() & active["ret30_calc"].notna()
        sit_calc = (active["mbr_calc"] < 1.0) & (active["ret30_calc"] < 0.0)
        # where the 90-bar range history is not in the record, fall back on the detector's decision
        sit_fallback = (active["regime"].astype(str) == "mean_reversion") & \
            (active["ret30_calc"].isna() | (active["ret30_calc"] < 0.0))
        situation = np.where(computable, sit_calc, sit_fallback)
        ok = situation & (active["forecast"].values > 0)
        agreement = float(np.mean(ok))
        passed = agreement >= 0.9

    reading = ("Situation recomputed per window from prices with bar range (high-low)/close, the 90/30 "
               "mean-range ratio and the 30-day return (the recorded fall30 raw value where present), falling "
               "back on the recorded regime where 90 bars of history are not in the record; the main measure "
               "uses every mean_reversion bar with a next-day return (zero forecasts included), its t clusters "
               "deviations by UTC day across coins; 'regime days with a position' are mean_reversion (coin, day) "
               "bars with a non-zero postRebalance_current_allocation; terciles are the lowest and highest n//3 "
               "regime bars pooled by forecast (stable sort).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None, "supporting_check": None, "counts": {},
            "decided_by": ("fewer than 90% of bars with a non-zero forecast are long bars of the plan's situation "
                           "(90/30 mean bar range ratio below 1 and 30-day return below 0)"),
            "reading": reading}

    # ---------- coin mean daily return over all windows ----------
    coin_mean = all_bars.groupby("coin")["ret1"].mean()
    all_bars["excess"] = all_bars["ret1"] - all_bars["coin"].map(coin_mean)

    reg = all_bars[(regime == "mean_reversion") & all_bars["excess"].notna()].copy()
    reg["x"] = reg["forecast"] / 10.0 * reg["excess"]

    alloc = pd.to_numeric(all_bars["postRebalance_current_allocation"], errors="coerce").fillna(0.0)
    n_pos_days = int(((regime == "mean_reversion") & (alloc != 0)).sum())

    n = len(reg)
    mean_val = float(reg["x"].mean()) if n > 0 else None
    t_val = None
    n_days = int(reg["day"].nunique()) if n > 0 else 0
    if n > 1:
        dev = reg["x"] - mean_val
        D = dev.groupby(reg["day"]).sum()
        G = len(D)
        ss = float((D ** 2).sum())
        if G > 1 and ss > 0:
            se = np.sqrt(G / (G - 1.0) * ss) / n
            t_val = float(mean_val / se)

    # ---------- supporting check ----------
    diff = None
    if n >= 3:
        order = np.argsort(reg["forecast"].values, kind="mergesort")
        k = n // 3
        ex = reg["excess"].values
        bottom = ex[order[:k]]
        top = ex[order[n - k:]]
        diff = float(np.mean(top) - np.mean(bottom))
    sup_passed = None if diff is None else bool(diff > 0)

    counts = {"regime days with a position": n_pos_days,
              "regime bars in main measure": int(n),
              "independent days (t clusters)": n_days}

    main = {"name": "mean of (forecast/10) x excess next-day return on mean_reversion bars",
            "value": mean_val,
            "statistic": None if t_val is None else {"name": "t of the mean, clustered by day", "value": t_val},
            "threshold": "confirm t >= 2 (with top-minus-bottom > 0); reject t <= -2"}
    support = {"name": "top third minus bottom third mean excess next-day return",
               "value": diff, "passed": sup_passed}

    if n_pos_days < 100:
        status = "not observable"
        decided = f"only {n_pos_days} regime days with a position, below the plan's minimum of 100"
    elif t_val is None:
        status = "inconclusive"
        decided = "the main measure's t could not be computed"
    elif t_val >= 2 and sup_passed:
        status = "confirmed"
        decided = "main measure t >= 2 and the top-minus-bottom difference is above 0"
    elif t_val <= -2:
        status = "rejected"
        decided = "main measure t <= -2"
    elif t_val >= 2:
        status = "inconclusive"
        decided = "main measure t >= 2 but the top-minus-bottom difference is at or below 0"
    else:
        status = "inconclusive"
        decided = "main measure t between -2 and 2"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
