import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 84
    FALL = 6
    BAND = 2.0
    RAW = "debug_info.components.panic.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            prev = close.shift(FALL)
            fall_ok = prev.notna() & close.notna()
            fall = close < prev
            raw_ok = raw.notna()
            raw_pos = raw > 0
            situ = np.where(
                fall_ok & raw_ok, fall & raw_pos,
                np.where(fall_ok, fall, np.where(raw_ok, raw_pos, False)),
            ).astype(bool)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & pd.Series(situ, index=df.index) & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of a 24-hour fall "
                           "(close below its level 6 bars ago) with a positive range-multiple x volatility-ratio value."),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    def grid_returns(close):
        c = close.values
        out = []
        n = len(c)
        for p in range(0, n, H):
            if p + H < n and np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                out.append(c[p + H] / c[p] - 1.0)
        return out

    cases = []  # (unusual move, forecast size)
    for coin, wins in bars.items():
        # coin's normal drift over all windows (non-overlapping grid)
        allr = []
        for w, df in wins.items():
            allr += grid_returns(pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True))
        if len(allr) == 0:
            continue
        drift = float(np.mean(allr))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(df)
            # long bets: forecast rise >= band from its lowest level since last bet (0 after flat)
            bet = np.zeros(n, dtype=bool)
            low = 0.0
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    bet[i] = True
                    low = f
                else:
                    low = min(low, f)
            # one case per grid cell: the first bet in the cell
            for p in range(0, n, H):
                idx = np.where(bet[p:p + H])[0]
                if len(idx) == 0:
                    continue
                t = p + int(idx[0])
                if t + H < n and np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] != 0:
                    r = close[t + H] / close[t] - 1.0
                    cases.append((r - drift, float(fc[t])))

    n_cases = len(cases)
    counts = {"cases in total": int(n_cases)}
    threshold = "mean > 0 with t >= 2 (confirm, with supporting check); mean < 0 with t <= -2 (reject)"

    if n_cases > 0:
        um = np.array([c[0] for c in cases])
        mean = float(um.mean())
        if n_cases > 1 and um.std(ddof=1) > 0:
            t = float(mean / (um.std(ddof=1) / np.sqrt(n_cases)))
        else:
            t = None
    else:
        mean, t = None, None

    sup_val, sup_pass = None, None
    if n_cases >= 2:
        sizes = np.array([c[1] for c in cases])
        order = np.argsort(sizes, kind="mergesort")
        half = n_cases // 2
        bottom = um[order[:half]]
        top = um[order[n_cases - half:]]
        sup_val = float(top.mean() - bottom.mean())
        sup_pass = bool(sup_val > 0)

    main = {
        "name": "mean unusual 84-bar move per case (return minus coin's normal 84-bar drift)",
        "value": mean,
        "statistic": {"name": "ordinary t", "value": t} if t is not None else None,
        "threshold": threshold,
    }
    support = {"name": "top-half minus bottom-half forecast size mean unusual move",
               "value": sup_val, "passed": sup_pass}

    if n_cases < 30:
        status = "not observable"
        decided = f"Fewer than 30 cases in total ({n_cases}): the plan's minimum count is not reached."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed, so no confirm or reject rule is met."
    elif mean > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is above 0 with t >= 2 and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "A confirming t (>= 2) with a failed supporting check is inconclusive."
        
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": ("A case is the first long bet (forecast rise of at least 2 points from its lowest level since "
                    "the last bet, from 0 after flat) in each 84-bar grid cell of a window, its return taken from that "
                    "bar's close if 84 bars remain in the window; cases of all coins are pooled into one mean; "
                    "the halves of forecast size are split by rank at the signal bar (the middle case left out when "
                    "the count is odd); the plan's fewer-than-30-cases rule is treated as the minimum count."),
    }
