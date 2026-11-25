import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.low_close_wide_day.last_history_value"
    PPV = "debug_info.components.low_close_wide_day.post_pipeline_value"
    MIN_CASES = 300
    MIN_DAYS = 150

    def to_dt(s):
        if pd.api.types.is_numeric_dtype(s):
            v = pd.to_numeric(s, errors="coerce")
            mx = np.nanmax(np.abs(v.values)) if len(v) else 0
            unit = "ms" if mx > 1e11 else "s"
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True, errors="coerce")

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    frames = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fwd = close.shift(-1) / close - 1.0  # inside the window only
            coin_rets.append(fwd.dropna().values)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            ppv = pd.to_numeric(d[PPV], errors="coerce") if PPV in d.columns else pd.Series(np.nan, index=d.index)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)
            active = fc != 0
            # situation: agitated profile (regime not vetoed to chop), close below the day's high (raw > 0), long side
            situ = (regime != "chop") & (raw > 0) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
            ts = to_dt(d["timestamp"])
            coin_rows.append(pd.DataFrame({
                "coin": coin,
                "day": ts.dt.strftime("%Y-%m-%d"),
                "fwd": fwd,
                "x": ppv,
                "active": active,
            }))
        if coin_rows:
            allr = np.concatenate(coin_rets) if coin_rets else np.array([])
            mu = float(np.mean(allr)) if len(allr) else np.nan
            cdf = pd.concat(coin_rows, ignore_index=True)
            cdf["y"] = cdf["fwd"] - mu
            frames.append(cdf)

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "pooled OLS slope of next-day demeaned return on forecast (post_pipeline_value)"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 300 cases over at least 150 distinct days"
    reading = ("Situation bars are non-chop regime bars with a positive raw close-below-high value and a positive forecast; "
               "the regression has an intercept, and its t uses a day-clustered standard error (residual x centred forecast "
               "summed per UTC day) with the G/(G-1) correction, on every bar since the 1-bar grid is every bar.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": None, "distinct days": None},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are long bars in the agitated profile "
                           "with the close below the day's high, as the plan's situation requires."
                           if agreement is not None else "No bar has a nonzero forecast."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    data = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=["y", "x", "active", "day"])
    data = data[data["active"].astype(bool)]
    data = data.dropna(subset=["y", "x", "day"])
    n = int(len(data))
    n_days = int(data["day"].nunique()) if n else 0
    counts = {"cases": n, "distinct days": n_days}

    slope = None
    tval = None
    if n >= 3:
        x = data["x"].values.astype(float)
        y = data["y"].values.astype(float)
        xc = x - x.mean()
        sxx = float(np.sum(xc ** 2))
        if sxx > 0:
            b = float(np.sum(xc * (y - y.mean())) / sxx)
            a = float(y.mean() - b * x.mean())
            e = y - a - b * x
            sc = pd.Series(xc * e).groupby(data["day"].values).sum().values
            G = len(sc)
            var = float(np.sum(sc ** 2)) / sxx ** 2
            if G > 1:
                var *= G / (G - 1.0)
            se = np.sqrt(var)
            slope = b
            tval = float(b / se) if se > 0 else None

    main = {"name": main_name,
            "value": slope,
            "statistic": {"name": "slope t, day-clustered", "value": tval} if tval is not None else None,
            "threshold": threshold}

    if n < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        which = []
        if n < MIN_CASES:
            which.append(f"{n} cases < 300")
        if n_days < MIN_DAYS:
            which.append(f"{n_days} distinct days < 150")
        decided = "Minimum count not reached: " + ", ".join(which) + "."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = "Confirm rule: slope positive with t >= 2 on at least 300 cases over at least 150 distinct days."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "Reject rule: slope negative with t <= -2 on at least 300 cases over at least 150 distinct days."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
