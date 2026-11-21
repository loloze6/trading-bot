import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 26
    TEN, KIJ, SEN, DISP, LB = 9, 26, 52, 26, 26
    SF = "debug_info.components.slow_fall.last_history_value"

    def ichimoku_situation(df):
        # Recompute the regime detector's components from the window's prices only
        # (warm-up bars are not recorded, so early bars may not be computable -> NaN).
        h, l, c = df["high"].astype(float), df["low"].astype(float), df["close"].astype(float)
        tenkan = (h.rolling(TEN, min_periods=TEN).max() + l.rolling(TEN, min_periods=TEN).min()) / 2
        kijun = (h.rolling(KIJ, min_periods=KIJ).max() + l.rolling(KIJ, min_periods=KIJ).min()) / 2
        span_a = ((tenkan + kijun) / 2).shift(DISP)
        span_b = ((h.rolling(SEN, min_periods=SEN).max() + l.rolling(SEN, min_periods=SEN).min()) / 2).shift(DISP)
        bottom = np.minimum(span_a, span_b)
        mid = (span_a + span_b) / 2
        slope = mid / mid.shift(LB) - 1
        computable = bottom.notna() & slope.notna()
        sit = (c < bottom) & (slope < 0)
        return sit, computable

    # ---------- 1. situation check ----------
    n_active, n_agree = 0, 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            sit, comp = ichimoku_situation(df)
            # where the cloud cannot be recomputed inside the window, use the detector's own decision
            regime_trending = df["regime"].astype(str) == "trending"
            situation = np.where(comp, sit, regime_trending)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean 26-bar unusual move (return minus drift, short direction), before costs"
    main_thr = "confirm: mean > 0 with t >= 2; reject: t <= -2"
    sup_name = "slow-fall half minus fast-fall half excess return (26-bar return minus drift)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the active bars are short bars where the close is below the cloud bottom and the cloud's 26-bar slope is below 0.",
            "reading": "The cloud is recomputed from each window's prices (9/26/52/26, slope of the cloud mid over 26 bars); bars where it cannot be computed inside the window use the recorded regime 'trending'.",
        }

    # ---------- 2. criterion ----------
    # normal drift per coin: mean of non-overlapping 26-bar returns over all its windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True).values
            for p in range(0, len(c) - H, H):
                if c[p] > 0 and np.isfinite(c[p]) and np.isfinite(c[p + H]):
                    rets.append(c[p + H] / c[p] - 1)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    unusual, excess, sfv = [], [], []
    for coin, wins in bars.items():
        if not np.isfinite(drift[coin]):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).values
            sf = pd.to_numeric(df[SF], errors="coerce").values if SF in df.columns else np.full(len(df), np.nan)
            for p in range(0, len(df) - H, H):
                if reg[p] != "trending" or not (fc[p] < 0):
                    continue
                if not (np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0):
                    continue
                r = c[p + H] / c[p] - 1
                ex = r - drift[coin]
                unusual.append(-ex)
                excess.append(ex)
                sfv.append(sf[p])

    unusual = np.array(unusual, dtype=float)
    excess = np.array(excess, dtype=float)
    sfv = np.array(sfv, dtype=float)
    n = int(len(unusual))

    mean_u = float(np.mean(unusual)) if n > 0 else None
    t_u = None
    if n >= 2:
        sd = float(np.std(unusual, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n))) if sd > 0 else None

    ok = np.isfinite(sfv)
    diff, welch, n_slow, n_fast = None, None, 0, 0
    if ok.sum() >= 2:
        med = float(np.median(sfv[ok]))
        slow = excess[ok & (sfv > med)]
        fast = excess[ok & (sfv <= med)]
        n_slow, n_fast = int(len(slow)), int(len(fast))
        if n_slow >= 1 and n_fast >= 1:
            diff = float(np.mean(slow) - np.mean(fast))
        if n_slow >= 2 and n_fast >= 2:
            tt = stats.ttest_ind(slow, fast, equal_var=False)
            welch = float(tt.statistic) if np.isfinite(tt.statistic) else None
    sup_passed = None if diff is None else bool(diff < 0)

    counts = {"cases over all coins and windows": n, "slow-fall half": n_slow, "fast-fall half": n_fast}
    reading = ("Cases are grid bars (positions 0, 26, 52, ... of each window with a close 26 bars later in the same window) "
               "with regime 'trending' and forecast < 0, drift is each coin's mean non-overlapping 26-bar return over all its windows, "
               "the slow-fall half is slow_fall raw value strictly above the cases' median (ties go to the fast half), and the "
               "plan's 'fewer than 30 cases' is applied as the minimum count.")

    if n < 30:
        status = "not observable"
        decided = f"Only {n} cases over all coins and windows, fewer than the plan's minimum of 30."
    elif (t_u is not None and t_u <= -2) or (diff is not None and diff > 0 and welch is not None and welch >= 2):
        status = "rejected"
        if t_u is not None and t_u <= -2:
            decided = "Reject: the main mean unusual move has t <= -2 (the cases rise more than the drift)."
        else:
            decided = "Reject: the slow-minus-fast excess-return difference is positive with Welch t >= 2."
    elif mean_u is not None and mean_u > 0 and t_u is not None and t_u >= 2 and sup_passed is True:
        status = "confirmed"
        decided = "Confirm: the main mean unusual move is positive with t >= 2 and the slow-minus-fast difference is below 0."
    else:
        status = "inconclusive"
        if mean_u is not None and mean_u > 0 and t_u is not None and t_u >= 2:
            decided = "Inconclusive: the main t confirms but the slow-minus-fast difference is not below 0 (Welch t below 2)."
        else:
            decided = "Inconclusive: the main t lies between -2 and 2 and no reject rule is met."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": None if t_u is None else {"name": "t of the mean", "value": t_u},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_passed,
                             "welch_t": welch},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
