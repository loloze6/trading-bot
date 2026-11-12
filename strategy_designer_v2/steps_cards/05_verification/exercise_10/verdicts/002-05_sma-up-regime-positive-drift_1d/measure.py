import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    SPREAD_COL = "debug_info.components.sma_cross_spread.last_history_value"
    MIN_IN, MIN_OUT, MIN_STRETCHES = 100, 100, 3

    # ---------- 1. Situation check ----------
    # Situation (Fidelity): the stretch from an upward SMA cross to the next downward cross,
    # i.e. 50-day SMA above 200-day SMA (raw spread > 0). Expected side: long (price rises).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            if SPREAD_COL in df.columns:
                s = pd.to_numeric(df[SPREAD_COL], errors="coerce")
            else:
                s = pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            agree = active & (s > 0) & (f > 0)
            n_agree += int(agree.sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.90
    else:
        agreement = None
        passed = True  # no active bars: nothing contradicts the plan; minimum counts decide

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of active bars have the 50-day SMA above the "
                           f"200-day SMA with a positive (long) forecast, below the 90% needed: "
                           f"the config's forecast is not the plan's long-only cross-to-cross stretch."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    in_rets, out_rets = [], []
    n_stretches = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            f = pd.to_numeric(df["forecast"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0  # next-bar return inside this window only
            ok = nxt.notna() & f.notna() & np.isfinite(nxt)
            in_mask = ok & (f > 0)
            out_mask = ok & (f == 0)
            in_rets.extend(nxt[in_mask].tolist())
            out_rets.extend(nxt[out_mask].tolist())

            # distinct up-cross stretches: contiguous runs of raw spread > 0 in this window
            if SPREAD_COL in df.columns:
                s = pd.to_numeric(df[SPREAD_COL], errors="coerce")
                pos = (s > 0).fillna(False).astype(int).values
                starts = np.sum((pos[1:] == 1) & (pos[:-1] == 0)) + (1 if len(pos) and pos[0] == 1 else 0)
                n_stretches += int(starts)

    in_rets = np.asarray(in_rets, dtype=float)
    out_rets = np.asarray(out_rets, dtype=float)
    n_in, n_out = len(in_rets), len(out_rets)

    counts = {
        "in-stretch bars": int(n_in),
        "out-of-stretch bars": int(n_out),
        "distinct up-cross stretches": int(n_stretches),
    }

    diff = None
    t = None
    if n_in >= 2 and n_out >= 2:
        diff = float(in_rets.mean() - out_rets.mean())
        tt = stats.ttest_ind(in_rets, out_rets, equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None
    elif n_in >= 1 and n_out >= 1:
        diff = float(in_rets.mean() - out_rets.mean())

    sup_val = None
    sup_pass = None
    if n_in >= 1 and n_out >= 1:
        sup_val = float((in_rets > 0).mean() - (out_rets > 0).mean())
        sup_pass = bool(sup_val > 0)

    main = {
        "name": "mean next-bar return in-stretch minus out-of-stretch",
        "value": diff,
        "statistic": {"name": "Welch t", "value": t} if t is not None else None,
        "threshold": "confirm if difference > 0 with t >= 2; reject if difference < 0 with t <= -2; |t| < 2 inconclusive",
    }
    supporting = {
        "name": "share of up next-bars in-stretch minus out-of-stretch",
        "value": sup_val,
        "passed": sup_pass,
    }

    reading = ("In-stretch bars are forecast > 0 and out-of-stretch bars forecast = 0, next-bar returns "
               "pooled over all windows; distinct up-cross stretches are counted as contiguous runs of "
               "raw SMA spread > 0 within each window (a run already open at a window's start counts); "
               "the plan's minimum counts, when unmet, give 'not observable'; the supporting check passes "
               "when the up-share difference is positive.")

    short = []
    if n_in < MIN_IN:
        short.append(f"in-stretch bars {n_in} < {MIN_IN}")
    if n_out < MIN_OUT:
        short.append(f"out-of-stretch bars {n_out} < {MIN_OUT}")
    if n_stretches < MIN_STRETCHES:
        short.append(f"distinct up-cross stretches {n_stretches} < {MIN_STRETCHES}")

    sc = {"agreement": (float(agreement) if agreement is not None else None), "passed": True}

    if short or t is None or diff is None:
        if not short:
            short.append("Welch t could not be computed")
        return {
            "status": "not observable",
            "situation_check": sc,
            "main_measure": main,
            "supporting_check": supporting,
            "counts": counts,
            "decided_by": "Minimum count not reached: " + "; ".join(short) + ".",
            "reading": reading,
        }

    if diff > 0 and t >= 2:
        status = "confirmed"
        decided = f"The in-stretch minus out-of-stretch mean next-bar return is positive with Welch t = {t:.2f} >= 2."
    elif diff < 0 and t <= -2:
        status = "rejected"
        decided = f"The difference is negative with Welch t = {t:.2f} <= -2: moves after up crosses reverse."
    else:
        status = "inconclusive"
        decided = f"Welch t = {t:.2f} meets neither the confirm (t >= 2) nor the reject (t <= -2) rule."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
