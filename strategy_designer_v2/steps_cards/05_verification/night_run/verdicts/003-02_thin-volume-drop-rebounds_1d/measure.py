import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    FALL = "debug_info.components.fall.last_history_value"
    THIN = "debug_info.components.thin.last_history_value"

    # ---------- 1. Situation check ----------
    # The plan's situation: a down day (1-day return < 0) on volume below its prior 30-day mean.
    # The expected side is long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if "forecast" not in df.columns or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)

            # Prefer the recorded raw values; where a value is missing, rebuild it from the prices.
            ret_re = close / close.shift(1) - 1.0
            vr_re = vol / vol.shift(1).rolling(30, min_periods=30).mean()
            if FALL in df.columns:
                ret = pd.to_numeric(df[FALL], errors="coerce").fillna(ret_re)
            else:
                ret = ret_re
            if THIN in df.columns:
                lvr = pd.to_numeric(df[THIN], errors="coerce")
                vr = np.exp(lvr).fillna(vr_re)
            else:
                vr = vr_re

            situation = (ret < 0) & (vr < 1.0)  # NaN comparisons give False
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean of forecast/10 x excess 5-bar return, non-overlapping grid, forecast > 0, pooled"
    thr = "t >= 2 to confirm (with check difference > 0), t <= -2 to reject"
    sup_name = "mean excess 5-bar return above minus below the median positive forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {
                "agreement": float(agreement) if agreement is not None else None,
                "passed": False,
            },
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"grid cases with forecast > 0": None},
            "decided_by": (
                "Fewer than 90% of the active bars are long forecasts on down days with volume below "
                "its prior 30-day mean (no active bars at all)."
                if agreement is None
                else "Fewer than 90% of the active bars are long forecasts on down days with volume "
                     "below its prior 30-day mean, the plan's situation."
            ),
            "reading": "The situation is read as 1-day return < 0 and volume / prior 30-day mean volume < 1, long side.",
        }

    # ---------- 2. Criterion ----------
    fcs, exs = [], []
    for coin, wins in bars.items():
        coin_rows = []  # (forecast, fwd return) over all windows' grids
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            for i in range(0, len(df) - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                coin_rows.append((fc[i], c1 / c0 - 1.0))
        if not coin_rows:
            continue
        arr = np.array(coin_rows, dtype=float)
        coin_mean = float(np.mean(arr[:, 1]))
        mask = np.isfinite(arr[:, 0]) & (arr[:, 0] > 0)
        for f, r in arr[mask]:
            fcs.append(f)
            exs.append(r - coin_mean)

    fcs = np.array(fcs, dtype=float)
    exs = np.array(exs, dtype=float)
    n = int(len(fcs))
    counts = {"grid cases with forecast > 0": n}

    reading = (
        "The coin's mean 5-bar return is taken over the same non-overlapping grid (positions 0, 5, 10, ... "
        "of each window, with t+5 inside the window) across all its windows; the supporting check compares "
        "cases strictly above and strictly below the median positive forecast, ties left out; fewer than 30 "
        "cases gives 'not observable'."
    )

    value = None
    tstat = None
    if n > 0:
        x = fcs / 10.0 * exs
        value = float(np.mean(x))
        if n > 1:
            sd = float(np.std(x, ddof=1))
            if sd > 0:
                tstat = float(value / (sd / np.sqrt(n)))

    diff = None
    if n > 0:
        med = float(np.median(fcs))
        hi = exs[fcs > med]
        lo = exs[fcs < med]
        if len(hi) > 0 and len(lo) > 0:
            diff = float(np.mean(hi) - np.mean(lo))
    check_pass = None if diff is None else bool(diff > 0)

    main = {
        "name": main_name,
        "value": value,
        "statistic": {"name": "t of the mean", "value": tstat} if tstat is not None else None,
        "threshold": thr,
    }
    sup = {"name": sup_name, "value": diff, "passed": check_pass}

    if n < 30:
        status = "not observable"
        decided = f"Only {n} grid cases with forecast > 0, fewer than the 30 the plan requires."
    elif tstat is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed (zero spread), so neither confirm nor reject is met."
    elif tstat >= 2 and check_pass:
        status = "confirmed"
        decided = "The main measure's t is >= 2 and the supporting check's difference is > 0."
    elif tstat <= -2:
        status = "rejected"
        decided = "The main measure's t is <= -2."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "The main measure's t is >= 2 but the supporting check's difference is not > 0."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
