import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.loc_range.last_history_value"
    H = 1
    MIN_DAYS = 1000

    # ---------- gather per-bar data, within windows ----------
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        rets_all = []
        for w, df in wins.items():
            d = df.copy()
            d = d.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float)
            nxt = close.shift(-H) / close - 1.0
            rets_all.append(nxt.dropna().values)
            # raw component value: recorded, else recomputed from prices
            rng = (d["high"] - d["low"]).astype(float)
            mean_prev = rng.shift(1).rolling(20, min_periods=20).mean()
            recomputed = (2 * close - d["high"] - d["low"]) / mean_prev.replace(0, np.nan)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            rows.append(pd.DataFrame({
                "coin": coin,
                "window": w,
                "day": ts.dt.floor("D"),
                "forecast": pd.to_numeric(d["forecast"], errors="coerce").values,
                "raw": raw.values,
                "ret": nxt.values,
            }))
        r = np.concatenate(rets_all) if rets_all else np.array([])
        coin_rets[coin] = float(np.mean(r)) if r.size else np.nan

    data = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(
        columns=["coin", "window", "day", "forecast", "raw", "ret"])
    data["mu"] = data["coin"].map(coin_rets)

    # ---------- situation check ----------
    # Fidelity: low close (raw < 0) -> rise expected -> long; high close (raw > 0) -> fall -> short.
    active = data[(data["forecast"].notna()) & (data["forecast"] != 0)]
    n_active = len(active)
    if n_active > 0:
        expected = -np.sign(active["raw"].values)
        ok = (expected != 0) & np.isfinite(active["raw"].values) & \
             (np.sign(active["forecast"].values) == expected)
        agreement = float(ok.mean())
    else:
        agreement = 0.0
    passed = agreement >= 0.90

    main_name = "t of daily-summed (forecast/10) x next-day excess return"
    threshold = "confirm t >= 2 with top-minus-bottom third difference > 0; reject t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars have a forecast of the side the Fidelity expects "
                          "(long after a close in the lower half of the range, short after the upper half).",
            "reading": "Situation taken as raw close-location-times-range-multiple nonzero, expected side = minus its sign.",
        }

    # ---------- main measure ----------
    v = data[data["forecast"].notna() & data["ret"].notna() & data["mu"].notna()].copy()
    v["excess"] = v["ret"] - v["mu"]
    v["val"] = (v["forecast"] / 10.0) * v["excess"]
    daily = v.groupby("day")["val"].sum()
    n_days = int(len(daily))
    mean_val = float(daily.mean()) if n_days else np.nan
    if n_days > 1:
        sd = float(daily.std(ddof=1))
        t = mean_val / (sd / np.sqrt(n_days)) if sd > 0 else np.nan
    else:
        t = np.nan

    case_days = int(v.loc[v["forecast"] != 0, "day"].nunique())

    # ---------- supporting check ----------
    diff = None
    sup_passed = None
    if len(v) >= 3:
        a = v["forecast"].abs()
        rk = a.rank(method="first")
        terc = pd.qcut(rk, 3, labels=[0, 1, 2])
        s = np.sign(v["forecast"]) * v["excess"]
        top = s[terc == 2].mean()
        bot = s[terc == 0].mean()
        if np.isfinite(top) and np.isfinite(bot):
            diff = float(top - bot)
            sup_passed = bool(diff > 0)

    counts = {"days with cases": case_days, "days in main measure": n_days,
              "bars in main measure": int(len(v))}

    # ---------- decision ----------
    if case_days < MIN_DAYS:
        status = "not observable"
        decided = f"Only {case_days} days with cases, below the plan's minimum of {MIN_DAYS}."
    elif not np.isfinite(t):
        status = "inconclusive"
        decided = "The main measure's t could not be computed."
    elif t >= 2 and sup_passed:
        status = "confirmed"
        decided = "The main measure's t is 2 or more and the top-minus-bottom third difference is above 0."
    elif t >= 2:
        status = "inconclusive"
        decided = "The main measure's t is 2 or more but the top-minus-bottom third difference is 0 or below."
    elif t <= -2:
        status = "rejected"
        decided = "The main measure's t is -2 or less."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": mean_val if np.isfinite(mean_val) else None,
                         "statistic": {"name": "t of the mean over days", "value": float(t)} if np.isfinite(t) else None,
                         "threshold": threshold},
        "supporting_check": {"name": "top minus bottom third by |forecast| of sign(forecast) x next-day excess return",
                             "value": diff, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": "Every recorded bar with a next-day return in its window is used (zero forecasts included in the "
                   "daily sums and in the pooled tercile split by |forecast|, ties broken by order), days are UTC dates, "
                   "a day with cases is one with a nonzero forecast on any coin, and the plan's 1000-day minimum is "
                   "reported as 'not observable'.",
    }
