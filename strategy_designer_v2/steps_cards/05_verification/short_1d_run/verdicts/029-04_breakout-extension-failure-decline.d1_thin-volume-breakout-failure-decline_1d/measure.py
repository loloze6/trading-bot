import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    PERIOD = 20
    BAND = 2.0
    MIN_CASES = 20
    RAW = "debug_info.components.thin_fail.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            raw = (pd.to_numeric(df[RAW], errors="coerce").values
                   if RAW in df.columns else np.full(len(df), np.nan))
            high = pd.to_numeric(df["high"], errors="coerce").values
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            # prior 20-bar high, excluding the bar itself
            ph = pd.Series(high).shift(1).rolling(PERIOD, min_periods=PERIOD).max().values
            brk = close > ph
            for t in range(n):
                if f[t] == 0:
                    continue
                n_active += 1
                thin_ok = np.isfinite(raw[t]) and raw[t] > 0
                # price-based failed breakout: a breakout in the prior bars, close now back below its old high
                computable = t - 4 >= PERIOD
                price_ok = True
                if computable:
                    price_ok = False
                    for b in range(max(0, t - 4), t):
                        if np.isfinite(ph[b]) and brk[b] and close[t] <= ph[b]:
                            price_ok = True
                            break
                if thin_ok and price_ok and f[t] < 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active forecast bars are short bars on a thin-volume "
                           "failed breakout (raw thinness > 0 with a breakout in the last bars and a close "
                           "back below its prior 20-day high), as the plan's Fidelity requires."),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    # coin's mean 5-bar return over all windows (non-overlapping grid)
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    moves = []
    thins = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            raw = (pd.to_numeric(df[RAW], errors="coerce").values
                   if RAW in df.columns else np.full(len(df), np.nan))
            n = len(df)
            # short bets: a fall of the forecast of >= BAND from its level nearest zero on the short side since the last bet
            ref = 0.0
            signals = []
            for t in range(n):
                if f[t] >= 0:
                    ref = 0.0
                    continue
                mag = -f[t]
                if mag - ref >= BAND - 1e-12:
                    signals.append(t)
                    ref = mag
                else:
                    ref = min(ref, mag)
            used_cells = set()
            for t in signals:
                cell = t // H
                if cell in used_cells:
                    continue
                used_cells.add(cell)
                if t + H >= n or not np.isfinite(drift[coin]):
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                moves.append(-(r - drift[coin]))
                thins.append(raw[t])

    moves = np.array(moves, dtype=float)
    thins = np.array(thins, dtype=float)
    n_cases = int(len(moves))

    mean_move = float(np.mean(moves)) if n_cases > 0 else None
    t_stat = None
    if n_cases >= 2:
        sd = np.std(moves, ddof=1)
        if sd > 0:
            t_stat = float(mean_move / (sd / np.sqrt(n_cases)))

    rho = None
    mask = np.isfinite(thins) & np.isfinite(moves)
    if mask.sum() >= 3:
        r_, _ = stats.spearmanr(thins[mask], moves[mask])
        if np.isfinite(r_):
            rho = float(r_)
    corr_pass = None if rho is None else bool(rho > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} short-signal cases, below the plan's minimum of 20 cases."
    elif t_stat is not None and t_stat >= 2:
        if corr_pass:
            status = "confirmed"
            decided = "The mean short-signed unusual move has t >= 2 over at least 20 cases and the Spearman correlation with thinness is above 0."
        else:
            status = "inconclusive"
            decided = "A confirming t >= 2 with the supporting correlation at or below 0 (or not computable) is inconclusive."
    elif t_stat is not None and t_stat <= -2:
        status = "rejected"
        decided = "The mean short-signed unusual move has t <= -2 over at least 20 cases: these failures rise more than usual."
    else:
        status = "inconclusive"
        decided = "The t of the mean short-signed unusual move lies between -2 and 2 over at least 20 cases."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": {
            "name": "mean short-signed 5-bar unusual move after short signals (before costs)",
            "value": mean_move,
            "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
            "threshold": "confirm if t >= 2 over at least 20 cases; reject if t <= -2 over at least 20 cases",
        },
        "supporting_check": {
            "name": "Spearman correlation of thinness with short-signed unusual move > 0",
            "value": rho,
            "passed": corr_pass,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": ("A short signal is a fall of the forecast of at least 2 points from its level nearest zero on the "
                    "short side since the last bet (from 0 after flat), the first one per 5-bar grid cell counted from "
                    "each window's first row, with the coin's drift the mean of its non-overlapping 5-bar grid returns "
                    "pooled over all windows."),
    }
