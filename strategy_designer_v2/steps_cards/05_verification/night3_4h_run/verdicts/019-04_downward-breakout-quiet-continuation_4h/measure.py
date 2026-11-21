import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    BAND = 2.0
    LOOK = 12

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            prior_low = low.shift(1).rolling(LOOK, min_periods=LOOK).min()
            situ_known = prior_low.notna() & close.notna()
            situ = situ_known & (close < prior_low)
            active = fc.notna() & (fc != 0) & situ_known
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    main_name = "mean drift-adjusted 18-bar short gain per case"
    main_thr = "positive with t >= 2 confirms (with supporting check); negative with t <= -2 rejects"
    reading_base = ("Situation computed per window as close below the minimum low of the 12 prior bars, "
                    "active bars whose 12-bar history is not inside the window are left out of the agreement; ")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "independent cases": 0},
            "decided_by": (f"Only {agreement:.1%} of the active bars are short bars with the close below the prior "
                           "12-bar lowest low, under the 90% needed: the config's forecast does not follow the plan's situation."),
            "reading": reading_base.rstrip("; ") + ".",
        }

    # ---------- 2. Criterion ----------
    vals, absf = [], []
    for coin, wins in bars.items():
        # coin's normal 18-bar drift: non-overlapping grid over all its windows
        drift_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for p in range(0, len(c) - H, H):
                a, b = c[p], c[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    drift_rets.append(b / a - 1.0)
        if len(drift_rets) == 0:
            continue
        drift = float(np.mean(drift_rets))

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            n = len(df)
            # short bets: rise of |forecast| on the short side >= band from its lowest level since last bet
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if f >= 0:
                    ref = 0.0
                    continue
                m = -f
                if m - ref >= BAND:
                    bet[i] = True
                    ref = m
                else:
                    ref = min(ref, m)
            seen = set()
            for i in np.where(bet)[0]:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                a, b = c[i], c[i + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0):
                    continue
                r = b / a - 1.0
                vals.append(-r - drift)
                absf.append(abs(fc[i]))

    vals = np.asarray(vals, dtype=float)
    absf = np.asarray(absf, dtype=float)
    ncase = int(len(vals))

    mean = float(np.mean(vals)) if ncase > 0 else None
    tstat = None
    if ncase > 1:
        sd = float(np.std(vals, ddof=1))
        tstat = float(mean / (sd / np.sqrt(ncase))) if sd > 0 else None

    sup_val, sup_pass = None, None
    n_hi = n_lo = 0
    if ncase > 0:
        med = float(np.median(absf))
        hi = vals[absf > med]
        lo = vals[absf <= med]
        n_hi, n_lo = int(len(hi)), int(len(lo))
        if n_hi > 0 and n_lo > 0:
            sup_val = float(np.mean(hi) - np.mean(lo))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    reading = (reading_base +
               "a case is the first short bet (a rise of the short forecast of at least 2 points) in each 18-bar grid cell "
               "of a window, dropped if its 18-bar return leaves the window; drift is the coin's mean non-overlapping "
               "18-bar return over all its windows; the median split puts cases above the median absolute forecast "
               "in the larger half and the rest in the smaller half.")

    if ncase < 30:
        status = "not observable"
        decided = f"Only {ncase} independent cases, fewer than the plan's minimum of 30."
    elif tstat is not None and mean > 0 and tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean drift-adjusted short gain is positive with t >= 2 and the larger-forecast half beats the smaller one."
    elif tstat is not None and mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "The mean drift-adjusted short gain is negative with t <= -2."
    elif tstat is not None and tstat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the mean drift-adjusted short gain lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": ({"name": "t of the mean", "value": tstat} if tstat is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": "larger-forecast half minus smaller-forecast half drift-adjusted short gain",
                             "value": sup_val, "passed": sup_pass},
        "counts": {"independent cases": ncase, "larger-forecast half": n_hi,
                   "smaller-forecast half": n_lo, "active bars": int(n_active)},
        "decided_by": decided,
        "reading": reading,
    }
