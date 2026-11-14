import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.below_sma200.last_history_value"
    THR = 5.0
    MIN_CASES = 30

    # ---------- 1. Situation check ----------
    # The situation is a close below its SMA200, so the raw distance is < 0.
    # The expected side is long, so the forecast is > 0.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["forecast", RAW]].dropna()
            act = d["forecast"] != 0
            n_active += int(act.sum())
            ok = act & (d[RAW] < 0) & (d["forecast"] > 0)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "mean 10-bar forward return after forecast >= 5 minus the coin's mean 10-bar return"
    thr_words = ("confirm if the mean is > 0 with t >= 2; reject if the mean is < 0 with t <= -2; "
                 "otherwise inconclusive; at least 30 non-overlapping cases are needed")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_words},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are long bars with the close "
                           "below its SMA200: the forecast is positive whenever the distance sits below its "
                           "own 200-bar mean, not only when the close sits below the SMA200."
                           if n_active > 0 else "No active bars in the record."),
            "reading": ("The situation is the raw component value (percent distance from the SMA200) < 0, "
                        "with a forecast > 0."),
        }

    # ---------- 2. Criterion ----------
    # Build the non-overlapping grid: positions 0, 10, 20, ... of each window.
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].to_numpy(dtype=float)
            f = df["forecast"].to_numpy(dtype=float)
            n = len(df)
            for i in range(0, n - H, H):
                if np.isnan(c[i]) or np.isnan(c[i + H]) or np.isnan(f[i]) or c[i] == 0:
                    continue
                rows.append((coin, c[i + H] / c[i] - 1.0, f[i]))
    g = pd.DataFrame(rows, columns=["coin", "ret", "fc"])

    if len(g) == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_words},
            "supporting_check": None,
            "counts": {"non-overlapping 10-bar cases at forecast >= 5": 0},
            "decided_by": "Fewer than 30 non-overlapping 10-bar cases at forecast >= 5.",
            "reading": "No valid 10-bar returns in the record.",
        }

    # Coin's holding mean: the mean of its 10-bar returns on the grid, pooled over all its windows.
    coin_mean = g.groupby("coin")["ret"].mean()
    g["excess"] = g["ret"] - g["coin"].map(coin_mean)

    sel = g[g["fc"] >= THR]["excess"].to_numpy()
    n_cases = int(len(sel))
    mean_ex = float(np.mean(sel)) if n_cases > 0 else None
    if n_cases >= 2:
        sd = np.std(sel, ddof=1)
        t = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None
    else:
        t = None

    # Supporting check: OLS slope of the excess return on the forecast, over grid bars with forecast > 0.
    pos = g[g["fc"] > 0]
    slope = None
    sup_pass = None
    if len(pos) >= 3 and pos["fc"].nunique() > 1:
        slope = float(stats.linregress(pos["fc"].to_numpy(), pos["excess"].to_numpy()).slope)
        sup_pass = bool(slope > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = (f"Only {n_cases} non-overlapping 10-bar cases at forecast >= 5, "
                   f"below the plan's minimum of 30.")
    elif t is None:
        status = "inconclusive"
        decided = "The t-statistic cannot be computed (zero dispersion), so neither rule is met."
    elif mean_ex > 0 and t >= 2:
        status = "confirmed"
        decided = "The mean excess 10-bar return after forecast >= 5 is positive, with t >= 2."
    elif mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "The mean excess 10-bar return after forecast >= 5 is negative, with t <= -2."
    else:
        status = "inconclusive"
        decided = "-2 < t < 2 for the mean excess 10-bar return after forecast >= 5."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": {"name": "ordinary t of the mean (non-overlapping 10-bar blocks)", "value": t}
            if t is not None else None,
            "threshold": thr_words,
        },
        "supporting_check": {
            "name": "OLS slope of the 10-bar excess return on the forecast, forecast > 0",
            "value": slope,
            "passed": sup_pass,
        },
        "counts": {"non-overlapping 10-bar cases at forecast >= 5": n_cases},
        "decided_by": decided,
        "reading": ("Overlap is handled with the non-overlapping grid (positions 0, 10, 20, ... of each window) "
                    "and the ordinary t of the mean. The coin's holding mean is its mean grid 10-bar return over "
                    "all its windows. The supporting slope uses the same grid bars with forecast > 0 and is "
                    "reported but does not enter the decision, since the confirm and reject rules do not name it."),
    }
