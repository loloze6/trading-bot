import numpy as np
import pandas as pd


def _to_days(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype(float)
        med = np.nanmedian(v.values) if len(v) else 0.0
        if med > 1e17:
            unit = "ns"
        elif med > 1e14:
            unit = "us"
        elif med > 1e11:
            unit = "ms"
        else:
            unit = "s"
        dt = pd.to_datetime(v, unit=unit, utc=True)
    else:
        dt = pd.to_datetime(s, utc=True)
    return dt.dt.floor("D").dt.strftime("%Y-%m-%d").values


def measure(bars):
    RAW = "debug_info.components.fall_in_swings.last_history_value"

    # ---------- collect per-bar rows ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").astype(float)
            nxt = close.shift(-1) / close - 1.0           # inside the window only
            day_ret = close / close.shift(1) - 1.0        # inside the window only
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").astype(float)
            else:
                raw = pd.Series(np.nan, index=d.index)
            # fallback where the component is not recorded: sign of the day's
            # return (the 20-day std is positive, so it carries the raw sign)
            raw_sign = np.sign(raw)
            raw_sign = raw_sign.where(raw.notna(), np.sign(day_ret))
            part = pd.DataFrame({
                "coin": coin,
                "window": w,
                "day": _to_days(d["timestamp"]),
                "forecast": fc.values,
                "raw_sign": raw_sign.values,
                "next_ret": nxt.values,
            })
            rows.append(part)

    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "OLS slope of next-day excess return on forecast",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 confirms (with supporting mean > 0); t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"bars with forecast above 0": 0, "distinct days": 0},
            "decided_by": "The record holds no bars, so the minimum of 300 bars with forecast above 0 is not reached.",
            "reading": "none",
        }

    allb = pd.concat(rows, ignore_index=True)

    # ---------- situation check ----------
    active = allb[allb["forecast"].notna() & (allb["forecast"] != 0)]
    n_active = len(active)
    if n_active > 0:
        ok = (active["raw_sign"] < 0) & (active["forecast"] > 0)
        agreement = float(ok.mean())
    else:
        agreement = None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation = raw fall_in_swings value below 0 (a down day; day-return sign if not recorded) "
               "with forecast > 0 (long); slope t is cluster-robust by UTC day (CR1, all coins' bars of a day "
               "as one cluster); the 300-bar and 200-day minimums count bars with forecast above 0 that have a "
               "next-day return inside their window; coin mean daily return is over all its windows' next-day returns.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "OLS slope of next-day excess return on forecast",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 confirms (with supporting mean > 0); t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are down days (raw value below 0) with a long "
                           "forecast, so the config does not trade the plan's situation on its side."
                           if n_active > 0 else
                           "The forecast is never active, so the config does not trade the plan's situation."),
            "reading": reading,
        }

    # ---------- main measure ----------
    m = allb[allb["next_ret"].notna() & allb["forecast"].notna()].copy()
    coin_mean = m.groupby("coin")["next_ret"].mean()
    m["excess"] = m["next_ret"] - m["coin"].map(coin_mean)

    pos = m[m["forecast"] > 0]
    n_pos = int(len(pos))
    n_days = int(pos["day"].nunique())

    slope = None
    t_slope = None
    N = len(m)
    x = m["forecast"].values.astype(float)
    y = m["excess"].values.astype(float)
    if N >= 3:
        xc = x - x.mean()
        sxx = float(np.sum(xc * xc))
        if sxx > 0:
            slope = float(np.sum(xc * (y - y.mean())) / sxx)
            intercept = y.mean() - slope * x.mean()
            e = y - intercept - slope * x
            score = pd.Series(xc * e).groupby(m["day"].values).sum()
            G = len(score)
            if G > 1:
                meat = float(np.sum(score.values ** 2))
                corr = (G / (G - 1.0)) * ((N - 1.0) / (N - 2.0))
                var = corr * meat / (sxx ** 2)
                if var > 0:
                    t_slope = float(slope / np.sqrt(var))

    sup_mean = float(pos["excess"].mean()) if n_pos > 0 else None
    sup_pass = (sup_mean > 0) if sup_mean is not None else None

    counts = {"bars with forecast above 0": n_pos, "distinct days": n_days,
              "bars in slope": int(N), "day clusters": int(m["day"].nunique())}

    # ---------- decision ----------
    if n_pos < 300:
        status = "not observable"
        decided = f"Only {n_pos} bars with forecast above 0, below the plan's minimum of 300."
    elif n_days < 200:
        status = "not observable"
        decided = f"The bars with forecast above 0 fall on only {n_days} distinct days, below the plan's minimum of 200."
    elif t_slope is None:
        status = "not observable"
        decided = "The slope's t could not be computed (no variation in forecast or too few day clusters)."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess next-day return on forecast > 0 bars is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger falls in swing units are followed by lower next-day returns than usual."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting mean excess return is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "OLS slope of next-day excess return on forecast",
            "value": slope,
            "statistic": ({"name": "slope t, clustered by day", "value": t_slope}
                          if t_slope is not None else None),
            "threshold": "t >= 2 confirms (with supporting mean > 0); t <= -2 rejects; otherwise inconclusive",
        },
        "supporting_check": {
            "name": "mean next-day excess return on forecast > 0 bars above 0",
            "value": sup_mean,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
