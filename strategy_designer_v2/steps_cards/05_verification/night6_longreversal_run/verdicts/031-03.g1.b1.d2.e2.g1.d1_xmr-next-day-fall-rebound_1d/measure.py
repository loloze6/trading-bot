import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.fall_z.last_history_value"
    MIN_CASES = 100

    # Gather every window of XMR (the record's only coin), never joined across windows.
    frames = []
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys(), key=lambda s: int(str(s).lstrip("w") or 0)):
            df = bars[coin][w].copy()
            if "timestamp" in df.columns:
                df = df.sort_values("timestamp")
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            # Next-day return inside the window only.
            df["_next_ret"] = close.shift(-1) / close - 1.0
            # Situation value: the component's raw value, or the price return if missing.
            day_ret = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            df["_sit_val"] = raw.where(raw.notna(), day_ret)
            df["_coin"] = coin
            df["_window"] = w
            frames.append(df)

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "slope of next-day excess return on forecast",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 confirms (with positive mean excess), t <= -2 rejects"},
            "supporting_check": {"name": "mean excess next-day return over cases > 0",
                                 "value": None, "passed": None},
            "counts": {"cases": 0},
            "decided_by": "No bars in the record, so the minimum of 100 cases is not reached.",
            "reading": "none",
        }

    allb = pd.concat(frames, ignore_index=True)
    fc = pd.to_numeric(allb["forecast"], errors="coerce").fillna(0.0)

    # ---- Situation check: a one-day fall (raw value < 0), held long (forecast > 0).
    active = fc != 0
    n_active = int(active.sum())
    sit = allb["_sit_val"] < 0
    agree_mask = active & sit & (fc > 0)
    agreement = float(agree_mask.sum() / n_active) if n_active > 0 else 1.0
    passed = agreement >= 0.9

    reading = ("The situation is a bar whose raw fall_z value (return over 30-day volatility) is below 0, "
               "falling back to the price return where the raw value is missing; the coin's mean daily return "
               "is the mean of all next-day returns pooled over all windows; with a 1-bar horizon every bar is "
               "on the grid; the slope's t is the ordinary least-squares t of the slope; fewer than 100 cases "
               "is reported as 'not observable' as the workflow requires.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "slope of next-day excess return on forecast",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 confirms (with positive mean excess), t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"cases": None, "active_bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bets on a one-day "
                           "fall of XMR, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---- Main measure.
    coin_mean = float(allb["_next_ret"].dropna().mean())
    cases = allb[(fc > 0) & allb["_next_ret"].notna()].copy()
    cases["_fc"] = fc[cases.index]
    cases["_excess"] = cases["_next_ret"] - coin_mean
    n_cases = int(len(cases))

    slope = None
    t_slope = None
    mean_excess = None
    if n_cases >= 1:
        mean_excess = float(cases["_excess"].mean())
    if n_cases >= 3 and cases["_fc"].nunique() > 1:
        lr = stats.linregress(cases["_fc"].values, cases["_excess"].values)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    support_pass = None if mean_excess is None else bool(mean_excess > 0)

    main = {
        "name": "slope of next-day excess return on forecast",
        "value": slope,
        "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
        "threshold": "slope t >= 2 with positive mean excess confirms; slope t <= -2 rejects",
    }
    support = {"name": "mean excess next-day return over cases > 0",
               "value": mean_excess, "passed": support_pass}
    counts = {"cases": n_cases}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, below the plan's minimum of 100 cases."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and support_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess return over the cases is positive."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger falls are followed by smaller rebounds or further falls."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the mean excess return over the cases is not positive."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
