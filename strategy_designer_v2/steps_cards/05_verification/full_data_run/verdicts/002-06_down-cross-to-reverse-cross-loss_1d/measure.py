import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.sma_cross_spread.last_history_value"
    POS = "postRebalance_current_allocation"

    def newey_west_t(x, lag=10):
        x = np.asarray(x, dtype=float)
        n = len(x)
        if n < 2:
            return None
        m = x.mean()
        u = x - m
        s = np.dot(u, u) / n
        for k in range(1, min(lag, n - 1) + 1):
            w = 1.0 - k / (lag + 1.0)
            s += 2.0 * w * np.dot(u[k:], u[:-k]) / n
        if not np.isfinite(s) or s <= 0:
            return None
        return float(m / np.sqrt(s / n))

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for win in bars[coin]:
            df = bars[coin][win]
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce")
            ok = f.notna() & raw.notna()
            active = ok & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & (raw < 0) & (f < 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean excess return of position vs coin's window mean return",
                             "value": None, "statistic": None,
                             "threshold": "mean > 0 with Newey-West t >= 2 (confirm); mean < 0 with t <= -2 (reject)"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is a short held only while SMA50 is below SMA200 (raw spread < 0), "
                           "but fewer than 90% of the bars with a non-zero forecast are short bars with a negative spread."),
            "reading": "none",
        }

    # ---------- 2. main measure ----------
    pooled = []
    nonzero_pos_bars = 0
    n_runs = 0
    spans = []  # (coin, length, return)
    for coin in sorted(bars):
        for win in sorted(bars[coin], key=lambda w: int(str(w).lstrip("w")) if str(w).lstrip("w").isdigit() else str(w)):
            df = bars[coin][win]
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            pos = pd.to_numeric(df[POS], errors="coerce").to_numpy(dtype=float)
            raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            if n >= 2:
                r = close[1:] / close[:-1] - 1.0
                p = pos[:-1]
                rv = np.isfinite(r)
                if rv.any():
                    mu = r[rv].mean()
                    ok = rv & np.isfinite(p)
                    ex = p[ok] * (r[ok] - mu)
                    pooled.extend(ex.tolist())
                    nonzero_pos_bars += int(np.sum(p[ok] != 0))
            # down-cross spans (raw < 0 runs) within this window
            below = np.isfinite(raw) & (raw < 0)
            i = 0
            while i < n:
                if below[i]:
                    s = i
                    while i + 1 < n and below[i + 1]:
                        i += 1
                    e = i
                    n_runs += 1
                    started = s > 0 and np.isfinite(raw[s - 1]) and raw[s - 1] >= 0
                    ended = e + 1 < n and np.isfinite(raw[e + 1]) and raw[e + 1] >= 0
                    if started and ended and np.isfinite(close[s]) and np.isfinite(close[e + 1]):
                        L = e + 1 - s
                        spans.append((coin, L, close[e + 1] / close[s] - 1.0))
                i += 1

    pooled = np.asarray(pooled, dtype=float)
    mean_ex = float(pooled.mean()) if len(pooled) else None
    t_nw = newey_west_t(pooled, 10) if len(pooled) else None

    # ---------- 3. supporting check ----------
    cache = {}

    def median_same_length(coin, L):
        key = (coin, L)
        if key in cache:
            return cache[key]
        rets = []
        for win in bars[coin]:
            c = pd.to_numeric(bars[coin][win]["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) > L:
                rr = c[L:] / c[:-L] - 1.0
                rets.extend(rr[np.isfinite(rr)].tolist())
        val = float(np.median(rets)) if rets else None
        cache[key] = val
        return val

    below_med = 0
    judged = 0
    for coin, L, ret in spans:
        med = median_same_length(coin, L)
        if med is None:
            continue
        judged += 1
        if ret < med:
            below_med += 1
    share = (below_med / judged) if judged > 0 else None
    sup_passed = (share > 0.5) if share is not None else None

    # ---------- 4. decision ----------
    enough = nonzero_pos_bars >= 500 and n_runs >= 10
    if not enough:
        status = "inconclusive"
        decided = ("Fewer than 500 bars with a non-zero position or fewer than 10 distinct down-cross spans, "
                   "so the result is inconclusive.")
    elif mean_ex is None or t_nw is None:
        status = "inconclusive"
        decided = "The Newey-West t-statistic could not be computed, so the result is inconclusive."
    elif mean_ex > 0 and t_nw >= 2 and sup_passed is True:
        status = "confirmed"
        decided = "Mean excess return above 0 with t >= 2 and supporting share above 50%: confirmed."
    elif mean_ex < 0 and t_nw <= -2:
        status = "rejected"
        decided = "Mean excess return below 0 with t <= -2 (reversal after down crosses): rejected."
    elif mean_ex > 0 and t_nw >= 2:
        status = "inconclusive"
        decided = "A confirming t with a supporting share of 50% or less (or none measurable): inconclusive."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean excess return: position x (next-bar return - coin's window mean daily return), pooled",
            "value": mean_ex,
            "statistic": {"name": "Newey-West t (lag 10)", "value": t_nw} if t_nw is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 and supporting share > 50%; reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "share of completed down-cross spans returning below the coin's same-length span median",
            "value": float(share) if share is not None else None,
            "passed": sup_passed,
        },
        "counts": {
            "bars with a non-zero position": int(nonzero_pos_bars),
            "distinct down-cross spans": int(n_runs),
            "completed down-cross spans": int(judged),
        },
        "decided_by": decided,
        "reading": ("Excess returns use every bar (zero-position bars add zero) pooled in coin then window order for one "
                    "Newey-West series, the window mean is the mean of all next-bar returns in that window; a down-cross "
                    "span is a maximal run of bars with raw spread < 0 inside one window (all runs count toward the 10), "
                    "a completed span is bounded by non-negative spread on both sides and its return runs from the "
                    "cross bar's close to the close of the up-cross bar, compared with the median of all same-length "
                    "close-to-close returns of that coin across its windows."),
    }
