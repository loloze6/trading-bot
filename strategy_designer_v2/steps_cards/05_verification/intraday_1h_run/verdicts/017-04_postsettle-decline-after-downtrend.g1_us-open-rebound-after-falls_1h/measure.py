import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.fall72.last_history_value"
    H = 2
    MIN_CASES = 300

    def prep(df):
        d = df.copy()
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
        d = d.sort_values("timestamp").reset_index(drop=True)
        return d

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = prep(df)
            if len(d) == 0:
                continue
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            # raw 72-bar percent change: the recorded value, else recomputed from prices inside the window
            recomputed = d["close"] / d["close"].shift(72) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").fillna(recomputed)
            else:
                raw = recomputed
            # the coming bar starts at 12:00 or 13:00 UTC -> bars stamped 11:00 or 12:00
            coming_hour = (d["timestamp"] + pd.Timedelta(hours=1)).dt.hour
            in_clock = coming_hour.isin([12, 13])
            fell = raw < 0
            active = fc.notna() & (fc != 0)
            agree = active & in_clock & fell & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "mean of (forecast/10) x excess 2-bar return from the 11:00 bar's close, pooled over coins"
    threshold = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; at least 300 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": 0},
            "decided_by": ("No active bars in the record." if agreement is None else
                           f"Only {agreement:.1%} of active bars are long on bars stamped 11:00/12:00 UTC "
                           "after a 72-bar fall, below the 90% needed for the plan's situation."),
            "reading": "The situation is a bar stamped 11:00 or 12:00 UTC (coming bar 12:00 or 13:00) with a negative "
                       "72-bar price change, on the long side.",
        }

    # ---------- 2. criterion ----------
    values, fcs, excess = [], [], []
    for coin, wins in bars.items():
        # coin's mean 2-bar return over all windows, non-overlapping grid 0, 2, 4, ... of each window
        grid_rets = []
        prepped = {}
        for w, df in wins.items():
            d = prep(df)
            prepped[w] = d
            c = d["close"].to_numpy(dtype=float)
            if len(c) > H:
                idx = np.arange(0, len(c) - H, H)
                r = c[idx + H] / c[idx] - 1.0
                grid_rets.append(r[np.isfinite(r)])
        if not grid_rets:
            continue
        allr = np.concatenate(grid_rets)
        if len(allr) == 0:
            continue
        mu = float(np.mean(allr))

        seen_days = set()
        for w, d in prepped.items():
            if len(d) == 0:
                continue
            close_by_ts = pd.Series(d["close"].to_numpy(dtype=float), index=d["timestamp"])
            close_by_ts = close_by_ts[~close_by_ts.index.duplicated(keep="first")]
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            mask = (d["timestamp"].dt.hour == 11) & (d["timestamp"].dt.minute == 0) & (fc > 0)
            for i in np.where(mask.to_numpy())[0]:
                ts = d["timestamp"].iloc[i]
                day = ts.normalize()
                if day in seen_days:
                    continue
                ts13 = ts + pd.Timedelta(hours=2)
                if ts13 not in close_by_ts.index:
                    continue
                c0 = float(d["close"].iloc[i])
                c2 = float(close_by_ts.loc[ts13])
                f = float(fc.iloc[i])
                if not (np.isfinite(c0) and np.isfinite(c2) and np.isfinite(f)) or c0 == 0:
                    continue
                ex = c2 / c0 - 1.0 - mu
                seen_days.add(day)
                values.append(f / 10.0 * ex)
                fcs.append(f)
                excess.append(ex)

    n = len(values)
    v = np.asarray(values, dtype=float)
    mean = float(v.mean()) if n > 0 else None
    t = None
    if n > 1:
        sd = float(v.std(ddof=1))
        t = float(mean / (sd / np.sqrt(n))) if sd > 0 else None
    slope = None
    if n > 2 and np.ptp(np.asarray(fcs)) > 0:
        slope = float(stats.linregress(np.asarray(fcs), np.asarray(excess)).slope)
    slope_ok = None if slope is None else bool(slope > 0)

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's minimum of 300 cases."
    elif mean is not None and t is not None and mean > 0 and t >= 2 and slope_ok:
        status = "confirmed"
        decided = "The main measure has a mean above 0 with t >= 2 and the slope is above 0."
    elif mean is not None and t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "The main measure has a mean below 0 with t <= -2."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope is 0 or below (or undefined), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or is undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": None if t is None else {"name": "ordinary t of the mean", "value": t},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "OLS slope of excess 2-bar return on forecast",
            "value": slope,
            "passed": slope_ok,
        },
        "counts": {"cases": int(n)},
        "decided_by": decided,
        "reading": "The 2-bar return runs from the close of the bar stamped 11:00 to the close of the bar stamped 13:00 "
                   "of the same window (cases without that bar are dropped), the coin's mean 2-bar return is taken on "
                   "the non-overlapping grid 0, 2, 4, ... of each window pooled over all windows, and fewer than 300 "
                   "cases is reported as not observable.",
    }
