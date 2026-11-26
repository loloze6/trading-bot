import numpy as np
import pandas as pd
from scipy import stats


def _to_time(s):
    if np.issubdtype(s.dtype, np.number):
        mx = float(np.nanmax(s.values)) if len(s) else 0.0
        unit = "ms" if mx > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    RISE = "debug_info.components.rise.last_history_value"
    POS = "postRebalance_current_allocation"

    # ---------- coin drift: mean daily return over all windows (within windows only) ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            r = (c.shift(-1) / c - 1.0).dropna()
            rets.append(r.values)
        allr = np.concatenate(rets) if rets else np.array([])
        drift[coin] = float(np.mean(allr)) if allr.size else np.nan

    # ---------- collect rows ----------
    n_active = 0
    n_agree = 0
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            fc = d["forecast"].astype(float)
            regime = d["regime"].astype(str)

            # raw zret: recorded rise value; recompute from prices where missing
            r1 = c / c.shift(1) - 1.0
            z_px = r1 / r1.rolling(30, min_periods=30).std()
            if RISE in d.columns:
                z = d[RISE].astype(float).where(d[RISE].notna(), z_px)
            else:
                z = z_px

            situation = (regime == "mean_reversion") & (z > 0.0) & (z <= 1.0)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            # criterion rows: 1-bar grid = every bar of the window
            nxt = c.shift(-1) / c - 1.0
            pos = d[POS].astype(float)
            day = _to_time(d["timestamp"]).dt.floor("D")
            mu = drift[coin]
            sel = pos.notna() & (pos != 0) & nxt.notna()
            for i in np.where(sel.values)[0]:
                p = pos.iloc[i]
                rows.append({
                    "day": day.iloc[i],
                    "excess": p * nxt.iloc[i] - p * mu,
                    "dir_ret": np.sign(p) * (nxt.iloc[i] - mu),
                    "absf": abs(fc.iloc[i]) if pd.notna(fc.iloc[i]) else np.nan,
                })

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = (agreement >= 0.9) if agreement is not None else None

    reading = ("The falling-agitated profile is taken from the recorded regime (the profile vetoes send every other bar "
               "to chop, and its 60/365-bar inputs cannot be rebuilt inside the 120-bar windows) together with the "
               "recorded raw rise in (0, 1], expected side short; cases are all bars with a nonzero position on the "
               "1-bar grid, the day-clustered t sums each day's deviations from the mean, and the plan's "
               "'fewer than 100 cases' is reported as not observable.")

    main_name = "mean excess gain per position bar (position x next-day return minus position x coin drift)"
    thr = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2"

    if passed is False:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases on the 1-bar grid": len(rows), "active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are short bars of the falling agitated "
                           "regime with 0 < rise/30-day std <= 1."),
            "reading": reading,
        }

    R = pd.DataFrame(rows, columns=["day", "excess", "dir_ret", "absf"])
    n = int(len(R))
    n_days = int(R["day"].nunique()) if n else 0

    mean = float(R["excess"].mean()) if n else None
    t = None
    if n >= 2 and n_days >= 2:
        dev = R["excess"] - mean
        D = dev.groupby(R["day"]).sum().values
        var = (n_days / (n_days - 1)) * float(np.sum(D ** 2)) / (n ** 2)
        if var > 0:
            t = float(mean / np.sqrt(var))

    slope = None
    S = R.dropna(subset=["dir_ret", "absf"])
    if len(S) >= 3 and S["absf"].nunique() > 1:
        slope = float(stats.linregress(S["absf"].values, S["dir_ret"].values).slope)
    slope_pass = (slope is not None and slope > 0)

    counts = {"cases on the 1-bar grid": n, "days": n_days, "active bars": n_active}

    if n < 100:
        status = "not observable"
        decided = f"Only {n} cases on the 1-bar grid, below the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean excess gain could not be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and t >= 2 and slope_pass:
        status = "confirmed"
        decided = "The mean excess gain is above 0 with t >= 2 and the slope on |forecast| is above 0."
    elif mean > 0 and t >= 2:
        status = "inconclusive"
        decided = "The mean excess gain is above 0 with t >= 2 but the slope on |forecast| is at or below 0."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean excess gain is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess gain lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": None if t is None else {"name": "t of the mean, cases of one day pooled", "value": t},
            "threshold": thr,
        },
        "supporting_check": {
            "name": "slope of signal-direction next-day return minus drift on |forecast|",
            "value": slope,
            "passed": slope_pass if slope is not None else False,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
