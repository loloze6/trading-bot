import numpy as np
import pandas as pd


def measure(bars):
    RATIO = "debug_info.components.ratio.last_history_value"
    REGIME = "mean_reversion"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            if RATIO in d.columns:
                rr = pd.to_numeric(d[RATIO], errors="coerce")
            else:
                rr = pd.Series(np.nan, index=d.index)
            # Recompute the 90/30 mean bar range ratio from prices, inside the window, where not recorded
            rng = (pd.to_numeric(d["high"], errors="coerce") - pd.to_numeric(d["low"], errors="coerce"))
            rr_px = rng.rolling(90, min_periods=90).mean() / rng.rolling(30, min_periods=30).mean()
            rr = rr.where(rr.notna(), rr_px)
            active = fc.notna() & (fc != 0)
            situation = rr.notna() & (rr < 1.0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "day-clustered t of the slope of the next-day excess return on the forecast, regime bars"
    threshold = "confirm: t >= 2 with timing gain > 0; reject: t <= -2; at least 100 days with regime cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the 90-day "
                           "over 30-day mean bar range ratio is below 1, as the Fidelity's situation and rise require."),
            "reading": "none",
        }

    # ---------- 2. build per-bar data ----------
    rows = []
    for coin, wins in bars.items():
        frames = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce")
            r = c.shift(-1) / c - 1.0
            frames.append(pd.DataFrame({
                "coin": coin,
                "window": w,
                "day": pd.to_datetime(d["timestamp"], utc=True).dt.floor("D"),
                "ret": r,
                "forecast": pd.to_numeric(d["forecast"], errors="coerce"),
                "regime": d["regime"].astype(str),
                "alloc": pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce"),
            }))
        if not frames:
            continue
        cf = pd.concat(frames, ignore_index=True)
        mu = cf["ret"].mean()  # coin's mean daily return over all its windows
        cf["mu"] = mu
        cf["xret"] = cf["ret"] - mu
        rows.append(cf)
    allb = pd.concat(rows, ignore_index=True)

    # ---------- main measure: slope t, same-day cases clustered ----------
    reg = allb[(allb["regime"] == REGIME)].dropna(subset=["xret", "forecast"])
    n_cases = int(len(reg))
    n_days = int(reg["day"].nunique())

    slope = None
    t = None
    if n_cases >= 3 and n_days >= 2:
        x = reg["forecast"].to_numpy(float)
        y = reg["xret"].to_numpy(float)
        xm = x - x.mean()
        sxx = float(np.sum(xm ** 2))
        if sxx > 0:
            b = float(np.sum(xm * (y - y.mean())) / sxx)
            a = y.mean() - b * x.mean()
            e = y - a - b * x
            score = pd.Series(xm * e).groupby(reg["day"].to_numpy()).sum().to_numpy()
            G = len(score)
            var_b = (G / (G - 1.0)) * float(np.sum(score ** 2)) / sxx ** 2
            slope = b
            t = float(b / np.sqrt(var_b)) if var_b > 0 else None

    # ---------- supporting check: book's mean daily timing gain before costs ----------
    bk = allb.dropna(subset=["ret", "alloc"]).copy()
    bk["timing"] = bk["alloc"] * (bk["ret"] - bk["mu"])
    daily_timing = bk.groupby("day")["timing"].mean()
    timing = float(daily_timing.mean()) if len(daily_timing) else None
    sup_pass = None if timing is None else bool(timing > 0)

    counts = {"days carrying regime cases": n_days, "regime cases": n_cases}

    if n_days < 100:
        status = "not observable"
        decided = f"Only {n_days} days carry regime cases, below the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed on the regime cases."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the timing gain is positive (confirm rule)."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less (reject rule)."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the timing gain is 0 or below (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t is None else {"name": "OLS slope t, standard error clustered by day", "value": t},
            "threshold": threshold,
        },
        "supporting_check": {"name": "book's mean daily timing gain before costs", "value": timing, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Regime bars are those with regime 'mean_reversion' (zero forecasts included), the slope's t uses "
                    "a day-clustered standard error with a G/(G-1) correction so that same-day cases are summed into "
                    "one piece of evidence, the timing gain is the position after each bar's trade times the next "
                    "return minus the coin's mean daily return, averaged over coins per day and then over days, and "
                    "the bar range for any recomputed ratio is high minus low."),
    }
