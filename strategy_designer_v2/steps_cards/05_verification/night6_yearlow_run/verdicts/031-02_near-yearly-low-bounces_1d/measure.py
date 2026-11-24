import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    RAW = "debug_info.components.low_prox.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation (kept): the close's nearness to its 365-day lowest close.
    # The raw proximity 1/(1+D) lies in (0, 1] whenever it is defined.
    # Expected side (Outcome: rises): long, so forecast > 0.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            situ = raw.notna() & np.isfinite(raw) & (raw > 0) & (raw <= 1.0 + 1e-12)
            n_active += int(active.sum())
            n_agree += int((active & situ & (f > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "OLS slope t of excess 20-bar return on forecast, pooled non-overlapping cases"
    threshold = ("confirm: slope > 0 with t >= 2.0 and top-minus-bottom fifth > 0; "
                 "reject: slope < 0 with t <= -2.0; otherwise inconclusive; "
                 "at least 200 cases and 40 in the top fifth")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars where the "
                           "365-day-low proximity is defined with a long forecast, as the Fidelity "
                           "(nearness to the yearly low, a rise) requires."),
            "reading": "none",
        }

    # ---------- 2. Cases on non-overlapping 20-bar grids ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                rows.append({"coin": coin, "window": w,
                             "ret": c1 / c0 - 1.0, "forecast": fc[i]})
    cases = pd.DataFrame(rows, columns=["coin", "window", "ret", "forecast"])

    if len(cases) > 0:
        # Holding the coin: its mean 20-bar return over all its windows (same grid).
        coin_mean = cases.groupby("coin")["ret"].transform("mean")
        cases["excess"] = cases["ret"] - coin_mean
        cases = cases[np.isfinite(cases["forecast"]) & np.isfinite(cases["excess"])]

    n_cases = int(len(cases))

    slope = None
    t_slope = None
    if n_cases >= 3 and cases["forecast"].nunique() > 1:
        lr = stats.linregress(cases["forecast"].to_numpy(), cases["excess"].to_numpy())
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # Supporting check: top fifth minus bottom fifth of the forecast.
    diff = None
    n_top = 0
    n_bot = 0
    if n_cases > 0:
        q80 = float(np.quantile(cases["forecast"], 0.8))
        q20 = float(np.quantile(cases["forecast"], 0.2))
        top = cases[cases["forecast"] >= q80]
        bot = cases[cases["forecast"] <= q20]
        n_top = int(len(top))
        n_bot = int(len(bot))
        if n_top > 0 and n_bot > 0:
            diff = float(top["excess"].mean() - bot["excess"].mean())
    check_passed = None if diff is None else bool(diff > 0)

    counts = {"independent 20-bar cases": n_cases,
              "cases in the top fifth": n_top,
              "cases in the bottom fifth": n_bot}

    reading = ("Fifths are cut at the pooled 20th and 80th percentiles of the cases' forecasts "
               "(top: forecast >= 80th percentile, bottom: <= 20th, ties included), cases are the bars "
               "at positions 0, 20, 40, ... of each window with the 20-bar return inside the window, and "
               "the coin's mean 20-bar return is taken over these grid cases of all its windows.")

    if n_cases < 200 or n_top < 40:
        status = "not observable"
        decided_by = ("The plan's minimum counts (at least 200 independent 20-bar cases, at least 40 "
                      "in the top fifth) are not reached: %d cases, %d in the top fifth." % (n_cases, n_top))
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t_slope >= 2.0 and check_passed:
        status = "confirmed"
        decided_by = "Confirm rule: the slope is positive with t >= 2.0 and the top-minus-bottom difference is above 0."
    elif slope < 0 and t_slope <= -2.0:
        status = "rejected"
        decided_by = "Reject rule: the slope is negative with t <= -2.0."
    elif t_slope >= 2.0:
        status = "inconclusive"
        decided_by = "Inconclusive rule: t >= 2.0 but the top-minus-bottom check fails."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive rule: the slope t is between -2.0 and 2.0."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": t_slope}
                                       if t_slope is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean excess 20-bar return, top fifth minus bottom fifth of forecast",
                             "value": diff, "passed": check_passed},
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
