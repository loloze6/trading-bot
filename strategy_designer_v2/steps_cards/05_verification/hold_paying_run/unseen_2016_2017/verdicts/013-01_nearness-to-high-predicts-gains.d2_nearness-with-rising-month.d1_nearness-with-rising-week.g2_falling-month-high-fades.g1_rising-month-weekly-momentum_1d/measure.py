import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    R7 = "debug_info.components.r7.last_history_value"
    H = 7

    # ---------- 1. Situation check: r30 > 0 (recomputed from prices), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            r30 = close / close.shift(30) - 1.0
            reg_trend = (df["regime"].astype(str) == "trending")
            # where r30 cannot be recomputed inside the window (first 30 rows), use the detector's decision
            sit = np.where(r30.notna(), r30 > 0, reg_trend)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & pd.Series(sit, index=df.index).astype(bool) & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars with a positive "
                           "30-day return, so the config does not trade the plan's situation on its side"
                           if n_active > 0 else "No bar has a non-zero forecast, so the plan's situation is never traded"),
            "reading": "The situation is a positive 30-bar close-to-close return recomputed inside each window "
                       "(the detector's regime where fewer than 30 prior bars exist) and the expected side is long.",
        }

    # ---------- 2. Main measure: pooled regression on the non-overlapping 7-bar grid ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # coin mean 7-bar return over all windows (grid samples, all bars)
        all_f = []
        rows = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            for i in range(0, n, H):
                if i + H < n:
                    f = close[i + H] / close[i] - 1.0
                    if np.isfinite(f):
                        all_f.append(f)
                        if str(df["regime"].iloc[i]) == "trending" and R7 in df.columns:
                            x = pd.to_numeric(df[R7].iloc[i], errors="coerce")
                            if pd.notna(x) and np.isfinite(x):
                                rows.append((float(x), f))
        if not all_f:
            continue
        mu = float(np.mean(all_f))
        for x, f in rows:
            xs.append(x)
            ys.append(f - mu)

    xs = np.asarray(xs, float)
    ys = np.asarray(ys, float)
    n_cases = int(len(xs))
    slope, t_slope = None, None
    if n_cases >= 3 and np.var(xs) > 0:
        res = stats.linregress(xs, ys)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    # ---------- 3. Supporting check: timing part of the book's mean daily gain ----------
    book_parts, mkt_parts = [], []
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df.sort_values("timestamp")["close"].astype(float)
            rets.append(c.pct_change().dropna())
        allr = pd.concat(rets) if rets else pd.Series(dtype=float)
        if allr.empty:
            continue
        mu_d = float(allr.mean())
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            day = ts.dt.floor("D")
            d = pd.DataFrame({
                "day": day,
                "v": pd.to_numeric(df["postRebalance_total_value"], errors="coerce"),
                "a": pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce"),
            })
            d = d.groupby("day", sort=True).last()  # last bar of each day
            br = d["v"] / d["v"].shift(1) - 1.0
            mk = d["a"].shift(1) * mu_d
            ok = br.notna() & mk.notna() & np.isfinite(br)
            book_parts.append(pd.DataFrame({"day": d.index[ok], "coin": coin, "b": br[ok].values}))
            mkt_parts.append(pd.DataFrame({"day": d.index[ok], "coin": coin, "m": mk[ok].values}))
    timing = None
    if book_parts:
        B = pd.concat(book_parts)
        M = pd.concat(mkt_parts)
        if len(B):
            book_mean = float(B.groupby("day")["b"].mean().mean())
            mkt_mean = float(M.groupby("day")["m"].mean().mean())
            timing = book_mean - mkt_mean
    check_pass = None if timing is None else bool(timing > 0)

    # ---------- 4. Decision ----------
    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} independent grid cases in the trending regime, fewer than the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and check_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more with at least 100 independent cases and the timing gain is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less with at least 100 independent cases."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check (timing gain above 0) fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "slope of demeaned 7-bar forward return on raw 7-day return, trending bars",
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": "t >= 2 confirms (with supporting check), t <= -2 rejects, with at least 100 independent cases",
        },
        "supporting_check": {
            "name": "timing part of book's mean daily gain above 0",
            "value": timing,
            "passed": check_pass,
        },
        "counts": {"independent grid cases in the regime": n_cases},
        "decided_by": decided,
        "reading": ("Grid bars are positions 0,7,14,... of each window kept when regime is 'trending' with a 7-bar "
                    "forward return inside the window, the coin mean is the mean of all its grid 7-bar returns over all "
                    "windows, the book of each coin is its postRebalance_total_value at each day's last bar averaged "
                    "across coins per day, and the plan's 'fewer than 100 cases' is reported as not observable."),
    }
