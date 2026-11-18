import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    FC = "forecast"
    WICK_REC = "debug_info.components.wick_len.last_history_value"

    # ---------- 1. Situation check: recompute the flush condition from prices ----------
    n_active = 0
    n_agree = 0
    n_uncomputable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            o = d["open"].astype(float)
            h = d["high"].astype(float)
            l = d["low"].astype(float)
            c = d["close"].astype(float)
            v = d["volume"].astype(float)
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)

            ret1 = c / c.shift(1) - 1.0
            # usual move: 20-bar std of daily returns, with or without the current bar
            vol_incl = ret1.rolling(20, min_periods=20).std()
            vol_excl = ret1.shift(1).rolling(20, min_periods=20).std()
            fall_incl = ret1 / vol_incl.replace(0, np.nan)
            fall_excl = ret1 / vol_excl.replace(0, np.nan)
            fall_ok = (fall_incl <= -1.0) | (fall_excl <= -1.0)
            fall_known = fall_incl.notna() | fall_excl.notna()

            vmean = v.shift(1).rolling(30, min_periods=30).mean()
            vr = v / vmean.replace(0, np.nan)
            vr_ok = vr >= 2.0
            vr_known = vr.notna()

            rng = (h - l).replace(0, np.nan)
            wick_px = (np.minimum(o, c) - l) / rng
            if WICK_REC in d.columns:
                wick_rec = pd.to_numeric(d[WICK_REC], errors="coerce")
                wick = wick_rec.where(wick_rec.notna(), wick_px)
            else:
                wick = wick_px
            wick_ok = wick >= 0.333 - 1e-9
            wick_known = wick.notna()

            known = fall_known & vr_known & wick_known
            situation = fall_ok & vr_ok & wick_ok

            active = fc != 0
            for i in np.where(active.values)[0]:
                if not bool(known.iloc[i]):
                    n_uncomputable += 1
                    continue
                n_active += 1
                if bool(situation.iloc[i]) and fc.iloc[i] > 0:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90
    if n_active == 0:
        # nothing active to contradict the plan; treat as passed (the counts will decide observability)
        passed = True

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement) if agreement is not None else None,
                                "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active),
                       "active bars without enough history": int(n_uncomputable)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long flush bars "
                           "(1-day fall <= -1 usual move, volume >= 2x prior 30-day mean, lower wick >= 1/3 of range)."),
            "reading": ("The usual move is the 20-bar std of daily returns, with or without the current bar; "
                        "active bars without enough in-window history to recompute the condition are left out of the share."),
        }

    # ---------- 2. Criterion ----------
    excess = []
    fcs = []
    for coin, wins in bars.items():
        # coin's mean 3-bar return over all windows on the non-overlapping grid
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float).values
            fwd = np.full(len(c), np.nan)
            if len(c) > H:
                fwd[:-H] = c[H:] / c[:-H] - 1.0
            for p in range(0, len(c), H):
                if np.isfinite(fwd[p]):
                    grid_rets.append(fwd[p])
            fc = pd.to_numeric(d[FC], errors="coerce").values
            prepared.append((fc, fwd))
        if len(grid_rets) == 0:
            continue
        base = float(np.mean(grid_rets))

        for fc, fwd in prepared:
            flush_idx = [i for i in range(len(fc)) if np.isfinite(fc[i]) and fc[i] > 0]
            kept = []
            prev = None
            for i in flush_idx:
                if prev is not None and i - prev <= H:
                    prev = i  # within 3 bars of an earlier flush bar: dropped
                    continue
                kept.append(i)
                prev = i
            for i in kept:
                if np.isfinite(fwd[i]):
                    excess.append(fwd[i] - base)
                    fcs.append(float(fc[i]))

    n = len(excess)
    excess = np.array(excess, dtype=float)
    fcs = np.array(fcs, dtype=float)

    mean_ex = float(np.mean(excess)) if n > 0 else None
    t = None
    if n >= 2:
        sd = float(np.std(excess, ddof=1))
        if sd > 0:
            t = mean_ex / (sd / np.sqrt(n))
    rho = None
    if n >= 3 and np.std(fcs) > 0 and np.std(excess) > 0:
        r = stats.spearmanr(fcs, excess).correlation
        rho = float(r) if np.isfinite(r) else None
    check_passed = (rho is not None and rho > 0) if n >= 3 else None

    if n < 30:
        status = "not observable"
        decided = f"Fewer than 30 flush cases pooled across coins and windows ({n})."
    elif t is not None and t >= 2 and mean_ex > 0 and check_passed:
        status = "confirmed"
        decided = "Mean 3-bar excess return positive with t >= 2 over at least 30 flush cases, and Spearman correlation above 0."
    elif t is not None and t <= -2:
        status = "rejected"
        decided = "Mean 3-bar excess return has t <= -2 over at least 30 flush cases."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "Confirming t >= 2 but the Spearman correlation is at or below 0 (supporting check failed)."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 over at least 30 flush cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement) if agreement is not None else None,
                            "passed": bool(passed)},
        "main_measure": {
            "name": "mean 3-bar excess return after flush bars (vs coin's grid mean)",
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": float(t)} if t is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 over >= 30 cases; reject: t <= -2 over >= 30 cases",
        },
        "supporting_check": {
            "name": "Spearman(forecast, 3-bar excess return) > 0",
            "value": rho,
            "passed": check_passed,
        },
        "counts": {"flush cases": int(n)},
        "decided_by": decided,
        "reading": ("A flush bar is dropped when it lies 1 to 3 bars after any earlier flush bar in the same window "
                    "(the dedup is applied before dropping cases without a close 3 bars ahead in the window), and the "
                    "coin's mean is over grid positions 0, 3, 6, ... of each window pooled across all its windows."),
    }
