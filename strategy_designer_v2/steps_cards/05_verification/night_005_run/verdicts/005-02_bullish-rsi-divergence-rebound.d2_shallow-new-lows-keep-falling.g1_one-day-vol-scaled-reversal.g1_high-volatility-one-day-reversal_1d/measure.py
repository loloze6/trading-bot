import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FADE = "debug_info.components.fade.last_history_value"

    # ---------- gather per-bar data, window by window ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").astype(float)
            ret_prev = close / close.shift(1) - 1.0     # the day's own move (inside the window)
            ret_next = close.shift(-1) / close - 1.0    # next-bar return (inside the window)
            fc = pd.to_numeric(d["forecast"], errors="coerce").astype(float)
            if "postRebalance_current_allocation" in d.columns:
                pos = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce").astype(float)
            else:
                pos = pd.Series(np.nan, index=d.index)
            if FADE in d.columns:
                fade_raw = pd.to_numeric(d[FADE], errors="coerce").astype(float)
            else:
                fade_raw = pd.Series(np.nan, index=d.index)
            rows.append(pd.DataFrame({
                "coin": coin, "window": w,
                "timestamp": pd.to_datetime(d["timestamp"], utc=True),
                "ret_prev": ret_prev.values, "ret_next": ret_next.values,
                "forecast": fc.values, "pos": pos.values, "fade_raw": fade_raw.values,
            }))
    if not rows:
        return {"status": "not observable",
                "situation_check": {"agreement": None, "passed": False},
                "main_measure": {"name": "pooled slope of next-bar excess return on forecast",
                                 "value": None, "statistic": None,
                                 "threshold": "positive slope with t >= 2 confirms; negative with t <= -2 rejects"},
                "supporting_check": None,
                "counts": {"bars with a non-zero forecast": 0},
                "decided_by": "No bars in the record; at least 1000 bars with a non-zero forecast are needed.",
                "reading": "none"}
    a = pd.concat(rows, ignore_index=True)

    # ---------- situation check ----------
    # Situation: the day's vol-scaled 1-day move (raw fade component; its sign is the day's return sign),
    # recomputed from prices where the raw value is missing. Expected side: against the move.
    move_sign = np.sign(a["fade_raw"])
    miss = move_sign.isna()
    move_sign[miss] = np.sign(a.loc[miss, "ret_prev"])
    active = a["forecast"].notna() & (a["forecast"] != 0)
    n_active = int(active.sum())
    if n_active > 0:
        ok = (move_sign[active].notna()
              & (move_sign[active] != 0)
              & (np.sign(a.loc[active, "forecast"]) == -move_sign[active]))
        agreement = float(ok.sum() / n_active)
    else:
        agreement = None
    passed = agreement is not None and agreement >= 0.90

    main_name = "pooled OLS slope of next-bar coin return less coin mean daily return, on forecast"
    threshold = "confirm: slope > 0 with t >= 2 (and supporting check passes); reject: slope < 0 with t <= -2"
    reading = ("The situation is any bar with a non-zero day's move (sign of the raw fade component, else the price "
               "return) and the expected side is opposite to that move; the regression is OLS with an intercept on "
               "every bar with a next-bar return inside its window; the book's timing gain before costs is the "
               "position held after bar t-1's trade times (coin return on bar t minus the coin's mean daily return "
               "over all windows), averaged across coins each day and then over days.")

    if not passed:
        return {"status": "mismatch",
                "situation_check": {"agreement": agreement, "passed": False},
                "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
                "supporting_check": None,
                "counts": {"bars with a non-zero forecast": n_active},
                "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are against the day's move: the "
                               "config does not fade the vol-scaled 1-day move as the Fidelity states."
                               if agreement is not None else
                               "No bar has a non-zero forecast, so the config never takes the plan's contrarian side."),
                "reading": reading}

    # ---------- coin mean daily return over all windows ----------
    coin_mean = a.dropna(subset=["ret_next"]).groupby("coin")["ret_next"].mean()
    a["coin_mean"] = a["coin"].map(coin_mean)

    # ---------- main measure ----------
    reg = a.dropna(subset=["ret_next", "forecast", "coin_mean"])
    y = (reg["ret_next"] - reg["coin_mean"]).values
    x = reg["forecast"].values
    n_reg = int(len(reg))
    slope, t_val = None, None
    if n_reg >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_val = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- supporting check: book timing gain before costs ----------
    sup = a.dropna(subset=["pos", "ret_next", "coin_mean"]).copy()
    sup["gain"] = sup["pos"] * sup["ret_next"]
    sup["mkt"] = sup["pos"] * sup["coin_mean"]
    # the gain from bar t's close to t+1 belongs to day t+1; grouping by bar t's timestamp gives the same daily pairing
    daily = sup.groupby("timestamp")[["gain", "mkt"]].mean()
    timing = float((daily["gain"] - daily["mkt"]).mean()) if len(daily) else None
    sup_pass = None if timing is None else bool(timing > 0)

    counts = {"bars with a non-zero forecast": n_active,
              "bars in the regression": n_reg,
              "book days": int(len(daily))}

    # ---------- decision ----------
    if n_active < 1000:
        status = "not observable"
        decided = f"Only {n_active} bars with a non-zero forecast, below the plan's minimum of 1000."
    elif slope is None or t_val is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the timing gain before costs is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting timing-gain check failed."
    elif slope < 0 and t_val <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {"status": status,
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": slope,
                             "statistic": None if t_val is None else {"name": "OLS t of slope", "value": t_val},
                             "threshold": threshold},
            "supporting_check": {"name": "book timing gain before costs (mean daily) > 0",
                                 "value": timing, "passed": sup_pass},
            "counts": counts,
            "decided_by": decided,
            "reading": reading}
