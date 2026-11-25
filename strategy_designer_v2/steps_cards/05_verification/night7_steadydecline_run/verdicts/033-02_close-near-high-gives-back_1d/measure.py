import numpy as np
import pandas as pd


def measure(bars):
    LOC = "debug_info.components.close_loc.last_history_value"

    # ---------- collect rows per coin / window (no joins across windows) ----------
    frames = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            high = d["high"].astype(float)
            low = d["low"].astype(float)
            rng = high - low
            price_loc = np.where(rng > 0, (close - low) / rng.replace(0, np.nan), np.nan)
            if LOC in d.columns:
                loc = d[LOC].astype(float)
                loc = loc.where(loc.notna(), pd.Series(price_loc, index=d.index))
            else:
                loc = pd.Series(price_loc, index=d.index)
            out = pd.DataFrame({
                "coin": coin,
                "window": w,
                "timestamp": pd.to_datetime(d["timestamp"], utc=True),
                "loc": loc.values,
                "forecast": d["forecast"].astype(float).values if "forecast" in d.columns else np.nan,
                "ret1": (close.shift(-1) / close - 1.0).values,
            })
            frames.append(out)

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": None, "supporting_check": None,
            "counts": {"distinct days of cases": 0, "bars in the top fifth": 0},
            "decided_by": "No bars in the record.",
            "reading": "none",
        }

    allr = pd.concat(frames, ignore_index=True)

    # ---------- 1. situation check ----------
    # Situation: close's position in the range, graded; it holds wherever the close is above the low (loc > 0);
    # expected side: short (the outcome is a fall).
    fc = allr["forecast"]
    active = fc.notna() & (fc != 0)
    n_active = int(active.sum())
    if n_active > 0:
        ok = active & (allr["loc"] > 0) & (fc < 0)
        agreement = float(ok.sum()) / n_active
    else:
        agreement = 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the active bars are shorts on bars where the close sits above the "
                           "day's low, so the forecast does not do the graded short the Fidelity describes."),
            "reading": "Situation bars are those with close location > 0 (above the low), expected side short.",
        }

    # ---------- 2. criterion ----------
    # coin's mean daily return over all its windows
    coin_mean = allr.groupby("coin")["ret1"].mean()
    allr["y"] = allr["ret1"] - allr["coin"].map(coin_mean)
    s = allr.dropna(subset=["loc", "y"]).copy()
    s["day"] = s["timestamp"].dt.floor("D")

    n = len(s)
    n_days = int(s["day"].nunique())
    top = s[s["loc"] >= 0.8]
    n_top = int(len(top))
    counts = {"distinct days of cases": n_days, "bars in the top fifth": n_top, "cases": int(n)}

    slope = None
    t = None
    if n >= 3:
        x = s["loc"].values.astype(float)
        y = s["y"].values.astype(float)
        xc = x - x.mean()
        sxx = float(np.sum(xc ** 2))
        if sxx > 0:
            slope = float(np.sum(xc * y) / sxx)
            a = y.mean() - slope * x.mean()
            e = y - a - slope * x
            g = pd.Series(xc * e).groupby(s["day"].values).sum().values
            G = len(g)
            if G > 1:
                var = float(np.sum(g ** 2)) / sxx ** 2 * G / (G - 1)
                t = float(slope / np.sqrt(var)) if var > 0 else None

    top_mean = float(top["y"].mean()) if n_top > 0 else None
    sup_pass = (top_mean < 0) if top_mean is not None else None

    main = {
        "name": "pooled OLS slope of next-day return minus coin mean on close location",
        "value": slope,
        "statistic": {"name": "t clustered by day", "value": t} if t is not None else None,
        "threshold": "confirm: slope < 0 with t <= -2 (and top-fifth mean < 0); reject: slope > 0 with t >= +2",
    }
    support = {
        "name": "mean next-day return minus coin mean, close location >= 0.8",
        "value": top_mean,
        "passed": sup_pass,
    }
    reading = ("Every bar is a case (1-bar horizon, so non-overlapping); the slope's t uses standard errors "
               "clustered by UTC day (residual x centred location summed per day, G/(G-1) correction); "
               "the situation holds where close location > 0, on the short side.")

    sc = {"agreement": agreement, "passed": True}

    if n_days < 500 or n_top < 300:
        miss = []
        if n_days < 500:
            miss.append(f"distinct days of cases {n_days} < 500")
        if n_top < 300:
            miss.append(f"bars in the top fifth {n_top} < 300")
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": support, "counts": counts,
                "decided_by": "Minimum count not reached: " + "; ".join(miss) + ".",
                "reading": reading}

    if slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope < 0 and t <= -2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is negative with t <= -2 and the top-fifth mean is below 0 (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The slope is negative with t <= -2 but the top-fifth mean is not below 0 (inconclusive rule)."
    elif slope > 0 and t >= 2:
        status = "rejected"
        decided = "The slope is positive with t >= +2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope has |t| < 2 (inconclusive rule)."

    return {"status": status, "situation_check": sc, "main_measure": main,
            "supporting_check": support, "counts": counts,
            "decided_by": decided, "reading": reading}
