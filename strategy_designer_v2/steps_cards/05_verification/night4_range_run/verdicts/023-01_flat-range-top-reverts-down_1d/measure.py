import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    PERIOD = 30
    FLAT_MAX = 0.33
    MIN_CASES = 30
    RAW_COL = "debug_info.components.mid_dist.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            high = d["high"].astype(float)
            low = d["low"].astype(float)
            fc = d["forecast"].astype(float)
            net = (close - close.shift(PERIOD - 1)).abs()
            rng = high.rolling(PERIOD, min_periods=PERIOD).max() - low.rolling(PERIOD, min_periods=PERIOD).min()
            ratio = net / rng.replace(0, np.nan)
            flat = ratio <= FLAT_MAX
            # bars without 30 bars of history in the record: fall back to the detector's recorded regime
            no_hist = ratio.isna()
            if "regime" in d.columns:
                flat = flat.where(~no_hist, d["regime"].astype(str) == "mean_reversion")
            raw = d[RAW_COL].astype(float) if RAW_COL in d.columns else pd.Series(np.nan, index=d.index)
            active = fc.notna() & (fc != 0)
            side_ok = raw.notna() & (np.sign(fc) == -np.sign(raw)) & (raw != 0)
            agree = active & flat.fillna(False).astype(bool) & side_ok
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of (forecast/10) x (5-bar forward return minus coin's mean 5-bar return), non-overlapping grid, non-zero forecast"
    threshold = "confirm: mean > 0 with t >= 2 on at least 30 cases; reject: mean < 0 with t <= -2 on at least 30 cases"
    reading = ("Net move taken as |close[t] - close[t-29]| over the 30-bar high-low range of rows t-29..t (falling back to the "
               "recorded regime on bars with under 30 recorded bars), expected side short when the raw mid distance is above 0 "
               "and long below; the coin's mean 5-bar return is taken on the same non-overlapping grid over all its windows; "
               "the plan's 'fewer than 30 cases' is reported as not observable per the workflow's minimum-count rule.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of non-zero-forecast bars are flat-range bars (30-bar net move <= 0.33 of the range) "
                           "with the forecast on the side opposite to the close's distance from the range middle."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    values = []
    for coin, wins in bars.items():
        grid_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = d["forecast"].astype(float).values
            for i in range(0, len(d), H):
                if i + H >= len(d):
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                grid_rows.append((c1 / c0 - 1.0, fc[i]))
        if not grid_rows:
            continue
        rets = np.array([r for r, _ in grid_rows], dtype=float)
        mean_ret = float(np.mean(rets))
        for r, f in grid_rows:
            if np.isfinite(f) and f != 0:
                values.append((f / 10.0) * (r - mean_ret))

    vals = np.array(values, dtype=float)
    n = int(len(vals))
    mean = float(np.mean(vals)) if n > 0 else None
    t = None
    if n > 1:
        sd = float(np.std(vals, ddof=1))
        if sd > 0:
            t = float(mean / (sd / np.sqrt(n)))

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} non-zero-forecast grid cases, below the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero dispersion), so neither confirm nor reject is met."
    elif mean > 0 and t >= 2:
        status = "confirmed"
        decided = "The mean is above 0 with t of 2 or more on at least 30 cases (confirm rule)."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean is below 0 with t of -2 or less on at least 30 cases (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": {"non-zero-forecast grid cases": n},
        "decided_by": decided,
        "reading": reading,
    }
