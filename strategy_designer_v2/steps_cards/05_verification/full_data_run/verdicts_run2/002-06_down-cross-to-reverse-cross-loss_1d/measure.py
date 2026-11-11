import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.sma_cross_spread.last_history_value"
    POS = "postRebalance_current_allocation"
    LAG = 10

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            raw = pd.to_numeric(df[RAW], errors="coerce").values
            ok = ~np.isnan(f) & ~np.isnan(raw)
            act = ok & (f != 0)
            n_active += int(act.sum())
            n_agree += int((act & (raw < 0) & (f < 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"bars with a non-zero position": None, "distinct down-cross spans": None},
            "decided_by": ("The plan's situation is a short only while SMA50 is below SMA200 (raw spread < 0), "
                           "but fewer than 90% of the bars with a non-zero forecast are short bars with a negative "
                           "spread: the standardised-and-clipped forecast also goes short when the spread is above "
                           "zero but below its own 200-bar mean."),
            "reading": "Situation taken as raw SMA50-SMA200 spread < 0 with a negative forecast.",
        }

    # ---------- 2. main measure ----------
    segments = []
    n_pos = 0
    n_spans = 0
    completed = []  # (coin, L, ret)
    coin_closes = {}
    for coin, wins in bars.items():
        coin_closes[coin] = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            pos = pd.to_numeric(df[POS], errors="coerce").values.astype(float)
            raw = pd.to_numeric(df[RAW], errors="coerce").values.astype(float)
            coin_closes[coin].append(close)
            n = len(close)
            rnext = np.full(n, np.nan)
            if n > 1:
                rnext[:-1] = close[1:] / close[:-1] - 1.0
            mean_r = np.nanmean(rnext) if np.isfinite(rnext).any() else np.nan
            ex = pos * (rnext - mean_r)
            ex = ex[np.isfinite(ex)]
            if len(ex):
                segments.append(ex)
            n_pos += int((np.isfinite(pos) & (pos != 0)).sum())

            # spans of raw < 0
            neg = np.isfinite(raw) & (raw < 0)
            i = 0
            while i < n:
                if neg[i]:
                    s = i
                    while i + 1 < n and neg[i + 1]:
                        i += 1
                    e = i
                    n_spans += 1
                    if (s > 0 and np.isfinite(raw[s - 1]) and raw[s - 1] >= 0
                            and e + 1 < n and np.isfinite(raw[e + 1]) and raw[e + 1] >= 0):
                        if np.isfinite(close[s]) and np.isfinite(close[e + 1]) and close[s] != 0:
                            completed.append((coin, e + 1 - s, close[e + 1] / close[s] - 1.0))
                i += 1

    mean_ex = None
    t_nw = None
    if segments:
        allx = np.concatenate(segments)
        N = len(allx)
        mu = allx.mean()
        g = np.zeros(LAG + 1)
        for seg in segments:
            d = seg - mu
            for l in range(LAG + 1):
                if len(d) > l:
                    g[l] += np.sum(d[l:] * d[:len(d) - l])
        g /= N
        var = g[0] + 2.0 * sum((1.0 - l / (LAG + 1.0)) * g[l] for l in range(1, LAG + 1))
        mean_ex = float(mu)
        if var > 0 and N > 1:
            t_nw = float(mu / np.sqrt(var / N))

    # ---------- 3. supporting check ----------
    med_cache = {}

    def median_L(coin, L):
        key = (coin, L)
        if key not in med_cache:
            rs = []
            for c in coin_closes[coin]:
                if len(c) > L:
                    r = c[L:] / c[:-L] - 1.0
                    rs.append(r[np.isfinite(r)])
            rs = np.concatenate(rs) if rs else np.array([])
            med_cache[key] = float(np.median(rs)) if len(rs) else np.nan
        return med_cache[key]

    below = []
    for coin, L, ret in completed:
        m = median_L(coin, L)
        if np.isfinite(m):
            below.append(ret < m)
    share = float(np.mean(below)) if below else None
    sup_pass = None if share is None else bool(share > 0.5)

    # ---------- 4. decision ----------
    if n_pos < 500 or n_spans < 10:
        status = "inconclusive"
        decided = "Fewer than 500 bars with a non-zero position or fewer than 10 distinct down-cross spans, so the result is inconclusive."
    elif t_nw is None:
        status = "inconclusive"
        decided = "The Newey-West t-statistic could not be computed, so the result is inconclusive."
    elif mean_ex > 0 and t_nw >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean excess return above 0 with t >= 2 and supporting share above 50%: confirmed."
    elif mean_ex < 0 and t_nw <= -2:
        status = "rejected"
        decided = "Mean excess return below 0 with t <= -2: rejected (reversal)."
    elif mean_ex > 0 and t_nw >= 2:
        status = "inconclusive"
        decided = "A confirming t but a supporting share of 50% or less (or none): inconclusive."
    else:
        status = "inconclusive"
        decided = "The Newey-West t lies between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": {
            "name": "pooled mean excess return of position x (next-bar return - window mean daily return)",
            "value": mean_ex,
            "statistic": None if t_nw is None else {"name": "Newey-West t (lag 10)", "value": t_nw},
            "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject",
        },
        "supporting_check": {
            "name": "share of completed down-cross spans below the coin's median same-length span return",
            "value": share,
            "passed": sup_pass,
        },
        "counts": {
            "bars with a non-zero position": int(n_pos),
            "distinct down-cross spans": int(n_spans),
            "completed down-cross spans": int(len(below)),
        },
        "decided_by": decided,
        "reading": ("Excess returns use every bar (zero positions included) with the coin's mean next-bar return "
                    "in that window, pooled with Newey-West autocovariances taken within each coin-window only; "
                    "a span is a run of raw spread < 0 inside one window, counted for the minimum whether or not "
                    "it is completed, and a completed span (cross down and back up both seen) returns "
                    "close at the up-cross bar over close at its first negative bar, compared with the median of "
                    "all same-length close-to-close returns of that coin pooled over its windows."),
    }
