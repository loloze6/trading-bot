import numpy as np
import pandas as pd


def _to_dt(s):
    if np.issubdtype(s.dtype, np.number):
        v = s.astype(float)
        med = np.nanmedian(np.abs(v.values)) if len(v) else 0
        unit = "ms" if med > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 5
    RAW = "debug_info.components.dip.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            # distance below 5-day closing high (bar t included), from prices inside the window
            hi5 = close.rolling(5, min_periods=5).max()
            below_px = close < hi5
            # raw component value where recorded (negative = below the high)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            below = pd.Series(np.where(raw.notna(), raw < 0, below_px), index=df.index).astype(bool)
            in_profile = df["regime"].astype(str) == "unknown"
            active = fc.notna() & (fc != 0)
            situ = in_profile & below & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "clustered OLS slope t of 5-bar excess return on forecast (in-profile grid bars)"
    thr = "confirm if t >= 2 (with forecast-weighted mean excess > 0); reject if t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("fewer than 90% of active bars are in-profile (regime 'unknown') bars with the close below "
                           "its 5-day closing high and a long forecast" if n_active > 0 else
                           "no active bars: the config never takes the plan's long position in its situation"),
            "reading": "the rising calm profile is read from the recorded regime 'unknown'; below the high is the raw "
                       "dip value < 0 where recorded, else close below the 5-close rolling max inside the window.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        drift_rets = []
        coin_rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            ts = _to_dt(df["timestamp"])
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                drift_rets.append(r)
                if reg[i] == "unknown" and np.isfinite(fc[i]):
                    coin_rows.append((r, float(fc[i]), ts.iloc[i].strftime("%Y-%m-%d")))
        if not drift_rets:
            continue
        drift = float(np.mean(drift_rets))
        for r, f, d in coin_rows:
            rows.append((r - drift, f, d))

    n_cases = len(rows)
    n_pos = int(sum(1 for _, f, _ in rows if f > 0))
    counts = {"in-profile grid cases": n_cases, "cases with forecast above 0": n_pos}

    t_val = None
    slope = None
    wmean = None
    if n_cases > 0:
        y = np.array([r[0] for r in rows])
        f = np.array([r[1] for r in rows])
        days = np.array([r[2] for r in rows])
        if f.sum() > 0:
            wmean = float(np.sum(y * f) / np.sum(f))
        X = np.column_stack([np.ones(n_cases), f])
        groups = pd.unique(days)
        G = len(groups)
        if n_cases > 2 and G > 1 and np.var(f) > 0:
            XtX_inv = np.linalg.inv(X.T @ X)
            beta = XtX_inv @ X.T @ y
            e = y - X @ beta
            meat = np.zeros((2, 2))
            for g in groups:
                m = days == g
                s = X[m].T @ e[m]
                meat += np.outer(s, s)
            c = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - 2.0))
            V = c * XtX_inv @ meat @ XtX_inv
            slope = float(beta[1])
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            t_val = float(slope / se) if np.isfinite(se) and se > 0 else None

    sup_passed = None if wmean is None else bool(wmean > 0)
    reading = ("profile = recorded regime 'unknown'; grid = rows 0,5,10,... of each window with a 5-bar return inside it; "
               "normal drift = coin's mean 5-bar return on that grid over all its windows; slope t uses a "
               "day-clustered (CR1) OLS standard error, timestamps grouped by UTC date.")

    if n_cases < 100 or n_pos < 50:
        status = "not observable"
        decided = ("minimum not reached: fewer than 100 in-profile grid cases" if n_cases < 100
                   else "minimum not reached: fewer than 50 cases with forecast above 0")
    elif t_val is None:
        status = "inconclusive"
        decided = "the slope's t could not be computed, so neither the confirm nor the reject rule is met"
    elif t_val >= 2 and sup_passed:
        status = "confirmed"
        decided = "slope t >= 2 and forecast-weighted mean excess 5-bar return above 0"
    elif t_val >= 2:
        status = "inconclusive"
        decided = "slope t >= 2 but forecast-weighted mean excess return at or below 0"
    elif t_val <= -2:
        status = "rejected"
        decided = "slope t <= -2: deeper scaled dips followed by smaller excess returns"
    else:
        status = "inconclusive"
        decided = "slope t between -2 and 2"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": None if t_val is None else {"name": "OLS slope t, day-clustered", "value": t_val},
                         "threshold": thr},
        "supporting_check": {"name": "forecast-weighted mean excess 5-bar return > 0", "value": wmean,
                             "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
