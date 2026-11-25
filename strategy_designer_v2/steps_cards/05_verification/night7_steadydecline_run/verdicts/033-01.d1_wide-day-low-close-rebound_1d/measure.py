import numpy as np
import pandas as pd


def measure(bars):
    COMP = "debug_info.components.low_close_wide_day"
    RAW = COMP + ".last_history_value"
    POST = COMP + ".post_pipeline_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            high = df["high"].astype(float)
            low = df["low"].astype(float)
            close = df["close"].astype(float)
            rng = high - low
            # recomputation from prices (prior 20 bars, current excluded), used where the raw value is missing
            base = rng.shift(1).rolling(20, min_periods=20).mean()
            recomputed = (high - close) / base.replace(0, np.nan)
            if RAW in df.columns:
                raw = df[RAW].astype(float)
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            fc = df["forecast"].astype(float).fillna(0.0)
            active = fc != 0
            # situation: close below the day's high (the graded nearness-to-low x range multiple is positive), side long
            situation = (raw > 0) & (high > close)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "OLS slope of next-day excess return on post_pipeline_value"
    thr = "confirm: slope > 0 with day-clustered t >= 2 (and top-fifth mean excess > 0); reject: slope < 0 with t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "agreeing bars": n_agree},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars with the close below the day's high (positive raw low-close x wide-day value), as the plan's situation and long side require.",
            "reading": "The situation is taken as a positive raw component value (close below the high), on the long side, on every bar where forecast is non-zero.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            ret = close.shift(-1) / close - 1.0  # inside the window only
            post = df[POST].astype(float) if POST in df.columns else pd.Series(np.nan, index=df.index)
            d = pd.DataFrame({
                "coin": coin,
                "day": pd.to_datetime(df["timestamp"], utc=True).dt.floor("D"),
                "ret": ret,
                "x": post,
                "fc": df["forecast"].astype(float),
            })
            coin_rows.append(d)
        if not coin_rows:
            continue
        cd = pd.concat(coin_rows, ignore_index=True)
        coin_mean = cd["ret"].dropna().mean()  # mean daily return over all windows
        cd["ex"] = cd["ret"] - coin_mean
        # top fifth of forecast per coin (over all its windows)
        fcv = cd.loc[cd["ex"].notna() & cd["fc"].notna(), "fc"]
        q80 = fcv.quantile(0.8) if len(fcv) else np.nan
        cd["top"] = cd["fc"] >= q80 if np.isfinite(q80) else False
        rows.append(cd)

    data = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(columns=["coin", "day", "ret", "x", "fc", "ex", "top"])
    reg = data.dropna(subset=["ex", "x"])
    n_bars = int(len(reg))
    n_days = int(reg["day"].nunique()) if n_bars else 0

    slope = None
    tval = None
    if n_bars >= 3:
        x = reg["x"].values.astype(float)
        y = reg["ex"].values.astype(float)
        xc = x - x.mean()
        sxx = float(np.sum(xc ** 2))
        if sxx > 0:
            b = float(np.sum(xc * (y - y.mean())) / sxx)
            a = y.mean() - b * x.mean()
            e = y - a - b * x
            score = pd.Series(xc * e).groupby(reg["day"].values).sum().values
            se = float(np.sqrt(np.sum(score ** 2)) / sxx)
            slope = b
            tval = float(b / se) if se > 0 else None

    top = data[(data["top"] == True) & data["ex"].notna()]
    top_mean = float(top["ex"].mean()) if len(top) else None
    sup_pass = (top_mean is not None and top_mean > 0) if top_mean is not None else None

    counts = {"bars": n_bars, "distinct days": n_days, "top-fifth bars": int(len(top))}

    if n_bars < 1000 or n_days < 300:
        status = "not observable"
        decided = f"The plan's minimum of 1000 bars and 300 distinct days is not reached ({n_bars} bars, {n_days} days)."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed (no variation of post_pipeline_value or zero standard error)."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the top-fifth mean excess return is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the top-fifth mean excess return is <= 0."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's |t| is below 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "t with cases summed per day (day-clustered OLS t)", "value": tval} if tval is not None else None,
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean next-day excess return on bars in the per-coin top fifth of forecast",
            "value": top_mean,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "Every bar with a next close in its window and a post_pipeline_value is a case, the coin's mean is its mean 1-bar return over all windows, the t uses OLS score sums per UTC day without small-sample correction, the top fifth is forecast >= the coin's 80th percentile over all its windows, and missing minimum counts give 'not observable' rather than the plan's 'inconclusive'.",
    }
