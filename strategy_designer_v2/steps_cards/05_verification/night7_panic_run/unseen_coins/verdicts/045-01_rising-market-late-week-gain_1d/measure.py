import numpy as np
import pandas as pd
from scipy import stats


def _ts(s):
    if np.issubdtype(s.dtype, np.number):
        v = float(np.nanmedian(s.values)) if len(s) else 0.0
        unit = "s" if v < 1e11 else ("ms" if v < 1e14 else ("us" if v < 1e17 else "ns"))
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    RAW = "debug_info.components.trend60.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    frames = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            d["ts"] = _ts(d["timestamp"])
            d = d.sort_values("ts").reset_index(drop=True)
            close = d["close"].astype(float)
            d["ret_next"] = close.shift(-1) / close - 1.0
            # 60-bar return from prices, inside the window only (for bars where trend60 is not recorded)
            d["ret60_px"] = close / close.shift(60) - 1.0
            raw = d[RAW].astype(float) if RAW in d.columns else pd.Series(np.nan, index=d.index)
            d["trend_raw"] = raw.where(raw.notna(), d["ret60_px"])
            d["coin"] = coin
            d["window"] = w
            frames.append(d)

    if not frames:
        return {"status": "not observable",
                "situation_check": {"agreement": None, "passed": False},
                "main_measure": {"name": "mean excess position gain (position x (next-day return - coin mean daily return)), days summed across coins",
                                 "value": None, "statistic": None, "threshold": "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2"},
                "supporting_check": None,
                "counts": {"distinct days with a position": 0},
                "decided_by": "No bars in the record: fewer than 100 distinct days with a position.",
                "reading": "none"}

    all_bars = pd.concat(frames, ignore_index=True)

    # ---- Situation check ----
    next_wd = (all_bars["ts"] + pd.Timedelta(days=1)).dt.weekday  # weekday of the coming bar
    late_week = next_wd.isin([4, 5])
    rising = all_bars["trend_raw"] > 0
    situation = late_week & rising.fillna(False)
    fc = all_bars["forecast"].astype(float)
    active = fc.notna() & (fc != 0)
    n_active = int(active.sum())
    if n_active > 0:
        agree = float((situation & (fc > 0))[active].mean())
    else:
        agree = None
    passed = (agree is not None) and (agree >= 0.90)

    main_name = "mean excess position gain: position x (next-day return - coin's mean daily return), cases of a day summed across coins"
    threshold = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; else inconclusive; at least 100 distinct days with a position"
    reading = ("Situation = coming bar (timestamp + 1 day) is a Friday or Saturday and the 60-bar return (trend60 raw value, or "
               "recomputed from closes where not recorded) is above 0, side long; 'bars with a position' = bars with a non-zero "
               "post-rebalance allocation and a next close in the same window; the coin's mean daily return is the mean of all its "
               "next-day returns over all windows; the slope is an OLS of the excess next-day return on the forecast on those bars.")

    if not passed:
        return {"status": "mismatch",
                "situation_check": {"agreement": agree, "passed": False},
                "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
                "supporting_check": None,
                "counts": {"active bars": n_active},
                "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the coming bar is a Friday "
                               "or Saturday in a rising market (60-bar return > 0)." if n_active > 0 else
                               "No bar has a non-zero forecast, so the config never takes the plan's situation."),
                "reading": reading}

    # ---- Criterion ----
    coin_mean = all_bars.dropna(subset=["ret_next"]).groupby("coin")["ret_next"].mean()
    all_bars["coin_mu"] = all_bars["coin"].map(coin_mean)
    alloc = all_bars[ALLOC].astype(float)
    pos = alloc.notna() & (alloc != 0) & all_bars["ret_next"].notna()
    sel = all_bars[pos].copy()
    sel["alloc"] = alloc[pos]
    sel["excess"] = sel["ret_next"] - sel["coin_mu"]
    sel["gain"] = sel["alloc"] * sel["excess"]
    sel["day"] = sel["ts"].dt.floor("D")

    daily = sel.groupby("day")["gain"].sum()
    n_days = int(len(daily))
    n_cases = int(len(sel))

    mean_gain = float(daily.mean()) if n_days > 0 else None
    t_val = None
    if n_days > 1:
        sd = float(daily.std(ddof=1))
        t_val = float(mean_gain / (sd / np.sqrt(n_days))) if sd > 0 else None

    slope = None
    s2 = sel.dropna(subset=["forecast", "excess"])
    if len(s2) > 2 and s2["forecast"].astype(float).nunique() > 1:
        slope = float(stats.linregress(s2["forecast"].astype(float), s2["excess"].astype(float)).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    counts = {"distinct days with a position": n_days, "bars with a position": n_cases}
    main = {"name": main_name, "value": mean_gain,
            "statistic": {"name": "t of the mean (daily sums)", "value": t_val} if t_val is not None else None,
            "threshold": threshold}
    supp = {"name": "OLS slope of excess next-day return on forecast", "value": slope, "passed": slope_pass}

    if n_days < 100:
        status = "not observable"
        decided = f"Only {n_days} distinct days with a position, below the plan's minimum of 100."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean excess gain cannot be computed, so neither the confirm nor the reject rule is met."
    elif mean_gain > 0 and t_val >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "The mean excess position gain is above 0 with t >= 2 and the slope on the forecast is above 0."
        else:
            status = "inconclusive"
            decided = "The mean excess position gain is significantly positive but the slope is at or below 0 (or unavailable)."
    elif mean_gain < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean excess position gain is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess position gain lies between -2 and 2."

    return {"status": status,
            "situation_check": {"agreement": agree, "passed": True},
            "main_measure": main,
            "supporting_check": supp,
            "counts": counts,
            "decided_by": decided,
            "reading": reading}
