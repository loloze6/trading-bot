import numpy as np
import pandas as pd


def measure(bars):
    H = 72
    RET_PERIOD = 720
    MIN_CASES = 200
    RAW_COL = "debug_info.components.fall24h.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if RAW_COL in df.columns:
                raw = pd.to_numeric(df[RAW_COL], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(df), np.nan)
            regime = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))

            n = len(df)
            # 30-day return from prices inside the window; regime column where history is too short
            ret30 = np.full(n, np.nan)
            if n > RET_PERIOD:
                ret30[RET_PERIOD:] = close[RET_PERIOD:] / close[:-RET_PERIOD] - 1.0
            up30 = np.where(np.isfinite(ret30), ret30 > 0, regime == "mean_reversion")

            active = np.isfinite(fc) & (fc != 0)
            situation = up30 & np.isfinite(raw) & (raw < 0)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "forecast-weighted mean 72-bar unusual move (return minus coin's mean 72-bar return)"
    threshold = "confirm: > 0 with t >= 2 and top-minus-bottom third > 0; reject: < 0 with t <= -2"
    reading = ("The 30-day return is recomputed from closes 720 bars back inside each window and taken from the "
               "recorded regime where the window has fewer than 720 earlier bars; the coin's mean 72-bar return is "
               "the mean over all grid bars of all its windows; thirds are formed on all cases pooled across coins, "
               "sorted by forecast and split into three near-equal groups with numpy.array_split.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are bars with a positive 30-day return "
                           "and a 24-hour fall with a long forecast, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_f = []
    case_u = []
    for coin, wins in bars.items():
        grid_rets = []
        grid_cases = []  # (forecast, fwd return)
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for i in range(0, n, H):
                j = i + H
                if j >= n:
                    break
                if not (np.isfinite(close[i]) and np.isfinite(close[j]) and close[i] != 0):
                    continue
                r = close[j] / close[i] - 1.0
                grid_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    grid_cases.append((fc[i], r))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for f, r in grid_cases:
            case_f.append(f)
            case_u.append(r - drift)

    case_f = np.asarray(case_f, dtype=float)
    case_u = np.asarray(case_u, dtype=float)
    n_cases = int(len(case_f))

    wmean = None
    tval = None
    support = None
    if n_cases > 0 and case_f.sum() > 0:
        wmean = float(np.sum(case_f * case_u) / np.sum(case_f))
    if n_cases > 1:
        prod = case_f * case_u
        sd = np.std(prod, ddof=1)
        tval = float(np.mean(prod) / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0
    if n_cases >= 3:
        order = np.argsort(case_f, kind="mergesort")
        parts = np.array_split(order, 3)
        support = float(np.mean(case_u[parts[2]]) - np.mean(case_u[parts[0]]))
    support_passed = None if support is None else bool(support > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than {MIN_CASES} cases over all coins and windows ({n_cases})."
    elif wmean is not None and tval is not None and wmean > 0 and tval >= 2 and support_passed:
        status = "confirmed"
        decided = "The weighted mean unusual move is > 0 with t >= 2 and the top-minus-bottom-third difference is > 0."
    elif wmean is not None and tval is not None and wmean < 0 and tval <= -2:
        status = "rejected"
        decided = "The weighted mean unusual move is < 0 with t <= -2."
    elif tval is not None and tval >= 2 and not support_passed:
        status = "inconclusive"
        decided = "t >= 2 but the top-minus-bottom-third difference is not > 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t is between -2 and 2 (or sign and t disagree), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": wmean,
            "statistic": None if tval is None else {"name": "t of mean of forecast x unusual move", "value": tval},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "top-third minus bottom-third mean unusual move (by forecast)",
            "value": support,
            "passed": support_passed,
        },
        "counts": {"cases over all coins and windows": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
