import numpy as np
import pandas as pd
from scipy import stats


def _get_component(df, comp_id, field):
    """Return a Series of a component's recorded value (NaN where not recorded)."""
    flat = f"debug_info.components.{comp_id}.{field}"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    if "debug_info.components" in df.columns:
        out = []
        for v in df["debug_info.components"].values:
            val = np.nan
            if isinstance(v, dict):
                c = v.get(comp_id)
                if isinstance(c, dict):
                    x = c.get(field)
                    try:
                        val = float(x) if x is not None else np.nan
                    except (TypeError, ValueError):
                        val = np.nan
            out.append(val)
        return pd.Series(out, index=df.index, dtype=float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def _to_day(ts):
    s = ts
    if np.issubdtype(s.dtype, np.number):
        mx = float(np.nanmax(s.values)) if len(s) else 0.0
        unit = "ms" if mx > 1e11 else "s"
        t = pd.to_datetime(s, unit=unit, utc=True)
    else:
        t = pd.to_datetime(s, utc=True)
    return t.dt.strftime("%Y-%m-%d")


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    coin_frames = []
    for coin in sorted(bars.keys()):
        wins = bars[coin]
        rets_all = []
        per_win = []
        for w in sorted(wins.keys(), key=lambda k: (len(str(k)), str(k))):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            ret1 = close / close.shift(1) - 1.0          # the day's return, inside the window
            nxt = close.shift(-1) / close - 1.0          # next-day return, inside the window
            rets_all.append(ret1.dropna().values)
            raw = _get_component(df, "scaled_rise", "last_history_value")
            rise = raw.where(raw.notna(), ret1)          # sign of scaled return = sign of return
            regime = df["regime"].astype(str)
            in_profile = regime != "chop"
            situation = in_profile & (rise > 0)
            active = fc.notna() & (fc != 0)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
            day = _to_day(df["timestamp"])
            per_win.append(pd.DataFrame({"coin": coin, "day": day.values,
                                         "fc": fc.values, "nxt": nxt.values}))
        if not per_win:
            continue
        allr = np.concatenate(rets_all) if rets_all else np.array([])
        coin_mean = float(np.mean(allr)) if len(allr) else np.nan
        cf = pd.concat(per_win, ignore_index=True)
        cf["excess"] = cf["nxt"] - coin_mean
        coin_frames.append(cf)

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    main_name = "forecast-weighted mean next-day excess return (over coin's all-window mean daily return)"
    main_thr = "confirm: positive with t >= 2 and slope > 0; reject: negative with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars of a one-day "
                           "scaled rise inside the rising agitated profile (regime not chop)."
                           if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": "The profile is read from the recorded regime (not chop = rising agitated) and the rise from the scaled_rise raw value, or the day's return where it is not recorded.",
        }

    # ---------- 2. criterion ----------
    data = pd.concat(coin_frames, ignore_index=True) if coin_frames else pd.DataFrame(
        columns=["coin", "day", "fc", "nxt", "excess"])
    sel = data[(data["fc"] > 0) & data["excess"].notna()].copy()
    n_cases = int(len(sel))
    n_days = int(sel["day"].nunique()) if n_cases else 0

    value = None
    tval = None
    slope = None
    if n_cases > 0:
        f = sel["fc"].values.astype(float)
        x = sel["excess"].values.astype(float)
        sw = f.sum()
        value = float((f * x).sum() / sw)
        dev = f * (x - value) / sw
        D = pd.Series(dev).groupby(sel["day"].values).sum().values
        G = len(D)
        if G > 1:
            se = np.sqrt(G / (G - 1.0) * np.sum(D ** 2))
            tval = float(value / se) if se > 0 else None
        if n_cases > 2 and np.ptp(f) > 0:
            slope = float(stats.linregress(f, x).slope)

    counts = {"cases": n_cases, "distinct days": n_days}
    sup_passed = (slope > 0) if slope is not None else None
    supporting = {"name": "OLS slope of next-day excess return on forecast",
                  "value": slope, "passed": sup_passed}
    statistic = {"name": "t of weighted mean, cases of one day summed", "value": tval} if tval is not None else None

    if n_cases < 100 or n_days < 100:
        status = "not observable"
        decided = (f"Minimum count not reached: {n_cases} cases (need 100) on {n_days} distinct days (need 100).")
    elif tval is None:
        status = "inconclusive"
        decided = "The t could not be computed, so the numbers meet neither the confirm nor the reject rule."
    elif value > 0 and tval >= 2 and sup_passed is True:
        status = "confirmed"
        decided = "The forecast-weighted mean excess return is positive with t >= 2 and the slope is above 0."
    elif value < 0 and tval <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess return is negative with t <= -2."
    elif value > 0 and tval >= 2:
        status = "inconclusive"
        decided = "A positive t >= 2 with a slope at or below 0 is inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": value, "statistic": statistic, "threshold": main_thr},
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": ("The coin's mean daily return is the mean of all its within-window daily returns, the t uses "
                    "day-clustered deviations of the weighted mean (forecast-weighted, summed per UTC day), the "
                    "profile is read from the recorded regime (not chop), and the plan's minimum of 100 cases "
                    "and 100 days is applied as 'not observable'."),
    }
