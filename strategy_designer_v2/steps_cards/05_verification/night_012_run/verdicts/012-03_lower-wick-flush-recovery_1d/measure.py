import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    WICK = "debug_info.components.wick.post_pipeline_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)
            r1 = close / close.shift(1) - 1.0
            usual = r1.rolling(20, min_periods=20).std(ddof=1)
            fall = r1 / usual
            vmean = vol.shift(1).rolling(20, min_periods=20).mean()
            vburst = vol / vmean
            computable = fall.notna() & vburst.notna() & (usual > 0) & (vmean > 0)
            sit_calc = (fall <= -2.0) & (vburst >= 2.0)
            # Where the window lacks the 20-bar history (warm-up not recorded), use the detector's own decision.
            sit_fallback = df["regime"].astype(str) == "mean_reversion"
            situation = np.where(computable, sit_calc, sit_fallback)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope t of excess 3-bar return on wick (post_pipeline_value), pooled"
    thr = "confirm if slope t >= 2 with supporting check passing; reject if slope t <= -2; at least 30 independent flush bars"
    sup_name = "mean excess 3-bar return of flush bars with wick above flush-bar median > 0"
    reading = ("Situation recomputed as 1-bar return / std (ddof 1) of the last 20 one-bar returns including the bar <= -2 and "
               "volume / mean of the prior 20 volumes >= 2, falling back to the recorded regime on bars without 20 bars of in-window history; "
               "the coin's mean 3-bar return is taken on the non-overlapping grid (positions 0,3,6,... of every window) pooled over all windows; "
               "flush bars are thinned before dropping those without close[t+3] in the window, and the median for the check is over the kept flush bars.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"independent flush bars": None, "active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long on bars where the 1-bar return is at most "
                           "-2 usual moves with volume at least 2x its prior 20-bar mean, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin mean 3-bar return over all windows (non-overlapping grid)
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).to_numpy()
            for i in range(0, len(c) - H, H):
                if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]):
                    rets.append(c[i + H] / c[i] - 1.0)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    xs, ys = [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).to_numpy()
            reg = df["regime"].astype(str).to_numpy()
            wick = (pd.to_numeric(df[WICK], errors="coerce").to_numpy()
                    if WICK in df.columns else np.full(len(df), np.nan))
            last = None
            for i in range(len(df)):
                if reg[i] != "mean_reversion":
                    continue
                if last is not None and i - last < H:
                    continue
                last = i
                if i + H >= len(df):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                if not np.isfinite(wick[i]) or not np.isfinite(coin_mean[coin]):
                    continue
                xs.append(float(wick[i]))
                ys.append(c[i + H] / c[i] - 1.0 - coin_mean[coin])

    x = np.array(xs)
    y = np.array(ys)
    n = len(x)
    counts = {"independent flush bars": n}

    slope = None
    t = None
    if n >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t = float(res.slope / res.stderr) if res.stderr > 0 else None

    sup_val = None
    sup_pass = None
    if n > 0:
        med = np.median(x)
        above = y[x > med]
        if len(above) > 0:
            sup_val = float(np.mean(above))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n < 30:
        status = "not observable"
        decided = f"Only {n} independent flush bars, fewer than the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The slope t could not be computed (no variation in the wick), so neither confirm nor reject is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope t is 2 or more and the supporting check passes."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    elif t <= -2:
        status = "rejected"
        decided = "The slope t is -2 or less."
    else:
        status = "inconclusive"
        decided = "The slope t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": t} if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
