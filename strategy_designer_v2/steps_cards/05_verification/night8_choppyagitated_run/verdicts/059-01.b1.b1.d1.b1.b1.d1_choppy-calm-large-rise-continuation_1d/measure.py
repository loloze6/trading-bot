import numpy as np
import pandas as pd


def measure(bars):
    H = 14
    RAW = "debug_info.components.scaled_rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            # profile: choppy calm = the regime the vetoes did not turn to "chop" ("unknown")
            profile = d["regime"].astype(str) == "unknown"
            # the 7-day rise: sign of the raw scaled return; recomputed from prices where not recorded
            ret7 = close / close.shift(7) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                rise = np.where(raw.notna(), raw > 0, ret7 > 0)
            else:
                rise = (ret7 > 0).values
            rise = pd.Series(rise, index=d.index).astype(bool)
            situation = profile & rise
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "slope t of 14-bar excess return on forecast", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirms, t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"grid cases with a forecast above 0": 0},
            "decided_by": ("The forecast is active on bars that are not the plan's situation "
                           "(a 7-day rise inside the choppy-calm profile, long) on more than 10 % of active bars."),
            "reading": "The profile is read as the regime 'unknown' (no chop veto) and the rise as a positive raw scaled return.",
        }

    # ---------- 2. criterion ----------
    # coin's mean 14-bar return on the non-overlapping grid of all its windows (holding the coin)
    coin_hold = {}
    rows = []
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    rows.append((coin, ts.iloc[i].floor("D"), float(fc[i]), r))
        coin_hold[coin] = float(np.mean(all_rets)) if all_rets else np.nan

    cases = pd.DataFrame(rows, columns=["coin", "day", "f", "r"])
    if len(cases):
        cases["x"] = cases["r"] - cases["coin"].map(coin_hold)
        cases = cases.dropna(subset=["x", "f"]).reset_index(drop=True)
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    def slope_cluster_t(df):
        y = df["x"].values
        X = np.column_stack([np.ones(len(df)), df["f"].values])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) < 2:
            return np.nan, np.nan
        XtX_inv = np.linalg.inv(XtX)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        meat = np.zeros((2, 2))
        groups = df.groupby("day").indices
        for _, idx in groups.items():
            s = X[idx].T @ e[idx]
            meat += np.outer(s, s)
        G, n, k = len(groups), len(y), 2
        if G < 2 or n <= k:
            return float(beta[1]), np.nan
        corr = G / (G - 1) * (n - 1) / (n - k)
        V = corr * XtX_inv @ meat @ XtX_inv
        se = np.sqrt(V[1, 1])
        return float(beta[1]), (float(beta[1] / se) if se > 0 else np.nan)

    def mean_cluster_t(df):
        x = df["x"].values
        n = len(x)
        if n == 0:
            return np.nan, np.nan
        m = float(x.mean())
        dev = pd.Series(x - m).groupby(df["day"].values).sum().values
        G = len(dev)
        if G < 2:
            return m, np.nan
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / n
        return m, (float(m / se) if se > 0 else np.nan)

    slope, t_slope = (np.nan, np.nan)
    top_mean, top_t = (np.nan, np.nan)
    n_top = 0
    if n_cases >= 3:
        slope, t_slope = slope_cluster_t(cases)
        n_top = int(np.ceil(n_cases / 3.0))
        top = cases.sort_values("f", ascending=False, kind="mergesort").head(n_top)
        top_mean, top_t = mean_cluster_t(top)

    def num(v):
        return None if v is None or not np.isfinite(v) else float(v)

    sup_pass = None if not np.isfinite(top_mean) else bool(top_mean > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} grid cases with a forecast above 0, fewer than the plan's minimum of 30."
    elif (np.isfinite(t_slope) and t_slope <= -2) or (np.isfinite(top_t) and top_t <= -2):
        status = "rejected"
        decided = "Reject rule: the slope's t is -2 or less, or the top third's mean excess return has a t of -2 or less."
    elif np.isfinite(t_slope) and t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm rule: the slope's t is 2 or more and the top third's mean excess return is above 0."
    else:
        status = "inconclusive"
        decided = ("Inconclusive rule: the slope's t lies between -2 and 2, or the top third does not beat holding "
                   "without a t of -2 or less.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "slope of 14-bar excess return on forecast (grid cases, forecast > 0)",
                         "value": num(slope),
                         "statistic": {"name": "slope t, clustered by day", "value": num(t_slope)},
                         "threshold": "t >= 2 confirms (with top third > 0), t <= -2 rejects"},
        "supporting_check": {"name": "mean excess 14-bar return of the top third of forecasts",
                             "value": num(top_mean), "passed": sup_pass},
        "counts": {"grid cases with a forecast above 0": n_cases,
                   "days of the cases": n_days,
                   "top third cases": n_top},
        "decided_by": decided,
        "reading": ("The profile is the regime 'unknown' and the rise a positive raw scaled return; the grid is bars 0, 14, 28, ... "
                    "of each window with a full 14-bar return; the slope's t uses day-clustered standard errors (CR1); the top "
                    "third is the ceil(n/3) largest forecasts, its t with deviations summed per day; the minimum of 30 cases "
                    "is applied first as 'not observable'."),
    }
