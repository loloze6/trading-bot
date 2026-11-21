import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    VOL_COL = "debug_info.components.vol7d.last_history_value"
    ONE_H = pd.Timedelta(hours=1)
    TWO_H = pd.Timedelta(hours=2)

    def to_ts(s):
        if np.issubdtype(s.dtype, np.number):
            unit = "ms" if s.dropna().abs().max() > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0

    event_ret, event_vol_rec, event_vol_calc = [], [], []
    other_ret = []

    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = to_ts(df["timestamp"]).reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            # hour at which the coming bar starts (= close time of this bar)
            next_hour = (ts + ONE_H).dt.hour.to_numpy()
            ts_hour = ts.dt.hour.to_numpy()

            situation = np.isin(next_hour, [20, 21])
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

            # recomputed 7-day vol: std of the last 168 hourly returns, inside the window
            r1 = pd.Series(close).pct_change()
            ts_ok = (ts.diff() == ONE_H).to_numpy()
            r1 = r1.where(ts_ok)
            vol_calc = r1.rolling(168, min_periods=168).std().to_numpy()
            if VOL_COL in df.columns:
                vol_rec = pd.to_numeric(df[VOL_COL], errors="coerce").to_numpy(dtype=float)
            else:
                vol_rec = np.full(len(df), np.nan)

            n = len(df)
            ts_arr = ts.to_numpy()
            for i in range(n - 2):
                h = ts_hour[i]
                if h % 2 == 0:
                    continue  # blocks start at closes on even UTC hours (bars starting on odd hours)
                if ts_arr[i + 2] - ts_arr[i] != np.timedelta64(2, "h"):
                    continue
                if not (np.isfinite(close[i]) and np.isfinite(close[i + 2]) and close[i] > 0):
                    continue
                ret = close[i + 2] / close[i] - 1.0
                if h == 19:
                    event_ret.append(ret)
                    event_vol_rec.append(vol_rec[i])
                    event_vol_calc.append(vol_calc[i])
                else:
                    other_ret.append(ret)

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    threshold_txt = "confirm: difference > 0 with Welch t >= 2 (and slope t >= 2); reject: Welch t <= -2 or slope t <= -2"
    main_name = "mean 20:00-22:00 2-bar return minus mean other-hour 2-bar return"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars whose coming bar "
                           "starts at 20:00 or 21:00 UTC, so the config does not hold the plan's long-only "
                           "20:00-22:00 situation."),
            "reading": "The situation is the bars whose next bar starts at 20:00 or 21:00 UTC (bar start 19:00 or 20:00), side long.",
        }

    ev = np.asarray(event_ret, dtype=float)
    ot = np.asarray(other_ret, dtype=float)
    n_ev = int(ev.size)
    n_ot = int(ot.size)

    # main measure
    diff = None
    t_main = None
    if n_ev >= 2 and n_ot >= 2:
        diff = float(ev.mean() - ot.mean())
        t_main = float(stats.ttest_ind(ev, ot, equal_var=False).statistic)

    # supporting check: slope of event return on vol7d at the 19:00 bar
    vr = np.asarray(event_vol_rec, dtype=float)
    vc = np.asarray(event_vol_calc, dtype=float)
    use_recorded = n_ev > 0 and np.isfinite(vr).sum() >= 0.5 * n_ev
    vol = vr if use_recorded else vc
    m = np.isfinite(vol) & np.isfinite(ev) if n_ev > 0 else np.array([], dtype=bool)
    slope = None
    t_slope = None
    n_reg = int(m.sum()) if n_ev > 0 else 0
    if n_reg >= 3 and np.std(vol[m]) > 0:
        lr = stats.linregress(vol[m], ev[m])
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    slope_pass = None if t_slope is None else bool(t_slope >= 2)

    counts = {
        "daily 20:00-22:00 cases": n_ev,
        "other-hour cases": n_ot,
        "regression cases": n_reg,
    }

    reading = ("Cases are 2-bar returns on bars starting at odd UTC hours (closes on even hours) within each window "
               "with exactly 2 hours between the two closes, the bar starting at 19:00 giving the 20:00-22:00 case "
               "and all other such blocks the other-hour cases; vol7d is the recorded last_history_value at the "
               "19:00 bar (recomputed as the std of 168 hourly returns only if it is not recorded on most of those "
               "bars, rows missing it left out). "
               + ("Recorded vol7d used." if use_recorded else "Recomputed vol7d used."))

    if n_ev < 500 or n_ot < 1500:
        status = "not observable"
        missing = []
        if n_ev < 500:
            missing.append(f"only {n_ev} daily 20:00-22:00 cases (minimum 500)")
        if n_ot < 1500:
            missing.append(f"only {n_ot} other-hour cases (minimum 1500)")
        decided = "Minimum count not reached: " + "; ".join(missing) + "."
    elif (t_main is not None and t_main <= -2) or (t_slope is not None and t_slope <= -2):
        status = "rejected"
        decided = "Reject rule met: the main difference has Welch t <= -2 or the volatility slope has t <= -2."
    elif diff is not None and diff > 0 and t_main is not None and t_main >= 2 and slope_pass:
        status = "confirmed"
        decided = "Confirm rule met: the main difference is positive with Welch t >= 2 and the volatility slope has t >= 2."
    else:
        status = "inconclusive"
        if t_main is not None and t_main >= 2 and diff is not None and diff > 0:
            decided = "Inconclusive: the main difference is positive with Welch t >= 2 but the volatility slope t is not >= 2."
        else:
            decided = "Inconclusive: the main Welch t is between -2 and 2 and no reject rule is met."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": diff,
            "statistic": None if t_main is None else {"name": "Welch t", "value": t_main},
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "t of slope of 20:00-22:00 return on vol7d at 19:00 bar (must be >= 2)",
            "value": t_slope,
            "passed": slope_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
