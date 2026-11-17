import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    VR_COL = "debug_info.components.volratio.last_history_value"

    # ---------- 1. Situation check: sharp fall (vol-scaled 1-bar return <= -2), expected side long ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            r = close / close.shift(1) - 1.0
            # two common conventions for the 20-bar usual move: including or excluding the current bar
            vol_incl = r.rolling(20, min_periods=20).std()
            vol_excl = r.shift(1).rolling(20, min_periods=20).std()
            z_incl = r / vol_incl
            z_excl = r / vol_excl
            computable = z_incl.notna() | z_excl.notna()
            sharp_fall = (z_incl <= -2.0) | (z_excl <= -2.0)
            # where the 20-bar history is not available inside the window, fall back on the detector's decision
            fallback = (df["regime"] == "mean_reversion") & (r.fillna(-1.0) < 0)
            situation = np.where(computable, sharp_fall, fallback)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & pd.Series(situation, index=df.index) & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "t of slope of excess 3-bar return on raw volume ratio, sharp-fall bars",
                "value": None, "statistic": None,
                "threshold": "confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2",
            },
            "supporting_check": None,
            "counts": {"kept sharp-fall cases": None, "active bars": n_active},
            "decided_by": ("Fewer than 90% of active (non-zero forecast) bars are sharp-fall bars "
                           "(vol-scaled 1-bar return <= -2) with a long forecast, as the Fidelity requires."
                           if n_active > 0 else "No active bars: the config never takes the plan's position."),
            "reading": ("The sharp-fall rule was recomputed from closes as the 1-bar return over the 20-bar std of "
                        "1-bar returns (current bar included or excluded), using the recorded regime where the "
                        "window lacks 20 bars of history."),
        }

    # ---------- 2. Criterion ----------
    # coin mean 3-bar return over all windows, non-overlapping grid 0,3,6,... per window
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df.sort_values("timestamp")["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                rets.append(c[i + H] / c[i] - 1.0)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    xs, ys = [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            vr = pd.to_numeric(df[VR_COL], errors="coerce").values if VR_COL in df.columns else np.full(len(df), np.nan)
            mr_idx = np.where(df["regime"].values == "mean_reversion")[0]
            last_kept = None
            for i in mr_idx:
                if last_kept is not None and i - last_kept < H:
                    continue
                last_kept = i
                if i + H >= len(c):
                    continue
                if not np.isfinite(vr[i]) or not np.isfinite(coin_mean[coin]):
                    continue
                fr = c[i + H] / c[i] - 1.0
                if not np.isfinite(fr):
                    continue
                xs.append(float(vr[i]))
                ys.append(fr - coin_mean[coin])

    n = len(xs)
    xs = np.array(xs)
    ys = np.array(ys)

    slope = None
    t = None
    if n >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    top_mean = None
    check_passed = None
    if n >= 3:
        k = max(1, n // 3)
        order = np.argsort(-xs, kind="mergesort")
        top_mean = float(np.mean(ys[order[:k]]))
        check_passed = bool(top_mean > 0)

    if n < 30:
        status = "not observable"
        decided = f"Only {n} kept sharp-fall cases, below the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed with enough cases."
    elif slope > 0 and t >= 2 and check_passed:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the top third's mean excess return is above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check failed, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of excess 3-bar return on raw volume ratio, sharp-fall bars",
            "value": slope,
            "statistic": {"name": "OLS t of slope", "value": t} if t is not None else None,
            "threshold": "confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "mean excess 3-bar return of top third by volume ratio > 0",
            "value": top_mean,
            "passed": check_passed,
        },
        "counts": {"kept sharp-fall cases": int(n)},
        "decided_by": decided,
        "reading": ("Kept bars are thinned greedily per window on regime bars before dropping those without a "
                    "3-bar forward return inside the window, the coin's mean 3-bar return uses the non-overlapping "
                    "grid 0,3,6,... pooled over all windows, and the top third is the floor(n/3) cases with the "
                    "largest volume ratio."),
    }
