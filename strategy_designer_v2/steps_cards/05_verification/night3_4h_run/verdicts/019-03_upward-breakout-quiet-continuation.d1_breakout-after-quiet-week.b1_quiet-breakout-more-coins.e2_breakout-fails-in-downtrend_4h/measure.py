import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    BAND = 2.0
    BRK_PERIOD = 12
    RET_COL = "debug_info.components.fall_depth.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            high = d["high"].astype(float)
            fc = d["forecast"].astype(float).fillna(0.0)
            prior_high = high.shift(1).rolling(BRK_PERIOD, min_periods=BRK_PERIOD).max()
            brk = close - prior_high
            if RET_COL in d.columns:
                ret = pd.to_numeric(d[RET_COL], errors="coerce")
            else:
                ret = pd.Series(np.nan, index=d.index)
            ret_px = close / close.shift(180) - 1.0
            ret = ret.where(ret.notna(), ret_px)
            active = fc != 0
            computable = brk.notna() & ret.notna()
            situ = (brk > 0) & (ret < 0)
            ok = active & computable
            n_active += int(ok.sum())
            n_active_uncomputable += int((active & ~computable).sum())
            n_agree += int((ok & situ & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active},
            "decided_by": ("Fewer than 90% of the active bars are 4h closes above the prior 12-bar high "
                           "with a negative 180-bar return and a short forecast, so the config does not do what the Fidelity states."
                           if agreement is not None else
                           "No active bar on which the plan's situation could be checked."),
            "reading": ("Breakout recomputed as close above the maximum high of the 12 preceding bars of the same window; "
                        "the 180-bar return taken from fall_depth's raw value (same component as ret30), else from prices; "
                        "active bars where either could not be computed are left out."),
        }

    # ---------- 2. criterion ----------
    unusual = []
    absfc = []
    for coin, wins in bars.items():
        # coin's normal 72-bar drift over all its windows (non-overlapping grid)
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).to_numpy()
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = d["close"].astype(float).to_numpy()
            fc = d["forecast"].astype(float).fillna(0.0).to_numpy()
            n = len(d)
            ref = 0.0
            used_cells = set()
            for t in range(n):
                s = -fc[t] if fc[t] < 0 else 0.0
                if s <= 0:
                    ref = 0.0
                    continue
                if s - ref >= BAND:
                    ref = s
                    cell = t // H
                    if cell in used_cells:
                        continue
                    used_cells.add(cell)
                    if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] != 0:
                        r = c[t + H] / c[t] - 1.0
                        unusual.append(-(r - drift))
                        absfc.append(abs(fc[t]))
                else:
                    ref = min(ref, s)

    u = np.array(unusual, dtype=float)
    a = np.array(absfc, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    if n_cases >= 2:
        sd = float(np.std(u, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None
    else:
        t_u = None
    if n_cases >= 3 and np.std(a) > 0 and np.std(u) > 0:
        corr = float(stats.pearsonr(a, u)[0])
    else:
        corr = None
    corr_pass = None if corr is None else bool(corr > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases across all coins and windows, fewer than the plan's minimum of 30."
    elif t_u is not None and mean_u > 0 and t_u >= 2:
        if corr_pass:
            status = "confirmed"
            decided = "Mean short-direction unusual move above 0 with t >= 2 and a positive correlation between |forecast| and the move."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the correlation between |forecast| and the short-direction unusual move is 0 or less."
    elif t_u is not None and mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided = "Mean short-direction unusual move below 0 with t <= -2: the coin rises more than usual after these breakouts."
    else:
        status = "inconclusive"
        decided = "The t of the mean short-direction unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean short-direction unusual 72-bar move per case",
            "value": mean_u,
            "statistic": {"name": "t of the mean", "value": t_u} if t_u is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 (and correlation > 0); reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "Pearson correlation of |forecast| at signal bar with short-direction unusual move",
            "value": corr,
            "passed": corr_pass,
        },
        "counts": {"cases across all coins and windows": n_cases},
        "decided_by": decided,
        "reading": ("A case is the first short-side bet (forecast magnitude rising >= 2 points from its lowest level since the last bet, "
                    "reset to 0 when flat) in each 72-bar grid cell counted from the window's first row, kept only if 72 bars remain "
                    "in the window; the drift is the mean non-overlapping 72-bar return over all the coin's windows; the correlation "
                    "is Pearson; breakout for the situation check is close above the max high of the 12 preceding bars."),
    }
