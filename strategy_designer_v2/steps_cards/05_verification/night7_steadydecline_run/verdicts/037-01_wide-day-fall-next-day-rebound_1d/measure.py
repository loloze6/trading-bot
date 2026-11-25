import numpy as np
import pandas as pd
from scipy import stats


def _to_dt(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = float(np.nanmax(np.abs(s.values))) if len(s) else 0.0
        unit = "ns" if v > 1e17 else ("us" if v > 1e14 else ("ms" if v > 1e11 else "s"))
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    RAW = "debug_info.components.wide_fall.last_history_value"
    POST = "debug_info.components.wide_fall.post_pipeline_value"

    frames = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            d["coin"] = coin
            d["window"] = w
            d["day"] = _to_dt(d["timestamp"]).dt.floor("D").values
            close = pd.to_numeric(d["close"], errors="coerce")
            d["ret_next"] = close.shift(-1) / close - 1.0
            d["ret_bar"] = close / close.shift(1) - 1.0
            d["fc"] = pd.to_numeric(d["forecast"], errors="coerce")
            d["pos"] = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce")
            d["raw"] = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else np.nan
            d["post"] = pd.to_numeric(d[POST], errors="coerce") if POST in d.columns else np.nan
            frames.append(d[["coin", "window", "day", "ret_next", "ret_bar", "fc", "pos", "raw", "post"]])
    if not frames:
        return {"status": "not observable", "situation_check": {"agreement": None, "passed": False},
                "main_measure": None, "supporting_check": None,
                "counts": {"bars with forecast > 0": 0, "distinct days": 0},
                "decided_by": "No bars in the record.", "reading": "none"}
    allb = pd.concat(frames, ignore_index=True)

    # ---- situation check: a one-day fall (close below previous close), long side ----
    fall_price = allb["ret_bar"] < 0
    # first bar of a window has no previous close inside the window: fall from the raw component (nonzero only on falls)
    first = allb["ret_bar"].isna()
    fall_raw = allb["raw"].notna() & (allb["raw"] != 0)
    situation = np.where(first, fall_raw, fall_price)
    situation = pd.Series(situation, index=allb.index).astype(bool) & allb["raw"].notna()
    active = allb["fc"].notna() & (allb["fc"] != 0)
    n_active = int(active.sum())
    if n_active > 0:
        agree = float(((situation) & (allb["fc"] > 0))[active].mean())
    else:
        agree = None
    passed_sit = agree is not None and agree >= 0.9

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agree, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"bars with forecast > 0": int((allb["fc"] > 0).sum()),
                       "distinct days": int(allb.loc[allb["fc"] > 0, "day"].nunique())},
            "decided_by": ("Fewer than 90% of the active bars are long bars on a one-day fall, "
                           "the plan's situation and side." if agree is not None
                           else "The forecast is never active, so the long-on-fall situation is never traded."),
            "reading": "Situation taken as close below the previous close inside the window (raw component nonzero on a window's first bar), side long.",
        }

    # ---- coin mean daily return over all windows ----
    mu = allb.dropna(subset=["ret_next"]).groupby("coin")["ret_next"].mean()
    allb["mu"] = allb["coin"].map(mu)
    allb["excess"] = allb["ret_next"] - allb["mu"]

    # ---- main measure: timing gain, averaged per day across coins, t over days ----
    m = allb.dropna(subset=["pos", "excess"]).copy()
    m["gain"] = m["pos"] * m["excess"]
    daily = m.groupby("day")["gain"].mean()
    n_days_main = int(len(daily))
    if n_days_main >= 2:
        mean_main = float(daily.mean())
        sd = float(daily.std(ddof=1))
        t_main = float(mean_main / (sd / np.sqrt(n_days_main))) if sd > 0 else None
    else:
        mean_main = float(daily.mean()) if n_days_main else None
        t_main = None

    # ---- supporting check ----
    pos_bars = allb[allb["fc"] > 0]
    s = pos_bars.dropna(subset=["post", "excess"])
    sup_val, sup_t, sup_pass = None, None, None
    if len(s) >= 4:
        med = float(s["post"].median())
        up = s.loc[s["post"] > med, "excess"]
        lo = s.loc[s["post"] <= med, "excess"]
        if len(up) >= 2 and len(lo) >= 2:
            sup_val = float(up.mean() - lo.mean())
            tt = stats.ttest_ind(up.values, lo.values, equal_var=False)
            sup_t = float(tt.statistic) if np.isfinite(tt.statistic) else None
            sup_pass = bool(sup_val > 0 and sup_t is not None and sup_t >= 1)
        else:
            sup_pass = False
    else:
        sup_pass = False

    n_pos = int(len(pos_bars))
    n_pos_days = int(pos_bars["day"].nunique())
    counts = {"bars with forecast > 0": n_pos, "distinct days": n_pos_days,
              "days in main measure": n_days_main}

    main = {"name": "timing gain before costs, per-day mean across coins",
            "value": mean_main,
            "statistic": {"name": "t of the mean over days", "value": t_main} if t_main is not None else None,
            "threshold": "confirm if t >= 2 and mean > 0 (with supporting check); reject if t <= -2"}
    sup = {"name": "upper minus lower half (median post_pipeline_value) mean next-day excess return, Welch t",
           "value": sup_val, "passed": sup_pass}
    if sup_t is not None:
        sup["welch_t"] = sup_t

    if n_pos < 200 or n_pos_days < 100:
        status = "not observable"
        decided = (f"Minimum not reached: {n_pos} bars with forecast > 0 (need 200) over "
                   f"{n_pos_days} distinct days (need 100).")
    elif t_main is None:
        status = "inconclusive"
        decided = "The main measure's t could not be computed, so neither confirm nor reject is met."
    elif t_main >= 2 and mean_main > 0:
        if sup_pass:
            status = "confirmed"
            decided = "Main measure t >= 2 with a positive mean, and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "Main measure is at confirm level but the supporting check fails."
    elif t_main <= -2:
        status = "rejected"
        decided = "Main measure t <= -2."
    else:
        status = "inconclusive"
        decided = "Main measure t lies between -2 and 2 (or t >= 2 with a non-positive mean)."

    return {
        "status": status,
        "situation_check": {"agreement": agree, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": ("Days are UTC calendar days of the bar timestamp, the coin's mean is over all its within-window "
                    "next-day returns, the median split puts values above the median in the upper half and the rest "
                    "in the lower, and the plan's 'fewer is inconclusive' minimum is reported as not observable."),
    }
