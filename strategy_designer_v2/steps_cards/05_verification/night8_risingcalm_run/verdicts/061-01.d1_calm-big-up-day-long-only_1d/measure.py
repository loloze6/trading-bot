import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.up_day_swing.last_history_value"
    CALM = "unknown"  # the regime with a strategy; "chop" is the veto (agitated)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            ret1 = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                up = raw.where(raw.notna(), ret1) > 0
            else:
                up = ret1 > 0
            calm = df["regime"].astype(str) == CALM
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & calm & up.fillna(False) & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = True if n_active == 0 else bool(agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "slope t of 5-bar excess return on forecast (calm grid bars, clustered by date)",
                "value": None, "statistic": None,
                "threshold": "t >= 2 confirms (with check mean > 0), t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation": int(n_agree)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are calm-regime up days with a "
                           "positive (long) forecast, so the config does not do what the Fidelity's "
                           "situation and long side say."),
            "reading": "Calm = regime 'unknown' (not the 'chop' veto); an up day = raw component value > 0 "
                       "(close-to-close return > 0 where the raw value is missing).",
        }

    # ---------- 2. criterion ----------
    rows = []
    drift_samples = {}
    for coin, wins in bars.items():
        drift_samples[coin] = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                drift_samples[coin].append(r)
                if reg[t] == CALM and np.isfinite(fc[t]):
                    d = ts.iloc[t]
                    rows.append((coin, r, float(fc[t]),
                                 str(d.date()) if pd.notna(d) else f"{coin}_{w}_{t}"))

    drift = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in drift_samples.items()}
    g = pd.DataFrame(rows, columns=["coin", "ret", "fc", "date"])
    if len(g):
        g["excess"] = g["ret"] - g["coin"].map(drift)
        g = g.dropna(subset=["excess", "fc"])
    else:
        g = pd.DataFrame(columns=["coin", "ret", "fc", "date", "excess"])

    pos = g[g["fc"] > 0]
    n_pos = int(len(pos))
    n_grid = int(len(g))
    n_dates = int(g["date"].nunique()) if n_grid else 0

    # OLS slope with date-clustered (CR1) standard error
    slope, t_slope = None, None
    if n_grid >= 3 and n_dates >= 2 and float(np.var(g["fc"].values)) > 0:
        y = g["excess"].values.astype(float)
        X = np.column_stack([np.ones(n_grid), g["fc"].values.astype(float)])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in g.reset_index(drop=True).groupby("date").indices.items():
            s = X[idx].T @ u[idx]
            meat += np.outer(s, s)
        G, N, K = n_dates, n_grid, 2
        corr = (G / (G - 1)) * ((N - 1) / (N - K))
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t_slope = float(slope / se) if np.isfinite(se) and se > 0 else None

    check_mean = float(pos["excess"].mean()) if n_pos > 0 else None
    check_pass = (check_mean > 0) if check_mean is not None else None

    counts = {"grid bars with forecast > 0": n_pos,
              "calm grid bars": n_grid,
              "dates (clusters)": n_dates}

    if n_pos < 100:
        status = "not observable"
        decided = f"Only {n_pos} grid bars with forecast > 0, fewer than the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and check_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess return over forecast > 0 grid bars is above 0."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the check mean is at or below 0: inconclusive by the plan."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger calm up days are followed by smaller 5-day excess returns."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2: inconclusive by the plan."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of 5-bar excess return on forecast (calm grid bars), t clustered by date",
            "value": slope,
            "statistic": ({"name": "date-clustered OLS slope t", "value": t_slope}
                          if t_slope is not None else None),
            "threshold": "t >= 2 confirms (with check mean > 0); t <= -2 rejects; between is inconclusive"},
        "supporting_check": {"name": "mean 5-bar excess return over grid bars with forecast > 0",
                             "value": check_mean,
                             "passed": (bool(check_pass) if check_pass is not None else None)},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Calm = regime 'unknown' (not the 'chop' veto) at bar t; the normal 5-bar drift is each "
                    "coin's mean 5-bar return over all its non-overlapping grid bars in all windows (all regimes); "
                    "the regression pools all coins with an intercept and CR1 date-clustered errors; the 100 "
                    "minimum counts calm grid bars with forecast > 0 and, unmet, gives 'not observable'."),
    }
