import numpy as np
import pandas as pd

FC = "forecast"
RAW = "debug_info.components.panic.last_history_value"
H = 84
BAND = 2.0
MIN_CASES = 30


def _range_ratio(df):
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    width = high.rolling(6, min_periods=6).max() - low.rolling(6, min_periods=6).min()
    mbr = (high - low).rolling(180, min_periods=180).mean()
    ratio = width / mbr
    ratio[mbr <= 0] = np.nan
    return ratio


def _bets(fc):
    """Positions of long bets: rises of the forecast of at least the band from its lowest long level since the last bet."""
    out = []
    low = 0.0
    for i, f in enumerate(fc):
        if not np.isfinite(f) or f <= 0:
            low = 0.0
            continue
        if f - low >= BAND:
            out.append(i)
            low = f
        else:
            low = min(low, f)
    return out


def measure(bars):
    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df[FC], errors="coerce")
            active = fc.notna() & (fc != 0)
            if not active.any():
                continue
            ratio = _range_ratio(df)
            regime_mr = df["regime"].astype(str) == "mean_reversion"
            panic = pd.Series(np.where(ratio.notna(), ratio >= 7.5, regime_mr), index=df.index).astype(bool)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            fall_and_rise = raw.notna() & (raw > 0)
            ok = active & panic & fall_and_rise & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("The panic stretch is the 6-bar high-low width over the mean high-low of the last 180 bars "
               "(current bar included) >= 7.5, taken from the regime column where 180 bars are not available, "
               "the fall with a positive 90-day return is a positive raw panic value, and the side is long; "
               "a case is the first long bet in each 84-bar grid cell of its window (positions counted from the "
               "window's first row) whose 84-bar return lies inside the window, the normal drift is the mean of "
               "the coin's non-overlapping 84-bar returns over all its windows, the halves are forecast > median "
               "versus <= median, and fewer than 30 cases is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of a panic stretch "
                           "(6-bar range >= 7.5 mean bar ranges) with a fall and a positive 540-bar return, "
                           "as the plan's Fidelity requires." if n_active > 0 else
                           "No bar carries a non-zero forecast, so the forecast never acts in the plan's situation."),
            "reading": reading,
        }

    # ---------- criterion ----------
    unusual = []
    fcs = []
    for coin, wins in bars.items():
        # normal drift over all windows
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for p in range(0, len(c) - H, H):
                a, b = c[p], c[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df[FC], errors="coerce").to_numpy(dtype=float)
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
                fcs.append(fc[i])

    n = len(unusual)
    u = np.array(unusual, dtype=float)
    f = np.array(fcs, dtype=float)
    mean_u = float(u.mean()) if n > 0 else None
    t = None
    if n >= 2:
        sd = float(u.std(ddof=1))
        if sd > 0:
            t = float(mean_u / (sd / np.sqrt(n)))

    diff = None
    n_up = n_lo = 0
    if n >= 2:
        med = float(np.median(f))
        up = u[f > med]
        lo = u[f <= med]
        n_up, n_lo = len(up), len(lo)
        if n_up > 0 and n_lo > 0:
            diff = float(up.mean() - lo.mean())
    sup_pass = None if diff is None else bool(diff > 0)

    main = {
        "name": "mean unusual 84-bar move per long case",
        "value": mean_u,
        "statistic": {"name": "ordinary t of the mean", "value": t} if t is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 and upper-minus-lower half > 0; reject: mean < 0 with t <= -2",
    }
    sup = {"name": "upper-half minus lower-half mean unusual move (split at median forecast)",
           "value": diff, "passed": sup_pass}
    counts = {"cases": int(n), "upper half cases": int(n_up), "lower half cases": int(n_lo)}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases over all coins and windows, fewer than the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (no dispersion), so neither rule is met."
    elif mean_u > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 and the upper-half-minus-lower-half difference is above 0."
        else:
            status = "inconclusive"
            decided = "The mean unusual move is positive with t >= 2 but the upper-half-minus-lower-half difference is not above 0."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
