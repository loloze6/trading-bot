import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    RISE = "debug_info.components.rise14.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            ret60 = close / close.shift(60) - 1.0
            # where the 60-bar return cannot be recomputed inside the window, use the detector's recorded decision
            trending = np.where(ret60.notna(), ret60 > 0, df["regime"].astype(str) == "trending")
            trending = pd.Series(trending, index=df.index).astype(bool)
            has_rise = df[RISE].notna() if RISE in df.columns else pd.Series(False, index=df.index)
            fc = df["forecast"].astype(float)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & trending & has_rise & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    reading = ("The plan's situation is taken as a positive 60-bar return (recomputed from closes inside the window, "
               "falling back to the recorded regime where 60 prior bars are missing) with the graded 14-bar rise recorded and a long position, "
               "not requiring the 14-bar rise itself to be positive; the coin's mean 7-bar return is the mean over all its 7-bar grid samples in all windows; "
               "the timing gain is computed on the book's daily returns before fees (value before the day's trade over the previous value after rebalance).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "t of the slope of demeaned 7-bar forward return on forecast",
                             "value": None, "statistic": None,
                             "threshold": "slope t >= 2 confirms (with positive timing gain), t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars with a positive 60-bar return "
                           "and a recorded 14-bar rise, so the config does not do what the plan's Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. main measure ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                fwd = close[i + H] / close[i] - 1.0
                coin_rows.append({"coin": coin, "fwd": fwd,
                                  "regime": str(df["regime"].iloc[i]),
                                  "forecast": df["forecast"].iloc[i]})
        if coin_rows:
            cdf = pd.DataFrame(coin_rows)
            mu = cdf["fwd"].mean()
            cdf["ex"] = cdf["fwd"] - mu
            rows.append(cdf)

    if rows:
        allr = pd.concat(rows, ignore_index=True)
        tr = allr[(allr["regime"] == "trending")].dropna(subset=["ex", "forecast"])
    else:
        tr = pd.DataFrame(columns=["ex", "forecast"])
    n_cases = int(len(tr))
    n_pos = int((tr["forecast"].astype(float) > 0).sum()) if n_cases else 0

    slope = None
    t_slope = None
    if n_cases >= 3:
        x = tr["forecast"].astype(float).values
        y = tr["ex"].astype(float).values
        sxx = np.sum((x - x.mean()) ** 2)
        if sxx > 0:
            b = np.sum((x - x.mean()) * (y - y.mean())) / sxx
            a = y.mean() - b * x.mean()
            resid = y - (a + b * x)
            se = np.sqrt(np.sum(resid ** 2) / (n_cases - 2) / sxx)
            slope = float(b)
            t_slope = float(b / se) if se > 0 else None

    # ---------- 3. supporting check: timing gain ----------
    book_parts = []
    for coin, wins in bars.items():
        coin_frames = []
        all_r = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            df["day"] = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D")
            d = df.groupby("day").last().reset_index()
            close = d["close"].astype(float)
            r = close / close.shift(1) - 1.0
            all_r.append(r.dropna())
            gross = d["total_portfolio_value"].astype(float) / d["postRebalance_total_value"].astype(float).shift(1) - 1.0
            pos = d["postRebalance_current_allocation"].astype(float).shift(1)
            coin_frames.append(pd.DataFrame({"day": d["day"], "gross": gross, "pos": pos}).iloc[1:])
        if not coin_frames:
            continue
        mu_d = pd.concat(all_r).mean() if all_r else np.nan
        cf = pd.concat(coin_frames, ignore_index=True).dropna(subset=["gross", "pos"])
        cf["market"] = cf["pos"] * mu_d
        cf["coin"] = coin
        book_parts.append(cf)

    timing = None
    if book_parts:
        bp = pd.concat(book_parts, ignore_index=True).dropna(subset=["gross", "market"])
        if len(bp):
            daily = bp.groupby("day")[["gross", "market"]].mean()
            timing = float(daily["gross"].mean() - daily["market"].mean())
    timing_ok = None if timing is None else bool(timing > 0)

    # ---------- 4. decision ----------
    counts = {"independent 7-bar cases in trending regime": n_cases,
              "trending cases with forecast above 0": n_pos}
    if n_cases < 100 or n_pos < 30:
        status = "not observable"
        decided_by = ("The plan's minimum of 100 independent 7-bar trending cases with at least 30 having a forecast above 0 "
                      f"is not reached ({n_cases} cases, {n_pos} with forecast above 0).")
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed (no variation in the forecast), so neither confirm nor reject is met."
    elif t_slope >= 2 and slope > 0:
        if timing_ok:
            status = "confirmed"
            decided_by = "The slope is positive with t of 2 or more and the timing gain is positive (confirm rule)."
        else:
            status = "inconclusive"
            decided_by = "The slope's t is 2 or more but the timing gain is 0 or below, which the plan calls inconclusive."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "The slope is negative with t of -2 or less (reject rule)."
    else:
        status = "inconclusive"
        decided_by = "The slope's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "t of the slope of demeaned 7-bar forward return on forecast (trending, non-overlapping)",
                         "value": t_slope,
                         "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
                         "threshold": "positive slope with t >= 2 (and positive timing gain) confirms; t <= -2 rejects; otherwise inconclusive"},
        "supporting_check": {"name": "timing gain: book mean daily return before costs minus market-rise part",
                             "value": timing, "passed": timing_ok},
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
