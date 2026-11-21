import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.fall.last_history_value"

    # ---------- 1. Situation check ----------
    # Plan: the situation is a 1-day fall (raw vol-scaled 1-bar return < 0); the outcome is a rise, so the side is long.
    n_active = 0
    n_agree = 0
    rows = []  # (coin, forecast, next-day return) for the criterion
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            ret1 = close / close.shift(1) - 1.0
            # Std of the 30 daily returns before bar t, used only where the raw value is missing.
            vol = ret1.shift(1).rolling(30, min_periods=30).std()
            recomputed = ret1 / vol
            if RAW in df.columns:
                raw = df[RAW].astype(float)
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            fc = df["forecast"].astype(float)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & (raw < 0) & (fc > 0)).sum())

            # Next-day return, inside the window only.
            nxt = close.shift(-1) / close - 1.0
            for f, r in zip(fc.values, nxt.values):
                rows.append((coin, f, r))

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)
    situation_check = {"agreement": agreement, "passed": passed}

    main_name = "pooled OLS slope of next-day excess return on forecast"
    threshold = "slope t >= 2 confirms (with supporting check); t <= -2 rejects; otherwise inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "bars with forecast > 0": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are 1-day falls "
                           "(negative vol-scaled return) taken long, as the plan's Fidelity requires."),
            "reading": ("The situation is read as a negative raw component value (or the recomputed "
                        "return over 30-day std) with a positive forecast."),
        }

    # ---------- 2. Criterion ----------
    data = pd.DataFrame(rows, columns=["coin", "forecast", "ret"])
    data = data.dropna(subset=["forecast", "ret"])

    # The coin's mean daily return over all windows together.
    coin_mean = data.groupby("coin")["ret"].mean()
    data["excess"] = data["ret"] - data["coin"].map(coin_mean)

    x = data["forecast"].values.astype(float)
    y = data["excess"].values.astype(float)
    n = len(x)

    slope = None
    t_slope = None
    if n >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr > 0 else None

    pos = data["forecast"] > 0
    n_pos = int(pos.sum())
    mean_pos = float(data.loc[pos, "excess"].mean()) if n_pos > 0 else None
    sup_pass = bool(mean_pos is not None and mean_pos > 0)

    counts = {"bars with forecast > 0": n_pos, "bars": int(n)}

    if n_pos < 300 or t_slope is None:
        status = "not observable"
        decided = (f"Only {n_pos} bars with forecast > 0, fewer than the plan's minimum of 300."
                   if n_pos < 300 else "The slope's t-statistic could not be computed.")
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean next-day excess return on forecast > 0 bars is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more, but the supporting check failed."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean next-day excess return on bars with forecast > 0",
            "value": mean_pos,
            "passed": sup_pass if n_pos > 0 else None,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The 300-bar minimum is counted on forecast > 0 bars that have a next-day return inside "
                    "their window, and a shortfall is reported as 'not observable' per the workflow; the slope's "
                    "t is the ordinary OLS t over every pooled bar, with the coin mean taken over all its "
                    "windows' 1-bar returns."),
    }
