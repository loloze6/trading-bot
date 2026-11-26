import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.scaled_day_move.last_history_value"
    MIN_CASES = 100

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(d["close"], errors="coerce")
            day_ret = close / close.shift(1) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                move = raw.where(raw.notna(), day_ret)
            else:
                move = day_ret
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            in_profile = regime == "unknown"
            active = fc != 0
            exp_side = np.sign(move)
            agree = active & in_profile & (exp_side != 0) & (np.sign(fc) == exp_side)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of 5-bar forward excess return on forecast (pooled, non-overlapping grid, forecast != 0)"
    thr = "confirm: slope > 0 with t >= 2 and supporting check > 0; reject: slope < 0 with t <= -2"
    sup_name = "mean of sign(forecast) x excess 5-bar return on grid bars with |forecast| >= 10"
    reading = ("The plan's choppy calm profile is taken as the bars whose regime is 'unknown' (the detector's non-chop regime) "
               "and the expected side as the sign of the day's scaled move (raw component, else the close-to-close return); "
               "the coin's mean 5-bar return is the mean over all non-overlapping grid returns of all its windows; "
               "the slope is an OLS with intercept; the plan's minimum of 100 grid cases is applied as 'not observable'.")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": {"grid cases with a non-zero forecast": 0},
            "decided_by": "No bar has a non-zero forecast, so the minimum of 100 grid cases with a non-zero forecast is not reached.",
            "reading": reading,
        }

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on expected side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are choppy-calm-profile bars whose forecast "
                           "sign follows the day's move, as the Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                coin_rows.append((coin, c1 / c0 - 1.0, fc[i]))
        if not coin_rows:
            continue
        cdf = pd.DataFrame(coin_rows, columns=["coin", "fwd", "fc"])
        mu = cdf["fwd"].mean()
        cdf["excess"] = cdf["fwd"] - mu
        rows.append(cdf)

    if rows:
        g = pd.concat(rows, ignore_index=True)
        g = g[np.isfinite(g["fc"]) & np.isfinite(g["excess"])]
    else:
        g = pd.DataFrame(columns=["coin", "fwd", "fc", "excess"])

    cases = g[g["fc"] != 0]
    n_cases = int(len(cases))
    strong = cases[cases["fc"].abs() >= 10]
    n_strong = int(len(strong))

    slope = None
    t = None
    if n_cases >= 3 and cases["fc"].nunique() > 1:
        lr = stats.linregress(cases["fc"].values.astype(float), cases["excess"].values.astype(float))
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_val = None
    if n_strong > 0:
        sup_val = float((np.sign(strong["fc"]) * strong["excess"]).mean())
    sup_pass = bool(sup_val is not None and sup_val > 0)

    counts = {
        "grid cases with a non-zero forecast": n_cases,
        "grid cases with |forecast| >= 10": n_strong,
    }
    stat = {"name": "OLS slope t", "value": t} if t is not None else None

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} grid cases with a non-zero forecast, fewer than the plan's minimum of 100."
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the supporting check is above 0 (confirm rule)."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 (reject rule)."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the supporting check is not above 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The slope's |t| is below 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": slope, "statistic": stat, "threshold": thr},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass if sup_val is not None else False},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
