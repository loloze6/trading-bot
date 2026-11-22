import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.range_pos.last_history_value"
    PERIOD = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # recompute the 30-close range position from prices where the raw value is missing
            hi = close.rolling(PERIOD, min_periods=PERIOD).max()
            lo = close.rolling(PERIOD, min_periods=PERIOD).min()
            rng = hi - lo
            pos_px = np.where(rng > 0, 40.0 * (close - lo) / rng - 20.0, 0.0)
            pos_px = pd.Series(pos_px, index=df.index).where(hi.notna())
            pos = raw.where(raw.notna(), pos_px)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & pos.notna() & (pos != 0) & (np.sign(pos) == np.sign(fc))
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading_base = ("The situation is read as the graded range position: a bar is on the plan's side when the "
                    "forecast's sign equals the sign of the raw 30-close range position (above the middle long, "
                    "below short, as 'more the closer to the top' implies); the regression uses every grid bar "
                    "including zero forecasts, the coin mean is the mean of its grid 10-bar returns over all "
                    "windows, and the book's daily returns are bar-to-bar postRebalance_total_value changes "
                    "averaged over coins per timestamp.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars have a forecast whose sign matches the side of the close's "
                           "position in its 30-day closing range (long above the middle, short below)."),
            "reading": reading_base,
        }

    # ---------- 2. main measure: pooled slope on a non-overlapping 10-bar grid ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H < n:
                    c0, c1 = close[i], close[i + H]
                    if np.isfinite(c0) and np.isfinite(c1) and c0 > 0 and np.isfinite(fc[i]):
                        rows.append((coin, c1 / c0 - 1.0, float(fc[i])))
    g = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    n_cases = int(len(g))

    slope = None
    tval = None
    if n_cases >= 3:
        g["ex"] = g["ret"] - g.groupby("coin")["ret"].transform("mean")
        if g["fc"].std() > 0:
            lr = stats.linregress(g["fc"].values, g["ex"].values)
            slope = float(lr.slope)
            tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- supporting check: timing gain ----------
    book_parts = []
    mkt_parts = []
    for coin, wins in bars.items():
        rets_all = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            rets_all.append((c / c.shift(1) - 1.0).iloc[1:])
        rr = pd.concat(rets_all) if rets_all else pd.Series(dtype=float)
        mu = float(rr.dropna().mean()) if rr.notna().any() else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            v = pd.to_numeric(df["postRebalance_total_value"], errors="coerce")
            a = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            day = ts.dt.floor("D")
            last = pd.DataFrame({"day": day, "v": v, "a": a}).groupby("day").last()
            br = last["v"] / last["v"].shift(1) - 1.0
            mg = last["a"].shift(1) * mu
            sub = pd.DataFrame({"book": br, "mkt": mg}).iloc[1:]
            book_parts.append(sub["book"])
            mkt_parts.append(sub["mkt"])
    timing = None
    if book_parts:
        bk = pd.concat(book_parts)
        mk = pd.concat(mkt_parts)
        bday = bk.dropna().groupby(level=0).mean()
        mday = mk.dropna().groupby(level=0).mean()
        if len(bday) > 0 and len(mday) > 0:
            timing = float(bday.mean() - mday.mean())
    timing_pass = None if timing is None else bool(timing > 0)

    # ---------- decision ----------
    if n_cases < 200:
        status = "not observable"
        decided = f"Fewer than 200 grid cases ({n_cases}), the plan's minimum count."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if timing_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 over at least 200 grid cases and the timing gain is above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the timing gain is at or below 0, which the plan calls inconclusive."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 over at least 200 grid cases."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "pooled slope of 10-bar forward return minus coin mean on forecast",
            "value": slope,
            "statistic": None if tval is None else {"name": "OLS slope t", "value": tval},
            "threshold": "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; over at least 200 grid cases",
        },
        "supporting_check": {
            "name": "timing gain (book mean daily return minus market-rise gain) above 0",
            "value": timing,
            "passed": timing_pass,
        },
        "counts": {"grid cases": n_cases},
        "decided_by": decided,
        "reading": reading_base,
    }
