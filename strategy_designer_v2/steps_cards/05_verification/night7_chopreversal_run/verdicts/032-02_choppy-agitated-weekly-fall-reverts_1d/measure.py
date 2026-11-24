import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    RAW = "debug_info.components.fall7.last_history_value"

    def to_dt(s):
        if pd.api.types.is_numeric_dtype(s):
            mx = pd.to_numeric(s, errors="coerce").abs().max()
            unit = "ms" if mx is not None and mx > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True, errors="coerce")
        return pd.to_datetime(s, utc=True, errors="coerce")

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            recomputed = (close / close.shift(H) - 1.0) * 100.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            active = fc != 0
            n_active += int(active.sum())
            # situation: the coin fell over the past 7 bars; expected side: long
            agree = active & (raw < 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.90)

    main_name = "day-clustered slope of 7-bar excess return on forecast (forecast > 0 grid cells)"
    threshold = "confirm: slope t >= 2 with mean excess > 0; reject: slope t <= -2; at least 30 day-clustered positive-forecast cells"
    reading = ("Situation taken as a negative raw 7-bar return (fall7 last_history_value, recomputed from closes where missing) "
               "with a positive forecast, the choppy agitated profile being enforced by the regime and not re-checked; grid cells at "
               "positions 0,7,14,... of each window with a full 7-bar forward return inside the window; normal drift = mean of the "
               "coin's grid 7-bar returns over all its windows; slope from OLS with intercept and day-clustered (CR1) standard error; "
               "the 30-cell minimum counted as distinct days, and its shortfall reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("The plan's situation (a 7-day fall, held long) and the forecast disagree: only "
                           f"{agreement:.1%} of active bars are 7-day falls with a long forecast (needed 90%)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_cells = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            ts = to_dt(df["timestamp"])
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                f = fc[i]
                if np.isfinite(f) and f > 0 and pd.notna(ts.iloc[i]):
                    coin_cells.append((ts.iloc[i].normalize(), float(f), r))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for d, f, r in coin_cells:
            rows.append((d, f, r - drift))

    cells = pd.DataFrame(rows, columns=["day", "f", "ex"])
    n_cells = int(len(cells))
    n_days = int(cells["day"].nunique()) if n_cells else 0

    slope = None
    t_slope = None
    mean_ex = float(cells["ex"].mean()) if n_cells else None

    if n_cells >= 3 and n_days >= 2 and cells["f"].nunique() > 1:
        X = np.column_stack([np.ones(n_cells), cells["f"].to_numpy()])
        y = cells["ex"].to_numpy()
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ (X.T @ y)
        u = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in cells.groupby("day").indices.items():
            s = X[idx].T @ u[idx]
            meat += np.outer(s, s)
        G = n_days
        k = 2
        corr = (G / (G - 1.0)) * ((n_cells - 1.0) / (n_cells - k)) if n_cells > k else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t_slope = float(slope / se) if np.isfinite(se) and se > 0 else None

    sup_passed = (mean_ex > 0) if mean_ex is not None else None
    counts = {"independent positive-forecast grid cells (day-clustered)": n_days,
              "positive-forecast grid cells": n_cells}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} day-clustered positive-forecast grid cells, fewer than the plan's minimum of 30."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither rule is met."
    elif t_slope >= 2 and mean_ex > 0:
        status = "confirmed"
        decided = "Slope t >= 2 and the mean excess 7-bar return is positive: the plan's confirm rule."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Slope t <= -2: larger falls are followed by weaker next-week returns, the plan's reject rule."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "Slope t >= 2 but the mean excess return is 0 or below: the plan's inconclusive rule."
    else:
        status = "inconclusive"
        decided = "Slope t between -2 and 2: the plan's inconclusive rule."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": None if t_slope is None else {"name": "day-clustered slope t", "value": t_slope},
                         "threshold": threshold},
        "supporting_check": {"name": "mean excess 7-bar return over positive-forecast cells > 0",
                             "value": mean_ex,
                             "passed": None if sup_passed is None else bool(sup_passed)},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
