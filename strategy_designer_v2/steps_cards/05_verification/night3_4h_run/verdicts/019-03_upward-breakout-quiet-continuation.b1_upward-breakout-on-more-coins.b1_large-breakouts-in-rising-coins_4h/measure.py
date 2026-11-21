import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    BAND = 2.0
    RET_PERIOD = 180
    BRK_PERIOD = 12
    LHV = "debug_info.components.breakout.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            high = df["high"].astype(float)
            fc = df["forecast"].astype(float).fillna(0.0)

            # 180-bar return from prices (inside the window); fall back to the recorded regime where not computable
            ret180 = close / close.shift(RET_PERIOD) - 1.0
            regime_rec = df["regime"].astype(str).eq("trending")
            trend_ok = np.where(ret180.notna(), ret180 > 0, regime_rec)

            # breakout clearance: recorded raw value where present, else recomputed from prices
            prior_high = high.shift(1).rolling(BRK_PERIOD, min_periods=BRK_PERIOD).max()
            clr_price = close / prior_high - 1.0
            if LHV in df.columns:
                clr = df[LHV].astype(float).where(df[LHV].notna(), clr_price)
            else:
                clr = clr_price
            brk_ok = (clr > 0).fillna(False).values

            situation = np.asarray(trend_ok, dtype=bool) & brk_ok
            active = fc.values != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc.values > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "mean 18-bar excess return of bets over the coin's normal 18-bar drift"
    thr = "confirm: mean > 0 with t >= 2 and supporting check passing; reject: mean < 0 with t <= -2; fewer than 30 cases: not observable"
    reading = ("The 30-day return is recomputed from closes inside each window and, on bars too early in a window to compute it, "
               "the recorded regime stands in for it; a bet is a long-side forecast rise of at least 2 points from its lowest level "
               "since the last bet (from 0 after a flat); each 18-bar grid cell (positions 0,18,36,... of each window) keeps its first bet, "
               "dropped if its 18-bar return leaves the window; the drift is the coin's mean 18-bar return on the same grid over all its windows; "
               "the median split puts cases above the median forecast in the upper half and the rest in the lower half; "
               "the plan's fewer-than-30-cases rule is applied as the minimum count (not observable).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": 0, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the close clears the prior "
                           "12-bar high while the 180-bar return is positive, as the Fidelity's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_ret = []
    case_fc = []
    case_coin = []
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            close = df["close"].astype(float).reset_index(drop=True).values
            n = len(close)
            for p in range(0, n, H):
                if p + H < n and close[p] > 0 and np.isfinite(close[p]) and np.isfinite(close[p + H]):
                    grid_rets.append(close[p + H] / close[p] - 1.0)
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            n = len(fc)
            bet = np.zeros(n, dtype=bool)
            low = 0.0
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    bet[i] = True
                    low = f
                else:
                    low = min(low, f)
            for p in range(0, n, H):
                idx = np.where(bet[p:min(p + H, n)])[0]
                if len(idx) == 0:
                    continue
                t = p + int(idx[0])
                if t + H >= n:
                    continue
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0) or not np.isfinite(drift[coin]):
                    continue
                case_ret.append(c1 / c0 - 1.0 - drift[coin])
                case_fc.append(fc[t])
                case_coin.append(coin)

    ex = np.asarray(case_ret, dtype=float)
    fcs = np.asarray(case_fc, dtype=float)
    n_cases = int(len(ex))
    counts = {"cases": n_cases}

    mean_ex = float(ex.mean()) if n_cases > 0 else None
    tval = None
    if n_cases > 1:
        sd = ex.std(ddof=1)
        tval = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases > 0:
        med = float(np.median(fcs))
        up = ex[fcs > med]
        lo = ex[fcs <= med]
        counts["upper half cases"] = int(len(up))
        counts["lower half cases"] = int(len(lo))
        if len(up) > 0 and len(lo) > 0:
            sup_val = float(up.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {"name": main_name, "value": mean_ex,
            "statistic": {"name": "ordinary t of the mean", "value": tval} if tval is not None else None,
            "threshold": thr}
    supp = {"name": "mean excess of cases above median forecast minus at or below", "value": sup_val, "passed": sup_pass}

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases over all coins and windows, below the plan's minimum of 30."
    elif tval is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero dispersion), so neither confirm nor reject is met."
    elif mean_ex > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean excess return is positive with t >= 2 and the upper-minus-lower half difference is above 0."
    elif mean_ex < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean excess return is negative with t <= -2."
    elif tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check (upper minus lower half above 0) fails."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
