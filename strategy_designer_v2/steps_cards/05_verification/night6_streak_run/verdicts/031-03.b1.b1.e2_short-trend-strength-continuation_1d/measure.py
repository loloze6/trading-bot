import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.scaled_rise.last_history_value"
    PPV = "debug_info.components.scaled_rise.post_pipeline_value"

    # ---------- 1. Situation check ----------
    # Situation: a positive 10-day return (raw vol-scaled 10-day return > 0). Expected side: long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            close = pd.to_numeric(df["close"], errors="coerce")
            # When the raw value is missing, fall back to the 10-bar return inside the window.
            ret10 = close / close.shift(10) - 1.0
            sit = raw > 0
            sit = sit.where(raw.notna(), ret10 > 0)
            sit = sit.fillna(False).astype(bool)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "t of the slope of the 5-bar excess return on the forecast, grid bars with forecast > 0, clustered by day"
    threshold = "t >= 2 confirms (with the supporting check), t <= -2 rejects, at least 200 grid bars with a positive forecast"
    sup_name = "mean unusual 5-bar move of the cases (forecast rises >= 2 points, once per grid cell), long direction, > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are bars with a positive 10-day return on the long side, as the plan's situation requires.",
            "reading": "The situation is read as the component's raw volatility-scaled 10-day return above 0 (10-bar price return when missing), on the long side.",
        }

    # ---------- 2. Drift per coin: mean 5-bar return over all windows' grids ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for i in range(0, n, H):
                if i + H < n and np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0:
                    rets.append(close[i + H] / close[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. Main measure rows and supporting check cases ----------
    X, Y, D = [], [], []
    case_moves = []
    for coin, wins in bars.items():
        dr = drift.get(coin, np.nan)
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if PPV in df.columns:
                ppv = pd.to_numeric(df[PPV], errors="coerce").to_numpy(dtype=float)
            else:
                ppv = np.full(len(df), np.nan)
            ppv = np.where(np.isfinite(ppv), ppv, fc)
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            days = ts.dt.strftime("%Y-%m-%d").to_numpy()
            n = len(df)

            def fwd(i):
                if i + H < n and np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0:
                    return close[i + H] / close[i] - 1.0
                return np.nan

            # main measure: grid bars with forecast > 0
            for i in range(0, n, H):
                f = ppv[i]
                if not np.isfinite(f) or f <= 0:
                    continue
                r = fwd(i)
                if not np.isfinite(r) or not np.isfinite(dr):
                    continue
                X.append(f)
                Y.append(r - dr)
                D.append(days[i])

            # cases: forecast rises of at least BAND on the long side from its lowest level since the last bet
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    bet[i] = True
                    ref = f
                else:
                    ref = min(ref, f)
            # once per grid cell: the first case of the cell
            for start in range(0, n, H):
                idx = [j for j in range(start, min(start + H, n)) if bet[j]]
                if not idx:
                    continue
                j = idx[0]
                r = fwd(j)
                if np.isfinite(r) and np.isfinite(dr):
                    case_moves.append(r - dr)

    X = np.asarray(X, dtype=float)
    Y = np.asarray(Y, dtype=float)
    D = np.asarray(D)
    n_obs = int(len(X))

    slope = None
    t_slope = None
    if n_obs >= 3 and np.var(X) > 0:
        Xm = np.column_stack([np.ones(n_obs), X])
        XtX_inv = np.linalg.inv(Xm.T @ Xm)
        beta = XtX_inv @ Xm.T @ Y
        resid = Y - Xm @ beta
        groups = pd.Series(np.arange(n_obs)).groupby(D).indices
        G = len(groups)
        meat = np.zeros((2, 2))
        for _, ix in groups.items():
            s = Xm[ix].T @ resid[ix]
            meat += np.outer(s, s)
        if G > 1:
            k = 2
            corr = (G / (G - 1.0)) * ((n_obs - 1.0) / (n_obs - k))
            V = corr * XtX_inv @ meat @ XtX_inv
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            slope = float(beta[1])
            if np.isfinite(se) and se > 0:
                t_slope = float(beta[1] / se)

    n_cases = int(len(case_moves))
    sup_value = float(np.mean(case_moves)) if n_cases > 0 else None
    sup_pass = bool(sup_value is not None and sup_value > 0)

    counts = {"grid bars with a positive forecast": n_obs, "cases": n_cases}

    if n_obs < 200:
        status = "not observable"
        decided = f"Only {n_obs} grid bars with a positive forecast, fewer than the plan's minimum of 200."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more on at least 200 grid bars with a positive forecast, and the cases' mean unusual move is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less on at least 200 grid bars with a positive forecast."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the cases' mean unusual move is not above 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t, errors clustered by day", "value": t_slope} if t_slope is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": sup_value, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("The regression uses an intercept and CR1 day-clustered errors on grid bars (positions 0,5,10,... of each window) "
                    "with post_pipeline_value > 0 and a 5-bar forward return inside the window, the drift is the coin's mean 5-bar grid return "
                    "over all its windows, the cases are the first forecast rise of at least 2 points per grid cell, and the plan's "
                    "'fewer than 200 grid bars' is reported as not observable."),
    }
