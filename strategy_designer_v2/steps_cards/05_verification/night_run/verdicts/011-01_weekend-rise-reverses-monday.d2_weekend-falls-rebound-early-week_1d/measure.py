import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RAW = "debug_info.components.wkd_fall.last_history_value"
    MIN_POS = 300
    MIN_TOTAL = 600

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            # raw component value; recompute from prices where not recorded
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            r1 = close / close.shift(1) - 1.0
            vol = r1.rolling(20, min_periods=20).std()
            raw_re = r1 / vol
            raw = raw.where(raw.notna(), raw_re)
            # Sunday bar: bar starting Sunday UTC, closing at Monday's start
            is_sunday = ts.dt.dayofweek == 6
            fell = raw < 0
            active = fc.notna() & (fc != 0)
            situ_long = is_sunday & fell & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ_long).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "OLS slope of excess Sunday-to-Wednesday 3-bar return on forecast",
                "value": None,
                "statistic": None,
                "threshold": "t >= 2 confirms (with positive check), t <= -2 rejects",
            },
            "supporting_check": None,
            "counts": {"Sunday bars with forecast > 0": None, "Sunday bars in total": None},
            "decided_by": ("No active bars in the record." if agreement is None else
                           "Fewer than 90% of the bars with a non-zero forecast are Sunday bars after a "
                           "weekend fall (negative raw vol-scaled return) with a long forecast."),
            "reading": "Sunday bars are bars whose start timestamp is a Sunday UTC; a fall is a negative raw "
                       "wkd_fall value (recomputed from prices where missing); the expected side is long.",
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # coin's mean 3-bar return over all its windows, non-overlapping grid
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).to_numpy()
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        if len(grid_rets) == 0:
            continue
        coin_mean = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = d["close"].astype(float).to_numpy()
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy()
            reg = d["regime"].astype(str).to_numpy()
            n = len(d)
            for i in range(n):
                if reg[i] != "trending":
                    continue
                if i + H >= n:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and np.isfinite(fc[i])) or c[i] == 0:
                    continue
                ret = c[i + H] / c[i] - 1.0
                xs.append(float(fc[i]))
                ys.append(ret - coin_mean)

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    n_total = int(len(x))
    pos = x > 0
    n_pos = int(pos.sum())

    slope = None
    t = None
    if n_total >= 3 and np.ptp(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    check_val = None
    check_pass = None
    if n_pos > 0 and x[pos].sum() > 0:
        check_val = float(np.sum(y[pos] * x[pos]) / np.sum(x[pos]))
        check_pass = bool(check_val > 0)

    counts = {"Sunday bars with forecast > 0": n_pos, "Sunday bars in total": n_total}

    if n_pos < MIN_POS or n_total < MIN_TOTAL:
        status = "not observable"
        decided_by = (f"The minimum counts are not reached: {n_pos} Sunday bars with forecast > 0 "
                      f"(need 300) and {n_total} Sunday bars in total (need 600).")
    elif t is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and check_pass:
        status = "confirmed"
        decided_by = "The slope's t is 2 or more and the forecast-weighted mean excess return of Sunday bars with forecast > 0 is positive."
    elif t <= -2:
        status = "rejected"
        decided_by = "The slope's t is -2 or less."
    elif t >= 2:
        status = "inconclusive"
        decided_by = "The slope's t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided_by = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "OLS slope of excess Sunday-to-Wednesday 3-bar return on forecast",
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t} if t is not None else None),
            "threshold": "t >= 2 with a positive supporting check confirms; t <= -2 rejects; otherwise inconclusive",
        },
        "supporting_check": {
            "name": "forecast-weighted mean excess 3-bar return of Sunday bars with forecast > 0",
            "value": check_val,
            "passed": check_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("Sunday bars for the measure are the bars with regime 'trending' that have a full 3-bar "
                    "return inside their window, the coin mean is over the non-overlapping 3-bar grid of all its windows, "
                    "the regression includes zero-forecast Sunday bars, and the situation check takes Sunday as a "
                    "bar starting on Sunday UTC with a negative raw wkd_fall value and a positive forecast."),
    }
