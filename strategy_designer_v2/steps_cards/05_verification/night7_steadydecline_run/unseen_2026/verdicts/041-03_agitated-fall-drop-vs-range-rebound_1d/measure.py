import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.scaled_fall.last_history_value"
    PROFILE_REGIME = "unknown"  # the only regime with a strategy: the falling-agitated profile (vetoes send the rest to chop)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    coin_frames = {}
    for coin, wins in bars.items():
        frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            in_profile = d["regime"].astype(str) == PROFILE_REGIME
            prev_close = close.shift(1)
            fall_px = close < prev_close
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                fall = np.where(raw.notna(), raw > 0, fall_px)
            else:
                fall = fall_px.values
            fall = pd.Series(fall, index=d.index).astype(bool)
            active = fc != 0
            situ_ok = active & in_profile & fall & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(situ_ok.sum())
            # next-bar return inside the window only
            d["_ret1"] = close.shift(-1) / close - 1.0
            d["_fc"] = fc
            d["_inprof"] = in_profile
            d["_window"] = w
            frames.append(d)
        if frames:
            coin_frames[coin] = frames

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "forecast-weighted mean next-day excess return (vs coin's all-window mean daily return)"
    threshold = "confirm: mean > 0 with t >= 2 and positive slope; reject: mean < 0 with t <= -2; min 100 cases on 60 distinct days"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("No active bars in the record." if n_active == 0 else
                           "Fewer than 90% of bars with a non-zero forecast are long bars on a one-day fall inside the falling-agitated profile (regime 'unknown')."),
            "reading": "Profile bars are the bars whose recorded regime is the config's only active regime ('unknown'); a fall is a positive raw scaled_fall value (or a lower close than the prior bar where it is not recorded).",
        }

    # ---------- 2. criterion ----------
    cases = []
    for coin, frames in coin_frames.items():
        allr = pd.concat([f["_ret1"] for f in frames]).dropna()
        if len(allr) == 0:
            continue
        mu = float(allr.mean())
        for d in frames:
            sel = (d["_fc"] > 0) & d["_inprof"] & d["_ret1"].notna()
            sub = d.loc[sel]
            for ts, f, r in zip(sub["timestamp"], sub["_fc"], sub["_ret1"]):
                cases.append((ts.floor("D"), float(f), float(r) - mu))

    n_cases = len(cases)
    if n_cases:
        cdf = pd.DataFrame(cases, columns=["day", "f", "x"])
        n_days = int(cdf["day"].nunique())
    else:
        cdf = pd.DataFrame(columns=["day", "f", "x"])
        n_days = 0

    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    mean_w = None
    t = None
    slope = None
    if n_cases > 0:
        sw = cdf["f"].sum()
        mean_w = float((cdf["f"] * cdf["x"]).sum() / sw)
        dev = cdf["f"] * (cdf["x"] - mean_w)
        per_day = dev.groupby(cdf["day"]).sum()
        G = len(per_day)
        if G > 1:
            var = (per_day ** 2).sum() / sw ** 2 * G / (G - 1)
            se = float(np.sqrt(var))
            t = float(mean_w / se) if se > 0 else None
        if n_cases > 2 and cdf["f"].var() > 0:
            fx = cdf["f"] - cdf["f"].mean()
            slope = float((fx * (cdf["x"] - cdf["x"].mean())).sum() / (fx ** 2).sum())

    slope_pass = None if slope is None else bool(slope > 0)

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = f"Minimum not reached: {n_cases} cases (need 100) on {n_days} distinct days (need 60)."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the weighted mean could not be computed."
    elif mean_w > 0 and t >= 2 and slope_pass:
        status = "confirmed"
        decided = "Weighted mean excess next-day return above 0 with t >= 2 and a positive slope on forecast."
    elif mean_w < 0 and t <= -2:
        status = "rejected"
        decided = "Weighted mean excess next-day return below 0 with t <= -2."
    elif mean_w > 0 and t >= 2:
        status = "inconclusive"
        decided = "Confirming mean (t >= 2) but the slope on forecast is not positive."
    else:
        status = "inconclusive"
        decided = "t of the weighted mean lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_w,
            "statistic": None if t is None else {"name": "t of weighted mean, same-day cases summed", "value": t},
            "threshold": threshold,
        },
        "supporting_check": {"name": "OLS slope of next-day excess return on forecast", "value": slope, "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Profile bars are those with recorded regime 'unknown' (the config's only active regime); cases are every in-profile bar with forecast > 0 "
                    "and a next close in the same window; the coin's mean is the mean of all its within-window 1-bar returns; the t uses per-day sums of "
                    "weighted deviations from the weighted mean (cluster-by-day standard error); the slope is ordinary least squares on all cases; "
                    "the plan's minimum counts lead to 'not observable' when unmet."),
    }
