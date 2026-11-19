import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 240
    REG_PERIOD = 1440
    RAW_COL = "debug_info.components.rsi14d.last_history_value"

    # ---------- 1. Situation check ----------
    raw_all = []
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            if RAW_COL in df.columns:
                raw_all.append(pd.to_numeric(df[RAW_COL], errors="coerce").dropna().values)
    raw_all = np.concatenate(raw_all) if raw_all else np.array([])
    # The catalogue's exact output of RSIPullbackComponent is 50 - RSI. Fall back to RSI itself
    # only if the raw values plainly sit on the 0..100 RSI scale.
    raw_is_rsi = bool(raw_all.size > 0 and raw_all.min() >= 0 and raw_all.max() <= 100
                      and np.median(raw_all) > 20)

    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            ret = close / close.shift(REG_PERIOD) - 1.0
            regime_col = df["regime"].astype(str)
            # situation: 1440-bar return > 0 recomputed from prices; where the window lacks
            # 1440 bars of history, the detector's recorded regime stands in for it
            trend = np.where(ret.notna(), ret > 0, regime_col == "trending")
            if RAW_COL in df.columns:
                raw = pd.to_numeric(df[RAW_COL], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            rsi = raw if raw_is_rsi else 50.0 - raw
            expected_sign = np.sign(rsi - 50.0)
            active = fc.notna() & (fc != 0)
            agree = active & pd.Series(trend, index=df.index) & raw.notna() & \
                (np.sign(fc) == expected_sign) & (expected_sign != 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of slope of excess 240-bar forward return on forecast, trending grid bars pooled"
    threshold = "confirm: slope > 0 with t >= 2 and top-third check passes; reject: slope < 0 with t <= -2"
    reading = ("Cases are rows at positions 0, 240, 480, ... of each window with regime 'trending' and a full "
               "240-bar forward return inside the window; the coin's mean 240-bar return is the mean over all such "
               "grid bars of all its windows; the top third is the n//3 cases with the largest forecast; "
               "the plan's 'fewer than 100 cases' is reported as not observable; "
               "the situation check reads RSI as 50 minus the raw component value.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"independent trending cases": None, "active bars": n_active},
            "decided_by": ("Fewer than 90% of non-zero forecast bars are bars with a positive 1440-bar return "
                           "whose forecast sign matches the sign of RSI(336) - 50."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin in bars:
        grid_rets = []
        coin_rows = []
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if reg[t] == "trending" and np.isfinite(fc[t]):
                    coin_rows.append((r, fc[t]))
        if not grid_rets:
            continue
        mu = float(np.mean(grid_rets))
        for r, f in coin_rows:
            rows.append((r - mu, f))

    n_cases = len(rows)
    counts = {"independent trending cases": n_cases}

    if n_cases < 100:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean excess return of top-third forecast cases > 0",
                                 "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Only {n_cases} independent trending cases, fewer than the 100 the plan requires.",
            "reading": reading,
        }

    arr = np.array(rows, dtype=float)
    y, x = arr[:, 0], arr[:, 1]
    if np.std(x) == 0:
        slope, t_slope = 0.0, 0.0
    else:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else 0.0

    k = n_cases // 3
    order = np.argsort(-x, kind="mergesort")
    top = y[order[:k]]
    top_mean = float(np.mean(top)) if k > 0 else None
    check_pass = bool(top_mean is not None and top_mean > 0)

    if slope > 0 and t_slope >= 2 and check_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the top-third mean excess return is above 0."
    elif slope > 0 and t_slope >= 2:
        status = "inconclusive"
        decided = "The slope t is >= 2 but the top-third mean excess return is not above 0."
    elif slope < 0 and t_slope <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": t_slope,
                         "statistic": {"name": "OLS slope t", "value": t_slope},
                         "threshold": threshold},
        "supporting_check": {"name": "mean excess 240-bar return of top-third forecast cases > 0",
                             "value": top_mean, "passed": check_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
