import numpy as np
import pandas as pd
from scipy import stats


def _to_utc(ts):
    s = pd.Series(ts)
    if np.issubdtype(s.dtype, np.number):
        v = s.astype(float)
        med = np.nanmedian(np.abs(v.values)) if len(v) else 0.0
        if med > 1e17:
            unit = "ns"
        elif med > 1e14:
            unit = "us"
        elif med > 1e11:
            unit = "ms"
        else:
            unit = "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 2
    MIN_CASES = 200
    LHV = "debug_info.components.rise14.last_history_value"

    # ---------- per window preparation ----------
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True).copy()
            ts = _to_utc(d["timestamp"]).reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").astype(float).reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").astype(float).fillna(0.0).reset_index(drop=True)
            # 14-day return: recorded raw value where present, else recomputed from prices inside the window
            ret14_calc = close / close.shift(14) - 1.0
            if LHV in d.columns:
                rec = pd.to_numeric(d[LHV], errors="coerce").astype(float).reset_index(drop=True)
                ret14 = rec.where(rec.notna(), ret14_calc)
            else:
                ret14 = ret14_calc
            # Thursday close: the coming (next) bar is a Friday (weekday 4)
            next_wd = (ts + pd.Timedelta(days=1)).dt.weekday
            thursday = (next_wd == 4).values
            fwd2 = (close.shift(-H) / close - 1.0).values
            prepared[coin][w] = dict(close=close.values, fc=fc.values, ret14=ret14.values,
                                     thursday=thursday, fwd2=fwd2)

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in prepared.items():
        for w, p in wins.items():
            active = p["fc"] != 0
            sit = p["thursday"] & (np.nan_to_num(p["ret14"], nan=-np.inf) > 0)
            n_active += int(active.sum())
            n_agree += int((active & sit & (p["fc"] > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    threshold_txt = "slope t >= 2 with positive forecast-weighted mean excess confirms; t <= -2 rejects; at least 200 cases"
    main_name = "pooled OLS slope of excess 2-bar return on forecast, Thursday-close bars with forecast > 0"
    sup_name = "forecast-weighted mean excess 2-bar return > 0"
    reading = ("Thursday-close bars are those whose next bar (timestamp + 1 day, UTC) is a Friday; the coin's normal "
               "2-bar drift is the mean of non-overlapping 2-bar returns on a grid from each window's first row, pooled "
               "over all its windows; cases need close[t+2] inside the same window; the 14-day return is the recorded "
               "raw value or, where missing, recomputed from closes; the plan's 200-case minimum is applied as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are Thursday-close bars with a positive "
                           "14-day return and a long forecast, as the plan's Fidelity requires."
                           if n_active > 0 else "No bar has a non-zero forecast, so the test cannot show the plan's situation."),
            "reading": reading,
        }

    # ---------- coin drift ----------
    drift = {}
    for coin, wins in prepared.items():
        rets = []
        for w, p in wins.items():
            c = p["close"]
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                rets.extend([x for x in r if np.isfinite(x)])
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    xs, ys = [], []
    for coin, wins in prepared.items():
        if not np.isfinite(drift[coin]):
            continue
        for w, p in wins.items():
            sel = p["thursday"] & (p["fc"] > 0) & np.isfinite(p["fwd2"])
            for i in np.where(sel)[0]:
                xs.append(float(p["fc"][i]))
                ys.append(float(p["fwd2"][i] - drift[coin]))
    x = np.array(xs)
    y = np.array(ys)
    n = int(len(x))

    slope = None
    t = None
    if n >= 3 and np.ptp(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    wmean = float(np.sum(x * y) / np.sum(x)) if n > 0 and np.sum(x) > 0 else None
    sup_pass = (wmean is not None and wmean > 0) if wmean is not None else None

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases, below the plan's minimum of {MIN_CASES} cases."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no spread in the forecast), which meets neither the confirm nor the reject rule."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope has t >= 2 and the forecast-weighted mean excess return is above 0 (confirm rule)."
    elif t <= -2:
        status = "rejected"
        decided = "The slope has t <= -2 (reject rule)."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope has t >= 2 but the forecast-weighted mean excess return is <= 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The slope has -2 < t < 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": t} if t is not None else None),
                         "threshold": threshold_txt},
        "supporting_check": {"name": sup_name, "value": wmean, "passed": sup_pass},
        "counts": {"cases": n},
        "decided_by": decided,
        "reading": reading,
    }
