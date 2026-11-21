import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    PERIOD = 12
    BAND = 2.0
    FC = "forecast"
    QPOST = "debug_info.components.quiet.post_pipeline_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            high = df["high"].astype(float)
            prior_high = high.shift(1).rolling(PERIOD, min_periods=PERIOD).max()
            fc = df[FC].astype(float)
            computable = prior_high.notna() & fc.notna()
            active = (fc != 0) & computable
            situation = close > prior_high
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("The breakout is rebuilt from prices as close[t] > max(high[t-12..t-1]) inside each window, "
               "and the first 12 bars of a window, where it cannot be computed, are left out of the agreement; "
               "a case is a holding-period bet (a rise of a positive forecast of at least 2 points from its lowest "
               "level since the last bet, from 0 after a flat) on a trending bar, the first such bet in each 18-bar "
               "grid cell counted from the window's first row, with no case where the 18-bar return leaves the window; "
               "the normal drift is the coin's mean 18-bar return on the grid of all its windows; the halves are the "
               "cases strictly above and strictly below the median of quiet's post_pipeline_value (ties at the median "
               "left out); the plan's 'fewer than 30 cases / 15 per half' is reported as not observable.")

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bets on bars that close "
                           "above the prior 12-bar highest high, as the plan's Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_rows = []  # (coin, ret, quiet)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            for p in range(0, n - H, H):
                if close[p] > 0 and np.isfinite(close[p]) and np.isfinite(close[p + H]):
                    grid_rets.append(close[p + H] / close[p] - 1.0)
        drift[coin] = float(np.mean(grid_rets)) if len(grid_rets) > 0 else np.nan

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df[FC].astype(float).fillna(0.0).values
            regime = df["regime"].astype(str).values
            q = df[QPOST].astype(float).values if QPOST in df.columns else np.full(len(df), np.nan)
            n = len(df)
            ref = 0.0
            prev = 0.0
            taken_cells = set()
            for t in range(n):
                f = fc[t]
                is_bet = False
                if f > 0:
                    if prev <= 0:
                        ref = 0.0
                    if f - ref >= BAND:
                        is_bet = True
                        ref = f
                    else:
                        ref = min(ref, f)
                else:
                    ref = 0.0
                prev = f
                if not is_bet or regime[t] != "trending":
                    continue
                cell = t // H
                if cell in taken_cells:
                    continue
                taken_cells.add(cell)
                if t + H >= n:
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    continue
                ret = close[t + H] / close[t] - 1.0
                case_rows.append((coin, ret, q[t]))

    cases = pd.DataFrame(case_rows, columns=["coin", "ret", "quiet"])
    if len(cases) > 0:
        cases["unusual"] = cases["ret"] - cases["coin"].map(drift)
        cases = cases[np.isfinite(cases["unusual"])]
    else:
        cases["unusual"] = []

    n_cases = int(len(cases))
    mean_u = float(cases["unusual"].mean()) if n_cases > 0 else None
    t_main = None
    if n_cases > 1:
        sd = float(cases["unusual"].std(ddof=1))
        t_main = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    qc = cases[np.isfinite(cases["quiet"])] if n_cases > 0 else cases
    n_high = n_low = 0
    diff = None
    welch = None
    if len(qc) > 0:
        med = float(qc["quiet"].median())
        hi = qc.loc[qc["quiet"] > med, "unusual"]
        lo = qc.loc[qc["quiet"] < med, "unusual"]
        n_high, n_low = int(len(hi)), int(len(lo))
        if n_high > 0 and n_low > 0:
            diff = float(hi.mean() - lo.mean())
        if n_high > 1 and n_low > 1:
            tt = stats.ttest_ind(hi.values, lo.values, equal_var=False)
            welch = float(tt.statistic) if np.isfinite(tt.statistic) else None

    counts = {"cases": n_cases, "high-half cases": n_high, "low-half cases": n_low}

    if n_cases < 30 or n_high < 15 or n_low < 15:
        status = "not observable"
        sup_passed = None
        decided = ("A minimum count is not reached: fewer than 30 cases in total or fewer than 15 in either half "
                   f"({n_cases} cases, {n_high} high, {n_low} low).")
    else:
        sup_passed = bool(diff is not None and diff > 0)
        if (t_main is not None and t_main <= -2) or (welch is not None and welch <= -2):
            status = "rejected"
            decided = "Reject rule met: the main t is <= -2 or the supporting difference's Welch t is <= -2."
        elif mean_u is not None and mean_u > 0 and t_main is not None and t_main >= 2 and sup_passed:
            status = "confirmed"
            decided = ("Confirm rule met: the mean unusual move is positive with t >= 2 and the high-half minus "
                       "low-half difference is greater than 0.")
        else:
            status = "inconclusive"
            decided = ("Neither rule met: the main t is between -2 and 2, or it is positive with a supporting "
                       "difference <= 0 whose Welch t is above -2.")

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None),
                            "passed": bool(passed or n_active == 0)},
        "main_measure": {
            "name": "mean 18-bar unusual move of breakout bets",
            "value": mean_u,
            "statistic": ({"name": "t of the mean", "value": t_main} if t_main is not None else None),
            "threshold": "confirm: mean > 0 with t >= 2 (and supporting difference > 0); reject: t <= -2",
        },
        "supporting_check": {
            "name": "high-half minus low-half quiet mean unusual move",
            "value": diff,
            "passed": sup_passed,
            "welch_t": welch,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
