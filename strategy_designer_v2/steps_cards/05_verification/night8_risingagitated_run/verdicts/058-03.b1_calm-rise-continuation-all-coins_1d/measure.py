import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    FC = "forecast"
    RAW = "debug_info.components.ma_dist.last_history_value"
    PROFILE_REGIME = "unknown"  # the only regime with a strategy: rising calm (both vetoes pass)

    def _ts(s):
        return pd.to_datetime(s, utc=True, errors="coerce")

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            # distance above the 20-day SMA (today's close included): recorded raw value,
            # recomputed from the prices inside the window where not recorded
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            sma = close.rolling(20, min_periods=20).mean()
            recomputed = (close / sma - 1.0) * 100.0
            dist = raw.where(raw.notna(), recomputed)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)
            in_profile = regime == PROFILE_REGIME
            situation = in_profile & (dist > 0)
            active = fc != 0
            expected_side = fc > 0  # rise -> long
            n_active += int(active.sum())
            n_agree += int((active & situation & expected_side).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "OLS slope of 5-bar excess return (vs coin's mean 5-bar return) on forecast, grid bars with forecast > 0"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are rising-calm-profile bars with the "
                           "close above its 20-day average and a long forecast; the config does not do what the "
                           "Fidelity says." if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": "The profile is read as regime 'unknown' (the only regime with a strategy after both vetoes), "
                       "the situation as that regime with the ma_dist raw value above 0, side long.",
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_grid_returns = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d[FC], errors="coerce").to_numpy(dtype=float)
            ts = _ts(d["timestamp"])
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0 and pd.notna(ts.iloc[i]):
                    rows.append((coin, ts.iloc[i].normalize(), float(fc[i]), r))
        coin_grid_returns[coin] = float(np.mean(allr)) if len(allr) else np.nan

    cases = pd.DataFrame(rows, columns=["coin", "day", "f", "r"])
    if len(cases):
        cases["mu"] = cases["coin"].map(coin_grid_returns)
        cases["x"] = cases["r"] - cases["mu"]
        cases = cases.dropna(subset=["f", "x"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"grid cases with forecast above 0": n_cases, "distinct days": n_days}

    reading = ("The coin's mean 5-bar return is the mean over the same non-overlapping 5-bar grid of all its windows; "
               "the slope's t uses an OLS with intercept and standard errors clustered by UTC day of the signal bar "
               "(CR1 small-sample correction); the plan's 'fewer than 100 cases or 30 days' rule is applied as the "
               "minimum counts (status 'not observable').")

    slope = None
    tval = None
    if n_cases >= 3 and cases["f"].nunique() > 1:
        y = cases["x"].to_numpy(dtype=float)
        f = cases["f"].to_numpy(dtype=float)
        X = np.column_stack([np.ones(n_cases), f])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ (X.T @ y)
        e = y - X @ beta
        groups = cases["day"].to_numpy()
        meat = np.zeros((2, 2))
        dfg = pd.DataFrame({"g": groups, "s0": X[:, 0] * e, "s1": X[:, 1] * e}).groupby("g")[["s0", "s1"]].sum()
        S = dfg.to_numpy()
        meat = S.T @ S
        G = S.shape[0]
        K = 2
        if G > 1 and n_cases > K:
            corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - K))
            V = corr * XtX_inv @ meat @ XtX_inv
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            slope = float(beta[1])
            tval = float(slope / se) if np.isfinite(se) and se > 0 else None
        else:
            slope = float(beta[1])

    main = {
        "name": main_name,
        "value": slope,
        "statistic": {"name": "slope t, clustered by day", "value": tval} if tval is not None else None,
        "threshold": threshold,
    }

    if n_cases < 100 or n_days < 30:
        status = "not observable"
        decided_by = (f"Minimum counts not reached: {n_cases} grid cases with forecast above 0 (minimum 100) on "
                      f"{n_days} distinct days (minimum 30).")
    elif slope is None or tval is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided_by = "Confirm rule met: the slope is positive with t >= 2."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided_by = "Reject rule met: the slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive rule met: the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
