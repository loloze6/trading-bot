import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    reading = ("The situation is checked on the regime column (the detector's MovingAverageAgeComponent(200) >= 1 "
               "rule, labelled 'trending'), with forecast > 0 as the expected long side; "
               "the coin's mean 10-bar return uses every non-overlapping grid case of all its windows; "
               "the halves split all trending grid cases pooled across coins and windows by forecast rank. "
               "Ties are ordered stably by coin, window and bar. The bottom half takes the extra case when the "
               "count is odd.")

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w, df in bars[coin].items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            reg = df["regime"].astype(str).str.lower()
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & (reg == "trending") & (f > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "top-minus-bottom half (by forecast) mean forward 10-bar excess return, trending grid cases"
    threshold = "confirm if Welch t >= 2 with supporting check passing; reject if Welch t <= -2"
    sup_name = "mean forward 10-bar excess return of cases with forecast > 0 is above 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are trending-regime "
                           "(close above 200-day SMA) bars with a long forecast."
                           if n_active > 0 else "No bar has a non-zero forecast."),
            "reading": reading,
        }

    # ---------- grid cases ----------
    rows = []
    coin_rets = {}
    for coin in sorted(bars.keys()):
        allr = []
        wins = bars[coin]
        for w in sorted(wins.keys(), key=lambda s: int(str(s).lstrip("w")) if str(s).lstrip("w").isdigit() else str(s)):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            reg = df["regime"].astype(str).str.lower().to_numpy()
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                if reg[i] == "trending" and np.isfinite(f[i]):
                    rows.append((coin, f[i], r))
        coin_rets[coin] = float(np.mean(allr)) if len(allr) else np.nan

    fc = np.array([r[1] for r in rows], dtype=float)
    ex = np.array([r[2] - coin_rets[r[0]] for r in rows], dtype=float)
    ok = np.isfinite(ex) & np.isfinite(fc)
    fc, ex = fc[ok], ex[ok]
    N = len(fc)

    order = np.argsort(fc, kind="mergesort")
    n_top = N // 2
    n_bot = N - n_top
    bot = ex[order[:n_bot]]
    top = ex[order[n_bot:]]

    pos = ex[fc > 0]
    sup_val = float(np.mean(pos)) if len(pos) > 0 else None
    sup_pass = bool(sup_val is not None and sup_val > 0) if sup_val is not None else None

    counts = {"top half grid cases": int(len(top)), "bottom half grid cases": int(len(bot)),
              "trending grid cases": int(N), "cases with forecast > 0": int(len(pos))}

    diff = float(np.mean(top) - np.mean(bot)) if len(top) > 0 and len(bot) > 0 else None
    t = None
    if len(top) >= 2 and len(bot) >= 2:
        tt = stats.ttest_ind(top, bot, equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None

    main = {"name": main_name, "value": diff,
            "statistic": {"name": "Welch t", "value": t} if t is not None else None,
            "threshold": threshold}
    sup = {"name": sup_name, "value": sup_val, "passed": sup_pass}

    if len(top) < 100 or len(bot) < 100:
        status = "not observable"
        decided = "A half has fewer than the plan's minimum of 100 grid cases across all coins and windows."
    elif t is None:
        status = "inconclusive"
        decided = "The Welch t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Welch t >= 2 for top minus bottom and cases with forecast > 0 have a positive mean excess return."
    elif t <= -2:
        status = "rejected"
        decided = "Welch t <= -2: larger forecasts are followed by smaller 10-bar excess returns."
    elif t >= 2:
        status = "inconclusive"
        decided = "Welch t >= 2 but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "-2 < Welch t < 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
