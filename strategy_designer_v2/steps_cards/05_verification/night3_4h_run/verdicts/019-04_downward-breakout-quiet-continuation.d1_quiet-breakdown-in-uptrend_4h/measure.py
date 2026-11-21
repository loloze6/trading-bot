import numpy as np
import pandas as pd


def measure(bars):
    H = 18
    BAND = 2.0
    BRK_N = 12
    RET_N = 180

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    fallback_active = 0
    fallback_agree = 0

    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            low = pd.to_numeric(d["low"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)

            prior_low = low.shift(1).rolling(BRK_N, min_periods=BRK_N).min()
            brk = close / prior_low - 1.0
            ret = close / close.shift(RET_N) - 1.0
            computable = brk.notna() & ret.notna()
            situ = (brk < 0) & (ret > 0)

            active = fc != 0
            short = fc < 0
            act_comp = active & computable
            n_active += int(act_comp.sum())
            n_agree += int((act_comp & situ & short).sum())
            n_active_uncomputable += int((active & ~computable).sum())

            if "regime" in d.columns:
                reg = d["regime"].astype(str) == "trending"
                fallback_active += int(active.sum())
                fallback_agree += int((active & reg & short).sum())

    used_fallback = False
    if n_active > 0:
        agreement = n_agree / n_active
    elif fallback_active > 0:
        used_fallback = True
        agreement = fallback_agree / fallback_active
    else:
        agreement = None

    reading_parts = [
        "the situation is recomputed per window from prices (close below the minimum low of the 12 prior bars "
        "and close over the close 180 bars earlier above 1), and active bars whose 180-bar history lies before "
        "the window's first recorded row are left out of the agreement"
        + (" (none were computable, so the recorded regime 'trending' was used)" if used_fallback else ""),
        "a short bet is a rise of the short forecast's size by at least 2 points from its lowest size since the "
        "last bet (from 0 after a flat or a long), the first such bet in each 18-bar grid cell of a window is the "
        "cell's case, and cases without 18 bars left in their window are left out",
        "the normal drift is the mean of each coin's 18-bar returns on the 0,18,36,... grid of all its windows",
        "the supporting split puts cases with absolute forecast strictly above the median in the larger group "
        "and the rest in the smaller group",
        "the plan's 30-case minimum, when not reached, gives 'not observable'",
    ]
    reading = "; ".join(reading_parts) + "."

    if agreement is None or agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {
                "name": "mean short-signed unusual 18-bar move",
                "value": None,
                "statistic": None,
                "threshold": "positive with t >= 2 to confirm; negative with t <= -2 to reject",
            },
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active if not used_fallback else fallback_active),
                       "active bars agreeing": int(n_agree if not used_fallback else fallback_agree)},
            "decided_by": ("no active bars to compare with the plan's situation" if agreement is None else
                           "fewer than 90% of the non-zero forecast bars are short bars where the close is below "
                           "the prior 12-bar low while the 180-bar return is positive, as the plan's Fidelity says"),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    unusual = []
    absfc = []

    for coin, wins in bars.items():
        # normal drift of this coin
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values.astype(float)
            n = len(d)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    grid_rets.append(c1 / c0 - 1.0)
            prepared.append((close, fc))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for close, fc in prepared:
            n = len(close)
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if f < 0:
                    m = -f
                    if m - ref >= BAND:
                        bet[i] = True
                        ref = m
                    else:
                        ref = min(ref, m)
                else:
                    ref = 0.0
            for start in range(0, n, H):
                end = min(start + H, n)
                idx = np.nonzero(bet[start:end])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0):
                    continue
                r = c1 / c0 - 1.0
                unusual.append(-(r - drift))
                absfc.append(abs(fc[t]))

    unusual = np.array(unusual, dtype=float)
    absfc = np.array(absfc, dtype=float)
    n_cases = int(len(unusual))

    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    if n_cases > 1:
        sd = float(np.std(unusual, ddof=1))
        t_stat = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None
    else:
        t_stat = None

    sup_val = None
    sup_pass = None
    n_large = n_small = 0
    if n_cases > 0:
        med = float(np.median(absfc))
        large = unusual[absfc > med]
        small = unusual[absfc <= med]
        n_large, n_small = int(len(large)), int(len(small))
        if n_large > 0 and n_small > 0:
            sup_val = float(np.mean(large) - np.mean(small))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {
        "name": "mean short-signed unusual 18-bar move",
        "value": mean_u,
        "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
        "threshold": "positive with t >= 2 to confirm; negative with t <= -2 to reject",
    }
    supporting = {
        "name": "mean unusual move, larger minus smaller absolute forecast (median split)",
        "value": sup_val,
        "passed": sup_pass,
    }
    counts = {"cases over all coins and windows": n_cases,
              "larger-forecast cases": n_large,
              "smaller-forecast cases": n_small}

    if n_cases < 30:
        status = "not observable"
        decided = f"only {n_cases} cases over all coins and windows, fewer than the plan's minimum of 30."
    elif t_stat is None:
        status = "inconclusive"
        decided = "the t of the mean could not be computed (zero dispersion), so neither rule is met."
    elif mean_u > 0 and t_stat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "the mean short-signed unusual move is positive with t >= 2 and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "the mean short-signed unusual move is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "the t of the mean lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
