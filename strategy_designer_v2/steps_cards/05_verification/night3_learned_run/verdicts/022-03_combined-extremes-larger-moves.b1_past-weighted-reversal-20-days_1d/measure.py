import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    RAW = "debug_info.components.rev_weighted.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            ok = active & raw.notna() & (raw != 0) & (np.sign(f) == np.sign(raw))
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean signed excess 20-bar return over cases with abs(forecast) >= 2 (before costs)"
    main_thr = "t >= 2 over at least 30 cases confirms (with supporting check > 0); t <= -2 over at least 30 cases rejects"
    sup_name = "mean signed excess return, larger-|forecast| half minus smaller half"
    reading = ("The situation is taken as a non-zero raw term (the graded size), its side as the sign of the raw term, "
               "compared with the sign of a non-zero forecast; the median split puts cases with abs(forecast) above the "
               "median in the larger half and the rest in the smaller half; the drift is each coin's mean 20-bar return "
               "on the non-overlapping grid of all its windows; fewer than 30 cases is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases": None, "active bars": n_active},
            "decided_by": ("Fewer than 90 % of the active bars have a forecast whose sign matches the sign of the "
                           "raw weighted reversal term the plan's situation describes."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    case_rows = []  # (coin, ret, forecast)
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            f = pd.to_numeric(d["forecast"], errors="coerce").values
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(f[i]) and abs(f[i]) >= 2:
                    coin_cases.append((r, f[i]))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for r, fv in coin_cases:
            case_rows.append((np.sign(fv) * (r - drift), abs(fv)))

    n_cases = len(case_rows)
    vals = np.array([c[0] for c in case_rows], dtype=float)
    absf = np.array([c[1] for c in case_rows], dtype=float)

    mean_val = float(np.mean(vals)) if n_cases > 0 else None
    if n_cases > 1:
        sd = float(np.std(vals, ddof=1))
        t = float(mean_val / (sd / np.sqrt(n_cases))) if sd > 0 else float("nan")
    else:
        t = float("nan")

    diff = None
    if n_cases > 1:
        med = np.median(absf)
        large = vals[absf > med]
        small = vals[absf <= med]
        if len(large) > 0 and len(small) > 0:
            diff = float(np.mean(large) - np.mean(small))
    sup_passed = bool(diff is not None and diff > 0)

    t_out = None if not np.isfinite(t) else t

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases, below the plan's minimum of 30 cases."
    elif t_out is not None and t >= 2 and sup_passed:
        status = "confirmed"
        decided = "The main-measure t is 2 or more over at least 30 cases and the supporting check difference is above 0."
    elif t_out is not None and t >= 2:
        status = "inconclusive"
        decided = "A t of 2 or more with the supporting check not passing is inconclusive."
    elif t_out is not None and t <= -2:
        status = "rejected"
        decided = "The main-measure t is -2 or less over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The main-measure t is between -2 and 2, which is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": {"name": "t of the mean", "value": t_out} if t_out is not None else None,
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_passed if diff is not None else None},
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
