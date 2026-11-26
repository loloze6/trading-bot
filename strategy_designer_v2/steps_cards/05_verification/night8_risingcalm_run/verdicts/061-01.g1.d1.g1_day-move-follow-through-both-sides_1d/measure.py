import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.day_move_swing.last_history_value"
    H = 5
    MIN_CASES = 300

    # ---------- 1. Situation check ----------
    # Situation: the day's move, signed. Side: long after an up day, short after a down day.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            day_ret = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # Use the recorded raw value; fall back to the day's return from prices.
            move = raw.where(raw.notna(), day_ret)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & move.notna() & (move != 0) & (np.sign(move) == np.sign(fc))
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("The forecast's sign does not follow the sign of the day's move "
                           "(long after up days, short after down days) on at least 90% of active bars."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
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
                rows.append((coin, c1 / c0 - 1.0, fc[t]))

    data = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    if len(data):
        # coin's mean 5-bar return over all its windows (non-overlapping grid)
        data["excess"] = data["ret"] - data.groupby("coin")["ret"].transform("mean")
        data = data[np.isfinite(data["fc"]) & np.isfinite(data["excess"])]
    n_cases = int(len(data))

    slope = None
    t_slope = None
    top_mean = None
    n_top = 0
    if n_cases >= 3 and data["fc"].nunique() > 1:
        x = data["fc"].values.astype(float)
        y = data["excess"].values.astype(float)
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr > 0 else 0.0
    if n_cases > 0:
        a = data["fc"].abs()
        q = a.quantile(0.8)
        top = data[a >= q]
        n_top = int(len(top))
        if n_top > 0:
            top_mean = float((np.sign(top["fc"]) * top["excess"]).mean())

    check_passed = (top_mean > 0) if top_mean is not None else None

    if n_cases < MIN_CASES or slope is None:
        status = "not observable"
        decided_by = f"Fewer than {MIN_CASES} grid cases ({n_cases}), the plan's minimum count."
    elif slope > 0 and t_slope >= 2 and check_passed:
        status = "confirmed"
        decided_by = "Slope above 0 with t >= 2 over at least 300 cases, and the top-fifth mean is above 0."
    elif slope < 0 and t_slope <= -2 and top_mean is not None and top_mean < 0:
        status = "rejected"
        decided_by = "Slope below 0 with t <= -2 over at least 300 cases, and the top-fifth mean is below 0."
    else:
        status = "inconclusive"
        if abs(t_slope) < 2:
            decided_by = "Inconclusive: the slope's |t| is below 2."
        else:
            decided_by = "Inconclusive: the slope's sign disagrees with the top-fifth check."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "OLS slope of excess 5-bar return on forecast (non-overlapping grid)",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": "slope > 0 with t >= 2 to confirm; slope < 0 with t <= -2 to reject; over at least 300 cases",
        },
        "supporting_check": {
            "name": "mean sign(forecast) x excess 5-bar return in top fifth of |forecast|",
            "value": top_mean,
            "passed": check_passed,
        },
        "counts": {"grid cases": n_cases, "top-fifth cases": n_top},
        "decided_by": decided_by,
        "reading": ("All grid bars with a 5-bar forward return inside the window are cases (all coins pooled, "
                    "forecast 0 included), the coin's mean is over its grid returns in all windows, the top fifth "
                    "is |forecast| at or above its 80th percentile, and fewer than 300 cases is reported as not observable."),
    }
