import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    COL = "debug_info.components.since_high.last_history_value"
    MIN_EVENTS = 100

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if COL in df.columns:
                v = pd.to_numeric(df[COL], errors="coerce")
            else:
                v = pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0) & v.notna()
            n_active += int(active.sum())
            # situation: countdown since last new 20-day closing high is running (value > 0); side: long
            agree = active & (v > 0) & (fc > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Situation bars are those with the recorded countdown above 0 and the expected side is long; "
               "a new-high event is a bar whose recorded value equals 20; events are made non-overlapping per coin "
               "and window by keeping an event only if it is at least 10 bars after the last kept one; the coin's mean "
               "10-bar return is taken over every bar with a within-window 10-bar return, across all its windows; "
               "the supporting check takes events whose next close is below the new-high close.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean excess 10-bar return after new 20-day closing highs",
                             "value": None, "statistic": None,
                             "threshold": "mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"non-overlapping events": 0, "active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars within 20 bars of a "
                           "new 20-day closing high, so the config does not do what the plan's situation says."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    excess_all = []
    excess_support = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_events = []  # (ret, next_below)
        for w, df in wins.items():
            if "close" not in df.columns:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(c)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:n - H] = c[H:] / c[:n - H] - 1.0
            coin_rets.extend([x for x in fwd if np.isfinite(x)])
            if COL not in df.columns:
                continue
            v = pd.to_numeric(df[COL], errors="coerce").to_numpy(dtype=float)
            last_kept = None
            for t in range(n):
                if not (np.isfinite(v[t]) and np.isclose(v[t], 20.0)):
                    continue
                if not np.isfinite(fwd[t]):
                    continue
                if last_kept is not None and t - last_kept < H:
                    continue
                last_kept = t
                nb = bool(t + 1 < n and np.isfinite(c[t + 1]) and c[t + 1] < c[t])
                coin_events.append((fwd[t], nb))
        if len(coin_rets) == 0 or len(coin_events) == 0:
            continue
        mu = float(np.mean(coin_rets))
        for r, nb in coin_events:
            excess_all.append(r - mu)
            if nb:
                excess_support.append(r - mu)

    ex = np.array(excess_all, dtype=float)
    n_ev = int(len(ex))
    mean_ex = float(ex.mean()) if n_ev > 0 else None
    t_stat = None
    if n_ev > 1:
        sd = float(ex.std(ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n_ev)))

    es = np.array(excess_support, dtype=float)
    sup_val = float(es.mean()) if len(es) > 0 else None
    sup_pass = (bool(sup_val > 0) if sup_val is not None else None)

    if n_ev < MIN_EVENTS:
        status = "not observable"
        decided = f"Only {n_ev} non-overlapping events pooled across coins and windows, fewer than the plan's minimum of 100."
    elif t_stat is not None and mean_ex > 0 and t_stat >= 2:
        status = "confirmed"
        decided = "The mean excess 10-bar return is above 0 with t >= 2 on non-overlapping events."
    elif t_stat is not None and mean_ex < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean excess 10-bar return is below 0 with t <= -2, so new highs are followed by reversal relative to holding."
    else:
        status = "inconclusive"
        decided = "The t-statistic of the mean excess 10-bar return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean excess 10-bar return after new 20-day closing highs",
                         "value": mean_ex,
                         "statistic": ({"name": "t of the mean", "value": t_stat} if t_stat is not None else None),
                         "threshold": "mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects; at least 100 events"},
        "supporting_check": {"name": "mean excess 10-bar return, events whose next close is below the new high",
                             "value": sup_val, "passed": sup_pass},
        "counts": {"non-overlapping events": n_ev, "events with next close below the high": int(len(es))},
        "decided_by": decided,
        "reading": reading,
    }
