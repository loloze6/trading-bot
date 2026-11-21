import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    MIN_CASES = 100
    MOM_COL = "debug_info.components.mom30.last_history_value"

    # ---------- 1. Situation check: 30-day return > 0, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            # raw 30-day change: recorded mom30 (same quantity as the detector's ret30),
            # else recomputed from closes inside the window, else the detector's recorded regime
            if MOM_COL in df.columns:
                ret30 = pd.to_numeric(df[MOM_COL], errors="coerce")
            else:
                ret30 = pd.Series(np.nan, index=df.index)
            recomputed = close / close.shift(30) - 1.0
            ret30 = ret30.where(ret30.notna(), recomputed)
            sit = ret30 > 0
            if "regime" in df.columns:
                sit = sit.where(ret30.notna(), df["regime"].astype(str) == "trending")
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & sit.fillna(False).astype(bool) & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("Situation taken as the regime gate (30-day return above 0, read from the recorded mom30 raw value, "
               "else recomputed from closes in the window, else the recorded regime) with a long forecast, not requiring "
               "the range part to be positive since the forecast averages both parts; the coin's mean 7-bar return is the "
               "mean over all non-overlapping grid bars of all its windows; the supporting check splits the cases at the "
               "median forecast (above median = top half, at or below = bottom half), using excess returns.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "t of mean of forecast/10 x excess 7-bar return", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject"},
            "supporting_check": None,
            "counts": {"non-overlapping cases with forecast above 0": None},
            "decided_by": ("Fewer than 90% of active bars have a positive 30-day return with a long forecast, "
                           "so the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                coin_rows.append((coin, fc[i], c1 / c0 - 1.0))
        if not coin_rows:
            continue
        mean_ret = float(np.mean([r[2] for r in coin_rows]))
        for c, f, r in coin_rows:
            if np.isfinite(f) and f > 0:
                rows.append((f, r - mean_ret))

    n_cases = len(rows)
    counts = {"non-overlapping cases with forecast above 0": n_cases}

    t_val = None
    mean_prod = None
    if n_cases >= 2:
        f = np.array([r[0] for r in rows], dtype=float)
        ex = np.array([r[1] for r in rows], dtype=float)
        prod = f / 10.0 * ex
        mean_prod = float(prod.mean())
        sd = float(prod.std(ddof=1))
        t_val = float(mean_prod / (sd / np.sqrt(n_cases))) if sd > 0 else None
        med = np.median(f)
        top, bot = ex[f > med], ex[f <= med]
        if len(top) > 0 and len(bot) > 0:
            diff = float(top.mean() - bot.mean())
            check_pass = bool(diff > 0)
        else:
            diff, check_pass = None, None
    elif n_cases == 1:
        f0, e0 = rows[0]
        mean_prod = float(f0 / 10.0 * e0)
        diff, check_pass = None, None
    else:
        diff, check_pass = None, None

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases with a forecast above 0, fewer than the plan's minimum of 100."
    elif t_val is not None and t_val >= 2:
        if check_pass:
            status = "confirmed"
            decided = "Main t is 2 or more with at least 100 cases and the top-minus-bottom half excess return is above 0."
        else:
            status = "inconclusive"
            decided = "Main t is 2 or more but the supporting check (top-minus-bottom half excess return above 0) fails."
    elif t_val is not None and t_val <= -2:
        status = "rejected"
        decided = "Main t is -2 or less with at least 100 cases."
    else:
        status = "inconclusive"
        decided = "Main t lies between -2 and 2 with at least 100 cases."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": {
            "name": "mean of forecast/10 x (7-bar forward return minus coin mean 7-bar return)",
            "value": mean_prod,
            "statistic": None if t_val is None else {"name": "t of the mean", "value": t_val},
            "threshold": "t >= 2 (with check > 0) confirms, t <= -2 rejects, with at least 100 cases",
        },
        "supporting_check": {
            "name": "top-half minus bottom-half forecast mean excess 7-bar return",
            "value": diff,
            "passed": check_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
