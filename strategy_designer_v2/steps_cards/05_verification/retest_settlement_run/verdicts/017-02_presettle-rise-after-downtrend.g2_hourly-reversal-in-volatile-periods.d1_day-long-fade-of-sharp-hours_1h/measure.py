import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    RAW = "debug_info.components.fade.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: situation = last hour's move (scaled); outcome = price moves AGAINST that move,
    # so expected side = -sign(last hour's move).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            ret1 = np.full(len(close), np.nan)
            if len(close) > 1:
                ret1[1:] = close[1:] / close[:-1] - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
                raw = np.where(np.isnan(raw), ret1, raw)
            else:
                raw = ret1
            active = np.isfinite(f) & (f != 0)
            n_active += int(active.sum())
            expected = -np.sign(np.nan_to_num(raw, nan=0.0))
            agree = active & (expected != 0) & (np.sign(f) == expected)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "t of mean of forecast/10 x 24-bar excess return (non-overlapping grid, pooled)"
    main_thr = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"
    sup_name = "mean sign(forecast) x excess return, largest |forecast| third minus smallest third"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases with a non-zero forecast": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars have a forecast sign opposite to the last hour's move "
                           "(the plan's fade of the last hour), so the config does not do what the Fidelity says."),
            "reading": "Expected side taken as minus the sign of the component's raw value (the scaled last-hour return), "
                       "falling back to the 1-bar price return where the raw value is missing.",
        }

    # ---------- 2. Criterion ----------
    case_f, case_r, case_coin = [], [], []
    drift = {}
    for coin, wins in bars.items():
        all_rets = []
        per_coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if np.isfinite(f[i]) and f[i] != 0:
                    per_coin_cases.append((f[i], r))
        if len(all_rets) == 0:
            continue
        d = float(np.mean(all_rets))
        drift[coin] = d
        for fv, r in per_coin_cases:
            case_f.append(fv)
            case_r.append(r - d)
            case_coin.append(coin)

    case_f = np.array(case_f, dtype=float)
    excess = np.array(case_r, dtype=float)
    n_cases = int(len(case_f))
    counts = {"cases with a non-zero forecast": n_cases}

    reading = ("Cases are grid bars (positions 0, 24, 48, ... of each window) with a non-zero forecast and a 24-bar "
               "forward return inside the window; the coin's normal drift is the mean of all its grid 24-bar returns "
               "over all windows; thirds are formed by sorting cases on |forecast| (stable sort) and splitting into "
               "three near-equal groups; the plan's 500-case minimum, when not met, gives 'not observable'.")

    if n_cases < 500:
        val = float(np.mean(case_f / 10.0 * excess)) if n_cases > 0 else None
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": val, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Only {n_cases} cases with a non-zero forecast, below the plan's minimum of 500.",
            "reading": reading,
        }

    prod = case_f / 10.0 * excess
    mean_p = float(np.mean(prod))
    sd = float(np.std(prod, ddof=1))
    t = float(mean_p / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    order = np.argsort(np.abs(case_f), kind="mergesort")
    groups = np.array_split(order, 3)
    small, large = groups[0], groups[-1]
    se = np.sign(case_f) * excess
    diff = float(np.mean(se[large]) - np.mean(se[small]))
    sup_pass = bool(diff > 0)
    counts["cases in largest third"] = int(len(large))
    counts["cases in smallest third"] = int(len(small))

    if mean_p > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean product is positive with t >= 2 and the largest-third minus smallest-third difference is > 0 (confirm rule)."
    elif mean_p > 0 and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails (largest minus smallest third <= 0), which the plan calls inconclusive."
    elif mean_p < 0 and t <= -2:
        status = "rejected"
        decided = "The mean product is negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t of the mean product lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_p,
                         "statistic": {"name": "t of the mean", "value": t},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
