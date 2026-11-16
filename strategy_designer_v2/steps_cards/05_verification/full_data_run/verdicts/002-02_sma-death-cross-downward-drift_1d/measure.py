import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    MIN_CASES = 30
    RAW = "debug_info.components.sma_cross_down.last_history_value"

    # ---------- 1. Situation check ----------
    # Plan situation: the 50-day SMA is below the 200-day SMA, so the raw spread is < 0.
    # Expected side: short, so the forecast is < 0.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0) & raw.notna()
            n_active += int(active.sum())
            n_agree += int((active & (raw < 0) & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "|forecast|-weighted mean 10-bar excess gain of the short over holding (holding - forward return), pooled"
    threshold = "confirm if mean > 0 with t >= 2 (and top tercile > bottom tercile); reject if mean < 0 with t <= -2"
    reading = ("Active bars whose raw spread is missing are left out of the situation check; "
               "holding is the coin's mean 10-bar return on the non-overlapping grid (positions 0,10,20,... of each window) "
               "across all its windows; the short's excess gain is holding minus the forward return; "
               "the t of the weighted mean uses the weighted standard deviation and Kish's effective n; "
               "terciles split the short cases by rank of |forecast| into three near-equal groups, "
               "and each tercile's excess is its |forecast|-weighted mean; "
               "the plan's 'fewer than 30 short cases' rule is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "non-overlapping short cases": 0},
            "decided_by": ("Fewer than 90% of the active bars are bars where the 50-day SMA is below the "
                           "200-day SMA with a short forecast; the config's forecast is not limited to the "
                           "plan's death-cross situation on the short side."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    exc_list, wt_list = [], []
    for coin, wins in bars.items():
        grid_rows = []
        for w, df in wins.items():
            if "close" not in df.columns or "forecast" not in df.columns:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                grid_rows.append((c1 / c0 - 1.0, fc[p]))
        if not grid_rows:
            continue
        rets = np.array([r for r, _ in grid_rows])
        fcs = np.array([f for _, f in grid_rows])
        hold = float(np.mean(rets))
        mask = np.isfinite(fcs) & (fcs < 0)
        exc_list.extend(list(hold - rets[mask]))
        wt_list.extend(list(np.abs(fcs[mask])))

    exc = np.array(exc_list, dtype=float)
    wts = np.array(wt_list, dtype=float)
    n_cases = int(len(exc))

    def wmean(x, w):
        return float(np.sum(x * w) / np.sum(w)) if len(x) and np.sum(w) > 0 else None

    mean = wmean(exc, wts)
    t = None
    if n_cases >= 2 and np.sum(wts) > 0:
        var = float(np.sum(wts * (exc - mean) ** 2) / np.sum(wts))
        var *= n_cases / (n_cases - 1)
        n_eff = float(np.sum(wts) ** 2 / np.sum(wts ** 2))
        se = np.sqrt(var / n_eff) if var > 0 else 0.0
        t = float(mean / se) if se > 0 else None

    # Supporting check: tercile split by |forecast|
    sup_val, sup_pass = None, None
    if n_cases >= 3:
        order = np.argsort(wts, kind="mergesort")
        parts = np.array_split(order, 3)
        bot = wmean(exc[parts[0]], wts[parts[0]])
        top = wmean(exc[parts[2]], wts[parts[2]])
        if bot is not None and top is not None:
            sup_val = float(top - bot)
            sup_pass = bool(sup_val > 0)

    counts = {"non-overlapping short cases": n_cases}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping short cases, fewer than the plan's minimum of 30."
    elif mean is not None and t is not None and mean > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = ("The short's weighted mean excess gain is above 0 with t >= 2 and the top |forecast| "
                       "tercile beats the bottom one: price falls further than holding.")
        else:
            status = "inconclusive"
            decided = ("The main measure meets the confirm rule (mean > 0, t >= 2) but the supporting tercile "
                       "check fails, so the result is inconclusive.")
    elif mean is not None and t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = ("The short's weighted mean excess gain is below 0 with t <= -2: price rises relative to "
                   "holding while the short average is below the long one.")
    else:
        status = "inconclusive"
        decided = "The t-statistic is strictly between -2 and 2 (or undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": ({"name": "t of the weighted mean (effective n)", "value": t} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "top minus bottom |forecast| tercile weighted excess gain",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
