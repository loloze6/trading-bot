import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    BAND = 2.0
    RAW = "debug_info.components.nr_break_down.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            low = df["low"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce")

            # 180-bar return from prices, within the window only
            ret180 = close / close.shift(180) - 1.0

            # break below the prior 12-bar low: component raw value first, else prices
            prior_low = low.shift(1).rolling(12, min_periods=12).min()
            price_break = pd.Series(np.where(prior_low.notna(), (close < prior_low).astype(float), np.nan))
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                comp_break = pd.Series(np.where(raw.notna(), (raw > 0).astype(float), np.nan))
            else:
                comp_break = pd.Series(np.nan, index=df.index)
            brk = comp_break.where(comp_break.notna(), price_break)

            active = fc.notna() & (fc != 0)
            checkable = active & ret180.notna() & brk.notna()
            situ = (ret180 < 0) & (brk == 1.0) & (fc < 0)
            n_active += int(checkable.sum())
            n_agree += int((checkable & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("Situation = close below the prior 12-bar low (component raw value > 0, else from prices) and "
               "180-bar close-to-close return < 0 recomputed within each window, short side; active bars where "
               "either cannot be computed (first 180 bars of a window) are left out of the agreement; a case is "
               "the first short bet (forecast falling >= 2 points below its least-negative level since the last "
               "bet, reset to 0 after flat or side change) in each 18-bar grid cell from each window's first row; "
               "the larger half is |forecast| strictly above the median, the smaller half at or below it.")

    main_name = "mean unusual 18-bar move of short bets, short direction"
    main_thr = "mean > 0 with t >= 2 over at least 30 cases (reject: mean < 0 with t <= -2)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": ("Fewer than 90% of active bars are short bars with a close below the prior 12-bar low "
                           "in a negative 180-bar return regime, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    unusual = []
    absf = []
    for coin, wins in bars.items():
        # coin's normal drift: mean 18-bar return over grid samples of all windows
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
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(df)
            ref = 0.0
            prev = 0.0
            used_cells = set()
            for t in range(n):
                ft = f[t]
                if not np.isfinite(ft):
                    ft = 0.0
                bet = False
                if ft < 0:
                    depth = -ft
                    if prev >= 0:
                        ref = 0.0
                    if depth - ref >= BAND:
                        bet = True
                        ref = depth
                    else:
                        ref = min(ref, depth)
                else:
                    ref = 0.0
                prev = ft
                if bet:
                    cell = t // H
                    if cell in used_cells:
                        continue
                    used_cells.add(cell)
                    if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] != 0:
                        r = c[t + H] / c[t] - 1.0
                        unusual.append(-(r - drift))
                        absf.append(abs(ft))

    unusual = np.array(unusual, dtype=float)
    absf = np.array(absf, dtype=float)
    n_cases = int(len(unusual))

    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    t_u = None
    if n_cases > 1:
        sd = float(np.std(unusual, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    n_large = n_small = 0
    if n_cases > 0:
        med = float(np.median(absf))
        large = unusual[absf > med]
        small = unusual[absf <= med]
        n_large, n_small = int(len(large)), int(len(small))
        if n_large > 0 and n_small > 0:
            sup_val = float(np.mean(large) - np.mean(small))
            sup_pass = bool(sup_val > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases, below the plan's minimum of 30."
    elif t_u is not None and mean_u > 0 and t_u >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move positive with t >= 2 over at least 30 cases, and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting check (larger |forecast| half minus smaller half > 0) fails."
    elif t_u is not None and mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2, over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_u is None else {"name": "t of the mean", "value": t_u},
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "mean unusual move, larger |forecast| half minus smaller half",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases, "larger half": n_large, "smaller half": n_small},
        "decided_by": decided,
        "reading": reading,
    }
