import numpy as np
import pandas as pd


def _ts(series):
    s = series
    if np.issubdtype(s.dtype, np.number):
        mx = float(np.nanmax(s.values)) if len(s) else 0.0
        if mx > 1e17:
            unit = "ns"
        elif mx > 1e14:
            unit = "us"
        elif mx > 1e11:
            unit = "ms"
        else:
            unit = "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 3
    MIN_CASES = 100
    RAW = "debug_info.components.wkd_fall_vol.last_history_value"

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True).copy()
            d["_ts"] = _ts(d["timestamp"])
            d["_dow"] = d["_ts"].dt.dayofweek
            close = d["close"].astype(float)
            ret1 = close / close.shift(1) - 1.0
            fall = ret1 < 0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                # first row of a window: no previous close inside the window, use the raw component
                fall = fall.where(ret1.notna(), raw > 0)
            fall = fall.fillna(False).astype(bool)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            d["_fc"] = fc
            situation = (d["_dow"] == 6) & fall
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
            prepared[coin][w] = d

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean excess 3-bar return after Sunday bars with forecast >= 2"
    threshold = "confirm: mean > 0 with t >= 2 over >= 100 cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 100 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0, "active_bars": int(n_active)},
            "decided_by": "fewer than 90% of the bars with a non-zero forecast are Sunday bars (coming bar Monday) after a Sunday fall with a long forecast, as the plan's Fidelity states.",
            "reading": "Sunday bar = bar whose UTC start timestamp is a Sunday; fall = close below the previous close in the same window (raw component > 0 on a window's first row).",
        }

    # ---------- criterion ----------
    excess = []
    weights = []
    for coin, wins in prepared.items():
        # normal 3-bar drift: non-overlapping 3-bar returns on each window's grid, all windows together
        drift_samples = []
        for w, d in wins.items():
            c = d["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    drift_samples.append(c[i + H] / c[i] - 1.0)
        if len(drift_samples) == 0:
            continue
        drift = float(np.mean(drift_samples))
        for w, d in wins.items():
            c = d["close"].astype(float).values
            fc = d["_fc"].values
            dow = d["_dow"].values
            for i in range(len(d)):
                if dow[i] != 6 or not (fc[i] >= 2):
                    continue
                if i + H >= len(d):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H])) or c[i] == 0:
                    continue
                excess.append(c[i + H] / c[i] - 1.0 - drift)
                weights.append(float(fc[i]))

    ex = np.array(excess, dtype=float)
    wt = np.array(weights, dtype=float)
    n = int(len(ex))

    mean = float(ex.mean()) if n > 0 else None
    t = None
    if n >= 2:
        sd = float(ex.std(ddof=1))
        t = float(mean / (sd / np.sqrt(n))) if sd > 0 else None
    wmean = float((ex * wt).sum() / wt.sum()) if n > 0 and wt.sum() > 0 else None
    support_pass = (bool(wmean > mean) if (wmean is not None and mean is not None) else None)

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases, below the plan's minimum of 100 cases."
    elif t is not None and mean > 0 and t >= 2:
        if support_pass:
            status = "confirmed"
            decided = "Mean excess 3-bar return positive with t >= 2 over at least 100 cases, and the forecast-weighted mean exceeds the unweighted mean."
        else:
            status = "inconclusive"
            decided = "A confirming t (>= 2, positive mean) but the supporting check failed: the forecast-weighted mean is not larger than the unweighted mean."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean excess 3-bar return negative with t <= -2 over at least 100 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess 3-bar return lies between -2 and 2 (or is undefined) over at least 100 cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": ({"name": "ordinary t of the mean", "value": t} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "forecast-weighted mean excess minus unweighted mean",
            "value": (float(wmean - mean) if (wmean is not None and mean is not None) else None),
            "passed": support_pass,
        },
        "counts": {"cases": n},
        "decided_by": decided,
        "reading": "A case is any bar whose UTC start timestamp is a Sunday with forecast >= 2 and a full 3-bar return inside its window, the coin's normal drift is the mean of its 3-bar returns on each window's grid 0,3,6,... over all its windows, and the plan's 'fewer than 100 cases' is reported as not observable per the workflow.",
    }
