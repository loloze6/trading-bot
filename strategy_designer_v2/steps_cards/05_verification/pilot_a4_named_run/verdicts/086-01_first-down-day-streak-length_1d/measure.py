import json
import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    BAND = 2.0
    COMP = "broken_run"

    def _ts(s):
        if np.issubdtype(s.dtype, np.number):
            v = float(np.nanmax(np.abs(s.values))) if len(s) else 0.0
            unit = "ms" if v > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    def _lhv(df):
        col = "debug_info.components.%s.last_history_value" % COMP
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").values.astype(float)
        out = np.full(len(df), np.nan)
        if "debug_info.components" in df.columns:
            for i, v in enumerate(df["debug_info.components"].values):
                d = v
                if isinstance(d, str):
                    try:
                        d = json.loads(d)
                    except Exception:
                        d = None
                if isinstance(d, dict):
                    c = d.get(COMP)
                    if isinstance(c, dict):
                        x = c.get("last_history_value")
                        try:
                            out[i] = float(x)
                        except Exception:
                            pass
        return out

    # ---------- prepare ----------
    prepared = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values.astype(float)
            regime = d["regime"].astype(str).values if "regime" in d.columns else np.array([""] * len(d))
            prepared[(coin, w)] = {
                "close": close, "fc": fc, "regime": regime,
                "lhv": _lhv(d), "ts": _ts(d["timestamp"]),
            }

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for key, p in prepared.items():
        close, fc, lhv, regime = p["close"], p["fc"], p["lhv"], p["regime"]
        prev = np.concatenate([[np.nan], close[:-1]])
        down = np.where(np.isnan(prev), True, close < prev)
        situ = (lhv >= 2) & down & (regime == "trending")
        active = fc != 0
        n_active += int(active.sum())
        n_agree += int((active & situ & (fc < 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean short-direction unusual 3-bar move per case"
    main_thr = "mean > 0 with day-clustered t >= 2 confirms (with slope check); mean < 0 with t <= -2 rejects"
    sup_name = "OLS slope of unusual move on broken run length, t >= 1.5"
    reading = ("Situation = recorded broken_run count >= 2 on a down close (first window row accepted on the count alone) "
               "in regime 'trending' (profile vetoes passed), side short; a case is the first short bet (forecast magnitude "
               "rising >= 2 points from its lowest level since the last bet, from 0 after flat) in each 3-bar grid cell of a "
               "window, its return taken from that bar's close over 3 bars inside the window; drift = mean of the coin's "
               "non-overlapping 3-bar grid returns over all its windows; day-clustered t uses a G/(G-1) correction; slope t is "
               "the ordinary OLS t; the plan's 'fewer than 30 cases on 30 distinct days' is treated as the minimum count.")

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases": None, "distinct days": None},
            "decided_by": ("Only %.1f%% of active bars are short bars on a down close breaking a run of 2+ up days in the "
                           "trending (rising-agitated) regime, below 90%%." % (100 * agreement)),
            "reading": reading,
        }

    # ---------- normal drift per coin ----------
    drift = {}
    rets_by_coin = {}
    for (coin, w), p in prepared.items():
        c = p["close"]
        idx = np.arange(0, len(c) - H, H)
        r = c[idx + H] / c[idx] - 1.0
        r = r[np.isfinite(r)]
        rets_by_coin.setdefault(coin, []).extend(r.tolist())
    for coin, r in rets_by_coin.items():
        drift[coin] = float(np.mean(r)) if len(r) else np.nan

    # ---------- cases ----------
    cases = []
    for (coin, w), p in prepared.items():
        c, fc, lhv, ts = p["close"], p["fc"], p["lhv"], p["ts"]
        n = len(c)
        bet = np.zeros(n, dtype=bool)
        ref = 0.0
        for i in range(n):
            m = -fc[i] if fc[i] < 0 else 0.0
            if m <= 0:
                ref = 0.0
                continue
            if m - ref >= BAND:
                bet[i] = True
                ref = m
            else:
                ref = min(ref, m)
        for start in range(0, n, H):
            cell = np.where(bet[start:start + H])[0]
            if len(cell) == 0:
                continue
            t = start + int(cell[0])
            if t + H >= n:
                continue
            r = c[t + H] / c[t] - 1.0
            dr = drift.get(coin, np.nan)
            if not (np.isfinite(r) and np.isfinite(dr)):
                continue
            u = -(r - dr)
            day = pd.Timestamp(ts.iloc[t]).strftime("%Y-%m-%d")
            cases.append((u, lhv[t], day))

    n_cases = len(cases)
    days = sorted(set(x[2] for x in cases))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}
    sc = {"agreement": (float(agreement) if agreement is not None else None), "passed": passed}

    if n_cases < 30 or n_days < 30:
        mean_u = float(np.mean([x[0] for x in cases])) if n_cases else None
        return {
            "status": "not observable",
            "situation_check": sc,
            "main_measure": {"name": main_name, "value": mean_u, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": "Minimum not reached: fewer than 30 cases on at least 30 distinct days (%d cases, %d days)."
                          % (n_cases, n_days),
            "reading": reading,
        }

    u = np.array([x[0] for x in cases], dtype=float)
    mean_u = float(u.mean())
    dev = pd.Series(u - mean_u).groupby([x[2] for x in cases]).sum().values
    G = len(dev)
    var = (dev ** 2).sum() / n_cases ** 2 * (G / (G - 1.0) if G > 1 else 1.0)
    se = np.sqrt(var)
    t_main = float(mean_u / se) if se > 0 else 0.0

    L = np.array([x[1] for x in cases], dtype=float)
    ok = np.isfinite(L) & np.isfinite(u)
    slope = None
    slope_t = None
    sup_pass = False
    if ok.sum() >= 3 and np.std(L[ok]) > 0:
        lr = stats.linregress(L[ok], u[ok])
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else 0.0
        sup_pass = bool(slope > 0 and slope_t >= 1.5)

    if mean_u > 0 and t_main >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Confirm: mean unusual move above 0 with t >= 2 and the slope on run length positive with t >= 1.5."
        else:
            status = "inconclusive"
            decided = "Inconclusive: the mean meets the confirm rule but the slope check fails."
    elif mean_u < 0 and t_main <= -2:
        status = "rejected"
        decided = "Reject: mean unusual move below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": {"name": "t of the mean, same-day cases summed", "value": t_main},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": slope_t, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
