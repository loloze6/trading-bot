import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    MIN_EVENTS = 100
    COL = "debug_info.components.since_high.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: the countdown since the last new 20-day closing high is running (raw value > 0).
    # Expected side: long.
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
                continue  # a missing column is not a value of zero: these bars cannot agree
            raw = pd.to_numeric(df[COL], errors="coerce")
            agree = active & raw.notna() & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean excess 10-bar forward return after new-high bars (minus coin's mean 10-bar return), non-overlapping, pooled"
    threshold = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; at least 100 non-overlapping events"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"non-overlapping events": 0},
            "decided_by": (
                f"Only {agreement:.1%} of the {n_active} active bars are long bars with the recorded "
                "bars-since-high countdown above 0, below the 90% required by the plan's situation."
            ),
            "reading": "Situation taken as the recorded countdown being above 0 with a positive forecast.",
        }

    # ---------- 2. Criterion ----------
    excess_all = []
    excess_below = []
    for coin, wins in bars.items():
        # coin's mean 10-bar return over all its bars in all windows together
        all_rets = []
        per_window = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            all_rets.append(fwd[np.isfinite(fwd)])
            per_window.append((df, close, fwd))
        all_rets = np.concatenate(all_rets) if all_rets else np.array([])
        if all_rets.size == 0:
            continue
        coin_mean = float(np.mean(all_rets))

        for df, close, fwd in per_window:
            if COL not in df.columns:
                continue
            raw = pd.to_numeric(df[COL], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            last = None
            for i in range(n):
                if not (np.isfinite(raw[i]) and np.isclose(raw[i], 20.0)):
                    continue
                if not np.isfinite(fwd[i]):
                    continue
                if last is not None and i - last < H:
                    continue  # within 10 bars of a counted event: skipped
                last = i
                ex = fwd[i] - coin_mean
                excess_all.append(ex)
                if i + 1 < n and np.isfinite(close[i + 1]) and np.isfinite(close[i]) and close[i + 1] < close[i]:
                    excess_below.append(ex)

    excess_all = np.asarray(excess_all, dtype=float)
    excess_below = np.asarray(excess_below, dtype=float)
    n_ev = int(excess_all.size)
    n_below = int(excess_below.size)

    mean_ex = float(np.mean(excess_all)) if n_ev > 0 else None
    t_stat = None
    if n_ev > 1:
        sd = float(np.std(excess_all, ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n_ev)))

    sup_val = float(np.mean(excess_below)) if n_below > 0 else None
    sup_passed = None if sup_val is None else bool(sup_val > 0)

    if n_ev < MIN_EVENTS:
        status = "not observable"
        decided = f"Only {n_ev} non-overlapping new-high events pooled across coins and windows, fewer than the plan's minimum of 100."
    elif t_stat is not None and mean_ex > 0 and t_stat >= 2:
        status = "confirmed"
        decided = f"Mean excess 10-bar return {mean_ex:.4f} > 0 with t = {t_stat:.2f} >= 2 over {n_ev} non-overlapping events."
    elif t_stat is not None and mean_ex < 0 and t_stat <= -2:
        status = "rejected"
        decided = f"Mean excess 10-bar return {mean_ex:.4f} < 0 with t = {t_stat:.2f} <= -2 over {n_ev} non-overlapping events."
    else:
        status = "inconclusive"
        tv = "n/a" if t_stat is None else f"{t_stat:.2f}"
        decided = f"t = {tv} lies between -2 and 2 over {n_ev} non-overlapping events, meeting neither confirm nor reject."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 10-bar return of events whose next close is below the new high",
            "value": sup_val,
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping events": n_ev,
            "events with next close below the new high": n_below,
        },
        "decided_by": decided,
        "reading": (
            "A new-high bar is a bar whose recorded countdown equals 20 and that has a 10-bar forward return inside its window; "
            "within each window, events are taken in time order and one less than 10 bars after the last counted event is skipped; "
            "the coin's mean is over every bar with a 10-bar return in all its windows; the new high is that bar's close; "
            "the supporting check is reported only and does not change the status."
        ),
    }
