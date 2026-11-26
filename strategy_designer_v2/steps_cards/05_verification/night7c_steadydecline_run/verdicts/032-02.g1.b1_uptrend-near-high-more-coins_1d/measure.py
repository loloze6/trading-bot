import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    LOOK = 28
    RAW = "debug_info.components.high_prox.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            regime = d["regime"].astype(str).to_numpy() if "regime" in d.columns else np.array([""] * len(d))
            raw = (pd.to_numeric(d[RAW], errors="coerce").to_numpy(dtype=float)
                   if RAW in d.columns else np.full(len(d), np.nan))
            n = len(d)
            ret28 = np.full(n, np.nan)
            if n > LOOK:
                ret28[LOOK:] = close[LOOK:] / close[:-LOOK] - 1.0
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                if np.isfinite(ret28[i]):
                    in_sit = ret28[i] > 0
                else:
                    # 28-day return not computable inside the window: use the detector's decision
                    in_sit = regime[i] == "trending"
                # proximity to the high must be a recorded, positive value inside the regime
                prox_ok = np.isfinite(raw[i]) and raw[i] > 0
                if in_sit and prox_ok and f > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Situation = 28-bar close-to-close return > 0 recomputed from closes inside the window "
               "(the detector's 'trending' regime on the first 28 bars where it cannot be recomputed), long side, "
               "with a positive recorded high proximity; cases = bars with regime 'trending' at grid positions "
               "0,5,10,... of each window with a 5-bar forward return inside the window; normal drift = mean of the "
               "coin's non-overlapping 5-bar returns over all its windows; thirds = pooled cases sorted by forecast "
               "(stable sort), bottom and top floor(n/3) cases; a third below 30 cases is 'not observable'.")

    main_name = "mean excess 5-day return, top third minus bottom third of forecast"
    threshold = "confirm: difference > 0 with Welch t >= 2 and top third mean excess > 0; reject: difference < 0 with Welch t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars inside a 28-day "
                           "uptrend with a positive proximity to the 28-day high, as the Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_f, case_r, case_coin = [], [], []
    drift = {}
    for coin, wins in bars.items():
        all_r = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            regime = d["regime"].astype(str).to_numpy()
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                all_r.append(r)
                if regime[i] == "trending" and np.isfinite(fc[i]):
                    case_f.append(fc[i])
                    case_r.append(r)
                    case_coin.append(coin)
        drift[coin] = float(np.mean(all_r)) if len(all_r) > 0 else np.nan

    case_f = np.asarray(case_f, dtype=float)
    case_r = np.asarray(case_r, dtype=float)
    excess = np.array([case_r[k] - drift[case_coin[k]] for k in range(len(case_r))], dtype=float)
    ok = np.isfinite(excess) & np.isfinite(case_f)
    case_f, excess = case_f[ok], excess[ok]
    n_cases = int(len(case_f))
    k3 = n_cases // 3
    order = np.argsort(case_f, kind="mergesort")
    bottom = excess[order[:k3]] if k3 > 0 else np.array([])
    top = excess[order[n_cases - k3:]] if k3 > 0 else np.array([])

    counts = {"cases in trending regime": n_cases,
              "top third cases": int(len(top)),
              "bottom third cases": int(len(bottom))}

    if len(top) < 30 or len(bottom) < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "top third mean excess 5-day return > 0",
                                 "value": float(np.mean(top)) if len(top) else None, "passed": None},
            "counts": counts,
            "decided_by": "The plan's minimum of 30 cases in each third is not reached.",
            "reading": reading,
        }

    diff = float(np.mean(top) - np.mean(bottom))
    t = stats.ttest_ind(top, bottom, equal_var=False).statistic
    t = float(t) if np.isfinite(t) else 0.0
    top_mean = float(np.mean(top))
    sup_pass = bool(top_mean > 0)

    if diff > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The top-minus-bottom difference is positive with Welch t >= 2 and the top third's mean excess return is above 0."
    elif diff < 0 and t <= -2:
        status = "rejected"
        decided = "The top-minus-bottom difference is negative with Welch t <= -2."
    elif t >= 2 and not sup_pass:
        status = "inconclusive"
        decided = "Welch t >= 2 but the top third's mean excess return is at or below 0."
    else:
        status = "inconclusive"
        decided = "Welch t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": diff,
                         "statistic": {"name": "Welch t", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": "top third mean excess 5-day return > 0",
                             "value": top_mean, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
