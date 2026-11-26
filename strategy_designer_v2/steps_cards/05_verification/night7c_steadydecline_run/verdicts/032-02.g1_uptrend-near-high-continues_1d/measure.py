import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    LOOK = 28
    FC = "forecast"
    RAW = "debug_info.components.high_prox.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin], key=lambda s: int(str(s).lstrip("w") or 0)):
            df = bars[coin][w].reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0)
            rise = close / close.shift(LOOK) - 1.0
            reg_tr = df["regime"].astype(str) == "trending"
            # where 28 past closes are in the window, recompute rise28 from prices;
            # earlier bars fall back on the detector's recorded decision
            situ = np.where(rise.notna(), rise > 0, reg_tr)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                prox_ok = (raw > 0).fillna(False).to_numpy()
            else:
                prox_ok = np.zeros(len(df), dtype=bool)
            active = (fc != 0).to_numpy()
            good = active & situ.astype(bool) & prox_ok & (fc > 0).to_numpy()
            n_active += int(active.sum())
            n_agree += int(good.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope t of 5-bar forward excess return on forecast, in-regime non-overlapping grid"
    thr = "confirm: slope t >= 2 and supporting check passes; reject: slope t <= -2"
    sup_name = "top third minus bottom third of forecast, mean 5-bar excess return, Welch t > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "in-regime grid cases": None},
            "decided_by": "Fewer than 90% of active (non-zero forecast) bars are long bars where the 28-day return is above 0 with a positive high proximity, as the plan's Fidelity requires.",
            "reading": "rise28 recomputed as close[t]/close[t-28]-1 inside each window, with the recorded regime used on the first 28 bars of a window where it cannot be recomputed.",
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_rets = {}
    for coin in sorted(bars):
        allr = []
        for w in sorted(bars[coin], key=lambda s: int(str(s).lstrip("w") or 0)):
            df = bars[coin][w].reset_index(drop=True)
            close = df["close"].astype(float).to_numpy()
            n = len(df)
            fc = pd.to_numeric(df[FC], errors="coerce").to_numpy()
            reg = df["regime"].astype(str).to_numpy()
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                allr.append(r)
                if reg[i] == "trending" and np.isfinite(fc[i]):
                    rows.append((coin, float(fc[i]), float(r)))
        coin_rets[coin] = float(np.mean(allr)) if len(allr) else np.nan

    cases = pd.DataFrame(rows, columns=["coin", "fc", "r"])
    if len(cases):
        cases["ex"] = cases["r"] - cases["coin"].map(coin_rets)
        cases = cases.dropna(subset=["fc", "ex"])
    n_cases = int(len(cases))
    counts = {"in-regime grid cases": n_cases}
    reading = ("Grid = positions 0,5,10,... of each window with a 5-bar return inside the window; in-regime = recorded regime 'trending'; "
               "coin mean = mean of that coin's grid 5-bar returns over all windows; thirds = the n//3 lowest and n//3 highest forecasts by stable rank; "
               "the plan's 150-case minimum is applied as 'not observable'.")

    if n_cases < 150:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": "Fewer than 150 in-regime grid cases, the plan's minimum.",
            "reading": reading,
        }

    x = cases["fc"].to_numpy()
    y = cases["ex"].to_numpy()
    if np.std(x) == 0:
        slope, t_slope = None, None
    else:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    order = np.argsort(x, kind="mergesort")
    k = n_cases // 3
    bot = y[order[:k]]
    top = y[order[n_cases - k:]]
    if k >= 2:
        wt = stats.ttest_ind(top, bot, equal_var=False)
        sup_t = float(wt.statistic) if np.isfinite(wt.statistic) else None
    else:
        sup_t = None
    sup_pass = bool(sup_t is not None and sup_t > 0)
    counts["top third cases"] = int(k)
    counts["bottom third cases"] = int(k)

    if t_slope is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "Slope t is 2 or more and the top-minus-bottom-third Welch t is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Slope t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "Slope t is 2 or more but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "Slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": sup_t, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
