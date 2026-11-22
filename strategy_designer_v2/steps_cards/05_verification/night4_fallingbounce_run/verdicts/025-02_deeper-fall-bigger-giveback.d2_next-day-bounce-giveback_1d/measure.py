import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LH = "debug_info.components.bounce.last_history_value"
    BAND = 2.0
    MIN_CASES = 30

    # ---------- per-coin mean daily return over all windows ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    case_vals = []
    case_abs_f = []

    for coin, wins in bars.items():
        mu = coin_mu[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            regime = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * n)
            if LH in df.columns:
                lh = pd.to_numeric(df[LH], errors="coerce").to_numpy(dtype=float)
            else:
                lh = np.full(n, np.nan)

            # 90-day return from prices inside the window where possible, else the detector's regime label
            r90 = np.full(n, np.nan)
            if n > 90:
                r90[90:] = close[90:] / close[:-90] - 1.0
            fall90 = np.where(np.isfinite(r90), r90 < 0.0, regime == "mean_reversion")

            # scaled one-day rise: raw component value > 0 (graded threshold => any positive rise)
            rise = np.isfinite(lh) & (lh > 0.0)
            situation = fall90 & rise

            active = f != 0.0
            n_active += int(active.sum())
            n_agree += int((active & situation & (f < 0.0)).sum())

            # ---------- cases: short bets (forecast deepens by >= band from its reference level) ----------
            ref = 0.0
            for t in range(n):
                if f[t] >= 0.0:
                    ref = 0.0
                    continue
                m = -f[t]
                if m - ref >= BAND:
                    ref = m
                    if t + 1 < n and np.isfinite(close[t]) and np.isfinite(close[t + 1]) and np.isfinite(mu):
                        r = close[t + 1] / close[t] - 1.0
                        case_vals.append(-(r - mu))
                        case_abs_f.append(abs(f[t]))
                else:
                    ref = min(ref, m)

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed_sit = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean excess next-day fall over short bets (sign flipped, minus coin mean daily return)"
    threshold = "confirm t >= 2, reject t <= -2, over at least 30 cases"
    reading = ("A case is a bet as in the workflow's holding-period rule (the short forecast deepening by >= 2 points from "
               "its lowest short level since its last bet, reset to 0 after a flat or side change), the situation is "
               "a 90-day return below 0 (recomputed from closes inside the window where 90 prior bars exist, else the "
               "recorded regime) with a positive raw scaled one-day return, and the top half is the n//2 cases with the "
               "largest |forecast| (ties by time order), the rest the bottom half.")

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": int(len(case_vals)), "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are short bars in a 90-day fall after "
                           "a positive scaled one-day rise, as the Fidelity requires."),
            "reading": reading,
        }

    vals = np.array(case_vals, dtype=float)
    absf = np.array(case_abs_f, dtype=float)
    n_cases = int(len(vals))

    mean_v = float(np.mean(vals)) if n_cases > 0 else None
    t_main = None
    if n_cases > 1:
        sd = float(np.std(vals, ddof=1))
        t_main = float(mean_v / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    # supporting check: top half vs bottom half by |forecast|
    sup_t = None
    sup_pass = None
    n_top = n_bot = 0
    if n_cases >= 4:
        order = np.argsort(-absf, kind="stable")
        k = n_cases // 2
        top = vals[order[:k]]
        bot = vals[order[k:]]
        n_top, n_bot = int(len(top)), int(len(bot))
        if n_top > 1 and n_bot > 1:
            res = stats.ttest_ind(top, bot, equal_var=False)
            sup_t = float(res.statistic) if np.isfinite(res.statistic) else 0.0
            sup_pass = bool(sup_t > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases over all coins and windows, fewer than the plan's minimum of 30."
    elif t_main is not None and t_main >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "Main t >= 2 over at least 30 cases and the top-half cases show a larger mean excess fall (Welch t > 0)."
    elif t_main is not None and t_main <= -2:
        status = "rejected"
        decided = "Main t <= -2 over at least 30 cases: the coin rose more than its usual drift after the bounces."
    elif t_main is not None and t_main >= 2:
        status = "inconclusive"
        decided = "Main t >= 2 but the size check fails (top-half minus bottom-half Welch t not > 0)."
    else:
        status = "inconclusive"
        decided = "Main t is between -2 and 2 over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_v,
            "statistic": {"name": "t of the mean", "value": t_main} if t_main is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "top-half minus bottom-half |forecast| mean excess fall, Welch t > 0",
            "value": sup_t,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases, "top-half cases": n_top, "bottom-half cases": n_bot},
        "decided_by": decided,
        "reading": reading,
    }
