import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    BAND = 2.0
    BRK = "debug_info.components.break.last_history_value"
    R30 = "debug_info.components.fall30.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float).fillna(0.0)
            # ret30: recorded raw value, else recomputed from prices inside the window
            ret30_px = close / close.shift(30) - 1.0
            if R30 in df.columns:
                ret30 = df[R30].astype(float).where(df[R30].notna(), ret30_px)
            else:
                ret30 = ret30_px
            brk = df[BRK].astype(float) if BRK in df.columns else pd.Series(np.nan, index=df.index)
            active = fc != 0
            situ = (brk > 0) & (ret30 < 0)
            agree = active & situ & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean short-direction unusual 20-bar move per case"
    thr = "confirm t >= 2 over >= 20 cases with rank correlation > 0; reject t <= -2 over >= 20 cases"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": 0, "active bars": n_active},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars where the "
                          "break reading is above 0 and the 30-day return is below 0, as the Fidelity requires.",
            "reading": "Situation = break last_history_value > 0 and 30-day return < 0 (recorded, else recomputed "
                       "from closes); expected side short.",
        }

    # ---------- 2. criterion ----------
    unusual = []
    absfc = []
    for coin, wins in bars.items():
        # normal 20-bar drift: non-overlapping grid returns over all windows of the coin
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).to_numpy()
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).to_numpy()
            fc = df["forecast"].astype(float).fillna(0.0).to_numpy()
            n = len(df)
            ref = 0.0
            seen_cells = set()
            for t in range(n):
                f = fc[t]
                if f >= 0:
                    ref = 0.0
                    continue
                m = -f
                is_bet = (m - ref) >= BAND
                if is_bet:
                    ref = m
                else:
                    ref = min(ref, m)
                if not is_bet:
                    continue
                cell = t // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H])) or c[t] == 0:
                    continue
                r = c[t + H] / c[t] - 1.0
                unusual.append(-(r - drift))
                absfc.append(abs(f))

    u = np.asarray(unusual, dtype=float)
    a = np.asarray(absfc, dtype=float)
    ncases = int(len(u))
    mean_u = float(np.mean(u)) if ncases > 0 else None
    tval = None
    if ncases >= 2:
        sd = float(np.std(u, ddof=1))
        tval = float(mean_u / (sd / np.sqrt(ncases))) if sd > 0 else 0.0
    rho = None
    if ncases >= 3 and np.std(a) > 0 and np.std(u) > 0:
        rho = float(stats.spearmanr(a, u).correlation)
    sup_pass = None if rho is None else bool(rho > 0)

    if ncases < 20:
        status = "not observable"
        decided = f"Only {ncases} cases, fewer than the plan's minimum of 20."
    elif tval is not None and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "t >= 2 over at least 20 cases and the rank correlation is above 0."
    elif tval is not None and tval <= -2:
        status = "rejected"
        decided = "t <= -2 over at least 20 cases: the price rises beyond its drift after such breaks."
    elif tval is not None and tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the rank correlation is 0 or below (or undefined), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if tval is None else {"name": "t of the mean", "value": tval},
            "threshold": thr,
        },
        "supporting_check": {
            "name": "Spearman rank correlation of |entry forecast| vs short-direction unusual move",
            "value": rho,
            "passed": sup_pass,
        },
        "counts": {"cases": ncases},
        "decided_by": decided,
        "reading": "A case is the first short bet (a rise of at least 2 forecast points in short size from its lowest "
                   "level since the last bet) in each 20-bar grid cell of a window, dropped when its 20-bar return "
                   "would leave the window, with drift the coin's mean non-overlapping 20-bar return over all its windows.",
    }
