import numpy as np
import pandas as pd
from scipy import stats

RAW = "debug_info.components.failed_bo_calm.last_history_value"
H = 5
BAND = 2.0
MIN_CASES = 30


def _price_situation(close, period=20, fail_window=3):
    """Failed breakout recomputed from prices: a close above the prior 20-bar
    closing high 1 to 3 bars ago, and today's close below that old high."""
    c = pd.Series(np.asarray(close, dtype=float))
    prior_high = c.shift(1).rolling(period, min_periods=period).max()
    breakout = (c > prior_high).fillna(False).values
    ph = prior_high.values
    cv = c.values
    n = len(cv)
    out = np.zeros(n, dtype=bool)
    for t in range(n):
        for k in range(1, fail_window + 1):
            b = t - k
            if b >= 0 and breakout[b] and np.isfinite(ph[b]) and cv[t] < ph[b]:
                out[t] = True
                break
    return out


def _short_bets(f):
    """Short-side bets: a fall of the forecast of at least BAND below its highest
    level on the short side since its last bet (from 0 after flat or a long bar)."""
    n = len(f)
    bets = np.zeros(n, dtype=bool)
    ref = 0.0
    for i in range(n):
        x = f[i]
        if not np.isfinite(x) or x >= 0:
            ref = 0.0
            continue
        if x <= ref - BAND:
            bets[i] = True
            ref = x
        else:
            ref = max(ref, x)
    return bets


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            close = pd.to_numeric(df["close"], errors="coerce").values
            price_sit = _price_situation(close)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            sit = np.where(np.isfinite(raw), raw > 0, price_sit)
            active = np.isfinite(f) & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & sit & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars on which a "
                           "failed 20-day breakout (close back below the old high within 3 bars) holds, "
                           "so the config does not trade the plan's situation on its side."),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    unusual = []
    absf = []
    for coin, wins in bars.items():
        # coin drift: mean non-overlapping 5-bar return over all its windows
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(close)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            prepared.append((close, f))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for close, f in prepared:
            n = len(close)
            bets = _short_bets(f)
            for start in range(0, n, H):
                idx = np.where(bets[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                unusual.append(-(r - drift))
                absf.append(abs(f[t]))

    u = np.asarray(unusual, dtype=float)
    a = np.asarray(absf, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_u = None
    if n_cases > 1:
        sd = float(np.std(u, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    sup_val = None
    sup_pass = None
    n_top = n_bot = 0
    if n_cases > 0:
        med = float(np.median(a))
        top = u[a > med]
        bot = u[a <= med]
        n_top, n_bot = int(len(top)), int(len(bot))
        if n_top > 0 and n_bot > 0:
            sup_val = float(np.mean(top) - np.mean(bot))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {
        "name": "mean unusual 5-bar move in the short direction over short-bet cases",
        "value": mean_u,
        "statistic": {"name": "t of the mean", "value": t_u} if t_u is not None else None,
        "threshold": "confirm if mean > 0 with t >= 2 (and supporting check passes); reject if mean < 0 with t <= -2",
    }
    supporting = {
        "name": "mean unusual move of top half minus bottom half by |forecast|",
        "value": sup_val,
        "passed": sup_pass,
    }
    counts = {"independent cases": n_cases, "top half cases": n_top, "bottom half cases": n_bot}
    reading = ("A case is the first short bet (forecast falling at least 2 points below its highest short-side "
               "level since the last bet, reset to 0 on flat or long bars) inside each 5-bar grid cell counted from "
               "each window's first row, cases whose 5-bar return would leave the window are dropped, and the "
               "median split puts |forecast| strictly above the median in the top half.")

    if n_cases < MIN_CASES or t_u is None:
        status = "not observable"
        decided = f"Only {n_cases} independent cases over all coins and windows, fewer than the plan's minimum of 30."
    elif mean_u > 0 and t_u >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move in the short direction is above 0 with t >= 2 and the supporting check passes."
    elif mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided = "The mean unusual move in the short direction is below 0 with t <= -2: the coin rose more than usual after these cases."
    elif mean_u > 0 and t_u >= 2:
        status = "inconclusive"
        decided = "The t is confirming (>= 2) but the supporting check fails (top minus bottom half not above 0)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
