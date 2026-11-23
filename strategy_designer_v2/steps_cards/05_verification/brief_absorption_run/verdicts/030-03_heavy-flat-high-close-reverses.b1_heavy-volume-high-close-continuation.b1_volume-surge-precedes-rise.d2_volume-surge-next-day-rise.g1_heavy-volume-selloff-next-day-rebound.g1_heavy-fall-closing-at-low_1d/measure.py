import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"

    # ---------- collect per-bar data, strictly inside each window ----------
    frames = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            if "timestamp" in d.columns:
                d = d.sort_values("timestamp", kind="mergesort")
            d = d.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            prev_close = close.shift(1)
            next_close = close.shift(-1)
            out = pd.DataFrame({
                "coin": coin,
                "window": w,
                "forecast": pd.to_numeric(d[FC], errors="coerce"),
                "close": close,
                "prev_close": prev_close,
                "ret_next": next_close / close - 1.0,
            })
            # down day from prices: today's close below yesterday's close (same window only)
            out["down"] = (close < prev_close) & prev_close.notna() & close.notna()
            frames.append(out)

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "t of slope of next-day excess return on forecast, down days with forecast > 0",
                             "value": None, "statistic": None, "threshold": "t >= 2 confirms, t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"down-day bars with a forecast above 0": 0},
            "decided_by": "No bars in the record.",
            "reading": "none",
        }

    allb = pd.concat(frames, ignore_index=True)

    # ---------- situation check ----------
    active = allb[allb["forecast"].notna() & (allb["forecast"] != 0)]
    n_active = int(len(active))
    if n_active > 0:
        agree = int(((active["down"]) & (active["forecast"] > 0)).sum())
        agreement = agree / n_active
    else:
        agreement = 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    reading = ("Down day = close below the previous close within the same window (a window's first bar has no prior close "
               "and is not a down day); the regression pools every down-day bar with forecast > 0 and a next close in its "
               "window across all coins and windows, OLS slope t = slope / its standard error; the coin's mean daily return "
               "is the mean of all its in-window 1-day returns; the top fifth is the ceil(20 %) highest-forecast down-day bars "
               "(any forecast, ties by record order) pooled across coins; the plan's 200-case minimum gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "t of slope of next-day excess return on forecast, down days with forecast > 0",
                             "value": None, "statistic": None, "threshold": "t >= 2 confirms, t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90 % of the bars with a nonzero forecast are down days (close below the prior close) "
                           "with a long forecast, as the plan's situation and side require."),
            "reading": reading,
        }

    # ---------- excess returns ----------
    valid_ret = allb[allb["ret_next"].notna()]
    coin_mean = valid_ret.groupby("coin")["ret_next"].mean()
    allb["excess"] = allb["ret_next"] - allb["coin"].map(coin_mean)

    down = allb[allb["down"] & allb["excess"].notna() & allb["forecast"].notna()]
    reg = down[down["forecast"] > 0]
    n_reg = int(len(reg))

    # supporting check: top fifth of down-day bars by forecast
    n_down = int(len(down))
    top_mean = None
    n_top = 0
    if n_down > 0:
        n_top = int(np.ceil(n_down / 5.0))
        srt = down.sort_values("forecast", ascending=False, kind="mergesort")
        top_mean = float(srt["excess"].iloc[:n_top].mean())

    slope = None
    t_val = None
    if n_reg >= 3 and reg["forecast"].nunique() > 1:
        lr = stats.linregress(reg["forecast"].values.astype(float), reg["excess"].values.astype(float))
        slope = float(lr.slope)
        t_val = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    counts = {
        "down-day bars with a forecast above 0": n_reg,
        "down-day bars": n_down,
        "top-fifth down-day bars": n_top,
    }

    support_pass = None if top_mean is None else bool(top_mean > 0)
    main = {
        "name": "t of slope of next-day excess return on forecast, down days with forecast > 0",
        "value": t_val,
        "statistic": {"name": "OLS slope t", "value": t_val} if t_val is not None else None,
        "threshold": "t >= 2 (with top-fifth mean > 0) confirms; t <= -2 rejects; otherwise inconclusive",
    }
    main["slope"] = slope
    supporting = {"name": "top-fifth down-day mean next-day excess return",
                  "value": top_mean, "passed": support_pass}

    if n_reg < 200:
        status = "not observable"
        decided = (f"Only {n_reg} down-day bars with a forecast above 0, below the plan's minimum of 200 "
                   "across all coins and windows.")
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast)."
    elif t_val >= 2 and support_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the top-fifth mean excess return is above 0 (confirm rule)."
    elif t_val <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less (reject rule)."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the top-fifth mean excess return is at or below 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
