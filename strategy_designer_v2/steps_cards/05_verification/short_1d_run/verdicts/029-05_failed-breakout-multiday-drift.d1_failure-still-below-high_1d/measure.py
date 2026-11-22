import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 8
    PERIOD = 20
    BAND = 2.0
    MIN_CASES = 30

    def prior_high(close):
        # old 20-day closing high, current bar excluded
        return close.shift(1).rolling(PERIOD, min_periods=PERIOD).max()

    def gate_situation(close):
        """True where the close 2 bars ago sat below the old high of the most
        recent breakout made 3 to 5 bars ago; NaN where not computable."""
        c = close.values.astype(float)
        ph = prior_high(close).values.astype(float)
        n = len(c)
        out = np.full(n, np.nan)
        brk = np.where(np.isnan(ph), np.nan, (c > ph).astype(float))
        for t in range(n):
            s = t - 2
            lo = s - 3
            if lo < 0 or s < 0:
                continue
            window = brk[lo:s]  # bars s-3 .. s-1, i.e. t-5 .. t-3
            if np.any(np.isnan(window)):
                continue
            idx = np.where(window == 1.0)[0]
            if len(idx) == 0:
                out[t] = 0.0
                continue
            b = lo + idx[-1]
            out[t] = 1.0 if c[s] < ph[b] else 0.0
        return out

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            sit = gate_situation(close)
            for t in range(len(df)):
                if f[t] == 0 or np.isnan(sit[t]):
                    continue
                n_active += 1
                if sit[t] == 1.0 and f[t] < 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active},
            "decided_by": ("Fewer than 90% of active forecast bars are short bars where the close 2 bars ago "
                           "sat below the old 20-day high of a breakout made 3 to 5 bars ago"
                           if n_active > 0 else "No active forecast bars could be checked against the plan's situation"),
            "reading": ("Situation recomputed from closes (old high = max of the prior 20 closes, breakout = close above it, "
                        "most recent breakout 3 to 5 bars back); active bars without enough in-window history are left out."),
        }

    # ---------- main measure ----------
    moves = []
    absf = []
    for coin, wins in bars.items():
        # normal 8-bar drift over all windows of the coin (non-overlapping grid)
        rets = []
        for w, df in wins.items():
            c = df.sort_values("timestamp")["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        if len(rets) == 0:
            continue
        drift = float(np.mean(rets))

        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(df)
            # short bets: rise of the short forecast of at least the band from its low since the last bet
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            prev_short = False
            for t in range(n):
                if f[t] < 0:
                    m = -f[t]
                    if not prev_short:
                        ref = 0.0
                    ref = min(ref, m)
                    if m - ref >= BAND:
                        bet[t] = True
                        ref = m
                    prev_short = True
                else:
                    prev_short = False
                    ref = 0.0
            # once per 8-bar grid cell: first bet in the cell
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + idx[0]
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                moves.append(-(r - drift))
                absf.append(abs(f[t]))

    moves = np.array(moves, dtype=float)
    absf = np.array(absf, dtype=float)
    n_cases = int(len(moves))

    mean = float(np.mean(moves)) if n_cases > 0 else None
    tval = None
    if n_cases > 1:
        sd = np.std(moves, ddof=1)
        if sd > 0:
            tval = float(mean / (sd / np.sqrt(n_cases)))
    slope = None
    if n_cases >= 3 and np.std(absf) > 0:
        slope = float(stats.linregress(absf, moves).slope)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than {MIN_CASES} cases ({n_cases}), the plan's minimum count."
        sup_pass = None if slope is None else bool(slope > 0)
    else:
        sup_pass = None if slope is None else bool(slope > 0)
        if tval is not None and mean > 0 and tval >= 2:
            if sup_pass:
                status = "confirmed"
                decided = "Mean unusual move above 0 with t >= 2 over at least 30 cases, and the slope on |forecast| above 0."
            else:
                status = "inconclusive"
                decided = "A confirming mean (t >= 2) but the slope on |forecast| is at or below 0."
        elif tval is not None and tval <= -2:
            status = "rejected"
            decided = "Mean unusual move has t <= -2 over at least 30 cases."
        else:
            status = "inconclusive"
            decided = "t strictly between -2 and 2 over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean short-direction unusual 8-bar move per case",
            "value": mean,
            "statistic": {"name": "t of the mean", "value": tval} if tval is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 over >= 30 cases; reject: t <= -2 over >= 30 cases",
        },
        "supporting_check": {
            "name": "OLS slope of unusual move on |forecast|",
            "value": slope,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": ("Cases are the first short bet (a rise of the short forecast of at least 2 points from its low since "
                    "the last bet) in each 8-bar grid cell from each window's first row, dropped when 8 bars do not remain "
                    "in the window; the drift is the coin's mean non-overlapping 8-bar return over all its windows; the "
                    "situation is recomputed from closes and active bars without enough in-window history are left out of the check."),
    }
