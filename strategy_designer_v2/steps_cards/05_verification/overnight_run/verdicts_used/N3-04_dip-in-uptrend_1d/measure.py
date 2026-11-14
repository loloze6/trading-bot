import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    DD_COL = "debug_info.components.down_day.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if not active.any():
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            ret1_px = close / close.shift(1) - 1.0
            if DD_COL in df.columns:
                r1 = pd.to_numeric(df[DD_COL], errors="coerce")
                r1 = r1.where(r1.notna(), ret1_px)
            else:
                r1 = ret1_px
            trending = df["regime"].astype(str) == "trending"
            down = r1 < 0
            situ = trending & down & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "mean excess next-bar return (vs coin holding mean) on forecast > 0 bars"
    threshold = "confirm if mean > 0 with t >= 2.0; reject if mean < 0 with t <= -2.0; else inconclusive; at least 200 bars with forecast > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"bars with forecast > 0": None},
            "decided_by": "Fewer than 90% of active bars are trending-regime down days with a long (positive) forecast, as the plan's Fidelity situation requires.",
            "reading": "Uptrend checked on the regime column (detector components are not recorded); down day as a negative 1-day return from the down_day raw value, falling back to the close-to-close return.",
        }

    # ---------- 2. Criterion ----------
    # Holding mean per coin: mean next-bar return over all bars of all windows together
    hold_mean = {}
    per_coin_cases = {}
    for coin, wins in bars.items():
        all_rets = []
        cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            all_rets.append(nxt.dropna().values)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            m = (fc > 0) & nxt.notna()
            if m.any():
                cases.append(pd.DataFrame({"ret": nxt[m].values, "fc": fc[m].values}))
        allr = np.concatenate(all_rets) if all_rets else np.array([])
        hold_mean[coin] = float(np.mean(allr)) if allr.size else np.nan
        per_coin_cases[coin] = pd.concat(cases, ignore_index=True) if cases else None

    ex_list, fc_list = [], []
    for coin, c in per_coin_cases.items():
        if c is None or not np.isfinite(hold_mean[coin]):
            continue
        ex_list.append(c["ret"].values - hold_mean[coin])
        fc_list.append(c["fc"].values)
    excess = np.concatenate(ex_list) if ex_list else np.array([])
    fsize = np.concatenate(fc_list) if fc_list else np.array([])
    n = int(excess.size)

    mean_ex = float(np.mean(excess)) if n > 0 else None
    t_val = None
    if n > 1:
        sd = float(np.std(excess, ddof=1))
        if sd > 0:
            t_val = float(mean_ex / (sd / np.sqrt(n)))

    slope = None
    sup_passed = None
    if n > 2 and np.std(fsize) > 0:
        lr = stats.linregress(fsize, excess)
        slope = float(lr.slope)
        sup_passed = bool(slope > 0)

    if n < 200:
        status = "not observable"
        decided = f"Only {n} bars with forecast > 0 pooled across coins and windows, below the plan's minimum of 200."
    elif t_val is not None and mean_ex > 0 and t_val >= 2.0:
        status = "confirmed"
        decided = "The mean excess next-bar return is positive with t >= 2.0 (confirm rule)."
    elif t_val is not None and mean_ex < 0 and t_val <= -2.0:
        status = "rejected"
        decided = "The mean excess next-bar return is negative with t <= -2.0 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2.0 and 2.0 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t_val} if t_val is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "OLS slope of excess next-bar return on forecast size (positive expected)",
            "value": slope,
            "passed": sup_passed,
        },
        "counts": {"bars with forecast > 0": n},
        "decided_by": decided,
        "reading": "Holding mean is each coin's mean next-bar close-to-close return over every bar of all its windows pooled; cases are forecast > 0 bars with a next bar in the same window; the 200-bar minimum not reached is reported as not observable; uptrend checked on the regime column.",
    }
