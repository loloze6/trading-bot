import numpy as np
import pandas as pd


def _rsi_wilder(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = (-delta).clip(lower=0.0)
    avg_gain = gain.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100.0 - 100.0 / (1.0 + rs)
    rsi = rsi.where(avg_loss != 0, 100.0)
    rsi = rsi.where(avg_gain.notna() & avg_loss.notna())
    return rsi


def _situation(df, low_period=30, rsi_period=14, lookback=30, exclude=3):
    close = df["close"].astype(float).reset_index(drop=True)
    n = len(close)
    rsi = _rsi_wilder(close, rsi_period).values
    c = close.values
    sit = np.full(n, np.nan)
    for t in range(n):
        if t - low_period < 0 or t - lookback < 0:
            continue
        prior_low = np.min(c[t - low_period:t])
        lowdist = c[t] / prior_low - 1.0
        seg = c[t - lookback:t - exclude]  # bars t-30 .. t-4
        if len(seg) == 0:
            continue
        j = t - lookback + int(np.argmin(seg))
        if np.isnan(rsi[t]) or np.isnan(rsi[j]):
            continue
        rsichg = rsi[t] - rsi[j]
        sit[t] = 1.0 if (lowdist < 0.0 and rsichg > 0.0) else 0.0
    return sit


def measure(bars):
    H = 20
    MIN_EVENTS = 20

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            sit = _situation(df)
            for t in range(len(df)):
                if np.isnan(fc[t]) or fc[t] == 0:
                    continue
                if np.isnan(sit[t]):
                    n_active_uncomputable += 1
                    continue
                n_active += 1
                if sit[t] == 1.0 and fc[t] < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    reading_sit = ("Situation recomputed from closes inside each window (prior 30-bar low excluding the current bar; "
                   "Wilder 14-bar RSI now minus RSI at the lowest close of bars t-30..t-4); active bars where it cannot "
                   "be computed for lack of in-window history are left out of the agreement")
    reading_main = ("event spacing is greedy per window (an event, then the next one at least 20 bars later), events "
                    "without a full 20-bar forward return in their window are dropped, the coin mean is the pooled "
                    "mean of its 20-bar grid returns over all windows, the depth slope is OLS of excess return on "
                    "|forecast|, and fewer than 20 events is reported as not observable")
    reading = reading_sit + "; " + reading_main + "."

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active),
                       "active bars not computable": int(n_active_uncomputable)},
            "decided_by": ("Fewer than 90% of active bars are short bars on a new 30-bar closing low with RSI above its "
                           "reading at the prior low, so the forecast does not follow the plan's divergence situation."
                           if agreement is not None else
                           "No active bar could be checked against the plan's divergence situation."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin mean 20-bar return on the non-overlapping grid, over all windows
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).values
            for t in range(0, len(c) - H, H):
                if c[t] > 0 and not np.isnan(c[t]) and not np.isnan(c[t + H]):
                    rets.append(c[t + H] / c[t] - 1.0)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    excess = []
    depth = []
    events_per_coin = {}
    for coin, wins in bars.items():
        cnt = 0
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            last = -10 ** 9
            for t in range(len(df)):
                if reg[t] == "trending" and not np.isnan(fc[t]) and fc[t] < 0:
                    if t - last >= H:
                        last = t
                        if t + H < len(df) and not np.isnan(c[t + H]) and c[t] > 0 \
                                and not np.isnan(coin_mean[coin]):
                            excess.append(c[t + H] / c[t] - 1.0 - coin_mean[coin])
                            depth.append(abs(fc[t]))
                            cnt += 1
        events_per_coin[coin] = cnt

    excess = np.array(excess, dtype=float)
    depth = np.array(depth, dtype=float)
    n = len(excess)

    mean_ex = float(np.mean(excess)) if n > 0 else None
    t_stat = None
    if n >= 2:
        sd = float(np.std(excess, ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n)))
    slope = None
    if n >= 2 and np.unique(depth).size >= 2:
        slope = float(np.polyfit(depth, excess, 1)[0])
    slope_passed = None if slope is None else bool(slope < 0)

    counts = {"independent events": int(n)}
    for coin, k in events_per_coin.items():
        counts["events " + str(coin)] = int(k)

    if n < MIN_EVENTS:
        status = "not observable"
        decided_by = f"Only {n} independent event bars, below the plan's minimum of 20 events."
    elif t_stat is None:
        status = "inconclusive"
        decided_by = "The t of the mean excess return cannot be computed (zero dispersion), so neither rule is met."
    elif mean_ex < 0 and t_stat <= -2:
        if slope_passed:
            status = "confirmed"
            decided_by = "Mean excess return is negative with t <= -2 over at least 20 events and the depth slope is below 0."
        else:
            status = "inconclusive"
            decided_by = "A confirming t <= -2 but the depth slope is 0 or above (or not computable)."
    elif mean_ex > 0 and t_stat >= 2:
        status = "rejected"
        decided_by = "Mean excess return is positive with t >= +2 over at least 20 events."
    else:
        status = "inconclusive"
        decided_by = "The t of the mean excess return lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean excess 20-bar return after divergence-low event bars",
            "value": mean_ex,
            "statistic": None if t_stat is None else {"name": "ordinary t of the mean", "value": t_stat},
            "threshold": "confirm: negative with t <= -2 over at least 20 events; reject: positive with t >= +2 over at least 20 events",
        },
        "supporting_check": {
            "name": "slope of excess 20-bar return on |forecast| below 0",
            "value": slope,
            "passed": slope_passed,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
