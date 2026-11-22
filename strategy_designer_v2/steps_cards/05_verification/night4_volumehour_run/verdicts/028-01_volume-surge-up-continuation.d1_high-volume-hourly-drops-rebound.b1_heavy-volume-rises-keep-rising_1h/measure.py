import numpy as np
import pandas as pd

RAW = "debug_info.components.vol_move.last_history_value"
H = 24
BAND = 2.0
MIN_CASES = 30


def _bets(f):
    """Indices of long bets: rises of the forecast of at least BAND from its lowest positive level since the last bet."""
    out = []
    ref = 0.0
    for i, v in enumerate(f):
        if not np.isfinite(v) or v <= 0:
            ref = 0.0
            continue
        if v < ref:
            ref = v
        if v - ref >= BAND:
            out.append(i)
            ref = v
    return out


def measure(bars):
    # ---------- situation check ----------
    active = 0
    agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin], key=lambda s: int(str(s).lstrip("w")) if str(s).lstrip("w").isdigit() else str(s)):
            df = bars[coin][w]
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            ret1 = np.full(len(close), np.nan)
            if len(close) > 1:
                ret1[1:] = close[1:] / close[:-1] - 1
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(close), np.nan)
            # where the raw value is missing, its sign is the sign of the hour's return (volume ratio > 0)
            sit_val = np.where(np.isfinite(raw), raw, ret1)
            act = np.isfinite(f) & (f != 0)
            active += int(act.sum())
            agree += int((act & (f > 0) & np.isfinite(sit_val) & (sit_val > 0)).sum())
    agreement = float(agree / active) if active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": active},
            "decided_by": ("No active bars in the record." if active == 0 else
                           "Fewer than 90% of the bars with a non-zero forecast are long bars after a rising hour "
                           "(positive volume-weighted scaled return), as the plan's situation requires."),
            "reading": "The situation is a rising hour (raw component value > 0) with a positive forecast.",
        }

    # ---------- criterion ----------
    unusual = []
    fc_at_case = []
    for coin in sorted(bars):
        wins = bars[coin]
        # normal drift: mean of non-overlapping 24-bar returns over all windows of the coin
        grid_rets = []
        for w in wins:
            c = pd.to_numeric(wins[w]["close"], errors="coerce").to_numpy(dtype=float)
            for p in range(0, len(c) - H, H):
                r = c[p + H] / c[p] - 1
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for w in wins:
            df = wins[w]
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            seen = set()
            for i in _bets(f):
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= len(c):
                    continue
                r = c[i + H] / c[i] - 1
                if not np.isfinite(r):
                    continue
                unusual.append(r - drift)
                fc_at_case.append(f[i])

    u = np.asarray(unusual, dtype=float)
    fc = np.asarray(fc_at_case, dtype=float)
    n = int(len(u))
    mean = float(u.mean()) if n > 0 else None
    t = None
    if n > 1:
        sd = u.std(ddof=1)
        t = float(mean / (sd / np.sqrt(n))) if sd > 0 else None

    diff = None
    if n >= 2:
        order = np.argsort(fc, kind="mergesort")
        half = n // 2
        bottom = u[order[:half]]
        top = u[order[n - half:]]
        diff = float(top.mean() - bottom.mean())
    sup_pass = None if diff is None else bool(diff > 0)

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 30."
    elif t is not None and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move has t >= 2 over at least 30 cases and the top half beats the bottom half."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the top half's mean unusual move is not above the bottom half's."
    elif t is not None and t <= -2:
        status = "rejected"
        decided = "The mean unusual move has t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "mean unusual 24-bar move after each case",
            "value": mean,
            "statistic": None if t is None else {"name": "t of the mean", "value": t},
            "threshold": "confirm t >= 2, reject t <= -2, over at least 30 cases",
        },
        "supporting_check": {
            "name": "top half minus bottom half mean unusual move (by forecast)",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": {"cases": n},
        "decided_by": decided,
        "reading": ("A case is the first bet (forecast rise >= 2 from its lowest positive level since the last bet, "
                    "from 0 after flat) in each 24-bar cell counted from each window's first row, the drift is the "
                    "coin's mean non-overlapping 24-bar return over all its windows, and the halves are the lower and "
                    "upper floor(n/2) cases by forecast (stable sort), the middle case dropped when n is odd."),
    }
