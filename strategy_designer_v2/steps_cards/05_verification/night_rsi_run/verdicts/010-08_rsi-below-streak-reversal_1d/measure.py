import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 14
    RAW = "debug_info.components.below_age.last_history_value"
    MIN_CASES = 100

    # ---------- 1. Situation check ----------
    # Situation (Fidelity): RSI(14) has stayed below 50 without a break, i.e. the component's
    # signed run length is negative (a run below 50). Expected side: long (outcome is a higher return).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            situ = raw.notna() & (raw < 0)
            n_agree += int((active & situ & (fc > 0)).sum())

    if n_active == 0:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": 0},
            "decided_by": "The forecast is never non-zero, so the config never takes the long position the plan's situation (a run of RSI(14) below 50) calls for.",
            "reading": "Situation taken as the component's raw signed run length below zero (a run below 50), expected side long.",
        }

    agreement = n_agree / n_active
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": f"Only {agreement:.1%} of the bars with a non-zero forecast are long bars inside a run of RSI(14) below 50 (raw run length < 0), below the 90% required.",
            "reading": "Situation taken as the component's raw signed run length below zero (a run below 50), expected side long.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
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
                rows.append((coin, w, fc[i], c1 / c0 - 1.0))
    g = pd.DataFrame(rows, columns=["coin", "window", "forecast", "ret"])

    if len(g) > 0:
        coin_mean = g.groupby("coin")["ret"].mean()
        g["excess"] = g["ret"] - g["coin"].map(coin_mean)
    else:
        g["excess"] = []

    s = g[g["forecast"].notna() & (g["forecast"] > 0) & g["excess"].notna()].copy()
    n_cases = int(len(s))

    reading = ("Situation taken as the component's raw signed run length below zero, expected side long; "
               "each coin's mean 14-bar return is the mean over the same non-overlapping 14-bar grid of all its windows, "
               "the slope's t is the OLS t of excess return on forecast, and the thirds are the n//3 lowest and n//3 highest "
               "forecasts after a stable sort.")

    main = {"name": "OLS slope of excess next-14-bar return on forecast (grid bars, forecast > 0)",
            "value": None,
            "statistic": None,
            "threshold": "slope t >= +2 to confirm (with top-minus-bottom third > 0), t <= -2 to reject"}
    supp = {"name": "top-third minus bottom-third mean excess 14-bar return", "value": None, "passed": None}
    counts = {"independent grid bars with forecast > 0": n_cases}

    if n_cases < MIN_CASES:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": main,
            "supporting_check": supp,
            "counts": counts,
            "decided_by": f"Only {n_cases} independent grid bars with forecast > 0, fewer than the 100 the plan requires.",
            "reading": reading,
        }

    x = s["forecast"].values.astype(float)
    y = s["excess"].values.astype(float)
    if np.allclose(x, x[0]):
        slope, t_slope = float("nan"), float("nan")
    else:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else float("nan")

    order = np.argsort(x, kind="mergesort")
    k = n_cases // 3
    bottom = y[order[:k]]
    top = y[order[-k:]]
    diff = float(np.mean(top) - np.mean(bottom)) if k > 0 else float("nan")
    supp_pass = bool(np.isfinite(diff) and diff > 0)

    main["value"] = slope if np.isfinite(slope) else None
    main["statistic"] = {"name": "OLS t of slope", "value": t_slope if np.isfinite(t_slope) else None}
    supp["value"] = diff if np.isfinite(diff) else None
    supp["passed"] = supp_pass

    if np.isfinite(t_slope) and t_slope >= 2 and supp_pass:
        status = "confirmed"
        decided = f"The slope's t is {t_slope:.2f} (>= +2) and the top-minus-bottom-third difference is positive ({diff:.4f})."
    elif np.isfinite(t_slope) and t_slope <= -2:
        status = "rejected"
        decided = f"The slope's t is {t_slope:.2f}, -2 or less."
    elif np.isfinite(t_slope) and t_slope >= 2:
        status = "inconclusive"
        decided = f"The slope's t is {t_slope:.2f} (>= +2) but the top-minus-bottom-third difference is not positive."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and +2 (or undefined), so neither the confirm nor the reject rule is met."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
