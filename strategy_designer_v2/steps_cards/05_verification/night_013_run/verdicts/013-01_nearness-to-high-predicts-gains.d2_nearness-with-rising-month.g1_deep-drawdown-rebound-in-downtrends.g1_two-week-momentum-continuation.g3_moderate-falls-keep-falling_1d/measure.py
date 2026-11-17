import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    LHV = "debug_info.components.fall_short.last_history_value"
    LHV2 = "debug_info.components.deep_rebound.last_history_value"
    CROSS = np.sqrt(300.0)  # s where short turns to long in the graded hump (about 17.3)
    BAND = (15.0, 20.0)     # tolerance around the crossing: either side accepted there

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if LHV in df.columns:
                z = pd.to_numeric(df[LHV], errors="coerce")
            elif LHV2 in df.columns:
                z = pd.to_numeric(df[LHV2], errors="coerce")
            else:
                z = pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            if active.sum() == 0:
                continue
            za = z[active].values
            fa = fc[active].values
            s = -za
            fall = np.isfinite(za) & (za < 0)
            moderate = fall & (s < BAND[0])
            deep = fall & (s > BAND[1])
            near = fall & (s >= BAND[0]) & (s <= BAND[1])
            ok = (moderate & (fa < 0)) | (deep & (fa > 0)) | near
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of excess 7-bar return on forecast, non-overlapping grid, pooled"
    thr = "slope t >= +2 (with positive supporting difference) confirms; t <= -2 rejects"
    sup_name = "mean excess 7-bar return at forecast>0 minus at forecast<0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of non-zero forecasts are on 14-bar falls with short at moderate falls and long at the deepest falls, as the Fidelity states.",
            "reading": "The situation is a negative recorded fall_short value (14-bar change, standardised); the side is short for s < 15, long for s > 20, and either side is accepted between 15 and 20 around the hump's crossing.",
        }

    # ---------- 2. criterion ----------
    # coin mean 7-bar return over all windows (grid points, all bars)
    coin_rows = {}
    for coin, wins in bars.items():
        rets_all = []
        rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                rets_all.append(r)
                rows.append((fc[i], r))
        mu = float(np.mean(rets_all)) if rets_all else np.nan
        coin_rows[coin] = (mu, rows)

    X, Y = [], []
    for coin, (mu, rows) in coin_rows.items():
        if not np.isfinite(mu):
            continue
        for f, r in rows:
            if np.isfinite(f) and f != 0:
                X.append(f)
                Y.append(r - mu)
    X = np.asarray(X, float)
    Y = np.asarray(Y, float)
    n_nz = int(len(X))
    n_pos = int((X > 0).sum())
    n_neg = int((X < 0).sum())

    slope, tstat = None, None
    if n_nz >= 3 and np.var(X) > 0:
        xm, ym = X.mean(), Y.mean()
        sxx = np.sum((X - xm) ** 2)
        b = np.sum((X - xm) * (Y - ym)) / sxx
        a = ym - b * xm
        resid = Y - a - b * X
        s2 = np.sum(resid ** 2) / (n_nz - 2)
        se = np.sqrt(s2 / sxx)
        slope = float(b)
        tstat = float(b / se) if se > 0 else None

    diff = None
    if n_pos > 0 and n_neg > 0:
        diff = float(Y[X > 0].mean() - Y[X < 0].mean())
    sup_pass = None if diff is None else bool(diff > 0)

    counts = {"non-zero grid points": n_nz, "grid points with forecast > 0": n_pos,
              "grid points with forecast < 0": n_neg}

    if n_nz < 200:
        status = "not observable"
        decided = f"Fewer than 200 non-zero grid points ({n_nz})."
    elif n_pos < 30:
        status = "not observable"
        decided = f"Fewer than 30 grid points with forecast > 0 ({n_pos})."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope t could not be computed."
    elif tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "Slope t >= +2 and the supporting difference (forecast>0 minus forecast<0) is positive."
    elif tstat <= -2:
        status = "rejected"
        decided = "Slope t <= -2."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "Slope t >= +2 but the supporting difference is not positive."
    else:
        status = "inconclusive"
        decided = "Slope t is between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": None if tstat is None else {"name": "OLS slope t", "value": tstat},
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "The grid is positions 0, 7, 14, ... of each window with t+7 inside the window; the coin's mean 7-bar return is taken over all its grid points in all windows; the slope t is the ordinary OLS t with intercept; the situation check treats a negative fall_short last_history_value as the fall and accepts either side for s between 15 and 20, around the hump's crossing.",
    }
