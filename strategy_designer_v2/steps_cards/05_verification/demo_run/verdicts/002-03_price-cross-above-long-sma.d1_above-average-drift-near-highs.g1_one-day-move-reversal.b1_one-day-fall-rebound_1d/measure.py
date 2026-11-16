import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.fall.last_history_value"
    POS = "postRebalance_current_allocation"
    MIN_BARS = 100

    # ---------- collect per-window data (never across windows) ----------
    frames = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            if "timestamp" in d.columns:
                d = d.sort_values("timestamp")
            d = d.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            ret_today = close / close.shift(1) - 1.0          # inside the window only
            ret_next = close.shift(-1) / close - 1.0           # inside the window only
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            out = pd.DataFrame({
                "coin": coin,
                "window": w,
                "forecast": pd.to_numeric(d["forecast"], errors="coerce"),
                "pos": pd.to_numeric(d[POS], errors="coerce") if POS in d.columns else np.nan,
                "ret_today": ret_today,
                "raw": raw,
                "ret_next": ret_next,
            })
            frames.append(out)

    reading = ("A bar is in the situation when the coin's one-day return close[t]/close[t-1]-1 inside the window "
               "is negative (on a window's first bar, when the raw 'fall' component value is negative), the expected "
               "side is long; the 100-bar minimum counts positive-forecast bars with a next-day return in the same "
               "window; the coin's mean daily return is the mean of all its next-day returns over all windows; "
               "quintiles are forecast >= 80th and <= 20th percentile of the positive forecasts (ties included).")

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean of position x next-day excess return on forecast > 0 bars",
                             "value": None, "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject"},
            "supporting_check": None,
            "counts": {"positive-forecast bars": 0},
            "decided_by": "No bars in the record, so the minimum of 100 positive-forecast bars is not reached.",
            "reading": reading,
        }

    allb = pd.concat(frames, ignore_index=True)

    # ---------- situation check ----------
    fall = np.where(allb["ret_today"].notna(), allb["ret_today"] < 0,
                    np.where(allb["raw"].notna(), allb["raw"] < 0, False))
    active = allb["forecast"].notna() & (allb["forecast"] != 0)
    n_active = int(active.sum())
    if n_active > 0:
        agree = (active & pd.Series(fall, index=allb.index) & (allb["forecast"] > 0)).sum() / n_active
        agreement = float(agree)
    else:
        agreement = None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean of position x next-day excess return on forecast > 0 bars",
                             "value": None, "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject"},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the active bars are long positions on one-day-fall bars: the config's "
                           "forecast does not follow the plan's situation (a one-day fall, held long)."
                           if n_active > 0 else "The config produced no active bars, so it never acts on the plan's situation."),
            "reading": reading,
        }

    # ---------- main measure ----------
    coin_mean = allb.dropna(subset=["ret_next"]).groupby("coin")["ret_next"].mean()
    allb["excess"] = allb["ret_next"] - allb["coin"].map(coin_mean)
    sel = allb[(allb["forecast"] > 0) & allb["excess"].notna() & allb["pos"].notna()].copy()
    sel["prod"] = sel["pos"] * sel["excess"]
    n = int(len(sel))

    mean_prod = float(sel["prod"].mean()) if n > 0 else None
    t = None
    if n > 1:
        sd = float(sel["prod"].std(ddof=1))
        if sd > 0:
            t = float(mean_prod / (sd / np.sqrt(n)))

    # ---------- supporting check ----------
    diff = None
    n_top = n_bot = 0
    if n > 0:
        q80 = sel["forecast"].quantile(0.8)
        q20 = sel["forecast"].quantile(0.2)
        top = sel[sel["forecast"] >= q80]
        bot = sel[sel["forecast"] <= q20]
        n_top, n_bot = int(len(top)), int(len(bot))
        if n_top > 0 and n_bot > 0:
            diff = float(top["excess"].mean() - bot["excess"].mean())
    check_passed = None if diff is None else bool(diff > 0)

    # ---------- decision ----------
    if n < MIN_BARS:
        status = "not observable"
        decided = f"Only {n} positive-forecast bars, fewer than the plan's minimum of 100."
    elif t is not None and t >= 2 and check_passed:
        status = "confirmed"
        decided = "t >= 2 with at least 100 positive-forecast bars and the top-minus-bottom quintile excess return > 0."
    elif t is not None and t <= -2:
        status = "rejected"
        decided = "t <= -2 with at least 100 positive-forecast bars."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the top-minus-bottom quintile difference is <= 0, so neither confirm nor reject."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2 with at least 100 positive-forecast bars, so neither confirm nor reject."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean of position x next-day excess return on forecast > 0 bars",
            "value": mean_prod,
            "statistic": None if t is None else {"name": "t of the mean", "value": t},
            "threshold": "t >= 2 (with supporting check) to confirm, t <= -2 to reject, at least 100 positive-forecast bars",
        },
        "supporting_check": {
            "name": "top minus bottom forecast quintile mean next-day excess return > 0",
            "value": diff,
            "passed": check_passed,
        },
        "counts": {
            "positive-forecast bars": n,
            "top quintile bars": n_top,
            "bottom quintile bars": n_bot,
        },
        "decided_by": decided,
        "reading": reading,
    }
