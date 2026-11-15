import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"

    def _num(df, col):
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
        return np.full(len(df), np.nan)

    # ---------------- 1. Situation check ----------------
    # Situation (Fidelity): the 20-day and 60-day returns are both positive.
    # Expected side: long, because the outcome is a rise.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = _num(df, "close")
            fc = _num(df, FC)
            reg = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))
            n = len(df)
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                if i >= 60 and np.isfinite(close[i]) and np.isfinite(close[i - 20]) and np.isfinite(close[i - 60]) \
                        and close[i - 20] > 0 and close[i - 60] > 0:
                    # Recompute the detector's measures from the prices inside the window.
                    r20 = close[i] / close[i - 20] - 1.0
                    r60 = close[i] / close[i - 60] - 1.0
                    sit = (r20 > 0) and (r60 > 0)
                else:
                    # Too few bars in the window: use the detector's decision.
                    sit = (reg[i] == "trending")
                if sit and f > 0:
                    n_agree += 1

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation recomputed from closes (20- and 60-bar returns > 0) where the window holds 60 prior bars, "
               "otherwise taken from the detector's regime == 'trending' (the detector's own components are not recorded); "
               "active = forecast > 0 on each window's grid at positions 0, h, 2h, ... with a full h-bar forward return "
               "inside the window; holding-the-coin mean = the coin's mean h-bar return over all its grid bars in all windows; "
               "the plan's 'fewer than 100 cases' is reported as 'not observable' per the workflow.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the 20- and 60-day "
                           "returns are both positive (the plan's situation and side)."),
            "reading": reading,
        }

    # ---------------- 2. Criterion ----------------
    def grid_excess(h):
        per_coin = {}
        for coin, wins in bars.items():
            rows = []
            for w, df in wins.items():
                if df is None or len(df) == 0:
                    continue
                close = _num(df, "close")
                fc = _num(df, FC)
                n = len(df)
                for i in range(0, n, h):
                    if i + h >= n:
                        break
                    c0, c1 = close[i], close[i + h]
                    if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                        continue
                    rows.append((c1 / c0 - 1.0, fc[i]))
            per_coin[coin] = rows
        ex = []
        for coin, rows in per_coin.items():
            if not rows:
                continue
            rets = np.array([r for r, _ in rows], dtype=float)
            mu = rets.mean()
            for r, f in rows:
                if np.isfinite(f) and f > 0:
                    ex.append(r - mu)
        return np.array(ex, dtype=float)

    ex5 = grid_excess(5)
    ex20 = grid_excess(20)
    n5 = int(len(ex5))
    n20 = int(len(ex20))

    mean5 = float(ex5.mean()) if n5 > 0 else None
    t5 = None
    if n5 > 1:
        sd = ex5.std(ddof=1)
        if sd > 0:
            t5 = float(mean5 / (sd / np.sqrt(n5)))
    mean20 = float(ex20.mean()) if n20 > 0 else None

    support = None
    if mean5 is not None and mean20 is not None:
        support = float(mean5 / 5.0 - mean20 / 20.0)
    sup_passed = None if support is None else bool(support > 0)

    counts = {"active non-overlapping 5-bar cases": n5,
              "active non-overlapping 20-bar cases": n20}

    main = {"name": "mean forward 5-bar excess over holding the coin, active bars",
            "value": mean5,
            "statistic": {"name": "t of the mean", "value": t5} if t5 is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 (and supporting check > 0); reject: mean < 0 with t <= -2"}
    supp = {"name": "mean 5-bar excess / 5 minus mean 20-bar excess / 20", "value": support, "passed": sup_passed}

    if n5 < 100:
        status = "not observable"
        decided = f"Only {n5} active non-overlapping 5-bar cases, below the plan's minimum of 100."
    elif t5 is None:
        status = "inconclusive"
        decided = "The t of the mean 5-bar excess could not be computed (zero dispersion), so neither rule is met."
    elif mean5 > 0 and t5 >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "The mean 5-bar excess is positive with t >= 2 and the supporting check is above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2, but the supporting check is at or below 0, which the plan calls inconclusive."
    elif mean5 < 0 and t5 <= -2:
        status = "rejected"
        decided = "The mean 5-bar excess is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean 5-bar excess lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
