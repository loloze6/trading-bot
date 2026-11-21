import numpy as np
import pandas as pd

RAW_COL = "debug_info.components.break.last_history_value"
H = 120
BAND = 2.0
MIN_CASES = 30


def _bets_long(f):
    """Bar positions of long bets: a rise of the forecast on the long side of at least BAND,
    measured from its lowest long level since the last bet (from 0 after a flat or a change of side)."""
    bets = []
    low = 0.0
    on_long = False
    for i, v in enumerate(f):
        if not np.isfinite(v):
            continue
        if v > 0:
            if not on_long:
                low = 0.0
                on_long = True
            if v - low >= BAND:
                bets.append(i)
                low = v
            else:
                low = min(low, v)
        else:
            on_long = False
            low = 0.0
    return bets


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            high = pd.to_numeric(df["high"], errors="coerce")
            prior_high = high.shift(1).rolling(480, min_periods=480).max()
            price_sit = close > prior_high
            price_ok = prior_high.notna() & close.notna()
            if RAW_COL in df.columns:
                raw = pd.to_numeric(df[RAW_COL], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            raw_ok = raw.notna()
            sit = pd.Series(False, index=df.index)
            sit[raw_ok] = raw[raw_ok] > 0
            fb = (~raw_ok) & price_ok
            sit[fb] = price_sit[fb]
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & sit & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    main_name = "mean unusual 120-bar move of long bets (one per 120-bar grid cell)"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2; at least 30 cases"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars where the close is above "
                          "the prior 480-bar high (raw break > 0), as the plan's situation requires.",
            "reading": "Situation taken as raw break > 0 (price-based close > prior 480-bar high where raw is missing), expected side long.",
        }

    # ---------- 2. criterion ----------
    moves, raws = [], []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 120-bar returns over all windows of the coin
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
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            raw = (pd.to_numeric(df[RAW_COL], errors="coerce").to_numpy(dtype=float)
                   if RAW_COL in df.columns else np.full(len(df), np.nan))
            seen = set()
            for t in _bets_long(f):
                cell = t // H
                if cell in seen:
                    continue
                seen.add(cell)
                if t + H >= len(c):
                    continue
                a, b = c[t], c[t + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                moves.append(b / a - 1.0 - drift)
                raws.append(raw[t])
    moves = np.array(moves, dtype=float)
    raws = np.array(raws, dtype=float)
    n = int(len(moves))

    mean = float(np.mean(moves)) if n > 0 else None
    tstat = None
    if n > 1:
        sd = float(np.std(moves, ddof=1))
        tstat = float(mean / (sd / np.sqrt(n))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    n_up = n_lo = 0
    ok = np.isfinite(raws)
    if ok.sum() >= 2:
        r, m = raws[ok], moves[ok]
        med = float(np.median(r))
        up, lo = m[r > med], m[r <= med]
        n_up, n_lo = int(len(up)), int(len(lo))
        if n_up > 0 and n_lo > 0:
            sup_val = float(up.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)

    reading = ("Cases are the first long bet (forecast rise >= 2 points from its lowest long level since the last bet) "
               "in each 120-bar grid cell counted from each window's first row, dropped if t+120 leaves the window; "
               "the upper half is raw break strictly above the median of the cases, the lower half at or below it.")

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases over all coins and windows, fewer than the plan's minimum of 30."
    elif tstat is not None and mean > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move above 0 with t >= 2, and the larger-break half beats the smaller-break half."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the larger-break half does not beat the smaller-break half, so the plan calls it inconclusive."
    elif tstat is not None and mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2 (or is undefined)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": {"name": "t of the mean", "value": tstat} if tstat is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean unusual move, upper-break half minus lower-break half",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n, "upper half cases": n_up, "lower half cases": n_lo},
        "decided_by": decided,
        "reading": reading,
    }
