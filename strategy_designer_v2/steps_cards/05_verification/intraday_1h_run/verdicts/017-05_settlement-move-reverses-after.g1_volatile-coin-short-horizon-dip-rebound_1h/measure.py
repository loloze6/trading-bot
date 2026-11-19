import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    RAW = "debug_info.components.fall2h.last_history_value"
    REGIME = "mean_reversion"
    MIN_POS = 300

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            # the 2-hour move: the component's raw value (2-bar return / (168-bar std * sqrt 2));
            # where not recorded, the 2-bar return from the prices (same sign)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            back_ret = close / close.shift(H) - 1.0
            move = raw.where(raw.notna(), back_ret)
            in_regime = df["regime"].astype(str) == REGIME
            active = fc.notna() & (fc != 0)
            situation = in_regime & (move < 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement),
                                "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are long bars in the volatile regime "
                           "(volrank >= 0.5) after a 2-hour fall, as the plan's Fidelity requires"
                           if n_active > 0 else "The record has no active bars to compare with the plan's situation."),
            "reading": "The regime detector's decision is read from the recorded `regime` column; the 2-hour fall from the fall2h raw value (or the 2-bar price return where not recorded).",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_grid_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            reg = df["regime"].astype(str).to_numpy()
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_grid_rets.append(r)
                if reg[i] == REGIME and np.isfinite(fc[i]):
                    coin_rows.append((r, fc[i]))
        if len(coin_grid_rets) == 0:
            continue
        mu = float(np.mean(coin_grid_rets))
        for r, f in coin_rows:
            rows.append((r - mu, f))

    if rows:
        arr = np.array(rows, dtype=float)
        y, x = arr[:, 0], arr[:, 1]
    else:
        y, x = np.array([]), np.array([])

    n_sample = int(len(y))
    n_pos = int((x > 0).sum())

    slope, t_slope = None, None
    if n_sample >= 3 and np.ptp(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    top_mean, check_passed, n_top = None, None, 0
    if n_pos > 0:
        xp = x[x > 0]
        yp = y[x > 0]
        q80 = np.quantile(xp, 0.8)
        sel = xp >= q80
        n_top = int(sel.sum())
        if n_top > 0:
            top_mean = float(np.mean(yp[sel]))
            check_passed = bool(top_mean > 0)

    if n_pos < MIN_POS:
        status = "not observable"
        decided = f"Only {n_pos} grid bars with forecast > 0, fewer than the plan's minimum of 300."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t_slope >= 2 and check_passed:
        status = "confirmed"
        decided = "The slope is positive with t >= 2, the top-quintile mean excess return is above 0, and there are at least 300 grid bars with forecast > 0."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope t is >= 2 but the top-quintile mean excess return is not above 0, which the plan calls inconclusive."
    elif slope < 0 and t_slope <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2, with at least 300 grid bars with forecast > 0."
    else:
        status = "inconclusive"
        decided = "The slope t is between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "OLS slope of excess 2-bar forward return on forecast (mean_reversion grid bars, pooled)",
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 300 grid bars with forecast > 0",
        },
        "supporting_check": {
            "name": "mean excess 2-bar return over top quintile of positive forecasts > 0",
            "value": top_mean,
            "passed": check_passed,
        },
        "counts": {
            "grid bars where forecast > 0": n_pos,
            "grid bars in mean_reversion regime": n_sample,
            "top-quintile grid bars": n_top,
        },
        "decided_by": decided,
        "reading": ("The coin's mean 2-bar return is taken over the non-overlapping 2-bar grid of all its bars in all windows, "
                    "the regression is OLS with an intercept, the top quintile is positive-forecast grid bars at or above their 80th percentile, "
                    "and the regime is read from the recorded `regime` column."),
    }
