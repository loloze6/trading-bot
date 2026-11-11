import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    RAW = "debug_info.components.sma_cross_down.last_history_value"
    MIN_CASES = 30
    T_CUT = 2.0

    # ---------- 1. Situation check ----------
    # The plan's situation is "50-day SMA below the 200-day SMA". The raw component
    # value is the (50 SMA - 200 SMA) spread, so the situation holds where it is < 0.
    # The plan's outcome is a fall, so the expected side is short (forecast < 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            r = pd.to_numeric(df[RAW], errors="coerce")
            ok = f.notna() & r.notna()
            active = ok & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & (r < 0) & (f < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "|forecast|-weighted mean excess gain of the short over holding, 10 bars, non-overlapping, pooled"
    threshold = "confirm if > 0 with t >= 2; reject if < 0 with t <= -2; else inconclusive; fewer than 30 cases inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars where the 50-day SMA "
                           "is below the 200-day SMA with a short forecast: the config's standardised, clipped "
                           "spread does not take its positions only in the plan's situation on the short side."),
            "reading": "The situation is read as a raw component value (50 SMA minus 200 SMA spread) below 0, and the side as forecast below 0.",
        }

    # ---------- 2. Criterion ----------
    xs, ws = [], []
    for coin, wins in bars.items():
        # Holding: the coin's mean 10-bar forward return over all bars of all its windows.
        all_fwd = []
        per_win = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(c)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = c[H:] / c[: n - H] - 1.0
            all_fwd.append(fwd[np.isfinite(fwd)])
            per_win.append((fwd, f))
        all_fwd = np.concatenate(all_fwd) if all_fwd else np.array([])
        if all_fwd.size == 0:
            continue
        hold = float(np.mean(all_fwd))
        for fwd, f in per_win:
            idx = np.arange(0, len(fwd), H)
            for i in idx:
                if np.isfinite(fwd[i]) and np.isfinite(f[i]) and f[i] < 0:
                    # short side's excess gain = -(forward return - holding)
                    xs.append(-(fwd[i] - hold))
                    ws.append(abs(f[i]))

    x = np.asarray(xs, dtype=float)
    wgt = np.asarray(ws, dtype=float)
    n_cases = int(x.size)

    mean_w = None
    t_val = None
    if n_cases >= 2 and wgt.sum() > 0:
        sw = wgt.sum()
        mean_w = float(np.sum(wgt * x) / sw)
        se = np.sqrt(np.sum((wgt ** 2) * (x - mean_w) ** 2) * n_cases / (n_cases - 1)) / sw
        t_val = float(mean_w / se) if se > 0 else 0.0
    elif n_cases == 1:
        mean_w = float(x[0])

    # Supporting check: terciles of |forecast| among the short cases.
    sup_val = None
    sup_pass = None
    if n_cases >= 3:
        order = np.argsort(wgt, kind="mergesort")
        thirds = np.array_split(order, 3)
        lo, hi = thirds[0], thirds[-1]
        m_lo = float(np.sum(wgt[lo] * x[lo]) / np.sum(wgt[lo]))
        m_hi = float(np.sum(wgt[hi] * x[hi]) / np.sum(wgt[hi]))
        sup_val = m_hi - m_lo
        sup_pass = bool(sup_val > 0)

    if n_cases < MIN_CASES or mean_w is None or t_val is None:
        status = "inconclusive"
        decided = "Fewer than 30 non-overlapping short cases in total, which the plan calls inconclusive."
    elif mean_w > 0 and t_val >= T_CUT:
        status = "confirmed"
        decided = "The short side's weighted mean excess gain is above 0 with t >= 2: price falls further than holding while the short average is below the long one."
    elif mean_w < 0 and t_val <= -T_CUT:
        status = "rejected"
        decided = "The short side's weighted mean excess gain is below 0 with t <= -2: price rises relative to holding, so moves reverse."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies strictly between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_w,
            "statistic": None if t_val is None else {"name": "t of the |forecast|-weighted mean", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "top minus bottom tercile of |forecast|, weighted mean short excess gain",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"non-overlapping short cases": n_cases},
        "decided_by": decided,
        "reading": ("Holding is the coin's mean of all overlapping 10-bar forward returns over all its windows, "
                    "the short's excess gain is -(forward return - holding), cases are bars 0,10,20,... of each "
                    "window with forecast < 0, the t uses a weighted-mean standard error "
                    "sqrt(sum w^2 (x-m)^2 * n/(n-1)) / sum w, and terciles are equal-count thirds of the pooled cases "
                    "ranked by |forecast|, compared by their |forecast|-weighted means."),
    }
