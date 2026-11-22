import numpy as np
import pandas as pd
from scipy import stats

H = 5
BAND = 2.0
PERIOD = 20
FAIL_WINDOW = 4
RAW_COL = "debug_info.components.fail_exc.last_history_value"


def _price_situation(close):
    """Recompute the failed-breakout situation from closes: a closing break above the
    prior 20-day closing high within the last FAIL_WINDOW bars, and the close now back below that old high."""
    c = np.asarray(close, dtype=float)
    n = len(c)
    out = np.zeros(n, dtype=bool)
    for t in range(n):
        for b in range(max(PERIOD, t - FAIL_WINDOW + 1), t + 1):
            old_high = np.nanmax(c[b - PERIOD:b])
            if c[b] > old_high and c[t] < old_high:
                out[t] = True
                break
    return out


def _bets(fc):
    """Short-side bets: the forecast's short size rises by at least BAND from its lowest
    short size since the last bet (from 0 after flat or a change of side)."""
    f = np.nan_to_num(np.asarray(fc, dtype=float), nan=0.0)
    bets = np.zeros(len(f), dtype=bool)
    ref = 0.0
    for i, v in enumerate(f):
        if v >= 0:
            ref = 0.0
            continue
        m = -v
        if m - ref >= BAND:
            bets[i] = True
            ref = m
        else:
            ref = min(ref, m)
    return bets


def measure(bars):
    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            price_sit = _price_situation(close)
            if RAW_COL in df.columns:
                raw = pd.to_numeric(df[RAW_COL], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            sit = np.where(np.isnan(raw), price_sit, raw > 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean short-signed unusual 5-bar move of the short bets"
    main_thr = "confirm: > 0 with t >= 2 over at least 30 cases; reject: < 0 with t <= -2 over at least 30 cases"
    sup_name = "slope of raw 5-bar forward return on raw excursion among cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases": 0, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars of the plan's "
                           "failed-breakout situation (close back below the old 20-day closing high within 4 bars "
                           "of a closing breakout, positive raw excursion)."),
            "reading": "The situation is the component's raw excursion > 0, recomputed from closes where the raw value is missing.",
        }

    # ---------- criterion ----------
    unusual = []
    raw_ret = []
    exc = []
    for coin in sorted(bars):
        # coin drift: mean 5-bar return over all windows, non-overlapping grid
        grid_rets = []
        for w in sorted(bars[coin]):
            c = pd.to_numeric(bars[coin][w]["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            c = pd.to_numeric(df["close"], errors="coerce").values
            raw = (pd.to_numeric(df[RAW_COL], errors="coerce").values
                   if RAW_COL in df.columns else np.full(len(df), np.nan))
            bets = _bets(fc)
            n = len(df)
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bets[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n or not (np.isfinite(c[i]) and np.isfinite(c[i + H])) or c[i] <= 0:
                    continue
                r = c[i + H] / c[i] - 1.0
                unusual.append(-(r - drift))
                raw_ret.append(r)
                exc.append(raw[i])

    unusual = np.array(unusual, dtype=float)
    raw_ret = np.array(raw_ret, dtype=float)
    exc = np.array(exc, dtype=float)
    n_cases = int(len(unusual))

    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    if n_cases > 1:
        sd = float(np.std(unusual, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0
    else:
        t_u = None

    mask = np.isfinite(exc) & np.isfinite(raw_ret)
    n_reg = int(mask.sum())
    slope = None
    t_slope = None
    if n_reg >= 3 and np.std(exc[mask]) > 0:
        lr = stats.linregress(exc[mask], raw_ret[mask])
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else 0.0
    check_pass = None if slope is None else bool(slope < 0 and t_slope <= -2)

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30."
    else:
        main_conf = mean_u > 0 and t_u >= 2
        main_rej = mean_u < 0 and t_u <= -2
        slope_rej = slope is not None and slope > 0 and t_slope >= 2
        if main_conf and check_pass:
            status = "confirmed"
            decided = "Mean short-signed unusual move > 0 with t >= 2 over at least 30 cases, and the excursion slope is negative with t <= -2."
        elif main_rej or slope_rej:
            status = "rejected"
            decided = ("Mean short-signed unusual move < 0 with t <= -2 over at least 30 cases." if main_rej
                       else "The excursion slope is positive with t >= 2.")
        else:
            status = "inconclusive"
            decided = ("Main measure meets the confirm rule but the slope check fails." if main_conf
                       else "Main t between -2 and 2 and no reject condition met.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_u is None else {"name": "t of the mean", "value": t_u},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": slope, "passed": check_pass,
                             "t": t_slope, "n": n_reg},
        "counts": {"cases": n_cases, "regression cases": n_reg},
        "decided_by": decided,
        "reading": ("A case is the first short bet in each 5-bar grid cell of a window counted from its first row; the "
                    "excursion regressor is the raw value on that bet bar; the drift is the coin's mean 5-bar return on "
                    "the same non-overlapping grid over all its windows; the situation is the raw excursion > 0, "
                    "recomputed from closes where the raw value is missing."),
    }
