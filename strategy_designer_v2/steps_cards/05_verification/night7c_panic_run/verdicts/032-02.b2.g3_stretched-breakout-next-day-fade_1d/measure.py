import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.stretch.last_history_value"
    PERIOD = 30
    HORIZON = 1

    # ---------- collect per-coin frames, per-window computations ----------
    situation_rows = []   # (in_situation_on_side) for active bars
    case_frames = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float)
            high = d["high"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)

            # recomputed distance from prior 30-bar high (inside the window only)
            prior_high = high.shift(1).rolling(PERIOD, min_periods=PERIOD).max()
            dist_recomp = close / prior_high - 1.0
            if LHV in d.columns:
                lhv = pd.to_numeric(d[LHV], errors="coerce")
                dist = lhv.where(lhv.notna(), dist_recomp)
            else:
                dist = dist_recomp

            active = fc != 0
            for i in np.where(active.values)[0]:
                dv = dist.iloc[i]
                ok = bool(pd.notna(dv) and dv > 0 and fc.iloc[i] < 0)
                situation_rows.append(ok)

            # next-bar return inside the window (horizon 1: every bar is its own grid cell)
            fwd = close.shift(-HORIZON) / close - 1.0
            coin_rets.append(fwd.dropna())

            regime = d["regime"].astype(str)
            sel = (regime == "mean_reversion") & fwd.notna() & fc.notna()
            if sel.any():
                c = pd.DataFrame({
                    "coin": coin,
                    "day": d.loc[sel, "ts"].dt.floor("D").values,
                    "ret": fwd[sel].values,
                    "size": (-fc[sel]).values,
                })
                coin_cases.append(c)

        if coin_cases:
            allr = pd.concat(coin_rets) if coin_rets else pd.Series(dtype=float)
            drift = float(allr.mean()) if len(allr) else np.nan
            cc = pd.concat(coin_cases, ignore_index=True)
            cc["excess"] = cc["ret"] - drift
            case_frames.append(cc)

    # ---------- situation check ----------
    n_active = len(situation_rows)
    agreement = float(np.mean(situation_rows)) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars whose close is above "
                           "the prior 30-day high, so the config does not do what the plan's Fidelity states."
                           if n_active > 0 else
                           "The forecast is never non-zero, so no bar takes the plan's short breakout position."),
            "reading": "Situation taken from the recorded stretch raw value where present, else recomputed from prices inside the window.",
        }

    threshold = "t <= -2 confirms (with mean unusual short move > 0); t >= +2 rejects; otherwise inconclusive"
    reading = ("All bars with regime 'mean_reversion' and a next bar in the same window are cases, including those "
               "with forecast 0 (size 0); the slope's t uses day-clustered (CR1) standard errors from OLS of the "
               "drift-removed next-bar return on -forecast; the drift is each coin's mean next-bar return pooled over "
               "all its windows; days are UTC calendar days of the bar's timestamp.")

    cases = pd.concat(case_frames, ignore_index=True) if case_frames else pd.DataFrame(
        columns=["coin", "day", "ret", "size", "excess"])
    cases = cases.dropna(subset=["excess", "size"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    counts = {"distinct days with a breakout case": n_days, "breakout cases": n_cases}

    if n_days < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": "slope of excess next-bar return on breakout size (-forecast)",
                             "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean unusual move in short direction", "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Only {n_days} distinct days with a breakout case, below the plan's minimum of 30.",
            "reading": reading,
        }

    # ---------- OLS with day-clustered standard errors ----------
    y = cases["excess"].values.astype(float)
    x = cases["size"].values.astype(float)
    X = np.column_stack([np.ones_like(x), x])
    N, K = X.shape
    XtX = X.T @ X
    slope = None
    t_stat = None
    try:
        bread = np.linalg.inv(XtX)
        beta = bread @ X.T @ y
        e = y - X @ beta
        meat = np.zeros((K, K))
        groups = cases["day"].values
        codes, uniq = pd.factorize(groups)
        G = len(uniq)
        for g in range(G):
            m = codes == g
            s = X[m].T @ e[m]
            meat += np.outer(s, s)
        adj = (G / (G - 1.0)) * ((N - 1.0) / (N - K)) if G > 1 and N > K else 1.0
        V = adj * bread @ meat @ bread
        slope = float(beta[1])
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        t_stat = float(slope / se) if np.isfinite(se) and se > 0 else np.nan
    except np.linalg.LinAlgError:
        slope = np.nan
        t_stat = np.nan

    unusual_short = float(np.mean(-y))
    sup_pass = bool(unusual_short > 0)

    if t_stat is None or not np.isfinite(t_stat):
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in breakout size), so neither rule is met."
        t_out = None
    else:
        t_out = t_stat
        if t_stat <= -2:
            if sup_pass:
                status = "confirmed"
                decided = "Slope t <= -2 and the mean unusual short move is above 0: the plan's confirm rule."
            else:
                status = "inconclusive"
                decided = "Slope t <= -2 but the mean unusual short move is not above 0: inconclusive per the plan."
        elif t_stat >= 2:
            status = "rejected"
            decided = "Slope t >= +2: a larger stretch is followed by a larger rise than usual, the plan's reject rule."
        else:
            status = "inconclusive"
            decided = "Slope t is between -2 and +2: inconclusive per the plan."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "slope of excess next-bar return on breakout size (-forecast)",
                         "value": (float(slope) if slope is not None and np.isfinite(slope) else None),
                         "statistic": ({"name": "day-clustered OLS slope t", "value": t_out}
                                       if t_out is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "mean unusual move in short direction", "value": unusual_short,
                             "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
