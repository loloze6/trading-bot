import numpy as np
import pandas as pd


def measure(bars):
    H = 26
    MIN_CASES = 20
    BAND = 2.0
    RAW = "debug_info.components.prior_fall.last_history_value"

    def cloud_position(df):
        high = df["high"].astype(float)
        low = df["low"].astype(float)
        close = df["close"].astype(float)
        tenkan = (high.rolling(9, min_periods=9).max() + low.rolling(9, min_periods=9).min()) / 2.0
        kijun = (high.rolling(26, min_periods=26).max() + low.rolling(26, min_periods=26).min()) / 2.0
        span_a = ((tenkan + kijun) / 2.0).shift(26)
        span_b = ((high.rolling(52, min_periods=52).max() + low.rolling(52, min_periods=52).min()) / 2.0).shift(26)
        top = np.maximum(span_a, span_b)
        bot = np.minimum(span_a, span_b)
        pos = pd.Series(np.nan, index=df.index)
        known = top.notna() & bot.notna()
        pos[known & (close > top)] = 1.0
        pos[known & (close < bot)] = -1.0
        pos[known & (close <= top) & (close >= bot)] = 0.0
        return pos.values

    def cross_flags(pos):
        # returns array: 1 = cross bar, 0 = not cross, nan = not verifiable
        n = len(pos)
        out = np.full(n, np.nan)
        for t in range(n):
            if np.isnan(pos[t]):
                continue
            if pos[t] != 1.0:
                out[t] = 0.0
                continue
            # find last outside state before t
            j = t - 1
            state = None
            while j >= 0:
                if np.isnan(pos[j]):
                    state = None
                    break
                if pos[j] != 0.0:
                    state = pos[j]
                    break
                j -= 1
            if state is None:
                out[t] = np.nan
            else:
                out[t] = 1.0 if state == -1.0 else 0.0
        return out

    # ---------- situation check ----------
    n_active = 0
    n_verifiable = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            fc = df["forecast"].astype(float).values
            pos = cloud_position(df)
            cr = cross_flags(pos)
            raw = df[RAW].astype(float).values if RAW in df.columns else np.full(len(df), np.nan)
            for t in range(len(df)):
                if not np.isfinite(fc[t]) or fc[t] == 0:
                    continue
                n_active += 1
                if np.isnan(cr[t]):
                    continue
                n_verifiable += 1
                ok = (cr[t] == 1.0) and (fc[t] > 0) and np.isfinite(raw[t]) and (raw[t] < 0)
                if ok:
                    n_agree += 1

    agreement = (n_agree / n_verifiable) if n_verifiable > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("Cloud recomputed in-window from prices (9/26/52, displaced 26); active bars whose cloud history "
               "is not inside the window are left out of the agreement, which also requires a long forecast and a "
               "negative raw 26-bar return; cases are bars with forecast >= 2, first one per 26-bar grid cell from "
               "each window's first row with 26 bars left; normal drift is the coin's mean non-overlapping 26-bar "
               "return over all its windows; the median split puts cases above the median forecast in the larger "
               "half and the rest in the smaller half; the plan's 'fewer than 20 independent cases' is applied as "
               "the minimum count (not observable).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "verifiable active bars": int(n_verifiable)},
            "decided_by": ("Fewer than 90% of the verifiable active bars are upward cloud-cross bars after a "
                           "26-day fall with a long forecast, as the plan's Fidelity states."),
            "reading": reading,
        }

    # ---------- drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    moves = []
    fcs = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            seen = set()
            for t in range(len(df)):
                if not np.isfinite(fc[t]) or fc[t] < BAND:
                    continue
                if t + H >= len(df):
                    continue
                cell = t // H
                if cell in seen:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0) or not np.isfinite(drift[coin]):
                    continue
                seen.add(cell)
                moves.append(c[t + H] / c[t] - 1.0 - drift[coin])
                fcs.append(fc[t])

    moves = np.array(moves, dtype=float)
    fcs = np.array(fcs, dtype=float)
    n = len(moves)

    mean = float(np.mean(moves)) if n > 0 else None
    tval = None
    if n >= 2:
        sd = float(np.std(moves, ddof=1))
        tval = float(mean / (sd / np.sqrt(n))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    if n >= 2:
        med = float(np.median(fcs))
        hi = moves[fcs > med]
        lo = moves[fcs <= med]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(np.mean(hi) - np.mean(lo))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {
        "name": "mean unusual 26-bar move after the cross (return minus coin's normal drift)",
        "value": mean,
        "statistic": {"name": "ordinary t of the mean", "value": tval} if tval is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2",
    }
    support = {"name": "larger-forecast half minus smaller-forecast half, mean unusual move",
               "value": sup_val, "passed": sup_pass}
    counts = {"independent cases": int(n)}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} independent cases, fewer than the plan's minimum of 20 over all coins and windows."
    elif tval is not None and mean > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move positive with t >= 2 and the larger-fall half beats the smaller-fall half."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif tval is not None and mean < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 (or undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
