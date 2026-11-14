import numpy as np
import pandas as pd


def measure(bars):
    COL = "debug_info.components.since_high.last_history_value"
    H = 10
    MIN_EVENTS = 100

    # ---------- 1. Situation check ----------
    # Situation: within 20 bars after a new 20-day closing high, so the countdown is above 0. Side: long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if COL in df.columns:
                raw = pd.to_numeric(df[COL], errors="coerce")
                situ = raw.notna() & (raw > 0)
            else:
                situ = pd.Series(False, index=df.index)
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean excess 10-bar forward return after new-high bars (coin return minus coin's mean 10-bar return)"
    threshold = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; otherwise inconclusive; at least 100 non-overlapping events"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"non-overlapping events": 0},
            "decided_by": ("The plan's situation (long while the bars-since-20-day-closing-high countdown is above 0) "
                           f"covers only {agreement:.3f} of the active bars on the long side, below 90 %."),
            "reading": "Situation taken as the recorded since_high value above 0 with a positive forecast; missing values count as outside the situation.",
        }

    # ---------- 2. Criterion ----------
    excess_all = []
    excess_below = []
    for coin, wins in bars.items():
        # coin mean 10-bar return over all its bars in all windows (within-window returns only)
        rets_coin = []
        events_coin = []  # (forward return, next-bar-below flag)
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            rets_coin.extend([r for r in fwd if np.isfinite(r)])

            if COL not in df.columns:
                continue
            raw = pd.to_numeric(df[COL], errors="coerce").to_numpy(dtype=float)
            last = -10 ** 9
            for t in range(n):
                if not (np.isfinite(raw[t]) and np.isclose(raw[t], 20.0)):
                    continue
                if not np.isfinite(fwd[t]):
                    continue
                if t - last < H:
                    continue  # within 10 bars of a counted event: skipped
                last = t
                below = bool(t + 1 < n and np.isfinite(close[t + 1]) and close[t + 1] < close[t])
                events_coin.append((fwd[t], below))
        if len(rets_coin) == 0:
            continue
        mu = float(np.mean(rets_coin))
        for r, below in events_coin:
            excess_all.append(r - mu)
            if below:
                excess_below.append(r - mu)

    n_ev = len(excess_all)
    n_below = len(excess_below)
    x = np.asarray(excess_all, dtype=float)
    mean = float(np.mean(x)) if n_ev > 0 else None
    tstat = None
    if n_ev > 1:
        sd = float(np.std(x, ddof=1))
        if sd > 0:
            tstat = float(mean / (sd / np.sqrt(n_ev)))
    sup_val = float(np.mean(excess_below)) if n_below > 0 else None
    sup_pass = None if sup_val is None else bool(sup_val > 0)

    if n_ev < MIN_EVENTS:
        status = "not observable"
        decided = f"Only {n_ev} non-overlapping new-high events pooled across coins and windows, fewer than the plan's minimum of 100."
    elif tstat is not None and mean > 0 and tstat >= 2:
        status = "confirmed"
        decided = "Confirm rule met: the mean excess 10-bar return is above 0 with t >= 2 on non-overlapping events."
    elif tstat is not None and mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "Reject rule met: the mean excess 10-bar return is below 0 with t <= -2, new highs are followed by reversal relative to holding."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule met: t lies between -2 and 2 (or is undefined) with at least 100 events."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": None if tstat is None else {"name": "t of the mean", "value": tstat},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 10-bar return of events whose next close is below the new high",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"non-overlapping events": int(n_ev), "events with next close below the high": int(n_below)},
        "decided_by": decided,
        "reading": ("New-high bars are those with recorded since_high equal to 20 and a forward 10-bar return inside the window, "
                    "an event is skipped when it falls fewer than 10 bars after the last counted event in the same window, "
                    "the new high is that bar's close, the coin's mean is taken over all its overlapping 10-bar returns pooled across windows, "
                    "the supporting check is reported but does not change the status, and fewer than 100 events gives 'not observable'."),
    }
