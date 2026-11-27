import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    RAW = "debug_info.components.stretch.last_history_value"
    PROFILE_REGIME = "unknown"  # the only regime with a strategy: the 'choppy calm' profile (chop vetoes give null)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce")
            # stretch from prices, used only where the raw value is not recorded
            sma = close.rolling(20, min_periods=20).mean()
            sd = close.pct_change().rolling(20, min_periods=20).std()
            stretch_px = ((close - sma) / sd).values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
                raw = np.where(np.isnan(raw), stretch_px, raw)
            else:
                raw = stretch_px
            reg = df["regime"].astype(str).values
            active = fc != 0
            n_active += int(active.sum())
            in_profile = reg == PROFILE_REGIME
            side_ok = np.sign(fc) == np.sign(np.nan_to_num(raw, nan=0.0))
            n_agree += int((active & in_profile & side_ok & (np.sign(fc) != 0)).sum())

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "slope of drift-adjusted 10-bar forward return on forecast",
                             "value": None, "statistic": None,
                             "threshold": "positive with t >= 2 to confirm; negative with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"grid cases with nonzero forecast": 0, "long cases": 0, "short cases": 0},
            "decided_by": "No bar has a nonzero forecast, so neither the situation nor the criterion can be read.",
            "reading": "none",
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": None,
            "decided_by": ("Fewer than 90% of active bars are in the choppy calm profile (regime 'unknown') with the "
                           "forecast's sign equal to the stretch's sign (long above the 20-day SMA, short below)."),
            "reading": "The profile is read from the recorded regime 'unknown'; the side from the sign of the stretch's raw value.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append({"coin": coin, "ret": c1 / c0 - 1.0,
                             "fc": fc[p], "day": ts.iloc[p].floor("D")})
    g = pd.DataFrame(rows, columns=["coin", "ret", "fc", "day"])
    if len(g):
        drift = g.groupby("coin")["ret"].mean()
        g["adj"] = g["ret"] - g["coin"].map(drift)
    else:
        g["adj"] = []
    cases = g[g["fc"].notna() & (g["fc"] != 0)].copy()
    n_cases = int(len(cases))
    n_long = int((cases["fc"] > 0).sum())
    n_short = int((cases["fc"] < 0).sum())
    counts = {"grid cases with nonzero forecast": n_cases, "long cases": n_long, "short cases": n_short}

    threshold = "slope positive with t >= 2 (and carry on both sides) to confirm; negative with t <= -2 to reject"
    slope = None
    tval = None
    if n_cases >= 3 and cases["fc"].nunique() > 1:
        x = cases["fc"].values.astype(float)
        y = cases["adj"].values.astype(float)
        X = np.column_stack([np.ones_like(x), x])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        days = cases["day"].values
        for d in pd.unique(days):
            m = days == d
            s = X[m].T @ u[m]
            meat += np.outer(s, s)
        G = len(pd.unique(days))
        N, K = len(y), 2
        corr = (G / (G - 1)) * ((N - 1) / (N - K)) if G > 1 else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        tval = float(slope / se) if np.isfinite(se) and se > 0 else None

    long_mean = float(cases.loc[cases["fc"] > 0, "adj"].mean()) if n_long else None
    short_mean = float((-cases.loc[cases["fc"] < 0, "adj"]).mean()) if n_short else None
    long_ok = long_mean is not None and long_mean > 0
    short_ok = short_mean is not None and short_mean > 0
    support_pass = bool(long_ok and short_ok)
    supporting = {
        "name": "carry on both sides (long mean adj. return > 0 and short sign-flipped mean > 0)",
        "value": {"long_mean": long_mean, "short_mean_flipped": short_mean},
        "passed": support_pass,
    }
    # value must be a number or null per spec: give the smaller side's mean, details in name
    sides = [v for v in (long_mean, short_mean) if v is not None]
    supporting["value"] = float(min(sides)) if len(sides) == 2 else None
    supporting["name"] = ("carry on both sides: smaller of long mean and sign-flipped short mean "
                          "drift-adjusted 10-bar return, must be > 0")

    main = {"name": "slope of drift-adjusted 10-bar forward return on forecast",
            "value": slope,
            "statistic": {"name": "OLS t, standard errors clustered by day", "value": tval} if tval is not None else None,
            "threshold": threshold}

    reading = ("Drift is the coin's mean 10-bar return on the non-overlapping grid of all its windows; 'cases on the same "
               "day together' is read as day-clustered standard errors of the OLS slope (with intercept); the supporting "
               "check is the sign of each side's mean; a minimum count not reached gives 'not observable'.")

    if n_cases < 200 or n_long < 50 or n_short < 50:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} grid cases (need 200), {n_long} long and {n_short} short "
                   f"(need 50 each).")
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2 and support_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the carry shows on both sides."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: stretches revert toward the average."
    elif slope > 0 and tval >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the carry shows on one side only."
    else:
        status = "inconclusive"
        decided = "The slope has |t| < 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
