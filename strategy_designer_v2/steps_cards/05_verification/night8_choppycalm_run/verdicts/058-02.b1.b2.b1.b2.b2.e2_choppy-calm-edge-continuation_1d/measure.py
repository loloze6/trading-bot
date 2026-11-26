import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.range_pos.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            act = f.notna() & (f != 0)
            n_active += int(act.sum())
            if not act.any():
                continue
            reg = df["regime"].astype(str)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            ok = act & (reg == "unknown") & raw.notna() & (np.sign(raw) == np.sign(f))
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    main_name = "slope of 5-day forward return minus coin mean on forecast (grid, non-zero forecast)"
    main_thr = "confirm: slope > 0 with t >= 2 on >= 100 cases and timing gain > 0; reject: slope < 0 with t <= -2 on >= 100 cases"
    reading = ("Situation bars are bars whose regime is 'unknown' (the choppy calm profile, no veto fired) where the "
               "forecast's sign equals the sign of the raw range position; the slope's t uses OLS with an intercept and "
               "day-clustered (CR1) standard errors; the coin's mean 5-day return is taken on all grid bars of all its "
               "windows; the plan's 'fewer than 100 grid cases' is applied as the minimum count (not observable); the "
               "book's daily return is the mean over coins with a bar that day of position x next close-to-close return.")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"grid cases": 0},
            "decided_by": "No bar has a non-zero forecast, so the minimum of 100 grid cases is not reached.",
            "reading": reading,
        }

    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are choppy-calm-profile bars traded toward the side of the "
                           "range position (long above the middle, short below)."),
            "reading": reading,
        }

    # ---------- 2. main measure ----------
    # coin mean 5-day return over all windows (non-overlapping grid)
    coin_mean5 = {}
    coin_mean1 = {}
    grid_rows = []
    daily_rows = []
    for coin, wins in bars.items():
        all5 = []
        all1 = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            day = ts.dt.floor("D")
            n = len(d)
            for i in range(0, n, H):
                if i + H < n and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    r = c[i + H] / c[i] - 1.0
                    all5.append(r)
                    grid_rows.append((coin, day.iloc[i], f[i], r))
            # daily returns
            if "postRebalance_current_allocation" in d.columns:
                pos = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce").to_numpy(dtype=float)
            else:
                pos = np.full(n, np.nan)
            for i in range(n - 1):
                if np.isfinite(c[i]) and np.isfinite(c[i + 1]) and c[i] != 0:
                    r1 = c[i + 1] / c[i] - 1.0
                    all1.append(r1)
                    daily_rows.append((coin, day.iloc[i], pos[i], r1))
        coin_mean5[coin] = float(np.mean(all5)) if all5 else np.nan
        coin_mean1[coin] = float(np.mean(all1)) if all1 else np.nan

    g = pd.DataFrame(grid_rows, columns=["coin", "day", "f", "r"])
    g = g[g["f"].notna() & (g["f"] != 0) & g["r"].notna()].copy()
    g["y"] = g["r"] - g["coin"].map(coin_mean5)
    g = g[g["y"].notna()]
    n_cases = int(len(g))
    n_days = int(g["day"].nunique()) if n_cases else 0

    slope = None
    tval = None
    if n_cases >= 3 and g["f"].nunique() > 1 and n_days >= 2:
        X = np.column_stack([np.ones(n_cases), g["f"].to_numpy(dtype=float)])
        y = g["y"].to_numpy(dtype=float)
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in g.groupby("day").indices.items():
            s = X[idx].T @ e[idx]
            meat += np.outer(s, s)
        G = n_days
        k = 2
        cfac = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - k))
        V = cfac * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        tval = float(slope / se) if np.isfinite(se) and se > 0 else None

    # ---------- supporting check: timing gain ----------
    dd = pd.DataFrame(daily_rows, columns=["coin", "day", "pos", "r"])
    dd = dd[dd["pos"].notna() & dd["r"].notna()].copy()
    timing = None
    if len(dd):
        dd["gain"] = dd["pos"] * dd["r"]
        dd["mkt"] = dd["pos"] * dd["coin"].map(coin_mean1)
        dd = dd[dd["mkt"].notna()]
        if len(dd):
            per_day = dd.groupby("day")[["gain", "mkt"]].mean()
            timing = float(per_day["gain"].mean() - per_day["mkt"].mean())
    support_pass = (timing is not None) and (timing > 0)

    counts = {"grid cases": n_cases, "days of cases": n_days}
    support = {"name": "book timing gain (mean daily return before costs minus market-rise gain)",
               "value": timing, "passed": bool(support_pass) if timing is not None else None}
    statistic = {"name": "slope t, day-clustered", "value": tval} if tval is not None else None

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} grid cases, below the plan's minimum of 100."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed on the grid cases."
    elif slope > 0 and tval >= 2:
        if support_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 on at least 100 cases and the timing gain is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting check (timing gain > 0) fails."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 on at least 100 cases: edges revert."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": slope, "statistic": statistic, "threshold": main_thr},
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
