import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    RAW = "debug_info.components.fall2h.last_history_value"

    def _ts(df):
        ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        return ts.reset_index(drop=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True).copy()
            ts = _ts(d)
            end = ts + pd.Timedelta(hours=1)
            settle = (end.dt.minute == 0) & end.dt.hour.isin([0, 16])
            close = pd.to_numeric(d["close"], errors="coerce")
            ret2 = close / close.shift(2) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                fallval = raw.where(raw.notna(), ret2)
            else:
                fallval = ret2
            fall = fallval < 0
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            ok = active & settle & fall & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())
            prepared[coin][w] = (close.values, fc.values, settle.values)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    main_name = "mean unusual 24-bar move of settlement bets (forecast >= 2)"
    thr = "confirm: mean > 0 with t >= 2 and supporting difference > 0; reject: mean < 0 with t <= -2; at least 30 independent cases"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": ("fewer than 90 % of the active bars are long bets on bars ending at the 00:00 or 16:00 UTC "
                           "settlement after a 2-bar fall" if n_active > 0 else
                           "the record has no active bar, so the plan's settlement-fall long situation never appears"),
            "reading": "a settlement bar is a 1h bar whose end (start + 1 h) is 00:00 or 16:00 UTC; a fall is a negative raw fall2h value (or 2-bar return when not recorded); the expected side is long.",
        }

    # ---------- 2. criterion ----------
    cases, small = [], []
    for coin, wins in prepared.items():
        grid = []
        for w, (close, fc, settle) in wins.items():
            n = len(close)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid.append(r)
        if len(grid) == 0:
            continue
        drift = float(np.mean(grid))
        for w, (close, fc, settle) in wins.items():
            n = len(close)
            seen_c, seen_s = set(), set()
            for t in range(n):
                if not settle[t] or t + H >= n:
                    continue
                f = fc[t]
                if not np.isfinite(f) or f <= 0:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                cell = t // H
                if f >= 2:
                    if cell not in seen_c:
                        seen_c.add(cell)
                        cases.append(r - drift)
                else:
                    if cell not in seen_s:
                        seen_s.add(cell)
                        small.append(r - drift)

    cases = np.array(cases, dtype=float)
    small = np.array(small, dtype=float)
    nc, ns = len(cases), len(small)
    mean_c = float(cases.mean()) if nc > 0 else None
    t_c = None
    if nc >= 2:
        sd = cases.std(ddof=1)
        t_c = float(mean_c / (sd / np.sqrt(nc))) if sd > 0 else None
    diff = None
    welch_t = None
    if nc >= 1 and ns >= 1:
        diff = float(cases.mean() - small.mean())
        if nc >= 2 and ns >= 2:
            welch_t = float(stats.ttest_ind(cases, small, equal_var=False).statistic)
    sup_pass = None if diff is None else bool(diff > 0)

    counts = {"independent cases": int(nc), "small-fall settlement bars": int(ns)}
    if nc < 30:
        status = "not observable"
        decided = f"only {nc} independent cases, fewer than the plan's minimum of 30."
    elif t_c is not None and mean_c > 0 and t_c >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "the cases' mean unusual move is positive with t >= 2 and the difference with the small falls is above 0."
    elif t_c is not None and mean_c < 0 and t_c <= -2:
        status = "rejected"
        decided = "the cases' mean unusual move is negative with t <= -2."
    elif t_c is not None and t_c >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting difference with the small falls is 0 or below (or not computable)."
    else:
        status = "inconclusive"
        decided = "the t of the cases' mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_c,
                         "statistic": ({"name": "t of the mean", "value": t_c} if t_c is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "Welch difference of mean unusual move, cases minus small falls (0 < forecast < 2)",
                             "value": diff, "passed": sup_pass,
                             "welch_t": welch_t},
        "counts": counts,
        "decided_by": decided,
        "reading": ("settlement bars are bars whose end (start + 1 h) is 00:00 or 16:00 UTC; cases and small falls are each "
                    "kept as the first such bar per 24-bar grid cell counted from each window's first row, with the 24-bar "
                    "forward return inside the window; the coin's mean 24-bar return is taken on the non-overlapping grid of "
                    "all its windows; the supporting check passes when the difference is above 0; fewer than 30 cases is "
                    "reported as not observable."),
    }
