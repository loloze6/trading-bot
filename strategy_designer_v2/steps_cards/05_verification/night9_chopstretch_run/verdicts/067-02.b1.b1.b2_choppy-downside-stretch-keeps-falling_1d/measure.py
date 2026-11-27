import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.stretch.last_history_value"
    CHOPPY_REGIME = "unknown"  # the only regime with a strategy: the code-added choppy profile

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            # price-based distance from SMA20 (sign only), used where the raw value is missing
            sma = close.rolling(20, min_periods=20).mean()
            below_px = close < sma
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            below = np.where(raw.notna(), raw < 0, below_px.fillna(False))
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            choppy = (regime == CHOPPY_REGIME).values
            active = (fc.fillna(0) != 0).values
            ok = active & choppy & below & (fc.fillna(0) < 0).values
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "mean short-direction unusual 5-bar move on grid cases with forecast < 0"
    threshold = "confirm: mean > 0 with t >= 2 and deeper half > shallower half; reject: mean < 0 with t <= -2"
    reading = ("Choppy is read as the regime 'unknown' (the only regime with a strategy, the choppy profile) and "
               "below-average as the raw stretch < 0 (close < SMA20 from prices where it is missing); the day-clustered "
               "t sums per-day deviations from the overall mean with a G/(G-1) correction; drift is the coin's mean of "
               "5-bar returns on the same non-overlapping grid over all its windows; the deeper half is forecast <= the "
               "median of all cases.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active_bars": n_active, "agreeing_bars": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars in the choppy regime "
                           "with the close below its 20-day average, as the Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []
    for coin, wins in bars.items():
        grid_rets = []
        per_win = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0 and pd.notna(ts.iloc[i]):
                    per_win.append((r, float(fc[i]), ts.iloc[i].strftime("%Y-%m-%d")))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for r, f, d in per_win:
            cases.append({"coin": coin, "u": -(r - drift), "fc": f, "day": d})

    cdf = pd.DataFrame(cases, columns=["coin", "u", "fc", "day"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    mean_u = float(cdf["u"].mean()) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        dev = cdf["u"] - mean_u
        s = dev.groupby(cdf["day"]).sum().values
        G = len(s)
        var = (s ** 2).sum() / (n_cases ** 2) * (G / (G - 1))
        se = float(np.sqrt(var))
        t_val = float(mean_u / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    deep_mean = shallow_mean = None
    if n_cases > 0:
        med = float(cdf["fc"].median())
        deep = cdf.loc[cdf["fc"] <= med, "u"]
        shallow = cdf.loc[cdf["fc"] > med, "u"]
        if len(deep) > 0 and len(shallow) > 0:
            deep_mean = float(deep.mean())
            shallow_mean = float(shallow.mean())
            sup_val = deep_mean - shallow_mean
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n_days < 30:
        status = "not observable"
        decided = f"The cases fall on {n_days} distinct days, fewer than the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean short-direction unusual move is above 0 with t >= 2 and the deeper half's mean exceeds the shallower half's."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the deeper half does not exceed the shallower half, which the plan calls inconclusive."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean short-direction unusual move is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t is between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": ({"name": "t of the mean, cases of each day taken together", "value": t_val}
                          if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "deeper-half mean minus shallower-half mean (split at median forecast)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases, "distinct days": n_days},
        "decided_by": decided,
        "reading": reading,
    }
