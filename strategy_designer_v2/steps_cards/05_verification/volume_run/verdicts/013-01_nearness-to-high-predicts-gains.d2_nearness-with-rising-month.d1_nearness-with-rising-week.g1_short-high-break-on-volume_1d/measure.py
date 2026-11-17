import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    MIN_N = 300
    NH = "debug_info.components.near_high.last_history_value"
    VR = "debug_info.components.vol_ratio.last_history_value"

    def standardise(x):
        x = pd.to_numeric(x, errors="coerce")
        denom = x.abs().shift(1).rolling(60, min_periods=20).mean()
        s = x / denom * 10.0
        s = s.replace([np.inf, -np.inf], np.nan)
        return s.clip(-20, 20)

    # ---------- 1. situation check ----------
    n_eval = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            if NH not in df.columns or VR not in df.columns:
                continue
            closeness = standardise(df[NH])
            volume = standardise(df[VR])
            score = (closeness + volume) / 2.0
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0) & score.notna() & (score != 0)
            n_eval += int(active.sum())
            n_agree += int((np.sign(fc[active]) == np.sign(score[active])).sum())

    agreement = (n_agree / n_eval) if n_eval > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading_sit = ("The graded situation is read as the sign of the equal-weight mean of the two raw components, "
                   "each recomputed per window as value / mean |previous 60 values| x 10 capped at +/-20 "
                   "(min 20 values), positive meaning the long side; active bars where it cannot be computed are left out")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_eval},
            "decided_by": ("The sign of the recorded forecast agrees with the plan's graded situation "
                           "(closer to the 20-day high and heavier volume means long) on fewer than 90% of active bars."),
            "reading": reading_sit + ".",
        }

    # ---------- 2. main measure ----------
    samples = []  # (coin, fwd, forecast)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                samples.append((coin, c1 / c0 - 1.0, fc[t]))

    sdf = pd.DataFrame(samples, columns=["coin", "fwd", "fc"])
    if len(sdf):
        sdf["excess"] = sdf["fwd"] - sdf.groupby("coin")["fwd"].transform("mean")
        sdf = sdf.dropna(subset=["excess", "fc"])
    n_samples = int(len(sdf))

    slope = None
    slope_t = None
    if n_samples >= 3 and sdf["fc"].nunique() > 1:
        lr = stats.linregress(sdf["fc"].values, sdf["excess"].values)
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- 3. supporting check: timing gain ----------
    coin_mean_daily = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce")
            rets.append((c / c.shift(1) - 1.0).iloc[1:])
        r = pd.concat(rets) if rets else pd.Series(dtype=float)
        coin_mean_daily[coin] = float(r.mean()) if r.notna().any() else np.nan

    rows = []
    for coin, wins in bars.items():
        mu = coin_mean_daily[coin]
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce")
            pos = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").shift(1)
            ret = c / c.shift(1) - 1.0
            day = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D")
            part = pd.DataFrame({"day": day, "gain": pos * ret, "mkt": pos * mu}).iloc[1:]
            part = part.dropna(subset=["gain", "mkt"])
            # one daily return per coin per day (bars are daily; sum if several bars fall on one day)
            part = part.groupby("day")[["gain", "mkt"]].sum().reset_index()
            part["coin"] = coin
            rows.append(part)

    timing = None
    if rows:
        allr = pd.concat(rows, ignore_index=True)
        if len(allr):
            daily = allr.groupby("day")[["gain", "mkt"]].mean()
            timing = float(daily["gain"].mean() - daily["mkt"].mean())
    timing_passed = None if timing is None else bool(timing > 0)

    # ---------- 4. decision ----------
    if n_samples < MIN_N or slope_t is None:
        status = "not observable"
        decided = f"Only {n_samples} non-overlapping 7-bar samples, below the plan's minimum of 300."
    elif slope_t >= 2 and timing_passed:
        status = "confirmed"
        decided = "The slope t is 2 or more and the timing gain is above 0."
    elif slope_t <= -2:
        status = "rejected"
        decided = "The slope t is -2 or less."
    elif slope_t >= 2:
        status = "inconclusive"
        decided = "The slope t is 2 or more but the timing gain is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "OLS slope of 7-day excess return on forecast",
            "value": slope,
            "statistic": None if slope_t is None else {"name": "OLS slope t", "value": slope_t},
            "threshold": "slope t >= 2 confirms (with timing gain > 0); slope t <= -2 rejects",
        },
        "supporting_check": {
            "name": "timing gain (book mean daily return before costs minus market-rise gain)",
            "value": timing,
            "passed": timing_passed,
        },
        "counts": {"non-overlapping samples": n_samples},
        "decided_by": decided,
        "reading": (reading_sit + "; the regression is OLS with intercept on all non-overlapping samples whose 7-bar "
                    "return stays in the window, the coin's mean being the mean of those samples over all its windows, "
                    "and the book's before-cost daily gain is the previous bar's post-rebalance allocation x the coin's "
                    "daily return, averaged over coins each day."),
    }
