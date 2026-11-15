import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    RET_COL = "debug_info.components.ret60.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if not active.any():
                continue
            n_active += int(active.sum())
            regime_ok = df["regime"].astype(str) == "trending"
            if RET_COL in df.columns:
                r60 = pd.to_numeric(df[RET_COL], errors="coerce")
                mom_ok = r60.notna() & (r60 > 0)
            else:
                mom_ok = pd.Series(False, index=df.index)
            agree = active & regime_ok & mom_ok & (fc > 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean of (forecast/10) x excess 20-bar forward return on active non-overlapping cases"
    main_thr = "t >= 2.0 confirms (with slope > 0), t <= -2.0 rejects, over at least 30 active cases"
    sup_name = "OLS slope of excess 20-bar forward return on forecast"
    reading = ("The situation is checked as regime == 'trending' (the detector's close-above-200-SMA rule) "
               "and ret60 last_history_value > 0 with a positive forecast; the coin's mean 20-bar return is "
               "the mean over all windows' non-overlapping grid bars (positions 0, 20, 40, ...), active or not, "
               "and a case is a grid bar with forecast > 0 and a forward return inside its window.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active non-overlapping cases": 0, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are long bars with the close above its 200-day SMA "
                           "(regime trending) and a positive 60-day return, so the forecast does not do what the "
                           "Fidelity says." if n_active > 0 else
                           "There are no active bars, so the forecast never takes the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    grid = {}  # coin -> list of DataFrames(forecast, fwd)
    for coin, wins in bars.items():
        rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for p in range(0, n, H):
                if p + H < n:
                    c0, c1 = close[p], close[p + H]
                    if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                        rows.append((fc[p], c1 / c0 - 1.0))
        if rows:
            grid[coin] = pd.DataFrame(rows, columns=["forecast", "fwd"])

    vals, fcs, exs = [], [], []
    for coin, g in grid.items():
        mu = g["fwd"].mean()
        sel = g[g["forecast"].notna() & (g["forecast"] > 0)]
        ex = sel["fwd"] - mu
        vals.extend(list((sel["forecast"] / 10.0 * ex).to_numpy()))
        fcs.extend(list(sel["forecast"].to_numpy()))
        exs.extend(list(ex.to_numpy()))

    vals = np.asarray(vals, dtype=float)
    fcs = np.asarray(fcs, dtype=float)
    exs = np.asarray(exs, dtype=float)
    n_cases = int(len(vals))

    mean_v = float(np.mean(vals)) if n_cases > 0 else None
    t = None
    if n_cases >= 2:
        sd = float(np.std(vals, ddof=1))
        if sd > 0:
            t = float(mean_v / (sd / np.sqrt(n_cases)))
    slope = None
    if n_cases >= 2 and np.ptp(fcs) > 0:
        slope = float(stats.linregress(fcs, exs).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} active non-overlapping cases across all coins and windows, below the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t-statistic cannot be computed (no variance), so neither the confirm nor the reject rule is met."
    elif t >= 2.0 and slope_pass:
        status = "confirmed"
        decided = "The main measure has t >= 2.0 over at least 30 active cases and the supporting slope is above 0."
    elif t >= 2.0:
        status = "inconclusive"
        decided = "t >= 2.0 but the supporting slope is <= 0 (or not computable), which the plan calls inconclusive."
    elif t <= -2.0:
        status = "rejected"
        decided = "The main measure has t <= -2.0 over at least 30 active cases."
    else:
        status = "inconclusive"
        decided = "t is between -2.0 and 2.0, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_v,
            "statistic": None if t is None else {"name": "ordinary t of the mean", "value": t},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": slope, "passed": slope_pass},
        "counts": {"active non-overlapping cases": n_cases, "active bars": int(n_active)},
        "decided_by": decided,
        "reading": reading,
    }
