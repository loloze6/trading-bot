import numpy as np
import pandas as pd


def measure(bars):
    H = 14
    RAW = "debug_info.components.vol_swell.last_history_value"

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
            sma50 = close.rolling(50, min_periods=50).mean()
            regime = df["regime"].astype(str)
            # close above its 50-day mean: from prices where 50 bars exist in the window,
            # otherwise the detector's own recorded decision (its component is not recorded)
            above = np.where(sma50.notna(), close > sma50, regime == "trending")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            swell = (raw > 0).fillna(False).to_numpy()
            situ = above.astype(bool) & swell
            active = (fc != 0).to_numpy()
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0).to_numpy()).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": None,
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the close is "
                           "above its 50-day mean and the 14-day mean volume exceeds the 30-day mean volume."),
            "reading": ("The 50-day mean is computed from the window's closes where 50 bars exist, otherwise the "
                        "recorded regime stands for the detector's decision; the swell is the raw vol_swell value above 0."),
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_means = {}
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            regime = df["regime"].astype(str).to_numpy()
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if regime[i] == "trending" and np.isfinite(fc[i]):
                    rows.append((coin, r, float(fc[i]), ts.iloc[i].floor("D")))
        coin_means[coin] = float(np.mean(all_rets)) if all_rets else np.nan

    d = pd.DataFrame(rows, columns=["coin", "ret", "fc", "day"])
    if len(d):
        d["ex"] = d["ret"] - d["coin"].map(coin_means)
        d = d[np.isfinite(d["ex"])]
    else:
        d["ex"] = []

    n_trend = int(len(d))
    pos = d[d["fc"] > 0] if n_trend else d
    n_pos = int(len(pos))

    sup_val = float(pos["ex"].mean()) if n_pos > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    slope, tval = None, None
    if n_trend >= 3 and d["fc"].nunique() > 1:
        y = d["ex"].to_numpy(float)
        X = np.column_stack([np.ones(n_trend), d["fc"].to_numpy(float)])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        groups = d["day"].to_numpy()
        G = 0
        for g in pd.unique(groups):
            m = groups == g
            s = X[m].T @ u[m]
            meat += np.outer(s, s)
            G += 1
        k = 2
        corr = (G / (G - 1)) * ((n_trend - 1) / (n_trend - k)) if G > 1 else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        tval = float(slope / se) if np.isfinite(se) and se > 0 else None

    counts = {"grid cases with forecast above 0": n_pos, "trending grid cases": n_trend}

    if n_pos < 100 or n_trend < 300:
        status = "not observable"
        decided = ("A minimum count is not reached: %d grid cases with forecast above 0 (minimum 100) and %d "
                   "trending grid cases (minimum 300)." % (n_pos, n_trend))
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess return of the forecast-above-0 cases is above 0."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": "slope of 14-bar excess return on forecast, trending grid cases",
            "value": slope,
            "statistic": None if tval is None else {"name": "day-clustered OLS t of the slope", "value": tval},
            "threshold": "t >= 2 (with supporting check) confirms; t <= -2 rejects; otherwise inconclusive",
        },
        "supporting_check": {
            "name": "mean excess 14-bar return of grid cases with forecast > 0 (long)",
            "value": sup_val,
            "passed": None if sup_pass is None else bool(sup_pass),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The coin's mean 14-bar return is taken over all its windows' grid bars (every regime), the "
                    "regime is the recorded one, the day-clustered t uses the usual G/(G-1)*(N-1)/(N-K) "
                    "correction, and the plan's minimum counts are applied as 'not observable'; in the situation "
                    "check the 50-day mean comes from the window's closes where 50 bars exist, otherwise from the "
                    "recorded regime."),
    }
