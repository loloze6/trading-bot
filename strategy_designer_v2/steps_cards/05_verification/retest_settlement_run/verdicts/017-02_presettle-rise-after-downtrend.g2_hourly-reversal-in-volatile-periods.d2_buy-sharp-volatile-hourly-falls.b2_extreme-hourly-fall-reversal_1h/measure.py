import numpy as np
import pandas as pd

H = 24
BAND = 2.0
MIN_CASES = 30
RAW_COL = "debug_info.components.fall_in_vol.last_history_value"


def _raw_from_prices(close):
    r = close.pct_change()
    vol = r.rolling(20, min_periods=20).std()
    return r / vol.replace(0, np.nan)


def _bets(fc):
    """Bar positions where the forecast rises on the long side by >= BAND
    from its lowest level since the last bet (from 0 after a flat or side change)."""
    out = []
    base = 0.0
    for i, f in enumerate(fc):
        if not np.isfinite(f) or f <= 0:
            base = 0.0
            continue
        if f - base >= BAND:
            out.append(i)
            base = f
        else:
            base = min(base, f)
    return out


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW_COL in df.columns:
                raw = pd.to_numeric(df[RAW_COL], errors="coerce")
                rec = _raw_from_prices(close)
                raw = raw.where(raw.notna(), rec)
            else:
                raw = _raw_from_prices(close)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw < 0) & (fc > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 24-bar move of the cases (return minus coin's normal 24-bar drift, long)"
    thr = "confirm: mean > 0 with t >= 2 over >= 30 cases and check passes; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("A bet is a rise of the forecast of >= 2 points above its lowest positive level since the last bet "
               "(reset to 0 when the forecast is not positive), the first bet in each 24-bar grid cell (from each "
               "window's first row) is the case, cases without 24 bars left in the window are dropped, the normal drift "
               "is the coin's mean non-overlapping 24-bar return over all its windows, and the median split sorts the "
               "cases by forecast (stable, in coin/window/time order) and puts the first floor(n/2) in the lower half.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": None, "active bars": n_active},
            "decided_by": ("The plan's situation (a falling hour, raw vol-scaled 1h return < 0, bought long) holds on "
                           f"only {agreement:.1%} of the bars with a non-zero forecast, below 90%."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    unusual = []
    case_fc = []
    for coin, wins in bars.items():
        # normal drift of the coin over all windows
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for p in range(0, len(c) - H, H):
                a, b = c[p], c[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            seen = set()
            for i in _bets(fc):
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= len(c):
                    continue
                a, b = c[i], c[i + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                unusual.append((b / a - 1.0) - drift)
                case_fc.append(fc[i])

    u = np.asarray(unusual, dtype=float)
    f = np.asarray(case_fc, dtype=float)
    n = int(len(u))
    mean_u = float(u.mean()) if n > 0 else None
    t = None
    if n > 1:
        sd = float(u.std(ddof=1))
        t = float(mean_u / (sd / np.sqrt(n))) if sd > 0 else None

    diff = None
    check_passed = None
    if n >= 2:
        order = np.argsort(f, kind="mergesort")
        k = n // 2
        lower = u[order[:k]]
        upper = u[order[k:]]
        if len(lower) > 0 and len(upper) > 0:
            diff = float(upper.mean() - lower.mean())
            check_passed = bool(diff > 0)

    counts = {"cases": n}
    stat = {"name": "t of the mean", "value": t} if t is not None else None
    sup = {"name": "upper-half minus lower-half mean unusual move (median split of forecast)",
           "value": diff, "passed": check_passed}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than 30 cases ({n}), so the plan's minimum count is not reached."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero dispersion), so neither rule is met."
    elif mean_u > 0 and t >= 2:
        if check_passed:
            status = "confirmed"
            decided = "Mean unusual move positive with t >= 2 over at least 30 cases, and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "Confirm-side t >= 2 but the supporting check fails (upper half not above lower half)."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_u, "statistic": stat, "threshold": thr},
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
