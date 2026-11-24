import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.midweek_gain.last_history_value"

    # ---------- per coin: mean daily return over all windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            r = c[1:] / c[:-1] - 1.0
            rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- situation check + collect cases ----------
    n_active = 0
    n_agree = 0
    case_f, case_x, case_sat = [], [], []

    for coin, wins in bars.items():
        mu = coin_mean.get(coin, np.nan)
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            # the bar whose next bar is Saturday: the bar stamped Friday (UTC)
            is_fri = ((ts + pd.Timedelta(days=1)).dt.dayofweek == 5).to_numpy()
            # midweek gain: close[t-1]/close[t-4]-1, inside the window
            mid = np.full(n, np.nan)
            if n > 4:
                mid[4:] = close[3:-1] / close[:-4] - 1.0
            if LHV in df.columns:
                lhv = pd.to_numeric(df[LHV], errors="coerce").to_numpy(dtype=float)
            else:
                lhv = np.full(n, np.nan)
            gain_pos = np.where(np.isfinite(lhv), lhv > 0, np.where(np.isfinite(mid), mid > 0, False))
            situation = is_fri & gain_pos

            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

            # cases: Friday bars with forecast > 0, Saturday's return inside the window
            nxt = np.full(n, np.nan)
            if n > 1:
                nxt[:-1] = close[1:] / close[:-1] - 1.0
            sel = is_fri & np.isfinite(fc) & (fc > 0) & np.isfinite(nxt)
            if np.isfinite(mu):
                for i in np.where(sel)[0]:
                    case_f.append(fc[i])
                    case_x.append(nxt[i] - mu)
                    case_sat.append(str((ts.iloc[i] + pd.Timedelta(days=1)).date()))

    threshold = "confirm if slope t >= 2 and forecast-weighted mean excess > 0; reject if slope t <= -2"
    mm_name = "slope of Saturday excess return on forecast (Friday bars, forecast > 0)"
    reading = ("Friday = bar stamped Friday UTC (next bar Saturday); situation from last_history_value > 0 "
               "(prices close[t-1]/close[t-4]-1 when not recorded); excess = Saturday return minus the coin's mean "
               "1-bar return over all its windows; slope from pooled OLS with intercept across coins, its t from "
               "cluster-robust errors with residual scores summed per Saturday date (G/(G-1) correction); the plan's "
               "'else inconclusive' for too few cases is applied as 'not observable' per the workflow.")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"Friday cases with forecast > 0": 0, "distinct Saturdays": 0},
            "decided_by": "No active bars: the minimum of 300 Friday cases with forecast > 0 is not reached.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are Friday bars after a positive "
                           "Monday-to-Thursday gain with a long forecast, as the Fidelity's situation requires."),
            "reading": reading,
        }

    f = np.asarray(case_f, dtype=float)
    x = np.asarray(case_x, dtype=float)
    sat = np.asarray(case_sat)
    n_cases = len(f)
    n_sat = int(len(np.unique(sat))) if n_cases else 0
    counts = {"Friday cases with forecast > 0": int(n_cases), "distinct Saturdays": n_sat}

    sup_val = float(np.sum(x * f) / np.sum(f)) if n_cases and np.sum(f) != 0 else None
    sup_pass = (sup_val is not None and sup_val > 0)

    slope, t = None, None
    if n_cases >= 3 and np.var(f) > 0 and n_sat >= 2:
        X = np.column_stack([np.ones(n_cases), f])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ x
        e = x - X @ beta
        meat = np.zeros((2, 2))
        for s in np.unique(sat):
            m = sat == s
            g = X[m].T @ e[m]
            meat += np.outer(g, g)
        G = n_sat
        V = XtX_inv @ meat @ XtX_inv * (G / (G - 1.0))
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t = float(slope / se) if np.isfinite(se) and se > 0 else None

    main = {"name": mm_name, "value": slope,
            "statistic": ({"name": "slope t, residuals summed per Saturday", "value": t} if t is not None else None),
            "threshold": threshold}
    support = {"name": "forecast-weighted mean Saturday excess return", "value": sup_val,
               "passed": bool(sup_pass) if sup_val is not None else None}
    sc = {"agreement": float(agreement), "passed": True}

    if n_cases < 300 or n_sat < 100:
        missing = []
        if n_cases < 300:
            missing.append(f"{n_cases} Friday cases with forecast > 0 (300 required)")
        if n_sat < 100:
            missing.append(f"{n_sat} distinct Saturdays (100 required)")
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": support, "counts": counts,
                "decided_by": "Minimum count not reached: " + "; ".join(missing) + ".",
                "reading": reading}

    if t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the forecast-weighted mean excess return is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the forecast-weighted mean excess return is not above 0."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {"status": status, "situation_check": sc, "main_measure": main,
            "supporting_check": support, "counts": counts,
            "decided_by": decided, "reading": reading}
