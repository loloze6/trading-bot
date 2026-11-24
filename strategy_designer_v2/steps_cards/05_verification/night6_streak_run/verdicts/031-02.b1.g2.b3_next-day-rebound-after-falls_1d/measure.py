import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.scaled_fall.last_history_value"

    # ---------- gather per-coin frames, returns inside each window only ----------
    rows = []
    coin_mu = {}
    for coin, windows in bars.items():
        all_daily = []
        frames = []
        for w, df in windows.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            d["ret_prev"] = close / close.shift(1) - 1.0   # the latest day's return (inside window)
            d["ret_next"] = close.shift(-1) / close - 1.0  # next day's return (inside window)
            all_daily.append(d["ret_prev"].dropna())
            d["coin"] = coin
            d["window"] = w
            frames.append(d)
        if not frames:
            continue
        allr = pd.concat(all_daily) if all_daily else pd.Series(dtype=float)
        coin_mu[coin] = float(allr.mean()) if len(allr) else np.nan
        cdf = pd.concat(frames, ignore_index=True)
        cdf["mu"] = coin_mu[coin]
        rows.append(cdf)

    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "timing gain before costs on forecast>0 bars, summed per day, t of mean over days",
                             "value": None, "statistic": None,
                             "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"distinct days with forecast > 0": 0},
            "decided_by": "No bars in the record, so the minimum of 300 distinct days with forecast > 0 is not reached.",
            "reading": "none",
        }

    data = pd.concat(rows, ignore_index=True)
    data["forecast"] = pd.to_numeric(data["forecast"], errors="coerce")

    # ---------- situation check: a fall on the latest day, long side ----------
    if RAW in data.columns:
        raw = pd.to_numeric(data[RAW], errors="coerce")
    else:
        raw = pd.Series(np.nan, index=data.index)
    # where the raw component is not recorded, recompute its sign from the prices
    fall = np.where(raw.notna(), raw < 0, data["ret_prev"] < 0)
    fall = pd.Series(fall, index=data.index).astype(bool)

    active = data["forecast"].notna() & (data["forecast"] != 0)
    n_active = int(active.sum())
    if n_active > 0:
        agree = float((fall & (data["forecast"] > 0) & active).sum() / n_active)
    else:
        agree = 0.0
    passed_sit = agree >= 0.9

    reading = ("Days are UTC calendar dates of the bar's timestamp; the 300-day minimum counts distinct dates of "
               "forecast>0 bars with a valid next-day return inside their window; thirds are the n//3 highest and "
               "n//3 lowest forecast>0 bars pooled across coins after a stable sort by forecast; the excess return "
               "removes the coin's mean daily return over all its windows.")

    main_name = "timing gain before costs on forecast>0 bars (position x (next-day return - coin mean)), summed per day across coins, mean over days"
    threshold = "confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2 and top-minus-bottom < 0"

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agree, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars after a down day "
                           "(negative raw scaled return), as the Fidelity's situation and side require."),
            "reading": reading,
        }

    # ---------- main measure ----------
    pos = pd.to_numeric(data["postRebalance_current_allocation"], errors="coerce")
    data["pos"] = pos
    data["excess"] = data["ret_next"] - data["mu"]
    data["day"] = data["timestamp"].dt.floor("D")

    sel = data[(data["forecast"] > 0)].copy()
    sel_main = sel.dropna(subset=["pos", "excess"])
    sel_main = sel_main.assign(gain=sel_main["pos"] * sel_main["excess"])
    daily = sel_main.groupby("day")["gain"].sum()
    n_days = int(len(daily))

    if n_days >= 2:
        m = float(daily.mean())
        sd = float(daily.std(ddof=1))
        t = float(m / (sd / np.sqrt(n_days))) if sd > 0 else float("nan")
    elif n_days == 1:
        m = float(daily.mean())
        t = float("nan")
    else:
        m = float("nan")
        t = float("nan")

    # ---------- supporting check ----------
    sc = sel.dropna(subset=["excess"])
    sc = sc.sort_values("forecast", kind="mergesort").reset_index(drop=True)
    k = len(sc) // 3
    if k >= 1:
        bottom = sc.iloc[:k]["excess"]
        top = sc.iloc[len(sc) - k:]["excess"]
        diff = float(top.mean() - bottom.mean())
        check_pass = bool(diff > 0)
    else:
        diff = float("nan")
        check_pass = None

    counts = {
        "distinct days with forecast > 0": n_days,
        "bars with forecast > 0": int(len(sel_main)),
        "bars per third": int(k),
    }

    def clean(x):
        return None if (x is None or (isinstance(x, float) and not np.isfinite(x))) else x

    result = {
        "situation_check": {"agreement": agree, "passed": True},
        "main_measure": {"name": main_name, "value": clean(m),
                         "statistic": {"name": "t of the mean over days", "value": clean(t)},
                         "threshold": threshold},
        "supporting_check": {"name": "mean next-day excess return, top third minus bottom third by forecast",
                             "value": clean(diff), "passed": check_pass},
        "counts": counts,
        "reading": reading,
    }

    # ---------- decision ----------
    if n_days < 300:
        result["status"] = "not observable"
        result["decided_by"] = (f"Only {n_days} distinct days with forecast > 0, below the plan's minimum of 300.")
        return result

    if np.isfinite(m) and np.isfinite(t) and m > 0 and t >= 2 and check_pass is True:
        result["status"] = "confirmed"
        result["decided_by"] = ("Confirm rule: the daily timing gain has a mean above 0 with t >= 2 and the top third "
                                "beats the bottom third.")
    elif np.isfinite(m) and np.isfinite(t) and m < 0 and t <= -2 and np.isfinite(diff) and diff < 0:
        result["status"] = "rejected"
        result["decided_by"] = ("Reject rule: the daily timing gain has a mean below 0 with t <= -2 and the "
                                "top-minus-bottom-third difference is below 0.")
    else:
        result["status"] = "inconclusive"
        if np.isfinite(t) and -2 < t < 2:
            why = "the t of the daily timing gain lies between -2 and 2"
        else:
            why = "the main measure and the top-minus-bottom-third check disagree"
        result["decided_by"] = f"Inconclusive rule: {why}."
    return result
