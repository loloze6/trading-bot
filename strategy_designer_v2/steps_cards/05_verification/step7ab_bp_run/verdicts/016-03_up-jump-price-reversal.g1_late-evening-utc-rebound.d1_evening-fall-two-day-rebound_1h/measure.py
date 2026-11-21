import numpy as np
import pandas as pd
from scipy import stats


def _ts(series):
    s = series
    if np.issubdtype(s.dtype, np.number):
        v = s.astype("float64")
        unit = "ms" if np.nanmedian(np.abs(v.values)) > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 48
    RAW = "debug_info.components.fall24.last_history_value"

    n_active = 0
    n_agree = 0
    coin_frames = {}

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        prepared = []
        for w in sorted(wins.keys(), key=lambda k: (len(str(k)), str(k))):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.copy()
            ts = _ts(df["timestamp"])
            df = df.assign(_ts=ts.values).sort_values("_ts").reset_index(drop=True)
            ts = pd.Series(pd.to_datetime(df["_ts"], utc=True))
            close = df["close"].astype(float).reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").reset_index(drop=True)
            close_time = ts + pd.Timedelta(hours=1)
            close_hour = close_time.dt.hour.values
            # raw 24-bar fall: recorded value, else recomputed from prices inside the window
            recomputed = (close / close.shift(24) - 1.0) * 100.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").reset_index(drop=True)
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            # situation check
            active = fc.notna() & (fc != 0)
            situ = (close_hour == 20) & (raw < 0).values & (fc > 0).values
            n_active += int(active.sum())
            n_agree += int((active.values & situ).sum())
            prepared.append((close, fc, close_hour, close_time))
        coin_frames[coin] = prepared

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    situation_check = {"agreement": float(agreement), "passed": passed}

    main_name = "pooled OLS slope of 48-bar excess return on forecast, 20:00-close cases"
    threshold = "confirm if slope t >= 2 (with top-third mean excess > 0); reject if t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "non-overlapping cases": None},
            "decided_by": "Fewer than 90 % of the bars with a non-zero forecast are long bars closing at 20:00 UTC after a 24-bar fall, as the plan's Fidelity situation requires.",
            "reading": "The situation is the bar whose close (timestamp + 1 h) is at 20:00 UTC with a negative raw 24-bar change and a positive forecast.",
        }

    xs, ys = [], []
    for coin, prepared in coin_frames.items():
        # coin's mean 48-bar return over all windows (non-overlapping grid 0, 48, 96, ...)
        grid_rets = []
        for close, fc, ch, ct in prepared:
            c = close.values
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                grid_rets.extend(list(r[np.isfinite(r)]))
        if len(grid_rets) == 0:
            continue
        mu = float(np.mean(grid_rets))
        for close, fc, ch, ct in prepared:
            c = close.values
            f = fc.values
            pos20 = np.where(ch == 20)[0]
            if len(pos20) == 0:
                continue
            days = ct.dt.floor("D").iloc[pos20]
            d0 = days.iloc[0]
            dayidx = ((days - d0) / pd.Timedelta(days=1)).round().astype(int).values
            for p, di in zip(pos20, dayidx):
                if di % 2 != 0:
                    continue
                if not (np.isfinite(f[p]) and f[p] > 0):
                    continue
                if p + H >= len(c):
                    continue
                r = c[p + H] / c[p] - 1.0
                if not np.isfinite(r):
                    continue
                xs.append(float(f[p]))
                ys.append(float(r - mu))

    x = np.array(xs)
    y = np.array(ys)
    n = int(len(x))
    reading = ("Non-overlap is taken as every other calendar day of 20:00-close bars per window, counted from the "
               "window's first one; the coin's mean is over its non-overlapping 48-bar grid across all windows; the top "
               "third is the pooled cases with forecast at or above the pooled 2/3 quantile; fewer than 100 cases is "
               "reported as not observable.")

    slope = None
    tval = None
    top_mean = None
    if n >= 3 and np.ptp(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    if n > 0:
        q = np.quantile(x, 2.0 / 3.0)
        top = y[x >= q]
        top_mean = float(np.mean(top)) if len(top) else None
    n_top = int(np.sum(x >= np.quantile(x, 2.0 / 3.0))) if n > 0 else 0

    sup_pass = None if top_mean is None else bool(top_mean > 0)
    supporting = {"name": "mean excess 48-bar return, top third of forecast", "value": top_mean, "passed": sup_pass}
    counts = {"non-overlapping cases": n, "top-third cases": n_top}
    main = {"name": main_name, "value": slope,
            "statistic": None if tval is None else {"name": "OLS slope t", "value": tval},
            "threshold": threshold}

    if n < 100:
        status = "not observable"
        decided = f"Only {n} non-overlapping cases, fewer than the plan's minimum of 100."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no spread in forecast), so neither confirm nor reject is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is at least 2 and the top-third mean excess return is positive."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is at least 2 but the top-third mean excess return is 0 or below."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: deeper falls are followed by weaker 48-bar moves than holding the coin."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
