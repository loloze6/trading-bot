import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.low_close.last_history_value"
    PROFILE = "unknown"  # the only regime with a strategy; the vetoes send everything else to "chop"

    def raw_from_prices(df):
        rng = (df["high"] - df["low"]).astype(float)
        val = (df["high"] - df["close"]).astype(float) / rng
        return val.where(rng > 0)

    # ---------- collect per-bar rows ----------
    rows = []
    for coin, wins in bars.items():
        frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            d["ret1"] = close.shift(-1) / close - 1.0  # inside the window only
            raw_rec = d[RAW].astype(float) if RAW in d.columns else pd.Series(np.nan, index=d.index)
            d["x"] = raw_rec.where(raw_rec.notna(), raw_from_prices(d))
            d["coin"] = coin
            d["window"] = w
            frames.append(d[["timestamp", "coin", "window", "forecast", "regime", "x", "ret1"]])
        if not frames:
            continue
        cdf = pd.concat(frames, ignore_index=True)
        coin_mean = cdf["ret1"].dropna().mean()  # the coin's mean daily return over all windows
        cdf["excess"] = cdf["ret1"] - coin_mean
        rows.append(cdf)

    reading = ("The falling agitated profile is read as the bars whose recorded regime is 'unknown' "
               "(the only regime with a strategy, the vetoes sending every other bar to 'chop'), the situation "
               "as an in-profile bar whose close sits below the day's high (raw value > 0) on the long side, "
               "the coin's mean daily return over all its windows' bars, every bar as a 1-bar case, and the "
               "slope's t as an OLS slope with day-clustered (per-day summed) standard error.")

    if not rows:
        return {"status": "not observable",
                "situation_check": {"agreement": None, "passed": False},
                "main_measure": {"name": "slope of next-day excess return on low_close raw value",
                                 "value": None, "statistic": None,
                                 "threshold": "slope t >= +2 confirms (with bottom-fifth mean > 0), <= -2 rejects"},
                "supporting_check": None,
                "counts": {"in-profile bars": 0, "bottom-fifth bars": 0},
                "decided_by": "No bars in the record.", "reading": reading}

    all_df = pd.concat(rows, ignore_index=True)
    fc = all_df["forecast"].astype(float).fillna(0.0)
    in_prof = all_df["regime"].astype(str) == PROFILE

    # ---------- situation check ----------
    active = fc != 0
    n_active = int(active.sum())
    situ = in_prof & (all_df["x"] > 0) & (fc > 0)
    agreement = float((active & situ).sum() / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "slope of next-day excess return on low_close raw value (in-profile)"
    threshold = "slope t >= +2 with bottom-fifth mean > 0 confirms; slope t <= -2 rejects"

    if not passed:
        return {"status": "mismatch",
                "situation_check": {"agreement": agreement, "passed": False},
                "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
                "supporting_check": None,
                "counts": {"active bars": n_active},
                "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are in-profile bars with a close "
                               "below the day's high on the long side, as the Fidelity's situation and side require"
                               if n_active > 0 else "The record has no bar with a non-zero forecast."),
                "reading": reading}

    # ---------- main measure ----------
    s = all_df[in_prof].dropna(subset=["x", "excess"]).copy()
    s["day"] = s["timestamp"].dt.floor("D")
    n = len(s)
    bottom = s[s["x"] >= 0.8]
    n_bottom = len(bottom)
    n_days = int(s["day"].nunique()) if n else 0

    slope, t_slope = None, None
    if n >= 3:
        x = s["x"].to_numpy(float)
        y = s["excess"].to_numpy(float)
        xm = x.mean()
        sxx = float(((x - xm) ** 2).sum())
        if sxx > 0:
            b = float(((x - xm) * (y - y.mean())).sum() / sxx)
            a = y.mean() - b * xm
            e = y - a - b * x
            score = pd.Series((x - xm) * e).groupby(s["day"].to_numpy()).sum().to_numpy()
            G = len(score)
            if G > 1:
                corr = (G / (G - 1.0)) * ((n - 1.0) / (n - 2.0))
                var_b = corr * float((score ** 2).sum()) / sxx ** 2
                slope = b
                t_slope = float(b / np.sqrt(var_b)) if var_b > 0 else None

    bottom_mean = float(bottom["excess"].mean()) if n_bottom > 0 else None
    sup_pass = None if bottom_mean is None else bool(bottom_mean > 0)

    counts = {"in-profile bars": int(n), "bottom-fifth bars": int(n_bottom),
              "days (in-profile)": n_days, "active bars": n_active}

    if n < 100 or n_bottom < 20:
        status = "not observable"
        decided_by = (f"The plan's minimum counts are not reached: {n} in-profile bars (needs 100) and "
                      f"{n_bottom} in the bottom fifth (needs 20).")
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided_by = "The slope's t is +2 or more and the bottom-fifth mean next-day excess return is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "The slope's t is -2 or less: lower closes are followed by smaller next-day returns."
    elif t_slope >= 2:
        status = "inconclusive"
        decided_by = "The slope's t is +2 or more but the bottom-fifth mean is at or below 0."
    else:
        status = "inconclusive"
        decided_by = "The slope's t is between -2 and +2."

    return {"status": status,
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name,
                             "value": slope,
                             "statistic": None if t_slope is None else {"name": "slope t (day-clustered)",
                                                                       "value": t_slope},
                             "threshold": threshold},
            "supporting_check": {"name": "mean next-day excess return, in-profile bars with raw >= 0.8",
                                 "value": bottom_mean, "passed": sup_pass},
            "counts": counts,
            "decided_by": decided_by,
            "reading": reading}
