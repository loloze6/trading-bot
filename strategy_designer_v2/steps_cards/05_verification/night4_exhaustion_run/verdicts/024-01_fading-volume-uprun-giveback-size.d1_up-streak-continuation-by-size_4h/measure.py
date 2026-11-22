import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    RAW = "debug_info.components.up_streak.last_history_value"
    MIN_CASES = 100

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            prev = close.shift(1)
            price_up = close > prev
            price_known = prev.notna() & close.notna()
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            raw_known = raw.notna()
            raw_pos = raw > 0
            # situation: on a bar of an unbroken up-streak (raw streak gain > 0 and the bar closed up)
            situ = pd.Series(True, index=d.index)
            situ &= np.where(raw_known, raw_pos, True)
            situ &= np.where(price_known, price_up, True)
            situ &= (raw_known | price_known)
            active = fc.notna() & (fc != 0)
            agree = active & situ & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of the mean of forecast/10 x excess 18-bar return on grid bars with forecast > 0"
    main_thr = "confirm if t >= 2 (with supporting check), reject if t <= -2"
    supp_name = "top-half minus bottom-half excess 18-bar return, split at median forecast (Welch t)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "grid cases with forecast above 0": None},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars of an ongoing up-streak "
                           "(raw streak gain > 0 and the bar closing up), so the forecast does not follow the plan's situation and side."),
            "reading": "The situation is a bar with a positive raw up-streak gain that closed above the previous close, on the long side.",
        }

    # ---------- 2. criterion ----------
    # coin drift: mean 18-bar return over the non-overlapping grids of all windows
    drift = {}
    cases = []  # (forecast, excess return)
    per_coin_grid = {}
    for coin, wins in bars.items():
        rets_all = []
        grid_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            n = len(d)
            for i in range(0, n, H):
                j = i + H
                if j >= n:
                    break
                c0, c1 = close[i], close[j]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                rets_all.append(r)
                grid_rows.append((fc[i], r))
        drift[coin] = float(np.mean(rets_all)) if rets_all else np.nan
        per_coin_grid[coin] = grid_rows

    for coin, rows in per_coin_grid.items():
        dr = drift[coin]
        if not np.isfinite(dr):
            continue
        for f, r in rows:
            if np.isfinite(f) and f > 0:
                cases.append((float(f), float(r - dr)))

    n_cases = len(cases)
    counts = {"grid cases with forecast above 0": int(n_cases)}

    if n_cases < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": supp_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Only {n_cases} grid cases with a forecast above 0 across all coins and windows, fewer than the plan's minimum of 100.",
            "reading": ("Grid bars are positions 0, 18, 36, ... of each window with the 18-bar return inside the window; drift is the coin's mean "
                        "18-bar return on these grids over all windows; the median split puts forecasts above the median in the top half, the rest in the bottom half."),
        }

    f_arr = np.array([c[0] for c in cases])
    x_arr = np.array([c[1] for c in cases])
    vals = f_arr / 10.0 * x_arr
    mean_v = float(np.mean(vals))
    sd_v = float(np.std(vals, ddof=1))
    t_main = float(mean_v / (sd_v / np.sqrt(n_cases))) if sd_v > 0 else 0.0

    med = float(np.median(f_arr))
    top = x_arr[f_arr > med]
    bot = x_arr[f_arr <= med]
    if len(top) >= 2 and len(bot) >= 2:
        diff = float(np.mean(top) - np.mean(bot))
        tw = stats.ttest_ind(top, bot, equal_var=False)
        t_supp = float(tw.statistic) if np.isfinite(tw.statistic) else 0.0
        supp_pass = bool(diff > 0 and t_supp >= 1.0)
    else:
        diff, t_supp, supp_pass = None, None, False
    counts["top half cases"] = int(len(top))
    counts["bottom half cases"] = int(len(bot))

    if t_main >= 2 and supp_pass:
        status = "confirmed"
        decided = "The main t is >= 2 and the top-half minus bottom-half excess return is above 0 with Welch t >= 1."
    elif t_main >= 2:
        status = "inconclusive"
        decided = "The main t is >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif t_main <= -2:
        status = "rejected"
        decided = "The main t is <= -2: forecast-weighted excess returns after up-streaks are reliably negative."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_v,
                         "statistic": {"name": "t of the mean", "value": t_main},
                         "threshold": main_thr},
        "supporting_check": {"name": supp_name, "value": diff, "passed": supp_pass,
                             "welch_t": t_supp},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Grid bars are positions 0, 18, 36, ... of each window with the 18-bar return inside the window; drift is the coin's mean "
                    "18-bar return on these grids over all windows; the median split puts forecasts above the median in the top half, the rest in the bottom half."),
    }
