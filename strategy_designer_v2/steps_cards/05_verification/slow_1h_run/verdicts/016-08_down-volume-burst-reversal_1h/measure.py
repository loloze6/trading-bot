import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    FC = "forecast"
    REG = "regime"

    # ---------- 1. Situation check: 72-bar return < 0, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d[FC], errors="coerce")
            ret72 = close / close.shift(H) - 1.0  # inside the window only
            active = fc.notna() & (fc != 0) & ret72.notna()
            n_active += int(active.sum())
            agree = active & (ret72 < 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("The 72-bar return is recomputed as close[t]/close[t-72]-1 inside each window, so the first 72 bars "
               "of each window are left out of the situation check; grid bars are kept on the recorded regime "
               "'mean_reversion'; the coin's mean 72-bar return is the mean of its non-overlapping grid returns "
               "over all windows; the median of forecast is taken over all kept grid bars of all coins pooled; and "
               "the plan's 'fewer than 30 grid cases in either half' minimum gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of active (non-zero forecast) bars are bars with a negative 72-bar "
                           "return and a long forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. Main measure ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(d[FC], errors="coerce").to_numpy()
            reg = d[REG].astype(str).to_numpy()
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                coin_rows.append((coin, c1 / c0 - 1.0, fc[i], reg[i]))
        if not coin_rows:
            continue
        cdf = pd.DataFrame(coin_rows, columns=["coin", "fwd", "fc", "reg"])
        coin_mean = cdf["fwd"].mean()
        cdf["excess"] = cdf["fwd"] - coin_mean
        rows.append(cdf)

    if rows:
        all_df = pd.concat(rows, ignore_index=True)
        sel = all_df[(all_df["reg"] == "mean_reversion") & all_df["fc"].notna() & all_df["excess"].notna()]
    else:
        sel = pd.DataFrame(columns=["coin", "fwd", "fc", "reg", "excess"])

    if len(sel) > 0:
        med = float(np.median(sel["fc"].to_numpy(dtype=float)))
        top = sel.loc[sel["fc"] > med, "excess"].to_numpy(dtype=float)
        bot = sel.loc[sel["fc"] <= med, "excess"].to_numpy(dtype=float)
    else:
        med = None
        top = np.array([])
        bot = np.array([])

    n_top, n_bot = int(len(top)), int(len(bot))
    counts = {"grid cases in top half": n_top, "grid cases in bottom half": n_bot,
              "active bars": n_active}

    diff = None
    t = None
    if n_top >= 2 and n_bot >= 2:
        diff = float(top.mean() - bot.mean())
        tt = stats.ttest_ind(top, bot, equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None

    main = {
        "name": "top-half minus bottom-half mean excess 72-bar forward return (mean_reversion grid bars, split at forecast median)",
        "value": diff,
        "statistic": {"name": "Welch t", "value": t} if t is not None else None,
        "threshold": "confirm: difference > 0 with Welch t >= 2; reject: difference < 0 with Welch t <= -2; otherwise inconclusive",
    }

    if n_top < 30 or n_bot < 30:
        status = "not observable"
        decided = "Fewer than 30 grid cases in at least one half (top %d, bottom %d), the plan's minimum count." % (n_top, n_bot)
    elif diff is None or t is None:
        status = "inconclusive"
        decided = "The Welch t could not be computed, so neither the confirm nor the reject rule is met."
    elif diff > 0 and t >= 2:
        status = "confirmed"
        decided = "The difference is positive with Welch t >= 2 (confirm rule)."
    elif diff < 0 and t <= -2:
        status = "rejected"
        decided = "The difference is negative with Welch t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The Welch t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
