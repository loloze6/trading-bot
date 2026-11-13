import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    MIN_EVENTS = 100
    COL = "debug_info.components.since_high.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation (adapted): within 20 bars after a new 20-day closing high, i.e. the raw countdown > 0. Side: long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or COL not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            ind = pd.to_numeric(df[COL], errors="coerce")
            ok = fc.notna()
            active = ok & (fc != 0)
            n_active += int(active.sum())
            situ = ind.notna() & (ind > 0)
            n_agree += int((active & situ & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The forecast is active on bars that are not within 20 bars after a new 20-day closing high "
                           "(countdown > 0) with a long sign in at least 90 % of cases"
                           if n_active > 0 else "The forecast is never active, so the situation cannot be matched."),
            "reading": "Situation taken as the recorded countdown being above 0, with a positive forecast as the long side.",
        }

    # ---------- 2. Criterion ----------
    excess_all = []
    excess_below = []
    for coin, wins in bars.items():
        # coin mean 10-bar return over all its bars in all windows together
        coin_rets = []
        frames = {}
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:n - H] = close[H:] / close[:n - H] - 1.0
            nxt = np.full(n, np.nan)
            if n > 1:
                nxt[:n - 1] = close[1:]
            frames[w] = (df, close, fwd, nxt)
            coin_rets.append(fwd[np.isfinite(fwd)])
        allr = np.concatenate(coin_rets) if coin_rets else np.array([])
        if allr.size == 0:
            continue
        coin_mean = float(np.mean(allr))

        for w, (df, close, fwd, nxt) in frames.items():
            if COL not in df.columns:
                continue
            ind = pd.to_numeric(df[COL], errors="coerce").to_numpy(dtype=float)
            last = None
            for t in range(len(ind)):
                if not (np.isfinite(ind[t]) and np.isclose(ind[t], 20.0)):
                    continue
                if not np.isfinite(fwd[t]):
                    continue
                if last is not None and t - last < H:
                    continue
                last = t
                ex = fwd[t] - coin_mean
                excess_all.append(ex)
                if np.isfinite(nxt[t]) and np.isfinite(close[t]) and nxt[t] < close[t]:
                    excess_below.append(ex)

    ea = np.asarray(excess_all, dtype=float)
    eb = np.asarray(excess_below, dtype=float)
    n = int(ea.size)
    nb = int(eb.size)

    def tstat(x):
        if x.size < 2:
            return None
        sd = np.std(x, ddof=1)
        if not np.isfinite(sd) or sd == 0:
            return None
        return float(np.mean(x) / (sd / np.sqrt(x.size)))

    mean_ex = float(np.mean(ea)) if n > 0 else None
    t = tstat(ea)
    mean_b = float(np.mean(eb)) if nb > 0 else None
    sup_passed = (mean_b > 0) if mean_b is not None else None

    if n < MIN_EVENTS:
        status = "not observable"
        decided = f"Only {n} non-overlapping new-high events pooled across coins and windows, fewer than the plan's minimum of 100."
    elif mean_ex is not None and t is not None and mean_ex > 0 and t >= 2:
        status = "confirmed"
        decided = "Confirm rule met: the mean excess 10-bar return after non-overlapping new highs is above 0 with t >= 2."
    elif mean_ex is not None and t is not None and mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "Reject rule met: the mean excess 10-bar return after non-overlapping new highs is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule met: the t of the mean excess 10-bar return lies between -2 and 2 with at least 100 events."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean excess 10-bar forward return after new 20-day closing highs (vs coin mean 10-bar return)",
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; at least 100 non-overlapping events",
        },
        "supporting_check": {
            "name": "mean excess 10-bar return of events whose next close is below the new high (must be > 0)",
            "value": mean_b,
            "passed": None if sup_passed is None else bool(sup_passed),
        },
        "counts": {
            "non-overlapping events": n,
            "events with next close below the new high": nb,
        },
        "decided_by": decided,
        "reading": ("A new-high event is a bar whose recorded countdown equals 20 and has a 10-bar forward return in its window; "
                    "events are kept greedily per window and one less than 10 bars after the last counted event is skipped; "
                    "the coin mean uses every bar with a 10-bar forward return across all its windows; "
                    "'closes below the new high' means close[t+1] < close[t]; the supporting check does not change the status."),
    }
