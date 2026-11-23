import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    PERIOD = 20
    FAIL_WINDOW = 3
    MIN_CASES = 30
    RAW = "debug_info.components.failed_breakout_depth.last_history_value"

    def situation_from_prices(close):
        # A failed breakout: the most recent bar 1..3 ago whose close beat the prior 20 closes,
        # and today's close below that bar's prior 20-close high. None when the window's prices
        # are too short to tell.
        n = len(close)
        out = [None] * n
        for t in range(n):
            if t - FAIL_WINDOW - PERIOD < 0:
                continue
            res = False
            for k in range(1, FAIL_WINDOW + 1):
                b = t - k
                prior = close[b - PERIOD:b]
                if np.any(~np.isfinite(prior)) or not np.isfinite(close[b]):
                    res = None
                    break
                hi = np.max(prior)
                if close[b] > hi:
                    res = bool(np.isfinite(close[t]) and close[t] < hi)
                    break
            out[t] = res
        return out

    # ---------- situation check ----------
    active = 0
    agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            raw = (pd.to_numeric(df[RAW], errors="coerce").to_numpy()
                   if RAW in df.columns else np.full(len(df), np.nan))
            sit_p = situation_from_prices(close)
            for t in range(len(df)):
                if not np.isfinite(fc[t]) or fc[t] == 0:
                    continue
                active += 1
                if sit_p[t] is not None:
                    sit = sit_p[t]
                else:
                    sit = bool(np.isfinite(raw[t]) and raw[t] != 0)
                if sit and fc[t] < 0:
                    agree += 1

    agreement = (agree / active) if active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)
    main_name = "mean short-direction 5-bar excess return over drift"
    thr = "mean > 0 with t >= 2 over at least 30 cases (confirm); mean < 0 with t <= -2 over at least 30 cases (reject)"
    sup_name = "Spearman rank correlation |forecast| vs short excess return"
    reading_txt = ("Situation recomputed from closes (most recent bar 1-3 ago with close above the max of its prior 20 closes, "
                   "today's close below that max), falling back to a nonzero raw component value where the window's prices are too short; "
                   "a case is a short bet (|forecast| rising by >= 2 from its lowest size on the short side since the last bet, reset to 0 on flat or side change), "
                   "the first one per non-overlapping 5-bar cell from each window's first row, with drift the coin's mean 5-bar grid return over all its windows.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(active), "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are short bars of a failed breakout "
                           "(close back below the prior 20-close high within 3 bars of the breakout), as the Fidelity requires."),
            "reading": reading_txt,
        }

    # ---------- drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df.sort_values("timestamp")["close"].astype(float).to_numpy()
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    excess = []
    absf = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            n = len(df)
            side = 0
            ref = 0.0
            bet_bars = []
            for t in range(n):
                f = fc[t]
                s = int(np.sign(f))
                if s != side:
                    side = s
                    ref = 0.0
                if s == 0:
                    ref = 0.0
                    continue
                m = abs(f)
                if m - ref >= BAND - 1e-12:
                    if s < 0:
                        bet_bars.append(t)
                    ref = m
                else:
                    ref = min(ref, m)
            seen = set()
            for t in bet_bars:
                cell = t // H
                if cell in seen:
                    continue
                seen.add(cell)
                if t + H >= n:
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    continue
                if not np.isfinite(drift.get(coin, np.nan)):
                    continue
                r = close[t + H] / close[t] - 1.0
                excess.append(-(r - drift[coin]))
                absf.append(abs(fc[t]))

    ncases = len(excess)
    ex = np.array(excess, dtype=float)
    mean = float(np.mean(ex)) if ncases > 0 else None
    tval = None
    if ncases > 1:
        sd = float(np.std(ex, ddof=1))
        if sd > 0:
            tval = float(mean / (sd / np.sqrt(ncases)))
    rho = None
    if ncases > 2:
        r_, _ = stats.spearmanr(np.array(absf), ex)
        if np.isfinite(r_):
            rho = float(r_)

    if ncases < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than 30 cases across all coins and windows ({ncases}): the minimum count is not reached."
    elif tval is not None and mean > 0 and tval >= 2:
        if rho is not None and rho > 0:
            status = "confirmed"
            decided = "Mean short-direction excess return above 0 with t >= 2 over at least 30 cases, and rank correlation above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the rank correlation is 0 or below (or undefined): inconclusive."
    elif tval is not None and mean < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean short-direction excess return below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2 (or undefined) with at least 30 cases: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": None if tval is None else {"name": "t of the mean", "value": tval},
            "threshold": thr,
        },
        "supporting_check": {"name": sup_name, "value": rho,
                             "passed": None if rho is None else bool(rho > 0)},
        "counts": {"cases": int(ncases)},
        "decided_by": decided,
        "reading": reading_txt,
    }
