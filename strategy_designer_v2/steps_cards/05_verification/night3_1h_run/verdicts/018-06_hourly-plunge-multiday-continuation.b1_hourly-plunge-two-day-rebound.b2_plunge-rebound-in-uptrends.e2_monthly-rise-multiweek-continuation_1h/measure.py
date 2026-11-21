import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 336
    RAW = "debug_info.components.ret30d.last_history_value"

    # ---------- 1. Situation check: 30-day return > 0, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float).reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").reset_index(drop=True)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").reset_index(drop=True)
            else:
                raw = pd.Series(np.nan, index=close.index)
            # where the raw value is not recorded, recompute the 720-bar return from prices (inside the window)
            price_ret = close / close.shift(720) - 1.0
            raw = raw.where(raw.notna(), price_ret)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "forecast-weighted mean excess 336-bar return over cells with forecast > 0"
    main_thr = "confirm: > 0 with t >= 2 (and slope t >= 2); reject: < 0 with t <= -2 or slope t <= -2; at least 200 cells"
    sup_name = "OLS slope of excess return on forecast, t"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a nonzero forecast are long bars with a positive 30-day (720-bar) return, as the plan's situation requires.",
            "reading": "The situation is a positive raw ret30d value (recomputed from prices where missing) with a positive forecast.",
        }

    # ---------- 2. Criterion ----------
    # coin's mean 336-bar return over all its windows (non-overlapping grid)
    cells = []  # (coin, forecast, return)
    coin_rets = {}
    for coin, wins in bars.items():
        rets_all = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = df["close"].astype(float).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(close)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                rets_all.append(r)
                f = fc[t]
                if np.isfinite(f) and f > 0:
                    cells.append((coin, float(f), float(r)))
        coin_rets[coin] = float(np.mean(rets_all)) if rets_all else np.nan

    f_arr = np.array([c[1] for c in cells], dtype=float)
    e_arr = np.array([c[2] - coin_rets[c[0]] for c in cells], dtype=float)
    ok = np.isfinite(f_arr) & np.isfinite(e_arr)
    f_arr, e_arr = f_arr[ok], e_arr[ok]
    n_cells = int(len(f_arr))

    wmean, t_main = None, None
    if n_cells >= 2 and f_arr.sum() > 0:
        wmean = float(np.sum(f_arr * e_arr) / np.sum(f_arr))
        y = f_arr * e_arr / np.mean(f_arr)
        sd = np.std(y, ddof=1)
        t_main = float(np.mean(y) / (sd / np.sqrt(n_cells))) if sd > 0 else None

    slope_t, slope = None, None
    if n_cells >= 3 and np.std(f_arr) > 0:
        lr = stats.linregress(f_arr, e_arr)
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_pass = None if slope_t is None else bool(slope is not None and slope > 0 and slope_t >= 2)

    counts = {"cells with forecast > 0": n_cells}

    if n_cells < 200:
        status = "not observable"
        decided = f"Only {n_cells} grid cells with forecast > 0, fewer than the plan's minimum of 200."
    else:
        reject_main = wmean is not None and t_main is not None and wmean < 0 and t_main <= -2
        reject_slope = slope_t is not None and slope_t <= -2
        confirm = (wmean is not None and t_main is not None and wmean > 0 and t_main >= 2 and sup_pass is True)
        if reject_main or reject_slope:
            status = "rejected"
            decided = ("Reject: the forecast-weighted mean excess return is negative with t <= -2"
                       if reject_main else
                       "Reject: the slope of excess return on forecast has t <= -2") + ", over at least 200 cells."
        elif confirm:
            status = "confirmed"
            decided = "Confirm: the weighted mean excess return is positive with t >= 2 and the slope t >= 2, over at least 200 cells."
        else:
            status = "inconclusive"
            if wmean is not None and t_main is not None and wmean > 0 and t_main >= 2:
                decided = "Inconclusive: the main measure is at t >= 2 but the slope t is below 2."
            else:
                decided = "Inconclusive: the main measure's t is between -2 and 2 and no reject rule is met."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": wmean,
            "statistic": None if t_main is None else {"name": "t of the forecast-weighted mean over cells", "value": t_main},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": slope_t, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("The t of the weighted mean is the ordinary t of the per-cell values forecast x excess / mean forecast "
                    "(whose mean equals the weighted mean), the coin's mean 336-bar return is taken on the same "
                    "non-overlapping grid over all its windows, and the slope's t is the OLS slope over its standard error."),
    }
