import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 30
    MIN_EVENTS = 30

    def _prep(df):
        df = df.copy()
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            df = df.sort_values("timestamp", kind="mergesort")
        return df.reset_index(drop=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin in sorted(bars.keys()):
        prepared[coin] = {}
        for win in sorted(bars[coin].keys(), key=lambda w: (len(str(w)), str(w))):
            df = _prep(bars[coin][win])
            prepared[coin][win] = df
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            high = pd.to_numeric(df["high"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            regime = df["regime"].astype(str).to_numpy()
            # Necessary condition from the prices available in the window:
            # close above every earlier high of the window (all within the 365-bar lookback).
            prior_max = np.full(len(df), -np.inf)
            if len(df) > 1:
                prior_max[1:] = np.maximum.accumulate(np.nan_to_num(high, nan=-np.inf))[:-1]
            above_prior_in_window = close > prior_max
            # The detector's recorded decision of "close above prior 365-bar high" is regime == trending.
            situation = (regime == "trending") & above_prior_in_window
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    if n_active == 0:
        agreement = None
        passed = False
    else:
        agreement = n_agree / n_active
        passed = agreement >= 0.90

    main_name = "Welch t of mean 30-bar excess return, top half of forecast minus bottom half (breakout events)"
    threshold = "confirm if Welch t >= 2.0 with top minus bottom positive; reject if Welch t <= -2.0 with top minus bottom negative; at least 30 events"
    reading = ("The breakout situation is taken as regime 'trending' (the detector's recorded close-above-prior-365-bar-high decision) "
               "together with close above every earlier high in the window, since 365 bars of history are not in the record; "
               "events are chosen greedily from each window's first trending bar, the coin mean 30-bar return uses the "
               "non-overlapping grid 0, 30, 60, ... of each window pooled over all windows, and the halves are the lower and "
               "upper floor(n/2) events after sorting all events by forecast (middle one dropped when n is odd).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("The forecast is not active on the plan's situation (close above the prior 52-week high, long) "
                           "on at least 90% of its active bars" if n_active > 0 else
                           "The forecast is never active, so it does not act on the plan's breakout situation."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin mean 30-bar return over all windows (non-overlapping grid)
    coin_mean = {}
    for coin, wins in prepared.items():
        rets = []
        for win, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for p in range(0, n - H, H):
                a, b = close[p], close[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    events = []  # (forecast, coin, timestamp-order key, excess)
    for coin, wins in prepared.items():
        cm = coin_mean[coin]
        for win, df in wins.items():
            n = len(df)
            if n == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            regime = df["regime"].astype(str).to_numpy()
            last = -10 ** 9
            for p in range(n):
                if regime[p] != "trending":
                    continue
                if p - last < H:
                    continue
                if p + H > n - 1:
                    continue
                a, b = close[p], close[p + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0 and np.isfinite(fc[p]) and np.isfinite(cm)):
                    continue
                last = p
                events.append((float(fc[p]), str(coin), str(win), p, (b / a - 1.0) - cm))

    n_events = len(events)
    counts = {"de-duplicated breakout events": n_events}

    if n_events < MIN_EVENTS:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Only {n_events} de-duplicated breakout events across all coins and windows, fewer than the plan's minimum of 30.",
            "reading": reading,
        }

    events_sorted = sorted(events, key=lambda e: (e[0], e[1], e[2], e[3]))
    half = n_events // 2
    bottom = np.array([e[4] for e in events_sorted[:half]], dtype=float)
    top = np.array([e[4] for e in events_sorted[n_events - half:]], dtype=float)
    counts["top half events"] = int(len(top))
    counts["bottom half events"] = int(len(bottom))

    diff = float(np.mean(top) - np.mean(bottom))
    t = stats.ttest_ind(top, bottom, equal_var=False).statistic
    t = float(t) if np.isfinite(t) else None

    if t is not None and t >= 2.0 and diff > 0:
        status = "confirmed"
        decided = f"Welch t = {t:.2f} >= 2.0 with the top half minus the bottom half positive, over {n_events} events (confirm rule)."
    elif t is not None and t <= -2.0 and diff < 0:
        status = "rejected"
        decided = f"Welch t = {t:.2f} <= -2.0, heavier pre-break volume followed by smaller excess returns, over {n_events} events (reject rule)."
    else:
        status = "inconclusive"
        decided = (f"Welch t = {t:.2f} lies between -2.0 and 2.0 over {n_events} events (inconclusive rule)."
                   if t is not None else "Welch t could not be computed (zero variance), meeting neither confirm nor reject rule.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": diff,
            "statistic": {"name": "Welch t", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
