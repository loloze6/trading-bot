import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    RAW = "debug_info.components.support_cluster.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            ret60 = close / close.shift(60) - 1.0
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            # 60-day return < 0: recomputed from the window's prices when 60 past closes exist,
            # otherwise the detector's recorded decision (its component is not recorded)
            down = np.where(ret60.notna(), ret60 < 0, regime == "mean_reversion")
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            cluster_above = (raw > 0).fillna(False).values
            active = (fc != 0).values
            agree = active & down & cluster_above & (fc < 0).values
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "|forecast|-weighted mean of short-direction 10-bar excess return (return minus drift, x -1)"
    thr = "confirm: weighted mean > 0 with t >= 2 and supporting check > 0; reject: weighted mean < 0 with t <= -2"
    reading_sit = ("the situation is a 60-day return below 0 (recomputed from the window's closes, the recorded regime "
                   "where fewer than 60 past closes exist) with a positive raw cluster value (a swing low above the close), "
                   "on the short side")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "cases": 0},
            "decided_by": ("fewer than 90% of the active bars are short bars with a negative 60-day return and a swing-low "
                           "cluster above the close, as the plan's situation requires"),
            "reading": reading_sit,
        }

    # ---------- 2. criterion ----------
    xs, ws = [], []
    for coin, wins in bars.items():
        # normal drift: mean 10-bar return on each window's non-overlapping grid, all windows together
        all_r = []
        per_win = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            n = len(d)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_r.append(r)
                per_win.append((r, fc[t]))
        if len(all_r) == 0:
            continue
        drift = float(np.mean(all_r))
        for r, f in per_win:
            if np.isfinite(f) and f < 0:
                xs.append(-(r - drift))
                ws.append(abs(f))

    xs = np.asarray(xs, dtype=float)
    ws = np.asarray(ws, dtype=float)
    n_cases = int(len(xs))

    wmean = None
    tval = None
    if n_cases >= 2 and ws.sum() > 0:
        wmean = float(np.sum(ws * xs) / np.sum(ws))
        var_w = float(np.sum(ws * (xs - wmean) ** 2) / np.sum(ws))
        n_eff = float(np.sum(ws) ** 2 / np.sum(ws ** 2))
        if n_eff > 1:
            sd = np.sqrt(var_w * n_eff / (n_eff - 1.0))
            tval = float(wmean / (sd / np.sqrt(n_eff))) if sd > 0 else None
    elif n_cases == 1:
        wmean = float(xs[0])

    diff = None
    if n_cases >= 2:
        order = np.argsort(-ws, kind="mergesort")
        half = n_cases // 2
        big = xs[order[:half]]
        small = xs[order[n_cases - half:]]
        diff = float(np.mean(big) - np.mean(small))
    sup_pass = None if diff is None else bool(diff > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"fewer than 30 cases across all coins and windows ({n_cases})."
    elif wmean is None or tval is None:
        status = "inconclusive"
        decided = "the t of the weighted mean could not be computed."
    elif wmean > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "the weighted mean is above 0 with t >= 2 and the larger-|forecast| half beats the smaller half."
    elif wmean > 0 and tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails (larger minus smaller half <= 0)."
    elif wmean < 0 and tval <= -2:
        status = "rejected"
        decided = "the weighted mean is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": wmean,
            "statistic": None if tval is None else {"name": "t of the |forecast|-weighted mean (effective n)", "value": tval},
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean short excess return, larger-|forecast| half minus smaller half",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": (reading_sit + "; cases are grid bars 0,10,20,... of each window with a full 10-bar return inside it, the drift "
                    "is the coin's mean grid 10-bar return over all windows, the t is the weighted mean over its weighted "
                    "standard error with Kish effective n, and the halves are the top and bottom n//2 cases by |forecast| "
                    "(middle case dropped when odd) compared by unweighted means."),
    }
