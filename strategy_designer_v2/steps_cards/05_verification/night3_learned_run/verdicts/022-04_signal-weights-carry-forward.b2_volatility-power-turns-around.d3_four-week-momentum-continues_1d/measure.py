import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.mom28.last_history_value"

    # ---------- 1. Situation check: forecast sign must follow the sign of the 28-day return ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                # fill missing raw values from prices (inside the window only)
                raw = raw.where(raw.notna(), close / close.shift(28) - 1.0)
            else:
                raw = close / close.shift(28) - 1.0
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            mask = fc.notna() & (fc != 0) & raw.notna()
            n_active += int(mask.sum())
            n_agree += int((np.sign(fc[mask]) == np.sign(raw[mask])).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"non-overlapping cases": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars have a forecast whose sign is the sign of the "
                           "28-day return (long after a rise, short after a fall), as the Fidelity states."),
            "reading": "Side taken as the sign of the raw 28-day return (mom28 last_history_value, recomputed from closes where missing).",
        }

    # ---------- 2. Main measure: pooled OLS slope of demeaned 5-bar forward return on forecast ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                r = close[t + H] / close[t] - 1.0
                if np.isfinite(r) and np.isfinite(fc[t]):
                    rows.append((coin, w, fc[t], r))
    cases = pd.DataFrame(rows, columns=["coin", "window", "forecast", "ret"])
    n_cases = int(len(cases))

    slope = None
    t_stat = None
    if n_cases >= 3:
        cases["y"] = cases["ret"] - cases.groupby("coin")["ret"].transform("mean")
        x = cases["forecast"].values.astype(float)
        y = cases["y"].values.astype(float)
        if np.std(x) > 0:
            lr = stats.linregress(x, y)
            slope = float(lr.slope)
            t_stat = float(lr.slope / lr.stderr) if lr.stderr > 0 else None

    # ---------- 3. Supporting check: timing gain of the book (before costs) ----------
    pieces = []
    for coin, wins in bars.items():
        coin_parts = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            nxt = close.shift(-1) / close - 1.0  # inside the window only
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            d = pd.DataFrame({
                "ts": pd.to_datetime(df["timestamp"], utc=True).dt.floor("D"),
                "window": w,
                "ret": nxt,
                "alloc": alloc,
            })
            coin_parts.append(d)
        cd = pd.concat(coin_parts, ignore_index=True)
        cd = cd.dropna(subset=["ret", "alloc"])
        mu = cd["ret"].mean()
        cd["gain"] = cd["alloc"] * cd["ret"]
        cd["mkt"] = cd["alloc"] * mu
        cd["coin"] = coin
        pieces.append(cd)
    timing = None
    if pieces:
        allp = pd.concat(pieces, ignore_index=True)
        if len(allp):
            daily = allp.groupby(["window", "ts"])[["gain", "mkt"]].mean()
            timing = float(daily["gain"].mean() - daily["mkt"].mean())
    timing_pass = None if timing is None else bool(timing > 0)

    # ---------- 4. Decision ----------
    if n_cases < 500 or t_stat is None:
        status = "not observable"
        decided_by = f"Only {n_cases} non-overlapping cases, below the plan's minimum of 500."
    elif slope > 0 and t_stat >= 2 and timing_pass:
        status = "confirmed"
        decided_by = "The slope is positive with t >= 2 and the timing gain is above 0."
    elif slope < 0 and t_stat <= -2:
        status = "rejected"
        decided_by = "The slope is negative with t <= -2."
    elif slope > 0 and t_stat >= 2:
        status = "inconclusive"
        decided_by = "The slope is positive with t >= 2 but the timing gain is 0 or below."
    else:
        status = "inconclusive"
        decided_by = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "pooled slope of demeaned 5-bar forward return on forecast",
            "value": slope,
            "statistic": None if t_stat is None else {"name": "OLS t of slope", "value": t_stat},
            "threshold": "confirm: slope > 0 with t >= 2 (and timing gain > 0); reject: slope < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "book timing gain (mean daily return before costs minus market-rise gain)",
            "value": timing,
            "passed": timing_pass,
        },
        "counts": {"non-overlapping cases": n_cases},
        "decided_by": decided_by,
        "reading": ("The regression is ordinary least squares with an intercept on all grid bars (positions 0,5,10,... with "
                    "close[t+5] in the window), the coin mean is the mean of its grid 5-bar returns over all windows, and the "
                    "book is the daily mean over coins of postRebalance_current_allocation x next-bar return, per window and day."),
    }
