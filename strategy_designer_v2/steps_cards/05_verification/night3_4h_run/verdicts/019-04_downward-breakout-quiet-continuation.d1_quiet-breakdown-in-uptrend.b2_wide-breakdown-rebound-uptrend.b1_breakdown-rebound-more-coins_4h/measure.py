import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    BAND = 2.0

    def tstat(x):
        x = np.asarray(x, dtype=float)
        n = len(x)
        if n < 2:
            return None
        sd = x.std(ddof=1)
        if not np.isfinite(sd) or sd == 0:
            return None
        return float(x.mean() / (sd / np.sqrt(n)))

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            low = df["low"].astype(float)
            fc = df["forecast"].astype(float).fillna(0.0)
            prior_low = low.shift(1).rolling(12, min_periods=12).min()
            ret180 = close / close.shift(180) - 1.0
            computable = prior_low.notna() & ret180.notna()
            situ = (close < prior_low) & (ret180 > 0)
            active = fc != 0
            act_c = active & computable
            n_active += int(act_c.sum())
            n_active_uncomputable += int((active & ~computable).sum())
            n_agree += int((act_c & situ & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    reading = (
        "Situation recomputed per window as close below the min low of the 12 prior bars and close/close[t-180]-1 > 0, "
        "agreement taken over active bars where both can be computed inside the window (%d active bars without 180 bars "
        "of in-window history left out); cases are long bets (forecast rise >= 2 points from its low since the last bet), "
        "the first per 18-bar grid cell of each window, with an in-window 18-bar return; drift is the coin's mean "
        "non-overlapping 18-bar return over all its windows; the wider half is cases with entry forecast above the "
        "pooled median, the narrower half those at or below it; fewer than 100 cases gives 'not observable'."
        % n_active_uncomputable
    )

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active},
            "decided_by": "Fewer than 90% of active bars are long bars where the close is below the prior 12-bar low "
                          "and the 180-bar return is positive, so the config does not do what the plan's Fidelity says.",
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_rets, case_fc = [], []
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            n = len(df)
            # coin's normal drift grid
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    grid_rets.append(c1 / c0 - 1.0)
            # bets
            side = 0
            lowlvl = 0.0
            bet_bars = []
            for i in range(n):
                f = fc[i]
                s = int(np.sign(f))
                if s == 0:
                    side = 0
                    lowlvl = 0.0
                    continue
                if s != side:
                    side = s
                    lowlvl = 0.0
                a = abs(f)
                if a - lowlvl >= BAND:
                    if s > 0:
                        bet_bars.append(i)
                    lowlvl = a
                else:
                    lowlvl = min(lowlvl, a)
            seen = set()
            for i in bet_bars:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H < n:
                    c0, c1 = close[i], close[i + H]
                    if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                        coin_cases.append((c1 / c0 - 1.0, fc[i]))
        if not coin_cases or not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for r, f in coin_cases:
            case_rets.append(r - drift)
            case_fc.append(f)

    x = np.asarray(case_rets, dtype=float)
    fcs = np.asarray(case_fc, dtype=float)
    n_cases = int(len(x))
    mean_val = float(x.mean()) if n_cases > 0 else None
    t_val = tstat(x) if n_cases > 0 else None

    sup_val, sup_t, sup_pass = None, None, None
    n_wide = n_narrow = 0
    if n_cases >= 2:
        med = float(np.median(fcs))
        wide = x[fcs > med]
        narrow = x[fcs <= med]
        n_wide, n_narrow = int(len(wide)), int(len(narrow))
        if n_wide >= 2 and n_narrow >= 2:
            sup_val = float(wide.mean() - narrow.mean())
            tt = stats.ttest_ind(wide, narrow, equal_var=False)
            sup_t = float(tt.statistic) if np.isfinite(tt.statistic) else None
            sup_pass = bool(sup_t is not None and sup_t > 0 and sup_val > 0)
        else:
            sup_pass = False

    if n_cases < 100:
        status = "not observable"
        decided = "Fewer than the plan's 100 independent cases (%d), so the data could not show the idea." % n_cases
    elif t_val is not None and mean_val > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move positive with t >= 2 and wider-minus-narrower Welch t > 0: confirm rule met."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the wider-minus-narrower difference is not positive: inconclusive by the plan's rule."
    elif t_val is not None and mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2: reject rule met."
    else:
        status = "inconclusive"
        decided = "t of the mean unusual move lies between -2 and 2 (or is undefined): inconclusive by the plan's rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean 18-bar unusual move of long cases (return minus coin drift)",
            "value": mean_val,
            "statistic": {"name": "t of the mean", "value": t_val} if t_val is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 and supporting check passing; reject: mean < 0 with t <= -2; at least 100 cases",
        },
        "supporting_check": {
            "name": "wider-minus-narrower half mean unusual move (Welch t > 0)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {
            "independent cases": n_cases,
            "wider half cases": n_wide,
            "narrower half cases": n_narrow,
            "active bars checked": n_active,
        },
        "decided_by": decided,
        "reading": reading,
    }
