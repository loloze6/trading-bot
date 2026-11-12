import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.rsi_low.last_history_value"
    SCALE = 0.4

    # ---------- 1. Situation check: RSI(14) < 50, short side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["forecast", RAW]].dropna()
            act = d["forecast"] != 0
            rsi = 50.0 - d[RAW] / SCALE
            situ = rsi < 50.0
            n_active += int(act.sum())
            n_agree += int((act & situ & (d["forecast"] < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Quintiles of |forecast| are cut over the pooled non-overlapping grid bars "
               "(positions 0,5,10,... of each window) that have a non-zero forecast and a valid "
               "5-bar forward return, extremes being |forecast| >= the 80th percentile and neutral "
               "being forecast 0 or |forecast| <= the 20th percentile; the difference is extremes "
               "minus neutral with Welch t; with only the coins present, the supporting check "
               "requires the same sign in at least 2 coins of those in the record.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "mean 5-bar forward return after extremes minus after neutral",
                "value": None, "statistic": None,
                "threshold": "confirm if negative with Welch t <= -2; reject if positive with t >= +2"},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("The plan's situation is RSI(14) below 50 with a short position, but only "
                           f"{agreement:.1%} of active bars are RSI<50 bars with a negative forecast "
                           "(fewer than 90%)."),
            "reading": reading,
        }

    # ---------- 2. Non-overlapping 5-bar forward returns ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = d["forecast"].astype(float).values
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1, f = close[i], close[i + H], fc[i]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 == 0:
                    continue
                rows.append((coin, w, f, c1 / c0 - 1.0))
    g = pd.DataFrame(rows, columns=["coin", "window", "forecast", "ret"])
    if len(g) == 0:
        g = pd.DataFrame({"coin": [], "window": [], "forecast": [], "ret": []})

    absf = g["forecast"].abs()
    nz = absf[absf > 0]
    if len(nz) > 0:
        hi = float(np.percentile(nz, 80))
        lo = float(np.percentile(nz, 20))
        ext = (absf > 0) & (absf >= hi)
        neu = (absf == 0) | ((absf > 0) & (absf <= lo))
    else:
        ext = pd.Series(False, index=g.index)
        neu = absf == 0

    r_ext = g.loc[ext, "ret"].values
    r_neu = g.loc[neu, "ret"].values
    n_ext = int(len(r_ext))
    n_neu = int(len(r_neu))

    diff = None
    t = None
    if n_ext >= 1 and n_neu >= 1:
        diff = float(np.mean(r_ext) - np.mean(r_neu))
    if n_ext >= 2 and n_neu >= 2:
        tt = stats.ttest_ind(r_ext, r_neu, equal_var=False)
        t = float(tt.statistic) if np.isfinite(tt.statistic) else None

    # ---------- supporting check: same sign per coin ----------
    coins = list(bars.keys())
    same = 0
    per_coin = {}
    for c in coins:
        m = g["coin"] == c
        e = g.loc[m & ext, "ret"]
        nn = g.loc[m & neu, "ret"]
        if len(e) > 0 and len(nn) > 0:
            dc = float(e.mean() - nn.mean())
            per_coin[c] = dc
            if diff is not None and np.sign(dc) == np.sign(diff) and dc != 0:
                same += 1
    needed = min(2, len(coins))
    sup_passed = bool(diff is not None and same >= needed) if diff is not None else None

    counts = {"non-overlapping extreme cases": n_ext,
              "non-overlapping neutral cases": n_neu}

    # ---------- decision ----------
    if n_ext < 30:
        status = "not observable"
        decided = f"Fewer than 30 non-overlapping extreme cases in total ({n_ext})."
    elif diff is None or t is None:
        status = "not observable"
        decided = "Too few neutral cases to compute the difference and its Welch t."
    elif diff < 0 and t <= -2:
        status = "confirmed"
        decided = f"Extremes minus neutral is negative ({diff:.4f}) with Welch t = {t:.2f} <= -2."
    elif diff > 0 and t >= 2:
        status = "rejected"
        decided = f"Extremes minus neutral is positive ({diff:.4f}) with Welch t = {t:.2f} >= +2 (reversal)."
    else:
        status = "inconclusive"
        decided = f"Welch t = {t:.2f} lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean 5-bar forward return after extremes minus after neutral",
            "value": diff,
            "statistic": {"name": "Welch t", "value": t} if t is not None else None,
            "threshold": "confirm if negative with Welch t <= -2; reject if positive with t >= +2"},
        "supporting_check": {
            "name": f"same sign in at least {needed} of {len(coins)} coins",
            "value": int(same),
            "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
