import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    BRK = "debug_info.components.break_touches.last_history_value"
    RUN = "debug_info.components.run20.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            brk = pd.to_numeric(d[BRK], errors="coerce") if BRK in d.columns else pd.Series(np.nan, index=d.index)
            run_rec = pd.to_numeric(d[RUN], errors="coerce") if RUN in d.columns else pd.Series(np.nan, index=d.index)
            run_px = close / close.shift(20) - 1.0  # inside this window only
            run = run_rec.where(run_rec.notna(), run_px)
            situ = (brk > 0) & (run > 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ.fillna(False) & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long bars where the close holds "
                           "above a 90-day swing-high level (break measure > 0) after a positive 20-day return, "
                           "as the plan's Fidelity requires."),
            "reading": "Situation = raw break_touches > 0 and raw 20-bar return > 0 (recorded value, else from closes), long side.",
        }

    # ---------- 2. Criterion ----------
    unusual = []
    entry_fc = []
    for coin, wins in bars.items():
        # normal 5-day drift: non-overlapping grid returns over all windows of the coin
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            n = len(close)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            prepared.append((close, fc))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for close, fc in prepared:
            n = len(close)
            # bets: rise of the forecast on its side of at least the band, from its lowest level since the last bet
            prev_side = 0
            trough = 0.0
            seen_cells = set()
            for t in range(n):
                f = fc[t]
                side = int(np.sign(f))
                if side == 0:
                    prev_side = 0
                    trough = 0.0
                    continue
                if side != prev_side:
                    trough = 0.0
                    prev_side = side
                lvl = abs(f)
                is_bet = (lvl - trough) >= BAND
                if is_bet:
                    trough = lvl
                else:
                    trough = min(trough, lvl)
                if not is_bet:
                    continue
                cell = t // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                unusual.append(side * (r - drift))
                entry_fc.append(float(f))

    u = np.array(unusual, dtype=float)
    ef = np.array(entry_fc, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(u, ddof=1))
        if sd > 0:
            t_stat = float(mean_u / (sd / np.sqrt(n_cases)))

    sup_val = None
    sup_pass = None
    if n_cases > 0:
        med = float(np.median(ef))
        hi = u[ef > med]
        lo = u[ef < med]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(np.mean(hi) - np.mean(lo))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} independent cases, fewer than the plan's minimum of 30: the data cannot decide."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed (zero spread), so neither rule is met."
    elif t_stat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move has t >= 2 over at least 30 independent cases and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "Mean unusual move has t >= 2 but the supporting check fails: a confirming t whose check fails is inconclusive."
    elif t_stat <= -2:
        status = "rejected"
        decided = "Mean unusual move has t <= -2 over at least 30 independent cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean 5-bar unusual move per case (return minus coin's normal 5-day drift), before costs",
            "value": mean_u,
            "statistic": {"name": "t of the mean", "value": t_stat} if t_stat is not None else None,
            "threshold": "confirm t >= 2, reject t <= -2, over at least 30 independent cases",
        },
        "supporting_check": {
            "name": "mean unusual move of cases with entry forecast above the median minus below it (> 0)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"independent cases": n_cases},
        "decided_by": decided,
        "reading": ("Cases are forecast rises of at least 2 points on the long side, the first per 5-bar grid cell of each "
                    "window, dropped when the 5-bar return leaves the window; the drift is the mean non-overlapping 5-bar "
                    "return over all the coin's windows; cases exactly at the median forecast are in neither group, and an "
                    "empty group fails the supporting check."),
    }
