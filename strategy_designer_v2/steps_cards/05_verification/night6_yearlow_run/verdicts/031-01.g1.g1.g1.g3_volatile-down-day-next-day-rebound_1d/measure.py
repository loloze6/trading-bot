import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.fall.last_history_value"

    # ---------- collect rows ----------
    rows = []
    all_next_rets = {}  # coin -> list of next-day returns over all bars of all windows
    for coin in sorted(bars.keys()):
        coin_rets = []
        for win in sorted(bars[coin].keys(), key=lambda w: int(str(w).lstrip("w")) if str(w).lstrip("w").isdigit() else str(w)):
            df = bars[coin][win]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0          # inside the window only
            day_ret = close / close.shift(1) - 1.0       # the bar's own return, inside the window
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0)
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            coin_rets.extend(nxt.dropna().tolist())
            for i in range(len(df)):
                rows.append({
                    "coin": coin, "window": win,
                    "day": ts.iloc[i].floor("D"),
                    "forecast": float(fc.iloc[i]),
                    "raw": raw.iloc[i], "day_ret": day_ret.iloc[i],
                    "regime": regime.iloc[i], "next": nxt.iloc[i],
                })
        all_next_rets[coin] = coin_rets
    data = pd.DataFrame(rows)

    reading = ("The regime part of the situation is read from the recorded `regime` column (the volatility-rank detector "
               "is not recorded and 365 days of history are not in the windows), the down day from the fall component's raw "
               "value < 0 (the bar's close-to-close return when the raw value is missing); the coin's mean daily return is "
               "the mean of all its 1-bar returns over all windows; the slope's t uses day-clustered errors (x-deviation times "
               "residual summed per day, with G/(G-1) correction); the top third is the ceil(n/3) bars with the largest "
               "forecast; the 100-bar minimum counts bars with forecast > 0 and a next-day return in the same window.")

    empty_main = {"name": "slope t of next-day excess return on forecast", "value": None,
                  "statistic": None, "threshold": "slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects"}

    if len(data) == 0:
        return {"status": "not observable",
                "situation_check": {"agreement": None, "passed": False},
                "main_measure": empty_main, "supporting_check": None,
                "counts": {"bars with forecast > 0": 0},
                "decided_by": "No bars in the record; the minimum of 100 bars with forecast > 0 is not reached.",
                "reading": reading}

    # ---------- situation check ----------
    active = data[data["forecast"] != 0]
    n_active = len(active)
    if n_active > 0:
        down = np.where(active["raw"].notna(), active["raw"] < 0, active["day_ret"] < 0)
        ok = (active["regime"].values == "mean_reversion") & down & (active["forecast"].values > 0)
        agreement = float(ok.mean())
    else:
        agreement = 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {"status": "mismatch",
                "situation_check": {"agreement": agreement, "passed": False},
                "main_measure": empty_main, "supporting_check": None,
                "counts": {"active bars": int(n_active)},
                "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars in the mean_reversion "
                               "(top-fifth volatility) regime on a down day, as the plan's situation requires."
                               if n_active > 0 else "The config produced no active bars."),
                "reading": reading}

    # ---------- main measure ----------
    coin_mean = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in all_next_rets.items()}
    sel = data[(data["forecast"] > 0) & data["next"].notna()].copy()
    sel["excess"] = sel["next"] - sel["coin"].map(coin_mean)
    sel = sel[sel["excess"].notna()]
    n = int(len(sel))
    n_days = int(sel["day"].nunique()) if n else 0
    counts = {"bars with forecast > 0": n, "days": n_days}

    if n < 100:
        return {"status": "not observable",
                "situation_check": {"agreement": agreement, "passed": True},
                "main_measure": empty_main, "supporting_check": None,
                "counts": counts,
                "decided_by": f"Only {n} bars with forecast > 0, below the plan's minimum of 100.",
                "reading": reading}

    x = sel["forecast"].values.astype(float)
    y = sel["excess"].values.astype(float)
    xd = x - x.mean()
    sxx = float(np.sum(xd ** 2))
    if sxx <= 0 or n_days < 2:
        slope, t = None, None
    else:
        slope = float(np.sum(xd * (y - y.mean())) / sxx)
        intercept = y.mean() - slope * x.mean()
        resid = y - intercept - slope * x
        score = pd.Series(xd * resid).groupby(sel["day"].values).sum().values
        G = len(score)
        var_b = (G / (G - 1.0)) * float(np.sum(score ** 2)) / sxx ** 2
        t = float(slope / np.sqrt(var_b)) if var_b > 0 else None

    # ---------- supporting check ----------
    k = int(np.ceil(n / 3.0))
    order = np.argsort(-x, kind="mergesort")
    top_mean = float(np.mean(y[order[:k]]))
    sup_pass = bool(top_mean > 0)
    counts["top third bars"] = k

    main = {"name": "slope t of next-day excess return on forecast",
            "value": slope,
            "statistic": {"name": "OLS slope t, residuals summed per day", "value": t} if t is not None else None,
            "threshold": "slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects"}
    support = {"name": "top-third mean next-day excess return", "value": top_mean, "passed": sup_pass}

    if t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), which the plan's other-result rule calls inconclusive."
    elif slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the top-third mean excess return is above 0 (confirm rule)."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 (reject rule)."
    elif slope > 0 and t >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the top-third mean excess return is <= 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2 (inconclusive rule)."

    return {"status": status,
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": main,
            "supporting_check": support,
            "counts": counts,
            "decided_by": decided,
            "reading": reading}
