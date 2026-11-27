import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    COMP = "debug_info.components.stretch.last_history_value"
    POST = "debug_info.components.stretch.post_pipeline_value"
    TREND_P = 60
    LO, HI = -10.0, 10.0
    EPS = 1e-9

    # ---------------- 1. situation check ----------------
    n_active_checked = 0
    n_agree = 0
    n_active_total = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            raw = (pd.to_numeric(df[COMP], errors="coerce").values.astype(float)
                   if COMP in df.columns else np.full(len(df), np.nan))
            n = len(df)
            trend = np.full(n, np.nan)
            if n > TREND_P:
                trend[TREND_P:] = (close[TREND_P:] / close[:-TREND_P] - 1.0) * 100.0
            for i in range(n):
                if not np.isfinite(fc[i]) or fc[i] == 0:
                    continue
                n_active_total += 1
                if not np.isfinite(trend[i]):
                    continue  # 60-day return not computable inside the window
                n_active_checked += 1
                choppy = (trend[i] >= LO - EPS) and (trend[i] <= HI + EPS)
                side_ok = np.isfinite(raw[i]) and raw[i] != 0 and np.sign(raw[i]) == np.sign(fc[i])
                if choppy and side_ok:
                    n_agree += 1

    agreement = float(n_agree / n_active_checked) if n_active_checked > 0 else None
    passed = agreement is not None and agreement >= 0.90

    reading = ("The 60-day return (percent, close[t]/close[t-60]-1) is recomputed from the prices inside each window, so "
               "active bars in a window's first 60 rows are left out of the situation check, and the choppy band is "
               "taken as inclusive of +-10 % like the config's strict vetoes; the expected side is the sign of the raw "
               "stretch; drift is the coin's mean 5-bar return on the non-overlapping grid of all its windows; the "
               "regressor is the stretch post_pipeline_value (forecast where missing), OLS with intercept, slope t with "
               "standard errors clustered by UTC day (CR1); the supporting check uses the signs of the side means only; "
               "the plan's minimum counts, though listed as inconclusive, give 'not observable' as the workflow requires.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "pooled slope of 5-bar excess return on forecast", "value": None,
                             "statistic": None, "threshold": "slope t >= 2 confirms, <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active_total), "active bars checked": int(n_active_checked)},
            "decided_by": ("Fewer than 90 % of the active bars are choppy bars (60-day return within +-10 %) with the "
                           "forecast on the side of the stretch, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------------- 2. criterion ----------------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            post = (pd.to_numeric(df[POST], errors="coerce").values.astype(float)
                    if POST in df.columns else np.full(len(df), np.nan))
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                grid_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] != 0:
                    x = post[i] if np.isfinite(post[i]) else fc[i]
                    coin_rows.append((coin, ts.iloc[i].strftime("%Y-%m-%d"), x, r))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for c, d, x, r in coin_rows:
            rows.append((c, d, x, r - drift))

    data = pd.DataFrame(rows, columns=["coin", "day", "x", "y"])
    n_cases = int(len(data))
    n_long = int((data["x"] > 0).sum()) if n_cases else 0
    n_short = int((data["x"] < 0).sum()) if n_cases else 0
    n_days = int(data["day"].nunique()) if n_cases else 0
    counts = {"grid cases": n_cases, "long cases": n_long, "short cases": n_short, "days": n_days}

    slope = None
    t_slope = None
    if n_cases >= 3 and data["x"].nunique() > 1:
        X = np.column_stack([np.ones(n_cases), data["x"].values])
        y = data["y"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        resid = y - X @ beta
        scores = X * resid[:, None]
        S = pd.DataFrame(scores).groupby(data["day"].values).sum().values
        G = S.shape[0]
        meat = S.T @ S
        V = XtX_inv @ meat @ XtX_inv
        if G > 1 and n_cases > 2:
            V = V * (G / (G - 1)) * ((n_cases - 1) / (n_cases - 2))
        slope = float(beta[1])
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        t_slope = float(slope / se) if np.isfinite(se) and se > 0 else None

    mean_long = float(data.loc[data["x"] > 0, "y"].mean()) if n_long else None
    mean_short = float(data.loc[data["x"] < 0, "y"].mean()) if n_short else None
    long_ok = mean_long is not None and mean_long > 0
    short_ok = mean_short is not None and mean_short < 0
    sup_passed = bool(long_ok and short_ok)

    main = {"name": "pooled slope of 5-bar excess return on forecast",
            "value": slope,
            "statistic": ({"name": "slope t, clustered by day", "value": t_slope} if t_slope is not None else None),
            "threshold": "slope t >= 2 (with both sides carrying) confirms; slope t <= -2 rejects"}
    supporting = {"name": "both sides carry (long mean excess > 0, short mean excess < 0)",
                  "value": {"long mean excess": mean_long, "short mean excess": mean_short},
                  "passed": sup_passed}
    # value must be number or null: report the smaller signed margin
    if mean_long is not None and mean_short is not None:
        supporting["value"] = float(min(mean_long, -mean_short))
    else:
        supporting["value"] = None

    if n_cases < 100 or n_long < 30 or n_short < 30:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} grid cases (need 100), {n_long} long and {n_short} short "
                   f"(need 30 on each side).")
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_passed:
        status = "confirmed"
        decided = "The slope t is at least 2 and both sides carry (long mean excess > 0, short mean excess < 0)."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope t is -2 or less: larger stretches are followed by a return toward the average."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope t is 2 or more but one side fails the both-sides-carry check."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
