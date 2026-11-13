import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    COL = "debug_info.components.since_high.last_history_value"

    # ---------- 1. Situation check ----------
    # Plan: long while the countdown since the last new 20-day closing high runs (value > 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if COL in df.columns:
                val = pd.to_numeric(df[COL], errors="coerce")
            else:
                val = pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & val.notna() & (val > 0) & (fc > 0)
            n_agree += int(agree.sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean excess 10-bar forward return after new-high bars (event minus coin's mean 10-bar return)"
    threshold = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; at least 100 non-overlapping events"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the "
                           "bars-since-high countdown is running (> 0), so the config does not trade the plan's situation."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    excess_all = []
    excess_below = []
    for coin, wins in bars.items():
        # coin's mean 10-bar return over all its bars in all windows (within-window returns only)
        coin_rets = []
        prepared = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            nxt = np.full(n, np.nan)
            if n > 1:
                nxt[: n - 1] = close[1:]
            coin_rets.append(fwd[np.isfinite(fwd)])
            if COL in df.columns:
                val = pd.to_numeric(df[COL], errors="coerce").to_numpy(dtype=float)
            else:
                val = None
            prepared.append((close, fwd, nxt, val))
        allr = np.concatenate(coin_rets) if coin_rets else np.array([])
        if allr.size == 0:
            continue
        coin_mean = float(np.mean(allr))

        for close, fwd, nxt, val in prepared:
            if val is None:
                continue
            last = None
            for i in range(len(close)):
                v = val[i]
                if not np.isfinite(v) or not np.isclose(v, 20.0):
                    continue
                if not np.isfinite(fwd[i]):
                    continue
                if last is not None and i - last < H:
                    continue
                last = i
                ex = fwd[i] - coin_mean
                excess_all.append(ex)
                if np.isfinite(nxt[i]) and np.isfinite(close[i]) and nxt[i] < close[i]:
                    excess_below.append(ex)

    n_ev = len(excess_all)
    n_below = len(excess_below)

    def mean_t(x):
        x = np.asarray(x, dtype=float)
        if x.size == 0:
            return None, None
        m = float(np.mean(x))
        if x.size < 2:
            return m, None
        sd = float(np.std(x, ddof=1))
        if sd == 0 or not np.isfinite(sd):
            return m, None
        return m, float(m / (sd / np.sqrt(x.size)))

    m, t = mean_t(excess_all)
    mb, _ = mean_t(excess_below)
    sup = {
        "name": "mean excess 10-bar return, events whose next bar closes below the new high",
        "value": mb,
        "passed": None if mb is None else bool(mb > 0),
    }

    if n_ev < 100:
        status = "not observable"
        decided = f"Only {n_ev} non-overlapping new-high events pooled across coins and windows, fewer than the plan's minimum of 100."
    elif t is not None and m > 0 and t >= 2:
        status = "confirmed"
        decided = "The mean excess 10-bar return after non-overlapping new highs is above 0 with t >= 2 (confirm rule)."
    elif t is not None and m < 0 and t <= -2:
        status = "rejected"
        decided = "The mean excess 10-bar return after non-overlapping new highs is below 0 with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "With at least 100 events, t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": m,
            "statistic": None if t is None else {"name": "t of the mean", "value": t},
            "threshold": threshold,
        },
        "supporting_check": sup,
        "counts": {"non-overlapping events": int(n_ev), "events with next close below the high": int(n_below)},
        "decided_by": decided,
        "reading": ("A new-high bar is a recorded since_high value equal to 20 with a full 10-bar forward return in its window, "
                    "an event is skipped if it lies fewer than 10 bars after the last counted event in the same window, "
                    "the coin's mean is over the overlapping 10-bar forward returns of all its bars in all windows, "
                    "'closes below the new high' means the next close is below the event bar's close, and the supporting "
                    "check is reported without changing the status, which the main measure alone decides."),
    }
