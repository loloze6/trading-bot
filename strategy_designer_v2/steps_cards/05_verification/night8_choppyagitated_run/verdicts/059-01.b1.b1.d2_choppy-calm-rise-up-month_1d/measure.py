import numpy as np
import pandas as pd

H = 14
BAND = 2.0
COL_RAW = "debug_info.components.week_rise.last_history_value"


def _bets(fc):
    """Long-side bets: a rise of the forecast of at least BAND from its lowest level
    on the long side since the last bet (from 0 after a flat or a change of side)."""
    fc = np.asarray(fc, dtype=float)
    out = np.zeros(len(fc), dtype=bool)
    low = 0.0
    for i, f in enumerate(fc):
        if not np.isfinite(f) or f <= 0:
            low = 0.0
            continue
        if f - low >= BAND:
            out[i] = True
            low = f
        else:
            low = min(low, f)
    return out


def _cluster_t(x, days):
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 2:
        return None
    m = x.mean()
    s = pd.Series(x - m).groupby(np.asarray(days)).sum().values
    g = len(s)
    if g < 2:
        return None
    var = (g / (g - 1.0)) * np.sum(s ** 2) / n ** 2
    if var <= 0:
        return None
    return float(m / np.sqrt(var))


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            regime = df["regime"].astype(str).values
            raw = (pd.to_numeric(df[COL_RAW], errors="coerce").values
                   if COL_RAW in df.columns else np.full(len(df), np.nan))
            ret30 = np.full(len(df), np.nan)
            if len(df) > 30:
                ret30[30:] = close[30:] / close[:-30] - 1.0
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active += 1
                sit = (regime[i] == "trending") and np.isfinite(raw[i]) and raw[i] > 0
                if sit and np.isfinite(ret30[i]) and not (ret30[i] > 0):
                    sit = False
                if sit and fc[i] > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean unusual 14-bar move of the cases (forecast rise >= 2, one per 14-bar grid cell)"
    thr = "confirm: mean > 0 with day-clustered t >= 2 and slope > 0; reject: t <= -2 or slope t <= -2"
    reading_base = ("Situation = regime 'trending' (choppy-calm profile plus 30-day return > 0, recomputed from prices "
                    "where 30 prior bars exist) with week_rise raw value > 0, side long; a case is the first long-side bet "
                    "(forecast rise >= 2 from its lowest level since the last bet, reset at flat) in each 14-bar grid cell "
                    "of its window, its 14-bar return read inside the window; the drift is the coin's mean 14-bar return "
                    "on the grid over all its windows; the t clusters cases by UTC signal day with a G/(G-1) correction; "
                    "the slope is OLS on grid bars with forecast > 0; the plan's 'fewer than 30 cases/days' is reported "
                    "as not observable as the workflow requires.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None, "distinct days": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of the plan's situation "
                           "(trending regime in the choppy-calm profile with a 7-day rise), so the config does not do "
                           "what the Fidelity says."),
            "reading": reading_base,
        }

    # ---------- 2. drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(close) - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    rets.append(r)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases and slope points ----------
    case_x, case_day = [], []
    sl_f, sl_y = [], []
    for coin, wins in bars.items():
        d = drift[coin]
        if not np.isfinite(d):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            bets = _bets(fc)
            n = len(df)
            for start in range(0, n, H):
                end = min(start + H, n)
                # case
                idx = np.where(bets[start:end])[0]
                if len(idx) > 0:
                    t = start + int(idx[0])
                    if t + H < n:
                        r = close[t + H] / close[t] - 1.0
                        if np.isfinite(r):
                            case_x.append(r - d)
                            case_day.append(ts.iloc[t].strftime("%Y-%m-%d"))
                # slope point on grid bar
                if start + H < n and fc[start] > 0:
                    r = close[start + H] / close[start] - 1.0
                    if np.isfinite(r):
                        sl_f.append(fc[start])
                        sl_y.append(r - d)

    n_cases = len(case_x)
    n_days = len(set(case_day))
    mean_u = float(np.mean(case_x)) if n_cases else None
    t_u = _cluster_t(case_x, case_day) if n_cases else None

    slope, slope_t = None, None
    if len(sl_f) >= 3:
        f = np.asarray(sl_f, float)
        y = np.asarray(sl_y, float)
        fm = f - f.mean()
        sxx = np.sum(fm ** 2)
        if sxx > 0:
            slope = float(np.sum(fm * (y - y.mean())) / sxx)
            resid = y - (y.mean() + slope * fm)
            s2 = np.sum(resid ** 2) / (len(f) - 2)
            se = np.sqrt(s2 / sxx) if s2 > 0 else 0.0
            slope_t = float(slope / se) if se > 0 else None

    counts = {"cases": int(n_cases), "distinct days": int(n_days),
              "slope grid cells": int(len(sl_f)), "active bars": int(n_active)}
    sup = {"name": "slope of drift-adjusted 14-bar return on forecast (grid cells, forecast > 0)",
           "value": slope, "passed": (None if slope is None else bool(slope > 0))}
    if slope_t is not None:
        sup["t"] = slope_t
    main = {"name": main_name, "value": mean_u,
            "statistic": (None if t_u is None else {"name": "t of the mean, cases of one day together", "value": t_u}),
            "threshold": thr}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = f"The plan's minimum of 30 cases on 30 distinct days is not reached ({n_cases} cases, {n_days} days)."
    elif (t_u is not None and t_u <= -2) or (slope_t is not None and slope_t <= -2):
        status = "rejected"
        decided = "Reject rule met: the mean unusual move has t <= -2 or the slope has t <= -2."
    elif mean_u is not None and mean_u > 0 and t_u is not None and t_u >= 2 and slope is not None and slope > 0:
        status = "confirmed"
        decided = "Confirm rule met: mean unusual move above 0 with t >= 2, and the slope is above 0."
    else:
        status = "inconclusive"
        decided = "Neither the confirm nor the reject rule is met (t between -2 and 2, or slope not above 0 without significance)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
