import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.rev24.last_history_value"
    POS = "postRebalance_current_allocation"
    H = 24

    def prep(df):
        df = df.copy().reset_index(drop=True)
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df["forecast"] = pd.to_numeric(df["forecast"], errors="coerce")
        if RAW in df.columns:
            df[RAW] = pd.to_numeric(df[RAW], errors="coerce")
        else:
            df[RAW] = np.nan
        if POS in df.columns:
            df[POS] = pd.to_numeric(df[POS], errors="coerce")
        else:
            df[POS] = np.nan
        return df

    data = {c: {w: prep(df) for w, df in wins.items() if df is not None and len(df) > 0}
            for c, wins in bars.items()}

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for c, wins in data.items():
        for w, df in wins.items():
            raw = df[RAW].copy()
            # where the component is not recorded, rebuild its sign from the prices (24-bar return)
            r24 = df["close"] / df["close"].shift(H) - 1.0
            raw = raw.where(raw.notna(), r24)
            f = df["forecast"]
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            # the situation: a non-zero 24h scaled return; expected side: against it (long after fall, short after rise)
            expected = -np.sign(raw)
            ok = active & raw.notna() & (raw != 0) & (np.sign(f) == expected)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t-statistic of the slope of next-24-bar excess return on forecast (non-overlapping grid, pooled)"
    threshold = "confirm if slope t >= 2 with timing gain > 0; reject if slope t <= -2; at least 500 independent 24-bar cases"
    reading = ("Coin mean 24-bar return taken as the mean of that coin's grid 24-bar returns pooled over all its windows; "
               "OLS with intercept; the book's daily return before costs is the sum of each bar's position x next-bar return "
               "over the day, the market gain uses the day's mean position x the coin's pooled mean daily return, "
               "and days are averaged across coins by date.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"independent 24-bar cases": 0, "active bars": n_active},
            "decided_by": ("Fewer than 90% of active bars have a forecast against the sign of the 24-hour volatility-scaled "
                           "return, so the config does not trade the plan's contrarian side of its situation."),
            "reading": reading,
        }

    # ---------- 2. main measure ----------
    rows = []
    for c, wins in data.items():
        for w, df in wins.items():
            n = len(df)
            idx = np.arange(0, n, H)
            idx = idx[idx + H < n]
            if len(idx) == 0:
                continue
            cl = df["close"].values
            fwd = cl[idx + H] / cl[idx] - 1.0
            fc = df["forecast"].values[idx]
            for x, y in zip(fc, fwd):
                rows.append((c, x, y))
    grid = pd.DataFrame(rows, columns=["coin", "f", "r"]) if rows else pd.DataFrame(columns=["coin", "f", "r"])
    grid = grid.replace([np.inf, -np.inf], np.nan)
    coin_mean = grid.dropna(subset=["r"]).groupby("coin")["r"].mean()
    grid["ex"] = grid["r"] - grid["coin"].map(coin_mean)
    g = grid.dropna(subset=["f", "ex"])
    n_cases = int(len(g))

    slope_t = None
    slope = None
    if n_cases >= 3 and np.std(g["f"].values) > 0:
        lr = stats.linregress(g["f"].values.astype(float), g["ex"].values.astype(float))
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- 3. supporting check: mean daily timing gain ----------
    # coin mean daily return over all windows
    coin_daily_mean = {}
    for c, wins in data.items():
        rets = []
        for w, df in wins.items():
            d = df["timestamp"].dt.floor("D")
            last_idx = df.groupby(d).tail(1).index.values
            cl = df["close"].values[last_idx]
            if len(cl) > 1:
                rets.append(cl[1:] / cl[:-1] - 1.0)
        allr = np.concatenate(rets) if rets else np.array([])
        allr = allr[np.isfinite(allr)]
        coin_daily_mean[c] = float(np.mean(allr)) if len(allr) else np.nan

    day_rows = []
    for c, wins in data.items():
        mu = coin_daily_mean.get(c, np.nan)
        for w, df in wins.items():
            d = df["timestamp"].dt.floor("D")
            last_idx = df.groupby(d).tail(1).index.values
            cl = df["close"].values
            pos = df[POS].values
            bar_ret = np.full(len(df), np.nan)
            if len(df) > 1:
                bar_ret[:-1] = cl[1:] / cl[:-1] - 1.0
            bar_gain = pos * bar_ret
            for k in range(1, len(last_idx)):
                a, b = last_idx[k - 1], last_idx[k]
                gseg = bar_gain[a:b]
                pseg = pos[a:b]
                if len(gseg) == 0 or np.any(~np.isfinite(gseg)) or not np.isfinite(mu):
                    continue
                book = float(np.sum(gseg))
                market = float(np.mean(pseg)) * mu
                day_rows.append((df["timestamp"].iloc[b].floor("D"), book - market))
    if day_rows:
        dd = pd.DataFrame(day_rows, columns=["day", "timing"])
        daily_timing = dd.groupby("day")["timing"].mean()
        timing_mean = float(daily_timing.mean())
        n_days = int(len(daily_timing))
    else:
        timing_mean = None
        n_days = 0
    check_pass = (timing_mean is not None) and (timing_mean > 0)

    # ---------- 4. decision ----------
    if n_cases < 500:
        status = "not observable"
        decided = f"Only {n_cases} independent 24-bar cases, below the plan's minimum of 500."
    elif slope_t is None:
        status = "inconclusive"
        decided = "The slope's t-statistic could not be computed (no variation in the forecast)."
    elif slope_t >= 2 and check_pass:
        status = "confirmed"
        decided = "The slope's t-statistic is 2 or more and the mean daily timing gain is above 0."
    elif slope_t >= 2:
        status = "inconclusive"
        decided = "The slope's t-statistic is 2 or more but the mean daily timing gain is not above 0."
    elif slope_t <= -2:
        status = "rejected"
        decided = "The slope's t-statistic is -2 or less: larger contrarian positions are followed by worse excess returns."
    else:
        status = "inconclusive"
        decided = "The slope's t-statistic lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope_t,
            "statistic": {"name": "OLS slope t", "value": slope_t} if slope_t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "book's mean daily timing gain (before costs) above 0",
            "value": timing_mean,
            "passed": bool(check_pass) if timing_mean is not None else None,
        },
        "counts": {"independent 24-bar cases": n_cases, "days in timing check": n_days},
        "decided_by": decided,
        "reading": reading,
    }
