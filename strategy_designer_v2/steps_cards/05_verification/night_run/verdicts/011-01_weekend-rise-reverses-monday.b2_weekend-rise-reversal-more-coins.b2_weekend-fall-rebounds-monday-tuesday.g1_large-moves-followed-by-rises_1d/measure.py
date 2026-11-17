import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    RAW = "debug_info.components.move_sq.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: the situation is any 1-day move, up or down, and the expected side is long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            ret1 = close / close.shift(1) - 1.0  # inside the window only
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # Use the component's raw value where recorded; otherwise use the price move.
            sit = pd.Series(False, index=df.index)
            has_raw = raw.notna()
            sit[has_raw] = raw[has_raw].abs() > 0
            use_px = (~has_raw) & ret1.notna()
            sit[use_px] = ret1[use_px].abs() > 0
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of excess next-2-bar return on forecast"
    threshold = "slope > 0 with t >= 2 (confirm, with supporting check); slope < 0 with t <= -2 (reject)"
    sup_name = "mean excess 2-bar return in top fifth of forecast > 0"
    reading = ("The coin's mean 2-bar return is the mean of its non-overlapping grid returns over all its windows; "
               "the OLS has an intercept; the top fifth is grid bars with forecast at or above the pooled 80th "
               "percentile of grid forecasts; the situation is a nonzero component value (or nonzero 1-day price "
               "move where it is not recorded) with a positive forecast.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are bars with a 1-day move on the long side, "
                           "as the plan's situation requires." if n_active > 0 else
                           "The config never takes a position, while the plan's situation (any 1-day move, long) "
                           "should be active on almost every bar."),
            "reading": reading,
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
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, fc[i], c1 / c0 - 1.0))

    s = pd.DataFrame(rows, columns=["coin", "forecast", "ret"])
    if len(s) > 0:
        coin_mean = s.groupby("coin")["ret"].mean()
        s["excess"] = s["ret"] - s["coin"].map(coin_mean)
        s = s.dropna(subset=["forecast", "excess"])

    n_cases = int(len(s))
    slope = None
    t = None
    n_top = 0
    sup_val = None
    sup_pass = None

    if n_cases >= 3 and s["forecast"].nunique() > 1:
        x = s["forecast"].values.astype(float)
        y = s["excess"].values.astype(float)
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else float("nan")

    if n_cases > 0:
        q80 = float(s["forecast"].quantile(0.8))
        top = s[s["forecast"] >= q80]
        n_top = int(len(top))
        if n_top > 0:
            sup_val = float(top["excess"].mean())
            sup_pass = bool(sup_val > 0)

    counts = {"non-overlapping cases": n_cases, "cases in the top fifth": n_top}
    stat = {"name": "OLS slope t", "value": t} if t is not None else None
    main = {"name": main_name, "value": slope, "statistic": stat, "threshold": threshold}
    sup = {"name": sup_name, "value": sup_val, "passed": sup_pass}
    sc = {"agreement": agreement, "passed": True}

    if n_cases < 500 or n_top < 100:
        status = "not observable"
        decided = ("Minimum counts not reached: at least 500 non-overlapping cases and 100 in the top fifth "
                   f"are required (got {n_cases} and {n_top}).")
    elif slope is None or t is None or not np.isfinite(t):
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the top-fifth mean excess return is above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check (top-fifth mean excess return > 0) fails."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
