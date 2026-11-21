import numpy as np
import pandas as pd


def measure(bars):
    H = 18
    BAND = 2.0
    FALL_COL = "debug_info.components.week_fall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_unknown = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            high = df["high"].astype(float)
            fc = df["forecast"].astype(float)
            prior_high = high.shift(1).rolling(12, min_periods=12).max()
            brk = (close - prior_high) / prior_high * 100.0
            fall_px = close / close.shift(42) - 1.0
            if FALL_COL in df.columns:
                fall_rec = pd.to_numeric(df[FALL_COL], errors="coerce")
                fall = fall_rec.where(fall_rec.notna(), fall_px)
            else:
                fall = fall_px
            known = brk.notna() & fall.notna()
            situ = (brk > 0) & (fall < 0)
            active = fc.notna() & (fc != 0)
            n_active_unknown += int((active & ~known).sum())
            act_k = active & known
            n_active += int(act_k.sum())
            n_agree += int((act_k & situ & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean drift-adjusted 18-bar short return per case"
    threshold = "t >= 2 with at least 30 cases (and deeper half ahead) confirms; t <= -2 with at least 30 cases rejects"
    sit_reading = ("Situation computed from prices (close above max high of previous 12 bars in the window, "
                   "42-bar return < 0, using the recorded week_fall raw value where present); active bars whose "
                   "situation cannot be computed inside the window (%d) are left out of the agreement share" % n_active_unknown)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of active (non-zero forecast) bars are short bars where the close is above "
                           "the prior 12-bar high and the 42-bar return is negative, as the Fidelity's situation requires."),
            "reading": sit_reading + ".",
        }

    # ---------- 2. criterion ----------
    adj = []
    absf = []
    for coin, wins in bars.items():
        # coin's normal drift: mean 18-bar return on the non-overlapping grid of all its windows
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
            c = df["close"].astype(float).to_numpy()
            f = df["forecast"].astype(float).to_numpy()
            n = len(f)
            ref = 0.0
            short_side = False
            seen_cells = set()
            for t in range(n):
                ft = f[t]
                if not np.isfinite(ft) or ft >= 0:
                    short_side = False
                    ref = 0.0
                    continue
                if not short_side:
                    short_side = True
                    ref = 0.0
                if ft <= ref - BAND:
                    ref = ft
                    cell = t // H
                    if cell in seen_cells:
                        continue
                    seen_cells.add(cell)
                    if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] != 0:
                        r = c[t + H] / c[t] - 1.0
                        adj.append(-(r - drift))
                        absf.append(abs(ft))
                else:
                    ref = max(ref, ft)

    adj = np.array(adj, dtype=float)
    absf = np.array(absf, dtype=float)
    n_cases = int(len(adj))

    mean_val = float(np.mean(adj)) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        sd = float(np.std(adj, ddof=1))
        t_val = float(mean_val / (sd / np.sqrt(n_cases))) if sd > 0 else None

    supp_val = None
    supp_pass = None
    if n_cases > 1:
        med = float(np.median(absf))
        deep = adj[absf > med]
        shallow = adj[absf <= med]
        if len(deep) > 0 and len(shallow) > 0:
            supp_val = float(np.mean(deep) - np.mean(shallow))
            supp_pass = bool(supp_val > 0)

    if n_cases < 30:
        status = "not observable"
        decided = "Fewer than 30 cases (%d), the plan's minimum count, so the data could not show the idea." % n_cases
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero spread), so neither confirm nor reject applies."
    elif t_val >= 2 and supp_pass:
        status = "confirmed"
        decided = "Confirm: t >= 2 with at least 30 cases and the deeper-fall half ahead of the shallower half."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "Inconclusive: t >= 2 but the deeper-fall half is not ahead of the shallower half."
    elif t_val <= -2:
        status = "rejected"
        decided = "Reject: t <= -2 with at least 30 cases (the coin rises more than usual after these breakouts)."
    else:
        status = "inconclusive"
        decided = "Inconclusive: t between -2 and 2 with at least 30 cases."

    reading = (sit_reading + "; a case is the first short bet (forecast falling >= 2 points below its highest short "
               "level since the last bet, reset to 0 after flat or a side change) in each 18-bar grid cell counted "
               "from each window's first row, cases without 18 bars left in the window are dropped, and the median "
               "split puts |forecast| above the median in the deeper half and the rest in the shallower half.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": ({"name": "t of the mean", "value": t_val} if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "deeper-fall half minus shallower half, mean drift-adjusted short return",
            "value": supp_val,
            "passed": supp_pass,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
