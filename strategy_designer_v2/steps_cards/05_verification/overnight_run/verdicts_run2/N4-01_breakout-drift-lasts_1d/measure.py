import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    COL = "debug_info.components.since_high.last_history_value"

    # ---------- 1. situation check ----------
    # Plan's situation: the countdown since the last new 20-day closing high is running
    # (recorded indicator > 0). The side is long because the outcome is a rise.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            if COL not in df.columns:
                # A missing column is not a value of zero, so these bars cannot be counted as agreeing.
                continue
            v = pd.to_numeric(df[COL], errors="coerce")
            sit = v.notna() & (v > 0)
            n_agree += int((active & sit & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    threshold_txt = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; minimum 100 non-overlapping events"
    main_name = "mean excess 10-bar forward return after new-high bars (event return minus coin's mean 10-bar return)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"non-overlapping events": 0},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars inside the 20-bar countdown after a new 20-day closing high, so the config does not do what the plan's situation says.",
            "reading": "The situation is read as the recorded since_high indicator being above 0 (countdown running), on the long side.",
        }

    # ---------- 2. criterion ----------
    # Coin mean 10-bar return over all its bars in all windows together.
    coin_mean = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) > H:
                r = c[H:] / c[:-H] - 1.0
                allr.append(r[np.isfinite(r)])
        allr = np.concatenate(allr) if allr else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if len(allr) else np.nan

    excess_all = []
    excess_below = []
    for coin, wins in bars.items():
        m = coin_mean.get(coin, np.nan)
        if not np.isfinite(m):
            continue
        for w, df in wins.items():
            if COL not in df.columns:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            v = pd.to_numeric(df[COL], errors="coerce").to_numpy(dtype=float)
            n = len(c)
            last = None
            for t in range(n):
                if not (np.isfinite(v[t]) and abs(v[t] - 20.0) < 1e-9):
                    continue
                if t + H >= n or not (np.isfinite(c[t]) and np.isfinite(c[t + H])) or c[t] == 0:
                    continue
                if last is not None and t - last < H:
                    continue  # within 10 bars of a counted event: skipped
                last = t
                ex = c[t + H] / c[t] - 1.0 - m
                excess_all.append(ex)
                if t + 1 < n and np.isfinite(c[t + 1]) and c[t + 1] < c[t]:
                    excess_below.append(ex)

    ea = np.array(excess_all, dtype=float)
    eb = np.array(excess_below, dtype=float)
    n_ev = int(len(ea))
    n_below = int(len(eb))

    mean_ex = float(np.mean(ea)) if n_ev > 0 else None
    if n_ev > 1 and np.std(ea, ddof=1) > 0:
        t_stat = float(np.mean(ea) / (np.std(ea, ddof=1) / np.sqrt(n_ev)))
    else:
        t_stat = None

    sup_val = float(np.mean(eb)) if n_below > 0 else None
    sup_pass = (bool(sup_val > 0) if sup_val is not None else None)

    if n_ev < 100:
        status = "not observable"
        decided = f"Only {n_ev} non-overlapping events were found, below the plan's minimum of 100 pooled across all coins and windows."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (zero dispersion), so neither confirm nor reject is met."
    elif mean_ex > 0 and t_stat >= 2:
        status = "confirmed"
        decided = "The mean excess 10-bar return is above 0 with t >= 2 on non-overlapping events (confirm rule)."
    elif mean_ex < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean excess 10-bar return is below 0 with t <= -2 on non-overlapping events (reject rule): new highs are followed by reversal relative to holding."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": t_stat} if t_stat is not None else None),
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "mean excess 10-bar return of events whose next close is below the new high (must be > 0)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"non-overlapping events": n_ev, "events with next close below the new high": n_below},
        "decided_by": decided,
        "reading": "A new-high bar is a bar whose recorded since_high value equals 20, events are taken in time order per coin and window with a new one counted only if it is at least 10 bars after the last counted event (so 10-bar returns do not overlap) and has a full 10-bar forward return inside its window, the coin mean is over all overlapping 10-bar returns of that coin in all its windows, the plan's 'fewer than 100 events' is treated as the minimum count giving 'not observable', and the supporting check is reported but does not change the status since the confirm and reject rules name only the main measure.",
    }
