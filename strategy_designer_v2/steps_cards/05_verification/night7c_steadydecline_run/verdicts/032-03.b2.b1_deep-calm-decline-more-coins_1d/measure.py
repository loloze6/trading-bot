import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    SHORT, LONG = 28, 90
    FALL_RAW = "debug_info.components.fall28.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            vol = pd.to_numeric(df["volume"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            # Volume ratio: mean of the last 28 volumes over the mean of the 90 before them.
            short_m = vol.rolling(SHORT, min_periods=SHORT).mean()
            long_m = vol.shift(SHORT).rolling(LONG, min_periods=LONG).mean()
            vr = short_m / long_m
            # Where the record is too short to rebuild the ratio, use the detector's own decision.
            regime_thin = df["regime"].astype(str) == "mean_reversion"
            thin = pd.Series(np.where(vr.notna(), vr < 1.0, regime_thin), index=df.index).astype(bool)
            # 28-day price change: recorded raw value, else rebuilt from the prices.
            if FALL_RAW in df.columns:
                fall = pd.to_numeric(df[FALL_RAW], errors="coerce")
            else:
                fall = pd.Series(np.nan, index=df.index)
            fall = fall.fillna(close / close.shift(SHORT) - 1.0)
            fell = (fall < 0).fillna(False)
            active = fc != 0
            ok = active & thin & fell & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of drift-adjusted 10-bar forward return on the forecast"
    threshold = "confirm: slope > 0 with t >= 2 and supporting mean > 0; reject: slope < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90 % of the bars with a non-zero forecast are thin-volume bars "
                          "(28-day mean volume below the 90 days before) after a 28-day fall with a short forecast.",
            "reading": "The volume ratio is rebuilt from in-window volumes where 118 bars exist, else taken from "
                       "the recorded regime; the fall from fall28's raw value.",
        }

    # ---------- 2. criterion ----------
    # Normal 10-bar drift per coin: mean over the non-overlapping grid of all its windows.
    rows = []
    drift = {}
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df) - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if reg[i] == "mean_reversion" and np.isfinite(fc[i]) and fc[i] < 0:
                    rows.append((coin, ts.iloc[i].floor("D"), float(fc[i]), r))
        drift[coin] = float(np.mean(all_rets)) if all_rets else np.nan

    cases = pd.DataFrame(rows, columns=["coin", "day", "x", "r"])
    if len(cases):
        cases["d"] = cases["coin"].map(drift)
        cases["y"] = cases["r"] - cases["d"]
        cases = cases.dropna(subset=["x", "y"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    slope = None
    tval = None
    supp = None
    if n_cases >= 3:
        x = cases["x"].values
        y = cases["y"].values
        X = np.column_stack([np.ones(n_cases), x])
        XtX_inv = np.linalg.pinv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        resid = y - X @ beta
        # Cluster-robust (by day) covariance, CR1 correction.
        meat = np.zeros((2, 2))
        days = cases["day"].values
        for dday in pd.unique(days):
            m = days == dday
            s = X[m].T @ resid[m]
            meat += np.outer(s, s)
        G = len(pd.unique(days))
        k = 2
        corr = (G / (G - 1)) * ((n_cases - 1) / (n_cases - k)) if G > 1 and n_cases > k else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        tval = float(beta[1] / se) if np.isfinite(se) and se > 0 else None
    if n_cases > 0:
        supp = float(np.mean(-cases["y"].values))
    supp_pass = None if supp is None else bool(supp > 0)

    counts = {"independent cases (distinct days)": n_days, "cases (coin grid cells)": n_cases}

    if n_days < 30:
        status = "not observable"
        decided = "Fewer than 30 independent cases (grid cells on distinct days): the minimum count is not reached."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed."
    elif slope > 0 and tval >= 2 and supp_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the mean short-direction drift-adjusted return is above 0."
    elif slope > 0 and tval >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the supporting mean is not above 0."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: deeper thin-volume falls are followed by relatively higher returns."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tval is None else {"name": "OLS slope t, day-clustered SE", "value": tval},
            "threshold": threshold,
        },
        "supporting_check": {"name": "mean of -(10-bar return - drift) over the cases", "value": supp, "passed": supp_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "Cases are grid bars 0,10,20,... of each window with a full 10-bar forward return, regime "
                   "mean_reversion and forecast < 0. The drift is the coin's mean grid 10-bar return over all its windows. "
                   "'Cases of the same day pooled' is read as a day-clustered (CR1) standard error of the slope. "
                   "For the situation check, the volume ratio is rebuilt from in-window volumes where 118 bars exist, "
                   "else taken from the recorded regime.",
    }
