import numpy as np
import pandas as pd
from scipy import stats

H = 72
BAND = 2.0
RAW_COL = "debug_info.components.dip_in_rise.last_history_value"


def _bet_bars(fc):
    """Long-side bets: rises of the forecast of at least BAND from its lowest
    positive level since the last bet (from 0 after a flat or a change of side)."""
    bets = []
    ref = 0.0
    for i, f in enumerate(fc):
        if not np.isfinite(f) or f <= 0:
            ref = 0.0
            continue
        if f - ref >= BAND:
            bets.append(i)
            ref = f
        else:
            ref = min(ref, f)
    return bets


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            if RAW_COL in df.columns:
                raw = pd.to_numeric(df[RAW_COL], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            c = pd.Series(close)
            r24 = (c / c.shift(24) - 1).values
            r720 = (c / c.shift(720) - 1).values
            for i in range(len(df)):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                if np.isfinite(raw[i]):
                    sit = raw[i] > 0
                elif np.isfinite(r24[i]) and np.isfinite(r720[i]):
                    sit = (r24[i] < 0) and (r720[i] > 0)
                else:
                    sit = False
                if sit and f > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are bars where the 24-hour return fell "
                          "inside a positive 30-day return (raw component > 0) with a long forecast, so the config "
                          "does not do what the plan's situation and long side state.",
            "reading": "The situation is read as the raw component being positive (a 24-hour fall times a positive "
                       "30-day return), recomputed from prices where the raw value is missing; the expected side is long.",
        }

    # ---------- 2. criterion ----------
    case_moves = []
    case_fc = []
    for coin in sorted(bars):
        # normal drift: mean 72-bar return on the non-overlapping grid of all windows
        grid_rets = []
        for w in sorted(bars[coin]):
            close = bars[coin][w]["close"].astype(float).values
            for t in range(0, len(close) - H, H):
                a, b = close[t], close[t + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for w in sorted(bars[coin]):
            df = bars[coin][w]
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            seen_cells = set()
            for t in _bet_bars(fc):
                cell = t // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if t + H >= len(close):
                    continue
                a, b = close[t], close[t + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                case_moves.append((b / a - 1) - drift)
                case_fc.append(fc[t])

    x = np.asarray(case_moves, dtype=float)
    fcs = np.asarray(case_fc, dtype=float)
    n = int(len(x))

    mean = float(np.mean(x)) if n > 0 else None
    tval = None
    if n > 1:
        sd = float(np.std(x, ddof=1))
        tval = float(mean / (sd / np.sqrt(n))) if sd > 0 else None

    # supporting check
    sup_val, sup_pass, sup_t = None, None, None
    n_up = n_lo = 0
    if n > 0:
        med = float(np.median(fcs))
        up = x[fcs > med]
        lo = x[fcs <= med]
        n_up, n_lo = int(len(up)), int(len(lo))
        if n_up > 0 and n_lo > 0:
            sup_val = float(np.mean(up) - np.mean(lo))
            sup_pass = bool(sup_val > 0)
            if n_up > 1 and n_lo > 1:
                tt = stats.ttest_ind(up, lo, equal_var=False)
                if np.isfinite(tt.statistic):
                    sup_t = float(tt.statistic)

    if n < 30:
        status = "not observable"
        decided = f"Only {n} independent cases pooled over coins and windows, fewer than the plan's minimum of 30."
    elif tval is not None and mean > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = ("Mean unusual move above 0 with t >= 2 over at least 30 independent cases, and the "
                       "upper-minus-lower median-forecast difference above 0.")
        else:
            status = "inconclusive"
            decided = "A confirming mean (above 0, t >= 2, at least 30 cases) whose supporting check fails."
    elif tval is not None and mean < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2 over at least 30 independent cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2 (or is undefined) with at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "mean 72-bar unusual move (return minus coin's normal 72-bar drift) of long bets",
            "value": mean,
            "statistic": {"name": "t of the mean", "value": tval} if tval is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 over at least 30 cases; reject: mean < 0 with t <= -2 over at least 30 cases",
        },
        "supporting_check": {
            "name": "Welch difference of mean unusual move, above minus at-or-below median entry forecast",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {
            "independent cases": n,
            "cases above median entry forecast": n_up,
            "cases at or below median entry forecast": n_lo,
        },
        "decided_by": decided,
        "reading": ("Bets are long-side rises of the forecast of at least 2 points from its lowest level since the "
                    "last bet (reset to 0 when flat), the first per 72-bar grid cell of each window counted from its "
                    "first row, with cases whose 72-bar return leaves the window dropped; cases tied at the median "
                    "entry forecast are put in the lower group, and the supporting check passes on the sign of the "
                    "difference, as the confirm rule states."),
    }
