import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    RAW = "debug_info.components.vol_ratio.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: the situation is the volume ratio (volume / 20-bar mean volume, today's bar
    # included), graded; outcome is a rise -> the expected side is long.
    # A bar is "of the situation" when the volume ratio is defined (finite, >= 0), taken from
    # the recorded raw component value or, where missing, recomputed from volume inside the window.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            recomputed = vol / vol.rolling(20, min_periods=20).mean()
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                ratio = raw.where(raw.notna(), recomputed)
            else:
                ratio = recomputed
            active = fc.notna() & (fc != 0)
            situation = ratio.notna() & np.isfinite(ratio) & (ratio >= 0)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope t of excess 7-bar return on forecast"
    threshold = "confirm if t >= 2 with supporting check passing; reject if t <= -2"
    sup_name = "per-coin slope of excess 7-bar return on forecast positive in at least 4 of 6 coins"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars with a "
                           "defined volume ratio, so the config does not take the long, volume-ratio "
                           "position the Fidelity describes."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    rows = []
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
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                rows.append((coin, w, (c1 / c0) - 1.0, fc[t]))

    data = pd.DataFrame(rows, columns=["coin", "window", "ret", "forecast"])
    # coin's mean 7-bar return over all windows (holding the coin)
    if len(data):
        data["coin_mean"] = data.groupby("coin")["ret"].transform("mean")
        data["excess"] = data["ret"] - data["coin_mean"]
    else:
        data["excess"] = []
    data = data.dropna(subset=["excess", "forecast"])
    n_cases = int(len(data))

    # per-coin slopes
    coin_slopes = {}
    for coin, g in data.groupby("coin"):
        if len(g) >= 3 and np.std(g["forecast"].values) > 0:
            coin_slopes[coin] = float(stats.linregress(g["forecast"].values,
                                                       g["excess"].values).slope)
        else:
            coin_slopes[coin] = float("nan")
    n_pos = int(sum(1 for s in coin_slopes.values() if np.isfinite(s) and s > 0))
    sup_passed = bool(n_pos >= 4)

    counts = {"non-overlapping 7-bar cases pooled across coins": n_cases,
              "coins with positive slope": n_pos}

    reading = ("Grid at positions 0, 7, 14, ... of each window keeping only points with a full 7-bar "
               "forward return inside the window, the coin's mean taken over its grid returns from all "
               "windows, OLS with intercept on all grid bars including zero forecasts, and the "
               "supporting check needs 4 positive per-coin slopes among the coins present.")

    if n_cases < 300:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold},
            "supporting_check": {"name": sup_name, "value": n_pos, "passed": sup_passed},
            "counts": counts,
            "decided_by": f"Only {n_cases} non-overlapping 7-bar cases, below the plan's minimum of 300.",
            "reading": reading,
        }

    x = data["forecast"].values.astype(float)
    y = data["excess"].values.astype(float)
    if np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else float("nan")
    else:
        slope, t = float("nan"), float("nan")

    if np.isfinite(t) and t >= 2 and sup_passed:
        status = "confirmed"
        decided = (f"Pooled slope t = {t:.2f} >= 2 over {n_cases} cases and {n_pos} coins have a "
                   f"positive slope (>= 4): confirm rule met.")
    elif np.isfinite(t) and t <= -2:
        status = "rejected"
        decided = (f"Pooled slope t = {t:.2f} <= -2 over {n_cases} cases: higher relative volume is "
                   f"followed by lower 7-day excess return.")
    elif np.isfinite(t) and t >= 2:
        status = "inconclusive"
        decided = (f"Pooled slope t = {t:.2f} >= 2 but only {n_pos} coins have a positive slope "
                   f"(< 4): supporting check fails.")
    else:
        status = "inconclusive"
        decided = f"Pooled slope t = {t:.2f} lies between -2 and 2 over {n_cases} cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": t if np.isfinite(t) else None,
                         "statistic": {"name": "OLS slope t", "value": t if np.isfinite(t) else None},
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": n_pos, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
