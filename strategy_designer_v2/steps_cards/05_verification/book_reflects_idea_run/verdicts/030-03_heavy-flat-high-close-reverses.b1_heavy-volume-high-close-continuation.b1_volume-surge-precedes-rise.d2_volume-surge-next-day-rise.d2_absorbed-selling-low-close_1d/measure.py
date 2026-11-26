import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.absorb.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            high = d["high"].astype(float)
            low = d["low"].astype(float)
            close = d["close"].astype(float)
            vol = d["volume"].astype(float)
            rng = (high - low).replace(0, np.nan)
            loc = (high - close) / rng
            vmean = vol.shift(1).rolling(20, min_periods=20).mean()
            recomputed = loc * vol / vmean.replace(0, np.nan)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of next-day excess return on forecast, pooled over coins and windows (1-bar grid)"
    main_thr = "confirm: slope > 0 with t >= 2 and supporting check passing; reject: slope < 0 with t <= -2"
    sup_name = "mean next-day excess return, top fifth of forecast bars minus bottom fifth"
    reading = ("Situation taken as the graded product (high-close)/(high-low) x volume / prior-20-day mean volume "
               "being above 0 with a long forecast (raw value recomputed from prices where not recorded); "
               "top and bottom fifths are the pooled bars ranked by forecast (stable sort, ties kept in record order), "
               "n//5 bars each; the 1000-bar minimum counts bars with forecast > 0 that have a next-day return, "
               "and failing it gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the active bars are bars where the low-close x heavy-volume product "
                           "is positive with a long forecast, as the plan's situation and side require."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        rets_all = []
        per_win = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            r = close.shift(-1) / close - 1.0
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            per_win.append((r, fc))
            rets_all.append(r.dropna().values)
        allr = np.concatenate(rets_all) if rets_all else np.array([])
        if allr.size == 0:
            continue
        mu = float(np.mean(allr))
        for r, fc in per_win:
            m = r.notna() & fc.notna()
            xs.append(fc[m].values.astype(float))
            ys.append((r[m] - mu).values.astype(float))

    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    n = int(x.size)
    n_pos = int(np.sum(x > 0))

    slope = None
    t = None
    if n >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr > 0 else float("nan")

    sup_val = None
    sup_pass = None
    k = n // 5
    if k >= 1:
        order = np.argsort(x, kind="mergesort")
        bottom = y[order[:k]]
        top = y[order[-k:]]
        sup_val = float(np.mean(top) - np.mean(bottom))
        sup_pass = bool(sup_val > 0)

    counts = {"bars with a forecast above 0": n_pos, "bars in the regression": n,
              "bars per fifth": int(k)}

    if n_pos < 1000:
        status = "not observable"
        decided = f"Only {n_pos} bars have a forecast above 0, fewer than the plan's minimum of 1000."
    elif slope is None or t is None or not np.isfinite(t):
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the top-minus-bottom fifth difference is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
