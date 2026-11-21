import numpy as np
import pandas as pd

H = 18
BAND = 2.0
COMP = "debug_info.components.break.last_history_value"


def _bets(fc):
    """Bars where the forecast rises on its side by at least BAND from its lowest level on that side since the last bet."""
    out = []
    ref = 0.0
    side = 0
    for i, f in enumerate(fc):
        if not np.isfinite(f) or f == 0:
            ref, side = 0.0, 0
            continue
        s = 1 if f > 0 else -1
        a = abs(f)
        if s != side:
            ref, side = 0.0, s
        if a - ref >= BAND:
            out.append((i, s))
            ref = a
        else:
            ref = min(ref, a)
    return out


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            high = df["high"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            # 42-bar return from prices, fallback to the recorded regime where not computable
            r7 = np.full(n, np.nan)
            if n > 42:
                r7[42:] = close[42:] / close[:-42] - 1.0
            reg_ok = np.where(np.isfinite(r7), r7 > 0,
                              df["regime"].astype(str).values == "trending")
            # break: recorded raw value, else recomputed from prices (prior 12 highs, bar t excluded)
            prior_hi = pd.Series(high).shift(1).rolling(12, min_periods=12).max().values
            brk_px = np.where(np.isfinite(prior_hi), close - prior_hi, np.nan)
            if COMP in df.columns:
                raw = df[COMP].astype(float).values
            else:
                raw = np.full(n, np.nan)
            brk = np.where(np.isfinite(raw), raw, brk_px)
            brk_ok = np.isfinite(brk) & (brk > 0)
            sit = reg_ok & brk_ok
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean unusual 18-bar move of forecast rises >= 2 (one per 18-bar grid cell)"
    thr = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars where the close breaks above the prior 12-bar high while the 42-bar return is positive, as the Fidelity's situation requires.",
            "reading": "Situation = close above max high of prior 12 bars (recorded break raw value > 0, else recomputed) and 42-bar close return > 0 (from prices, else the recorded regime where fewer than 42 bars exist), on the long side.",
        }

    # ---------- 2. drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    moves, fcs = [], []
    for coin, wins in bars.items():
        d = drift[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            seen = set()
            for i, s in _bets(fc):
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= len(c) or not (np.isfinite(c[i]) and np.isfinite(c[i + H])) or not np.isfinite(d):
                    continue
                r = c[i + H] / c[i] - 1.0
                moves.append(s * (r - d))
                fcs.append(fc[i])
    moves = np.array(moves, dtype=float)
    fcs = np.array(fcs, dtype=float)
    n = len(moves)

    mean = float(moves.mean()) if n > 0 else None
    if n > 1 and moves.std(ddof=1) > 0:
        t = float(mean / (moves.std(ddof=1) / np.sqrt(n)))
    else:
        t = None

    diff = None
    if n > 0:
        med = np.median(fcs)
        top = moves[fcs > med]
        bot = moves[fcs < med]
        if len(top) > 0 and len(bot) > 0:
            diff = float(top.mean() - bot.mean())
    check_pass = None if diff is None else bool(diff > 0)

    if n < 100:
        status = "not observable"
        decided = f"Only {n} independent cases pooled over coins and windows, fewer than the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero dispersion), so neither confirm nor reject is met."
    elif mean > 0 and t >= 2 and check_pass:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and cases above the median forecast have a larger mean unusual move than those below."
    elif mean > 0 and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check (top minus bottom half above 0) fails, which the plan calls inconclusive."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name,
                         "value": mean,
                         "statistic": None if t is None else {"name": "ordinary t of the mean", "value": t},
                         "threshold": thr},
        "supporting_check": {"name": "mean unusual move above minus below median forecast",
                             "value": diff, "passed": check_pass},
        "counts": {"independent cases": int(n)},
        "decided_by": decided,
        "reading": "A case is the first bet (forecast rise >= 2 from its lowest level on its side since the last bet) in each 18-bar grid cell counted from each window's first row, cases without 18 bars ahead in their window are dropped, drift is the coin's mean non-overlapping 18-bar return over all windows, and the median split uses strictly above and strictly below the median forecast (cases at the median left out).",
    }
