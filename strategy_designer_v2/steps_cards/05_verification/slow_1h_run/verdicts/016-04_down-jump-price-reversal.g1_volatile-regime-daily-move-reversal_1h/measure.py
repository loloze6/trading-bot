import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    MIN_CASES = 1000
    RAW_COL = "debug_info.components.fade_scaled_move.last_history_value"

    # ---------- 1. Situation check ----------
    # The raw value is the 24-bar return scaled by volatility. Fading it means the
    # forecast's sign is the opposite of the raw value's sign.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW_COL in df.columns:
                raw = pd.to_numeric(df[RAW_COL], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # Where the raw value is not recorded, rebuild its sign from prices.
            # The volatility factors are positive, so the sign is that of the 24-bar return in the window.
            ret_back = close / close.shift(H) - 1.0
            raw_sign = np.sign(raw)
            raw_sign = raw_sign.where(raw.notna(), np.sign(ret_back))
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw_sign.notna() & (raw_sign != 0) & (np.sign(fc) == -raw_sign)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed_sit = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled mean of forecast/10 x excess 24-bar return on the 24-bar grid"
    main_thr = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 1,000 independent cases"
    sup_name = "top-fifth minus bottom-fifth |forecast| mean of sign(forecast) x excess 24-bar return"

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "agreeing bars": n_agree},
            "decided_by": ("Fewer than 90% of active bars have a forecast opposite in sign to the "
                           "volatility-scaled 24-hour move, which the plan's fade requires."),
            "reading": "The situation is ungated, so every bar with a nonzero raw value is a situation bar, and the expected side is opposite to the raw move's sign.",
        }

    # ---------- 2. Grid samples ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(df)
            for p in range(0, n - H, H):
                c0, c1, f = close[p], close[p + H], fc[p]
                if np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f) and c0 > 0:
                    rows.append((coin, f, c1 / c0 - 1.0))
    g = pd.DataFrame(rows, columns=["coin", "fc", "ret"])

    if len(g) == 0:
        n_cases = 0
    else:
        g["excess"] = g["ret"] - g.groupby("coin")["ret"].transform("mean")
        g["prod"] = g["fc"] / 10.0 * g["excess"]
        n_cases = int(len(g))

    if n_cases >= 2:
        prod = g["prod"].to_numpy()
        mean = float(prod.mean())
        sd = float(prod.std(ddof=1))
        t_main = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0
    else:
        mean, t_main = None, None

    # ---------- Supporting check ----------
    sup_val, sup_t, sup_pass = None, None, None
    n_top = n_bot = 0
    if n_cases > 0:
        g["absfc"] = g["fc"].abs()
        g["sr"] = np.sign(g["fc"]) * g["excess"]
        g["rk"] = g.groupby("coin")["absfc"].rank(method="first")
        g["cnt"] = g.groupby("coin")["absfc"].transform("count")
        top = g.loc[g["rk"] > 0.8 * g["cnt"], "sr"].to_numpy()
        bot = g.loc[g["rk"] <= 0.2 * g["cnt"], "sr"].to_numpy()
        n_top, n_bot = int(len(top)), int(len(bot))
        if n_top >= 2 and n_bot >= 2:
            sup_val = float(top.mean() - bot.mean())
            tt = stats.ttest_ind(top, bot, equal_var=False).statistic
            sup_t = float(tt) if np.isfinite(tt) else 0.0
            sup_pass = bool(sup_val > 0 and sup_t >= 2)
        else:
            sup_pass = False

    # ---------- Decision ----------
    if n_cases < MIN_CASES or mean is None:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases, below the plan's minimum of 1,000."
    elif mean > 0 and t_main >= 2 and sup_pass:
        status = "confirmed"
        decided = "Pooled mean positive with t >= 2 over at least 1,000 cases, and the top-fifth minus bottom-fifth Welch t is >= 2."
    elif mean < 0 and t_main <= -2:
        status = "rejected"
        decided = "Pooled mean negative with t <= -2 over at least 1,000 cases."
    elif mean > 0 and t_main >= 2:
        status = "inconclusive"
        decided = "Main measure has t >= 2 but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "Main measure has |t| < 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed_sit},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": ({"name": "ordinary t of the mean", "value": t_main} if t_main is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": sup_name,
            "value": sup_val,
            "passed": sup_pass,
            "welch_t": sup_t,
        },
        "counts": {
            "independent cases": n_cases,
            "top fifth cases": n_top,
            "bottom fifth cases": n_bot,
        },
        "decided_by": decided,
        "reading": ("The coin's mean 24-bar return is the mean of its grid returns over all windows; "
                    "the top and bottom fifths are the rank-based top and bottom 20% of grid bars by |forecast| within each coin, pooled across coins; "
                    "the supporting check passes when that difference is positive with Welch t >= 2; "
                    "too few cases are reported as not observable."),
    }
