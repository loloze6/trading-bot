import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 48
    RAW = "debug_info.components.weekend_loss.last_history_value"
    MIN_WEEKS = 100

    def to_ts(s):
        if pd.api.types.is_numeric_dtype(s):
            mx = float(np.nanmax(s.values)) if len(s) else 0.0
            unit = "ms" if mx > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    active_total = 0
    active_agree = 0
    cases = []  # (coin, week_key, unusual_move, forecast)

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        # normal drift: mean 48-bar return on non-overlapping grid over all windows
        grid_rets = []
        prepared = {}
        for w in sorted(wins.keys(), key=lambda x: (len(str(x)), str(x))):
            df = wins[w].reset_index(drop=True).copy()
            if len(df) == 0:
                continue
            ts = to_ts(df["timestamp"])
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            n = len(close)
            for k in range(0, n - H, H):
                a, b = close[k], close[k + H]
                if np.isfinite(a) and np.isfinite(b) and a != 0:
                    grid_rets.append(b / a - 1.0)
            prepared[w] = (df, ts, close)
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan

        for w, (df, ts, close) in prepared.items():
            n = len(close)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values.astype(float)
            close_time = ts + pd.Timedelta(hours=1)
            is_mon0 = ((close_time.dt.dayofweek == 0) & (close_time.dt.hour == 0)
                       & (close_time.dt.minute == 0)).values
            # raw 48-bar return: recorded value, else recomputed from prices in the window
            recomputed = pd.Series(close).pct_change(H).values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values.astype(float)
                raw = np.where(np.isfinite(raw), raw, recomputed)
            else:
                raw = recomputed
            situation = is_mon0 & np.isfinite(raw) & (raw < 0)

            act = fc != 0
            active_total += int(act.sum())
            active_agree += int((act & situation & (fc > 0)).sum())

            # cases: forecast > 0 on a Monday 00:00 signal bar
            idx = np.where((fc > 0) & is_mon0)[0]
            for i in idx:
                if i + H >= n:
                    continue
                a, b = close[i], close[i + H]
                if not (np.isfinite(a) and np.isfinite(b) and a != 0 and np.isfinite(drift)):
                    continue
                um = (b / a - 1.0) - drift
                wk = close_time.iloc[i].normalize().strftime("%Y-%m-%d")
                cases.append((coin, wk, float(um), float(fc[i])))

    main_name = "mean over weeks of the cross-coin average unusual 48-bar move after a weekend-loss signal"
    thr = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2"
    reading = ("The signal bar is the bar whose close (timestamp + 1h) is Monday 00:00 UTC and the situation is a "
               "negative 48-bar raw return on it; a week is identified by that Monday's date; drift is the coin's mean "
               "48-bar return on a non-overlapping grid from each window's first row; fewer than 100 weeks with a case "
               "is treated as the minimum count not reached (not observable).")

    if active_total == 0:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": 0.0, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": 0},
            "decided_by": "The forecast is never non-zero, so it never takes the long bet after a weekend fall that the plan's situation calls for.",
            "reading": reading,
        }

    agreement = active_agree / active_total
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(active_total)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bets on the bar closing at "
                           "Monday 00:00 UTC after a 48-bar (weekend) fall, as the plan's situation requires."),
            "reading": reading,
        }

    cdf = pd.DataFrame(cases, columns=["coin", "week", "um", "fc"])
    n_cases = int(len(cdf))
    weekly = cdf.groupby("week")["um"].mean() if n_cases else pd.Series(dtype=float)
    n_weeks = int(len(weekly))

    mean_w = float(weekly.mean()) if n_weeks else None
    t_w = None
    if n_weeks >= 2:
        sd = float(weekly.std(ddof=1))
        if sd > 0:
            t_w = float(mean_w / (sd / np.sqrt(n_weeks)))

    slope = None
    if n_cases >= 3 and cdf["fc"].nunique() > 1:
        slope = float(stats.linregress(cdf["fc"].values, cdf["um"].values).slope)
    slope_pass = (slope > 0) if slope is not None else None

    counts = {"weeks that hold a case": n_weeks, "cases": n_cases}
    stat = {"name": "t of the mean over weeks", "value": t_w} if t_w is not None else None
    supp = {"name": "slope of unusual move on signal-bar forecast", "value": slope, "passed": slope_pass}

    if n_weeks < MIN_WEEKS:
        status = "not observable"
        decided = f"Only {n_weeks} weeks hold a case, fewer than the plan's minimum of 100."
    elif t_w is None:
        status = "inconclusive"
        decided = "The t over weeks cannot be computed (zero spread), so neither the confirm nor the reject rule is met."
    elif mean_w > 0 and t_w >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 and the slope on the forecast is positive."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the slope on the forecast is not positive, which the plan calls inconclusive."
    elif mean_w < 0 and t_w <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t over weeks lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean_w, "statistic": stat, "threshold": thr},
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
