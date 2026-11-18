import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    MIN_CASES = 30

    def situation_frame(df):
        o = df["open"].astype(float)
        h = df["high"].astype(float)
        l = df["low"].astype(float)
        c = df["close"].astype(float)
        v = df["volume"].astype(float)
        r1 = c / c.shift(1) - 1.0
        vol = r1.rolling(20, min_periods=20).std()
        ret = r1 / vol
        vmean = v.shift(1).rolling(20, min_periods=20).mean()
        vr = v / vmean
        rng = h - l
        wick = (np.minimum(o, c) - l) / rng.where(rng > 0)
        known = ret.notna() & vr.notna() & wick.notna() & np.isfinite(ret) & np.isfinite(vr)
        sit = (ret <= -2.0) & (vr >= 2.0) & (wick >= 0.3)
        return sit.fillna(False), known

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    n_unknown_active = 0
    n_unknown_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            sit, known = situation_frame(df)
            active = fc != 0
            # bars where the price history inside the window is too short to recompute the rule
            unk = active & ~known
            kn = active & known
            n_active += int(kn.sum())
            n_agree += int((kn & sit & (fc > 0)).sum())
            n_unknown_active += int(unk.sum())
            reg = df["regime"].astype(str) == "mean_reversion"
            n_unknown_agree += int((unk & reg & (fc > 0)).sum())

    if n_active > 0:
        agreement = n_agree / n_active
    elif n_unknown_active > 0:
        agreement = n_unknown_agree / n_unknown_active
    else:
        agreement = None

    reading_base = ("Situation recomputed from prices (return over 20-bar std of 1-bar returns incl. current, "
                    "volume over mean of prior 20, lower wick over range), active bars whose rule cannot be "
                    "recomputed in-window excluded; flush bars within <=3 bars of a kept one dropped; coin mean "
                    "3-bar return from the non-overlapping 0,3,6,... grid of every window pooled; OLS slope t; "
                    "fewer than 30 kept flush bars reported as not observable per the workflow's minimum-count rule.")

    if agreement is None or agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active + n_unknown_active},
            "decided_by": ("Fewer than 90% of the active bars are long bars of the plan's situation "
                           "(return <= -2 usual moves, volume >= 2x prior 20-bar mean, lower wick >= 0.3 of range)"
                           if agreement is not None else "No active bars: the config never forecasts in the plan's situation."),
            "reading": reading_base,
        }

    # ---------- coin mean 3-bar return ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).reset_index(drop=True).values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    rs.append(c[p + H] / c[p] - 1.0)
        coin_mean[coin] = float(np.mean(rs)) if rs else np.nan

    # ---------- flush cases ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        cm = coin_mean.get(coin, np.nan)
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = (df["regime"].astype(str) == "mean_reversion").values
            c = df["close"].astype(float).values
            idx = np.where(reg & (fc > 0))[0]
            last = None
            for p in idx:
                if last is not None and p - last <= H:
                    continue
                last = p
                if p + H >= len(c):
                    continue
                if not (np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0 and np.isfinite(cm)):
                    continue
                xs.append(float(fc[p]))
                ys.append(c[p + H] / c[p] - 1.0 - cm)

    n = len(xs)
    counts = {"kept flush bars": n}
    sc = {"agreement": float(agreement), "passed": True}
    threshold = "confirm: slope > 0 with t >= 2 and mean excess > 0; reject: slope < 0 with t <= -2"

    slope = None
    t = None
    mean_ex = None
    if n >= 3 and np.std(xs) > 0:
        lr = stats.linregress(np.array(xs), np.array(ys))
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    if n > 0:
        mean_ex = float(np.mean(ys))
    sup_pass = None if mean_ex is None else bool(mean_ex > 0)

    main = {"name": "OLS slope of excess 3-bar return on forecast, flush bars",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
            "threshold": threshold}
    sup = {"name": "mean excess 3-bar return of flush bars", "value": mean_ex, "passed": sup_pass}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} kept flush bars across all coins and windows, fewer than the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The slope t cannot be computed (no spread in the forecast), so neither rule is met."
    elif slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the mean excess 3-bar return is above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        decided = "The slope confirms (t >= 2) but the mean excess 3-bar return is not above 0."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
