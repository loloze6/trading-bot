import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    VR = "debug_info.components.vol_ratio.last_history_value"
    OFF = "debug_info.components.offset.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: today's volume against its own 30-day average volume.
    # Expected side: long when volume is heavier than usual, short when lighter.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            # Raw volume ratio: the recorded component value, else recomputed from prices
            # (within the window only).
            recomputed = vol / vol.rolling(30, min_periods=30).mean()
            if VR in df.columns:
                ratio = pd.to_numeric(df[VR], errors="coerce")
                ratio = ratio.where(ratio.notna(), recomputed)
            else:
                ratio = recomputed
            # If the recorded value is already standardised (the offset's recorded value is
            # not the raw constant 1), the usual level is the standardised centre 10;
            # otherwise the usual level is the ratio's mean over its past 60 values
            # (at least 20), falling back to 1 (volume equal to its 30-day average).
            standardised = False
            if OFF in df.columns:
                off = pd.to_numeric(df[OFF], errors="coerce").dropna()
                if len(off) > 0 and abs(float(off.median()) - 1.0) > 0.5:
                    standardised = True
            if standardised:
                ref = pd.Series(10.0, index=df.index)
            else:
                ref = ratio.shift(1).rolling(60, min_periods=20).mean()
                ref = ref.fillna(1.0)
            active = fc.notna() & (fc != 0)
            sit_side = np.sign(ratio - ref)
            agree = active & ratio.notna() & (sit_side == np.sign(fc))
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of demeaned 3-bar forward return on forecast (non-overlapping, pooled)"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive; at least 300 non-overlapping cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "The forecast's sign does not follow the plan's situation (long when the day's volume is above its usual ratio to the 30-day average, short when below) on at least 90% of active bars.",
            "reading": "Usual volume level taken as the ratio's mean over its past 60 values (or 1 without enough history, or 10 if the recorded value is already standardised).",
        }

    # ---------- 2. Criterion ----------
    rows = []  # (coin, forecast, fwd return)
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1, f = close[t], close[t + H], fc[t]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 == 0:
                    continue
                rows.append((coin, float(f), float(c1 / c0 - 1.0)))

    data = pd.DataFrame(rows, columns=["coin", "f", "r"])
    n_cases = int(len(data))
    counts = {"non-overlapping cases": n_cases}

    if n_cases < 300:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Only {n_cases} non-overlapping cases, below the plan's minimum of 300.",
            "reading": "Each coin's mean 3-bar return is taken over its non-overlapping grid samples of all windows; OLS with intercept.",
        }

    data["y"] = data["r"] - data.groupby("coin")["r"].transform("mean")
    x = data["f"].values
    y = data["y"].values
    if np.std(x) == 0:
        slope, tstat = float("nan"), float("nan")
    else:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        tstat = float(res.slope / res.stderr) if res.stderr > 0 else float("nan")

    if np.isfinite(tstat) and slope > 0 and tstat >= 2:
        status = "confirmed"
        decided = f"The slope is positive with t = {tstat:.2f} >= 2 on {n_cases} cases."
    elif np.isfinite(tstat) and slope < 0 and tstat <= -2:
        status = "rejected"
        decided = f"The slope is negative with t = {tstat:.2f} <= -2 on {n_cases} cases."
    else:
        status = "inconclusive"
        decided = f"The slope's t = {tstat:.2f} lies between -2 and 2 (inconclusive) on {n_cases} cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope if np.isfinite(slope) else None,
            "statistic": {"name": "OLS slope t", "value": tstat if np.isfinite(tstat) else None},
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": "Each coin's mean 3-bar return is taken over its non-overlapping grid samples pooled over all its windows, and the slope's t is from an ordinary least-squares fit with intercept.",
    }
