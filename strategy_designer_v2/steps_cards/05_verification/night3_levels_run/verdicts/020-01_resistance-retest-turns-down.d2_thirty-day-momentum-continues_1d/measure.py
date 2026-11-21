import numpy as np
import pandas as pd

RAW_COL = "debug_info.components.ret30.last_history_value"
H = 5
MIN_CASES = 300


def _num(df, col):
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    return pd.Series(np.nan, index=df.index, dtype=float)


def measure(bars):
    # ---------- 1. situation check ----------
    # Situation: the 30-day return; outcome "rises more" -> long when the 30-day return is positive,
    # short when negative (sign of the raw component value, which standardise keeps).
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            close = _num(df, "close").values
            fc = _num(df, "forecast").values
            raw = _num(df, RAW_COL).values.copy()
            # recompute the 30-day return from prices where the component is not recorded
            for i in range(len(df)):
                if np.isnan(raw[i]) and i >= 30 and close[i - 30] > 0:
                    raw[i] = (close[i] / close[i - 30] - 1.0) * 100.0
            for i in range(len(df)):
                if np.isnan(fc[i]) or fc[i] == 0:
                    continue
                n_active += 1
                if not np.isnan(raw[i]) and raw[i] != 0 and np.sign(raw[i]) == np.sign(fc[i]):
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"non-overlapping grid cases with a recorded forecast": None,
                       "active bars": int(n_active)},
            "decided_by": ("The forecast's sign agrees with the sign of the 30-day return (long after a rise, "
                           "short after a fall) on only %.1f%% of active bars, below 90%%." % (100 * agreement)),
            "reading": "Expected side taken as the sign of the raw 30-day return; bars with no computable 30-day return count as disagreeing.",
        }

    # ---------- 2. main measure: pooled OLS of de-drifted 5-bar returns on the forecast ----------
    xs, ys = [], []
    book_rows = []
    for coin in sorted(bars):
        grid = []  # (forward return, forecast)
        daily_all = []
        per_window = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            close = _num(df, "close").values
            fc = _num(df, "forecast").values
            alloc = _num(df, "postRebalance_current_allocation").values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            n = len(df)
            for i in range(0, n - H, H):
                if close[i] > 0 and not np.isnan(close[i + H]):
                    grid.append((close[i + H] / close[i] - 1.0, fc[i]))
            r1 = np.full(n, np.nan)
            if n > 1:
                r1[:-1] = close[1:] / close[:-1] - 1.0
            daily_all.extend([v for v in r1 if not np.isnan(v)])
            per_window.append((ts, alloc, r1))
        if not grid:
            continue
        g = np.array(grid, dtype=float)
        drift = np.nanmean(g[:, 0])
        mask = ~np.isnan(g[:, 0]) & ~np.isnan(g[:, 1])
        xs.extend(g[mask, 1].tolist())
        ys.extend((g[mask, 0] - drift).tolist())
        mean_daily = float(np.mean(daily_all)) if daily_all else np.nan
        for ts, alloc, r1 in per_window:
            m = ~np.isnan(alloc) & ~np.isnan(r1) & ts.notna().values
            if m.sum() == 0:
                continue
            book_rows.append(pd.DataFrame({
                "ts": ts.values[m],
                "gain": alloc[m] * r1[m],
                "mkt": alloc[m] * mean_daily,
            }))

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_cases = int(len(x))

    slope = None
    t_stat = None
    if n_cases >= 3:
        xm = x - x.mean()
        sxx = float(np.sum(xm ** 2))
        if sxx > 0:
            b = float(np.sum(xm * (y - y.mean())) / sxx)
            a = y.mean() - b * x.mean()
            resid = y - (a + b * x)
            s2 = float(np.sum(resid ** 2) / (n_cases - 2))
            se = np.sqrt(s2 / sxx)
            slope = b
            t_stat = float(b / se) if se > 0 else None

    # ---------- supporting check: timing gain ----------
    timing = None
    if book_rows:
        bk = pd.concat(book_rows, ignore_index=True)
        daily = bk.groupby("ts")[["gain", "mkt"]].mean()
        timing = float(daily["gain"].mean() - daily["mkt"].mean())
    timing_pass = None if timing is None else bool(timing > 0)

    # ---------- decision ----------
    if n_cases < MIN_CASES or t_stat is None:
        status = "not observable"
        decided_by = ("Only %d non-overlapping grid cases with a recorded forecast, fewer than the plan's minimum of 300."
                      % n_cases) if n_cases < MIN_CASES else "The slope's t could not be computed (no variation in the forecast)."
    elif t_stat >= 2 and timing_pass:
        status = "confirmed"
        decided_by = "Confirm: the slope's t is 2 or more and the book's timing gain is above 0."
    elif t_stat <= -2:
        status = "rejected"
        decided_by = "Reject: the slope's t is -2 or less."
    elif t_stat >= 2:
        status = "inconclusive"
        decided_by = "Inconclusive: the slope's t is 2 or more but the book's timing gain is 0 or less."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: the slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "OLS slope of de-drifted 5-bar forward return on the forecast (pooled, non-overlapping grid)",
            "value": slope,
            "statistic": None if t_stat is None else {"name": "OLS t of the slope", "value": t_stat},
            "threshold": "t >= 2 confirms (with timing gain > 0); t <= -2 rejects; at least 300 grid cases",
        },
        "supporting_check": {
            "name": "book's mean daily return before costs minus its gain from the market's rise",
            "value": timing,
            "passed": timing_pass,
        },
        "counts": {"non-overlapping grid cases with a recorded forecast": n_cases},
        "decided_by": decided_by,
        "reading": ("Grid bars are positions 0,5,10,... of each window with a full 5-bar return inside it, the drift is each "
                    "coin's mean grid return over all its windows, zero forecasts count as recorded, and the book is "
                    "position x next-bar return averaged over coins per day with fewer than 300 cases treated as not observable."),
    }
