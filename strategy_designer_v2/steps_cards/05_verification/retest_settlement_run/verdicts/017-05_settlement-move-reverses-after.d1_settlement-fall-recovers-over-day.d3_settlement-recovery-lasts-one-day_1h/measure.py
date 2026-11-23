import numpy as np
import pandas as pd
from scipy import stats


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype("float64")
        med = np.nanmedian(np.abs(v.values)) if len(v) else 0.0
        if med > 1e17:
            unit = "ns"
        elif med > 1e14:
            unit = "us"
        elif med > 1e11:
            unit = "ms"
        else:
            unit = "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def _slope_t(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    n = len(x)
    if n < 3 or np.std(x) == 0:
        return None, None, n
    res = stats.linregress(x, y)
    if not np.isfinite(res.stderr) or res.stderr == 0:
        return float(res.slope), None, n
    return float(res.slope), float(res.slope / res.stderr), n


def measure(bars):
    H = 24
    RAW = "debug_info.components.fall2h.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin in sorted(bars):
        prepared[coin] = {}
        for w in sorted(bars[coin], key=lambda k: (len(str(k)), str(k))):
            df = bars[coin][w].reset_index(drop=True).copy()
            if len(df) == 0:
                continue
            ts = _to_utc(df["timestamp"]).reset_index(drop=True)
            close = df["close"].astype(float).reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).reset_index(drop=True)
            close_hour = (ts + pd.Timedelta(hours=1)).dt.hour
            settle = close_hour.isin([0, 16])
            ret2 = close / close.shift(2) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").reset_index(drop=True)
                fallval = raw.where(raw.notna(), ret2)
            else:
                fallval = ret2
            fall = fallval < 0
            situation = settle & fall
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
            prepared[coin][w] = (df, close, fc)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("No active bars, so the forecast never takes the plan's situation."
                           if n_active == 0 else
                           "Fewer than 90% of the active bars are long bars at a 00:00/16:00 UTC settlement close after a 2-bar fall, as the Fidelity requires."),
            "reading": "The settlement bar is the bar whose close (timestamp + 1h) is 00:00 or 16:00 UTC, and the fall is a negative raw fall2h value (or 2-bar price return where not recorded).",
        }

    # ---------- 2. Criterion ----------
    xs, ys, xs2, ys2 = [], [], [], []
    for coin, wins in prepared.items():
        # normal 24-bar drift: mean of non-overlapping 24-bar returns over all windows
        grid_rets = []
        for w, (df, close, fc) in wins.items():
            c = close.values
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                grid_rets.extend(r[np.isfinite(r)].tolist())
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for w, (df, close, fc) in wins.items():
            c = close.values
            n = len(c)
            reg = df["regime"].astype(str).reset_index(drop=True).values
            cell = np.arange(n) // H
            seen = set()
            for i in range(n):
                if reg[i] != "mean_reversion":
                    continue
                if cell[i] in seen:
                    continue
                seen.add(cell[i])
                f = fc.iloc[i]
                if i + H < n:
                    r1 = c[i + H] / c[i] - 1.0 - drift
                    if np.isfinite(r1) and np.isfinite(f):
                        xs.append(float(f)); ys.append(float(r1))
                        if i + 2 * H < n:
                            r2 = c[i + 2 * H] / c[i + H] - 1.0 - drift
                            if np.isfinite(r2):
                                xs2.append(float(f)); ys2.append(float(r2))

    slope, t_main, n_cases = _slope_t(xs, ys)
    slope2, t_second, n_cases2 = _slope_t(xs2, ys2)
    n_pos = int(np.sum(np.asarray(xs) > 0)) if xs else 0

    sup_pass = None if t_second is None else bool(t_second < 2)
    counts = {"cases with forecast > 0": n_pos, "cases": int(n_cases),
              "second-day cases": int(n_cases2)}

    if n_pos < 200:
        status = "not observable"
        decided = f"Only {n_pos} cases with forecast > 0, below the plan's minimum of 200."
    elif t_main is None:
        status = "inconclusive"
        decided = "The main slope's t could not be computed, so neither confirm nor reject is met."
    elif slope > 0 and t_main >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Main slope positive with t >= 2 over at least 200 cases with forecast > 0, and the second-day slope's t is below 2."
        else:
            status = "inconclusive"
            decided = "Main t >= 2 but the second-day slope's t is not below 2, which the plan calls inconclusive."
    elif slope < 0 and t_main <= -2:
        status = "rejected"
        decided = "Main slope negative with t <= -2 over at least 200 cases with forecast > 0."
    else:
        status = "inconclusive"
        decided = "Main t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of drift-adjusted 24-bar forward return on forecast",
            "value": slope,
            "statistic": None if t_main is None else {"name": "OLS slope t", "value": t_main},
            "threshold": "positive slope with t >= 2 confirms (with second-day check), negative with t <= -2 rejects",
        },
        "supporting_check": {
            "name": "second-day (t+24 to t+48) slope t below 2",
            "value": t_second,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are the first regime 'mean_reversion' bar in each 24-row grid cell from each window's first row, all such cases (forecast 0 included) enter the regression, the drift is the coin's mean non-overlapping 24-bar return over all windows (used for both days), and the second-day regression uses those cases whose t+48 close lies in the same window."),
    }
