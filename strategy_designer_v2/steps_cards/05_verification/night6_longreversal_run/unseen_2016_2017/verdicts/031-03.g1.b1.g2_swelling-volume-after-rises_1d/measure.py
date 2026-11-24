import numpy as np
import pandas as pd


def measure(bars):
    H = 14
    COMP = "debug_info.components.vol_swell.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0

    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            vol = pd.to_numeric(d["volume"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")

            # 14-bar price change, inside the window only
            rise = close / close.shift(H) - 1.0

            # Volume ratio, centred: mean of the last 14 volumes over the mean of the last 30, minus 1
            ratio_re = (vol.rolling(14, min_periods=14).mean()
                        / vol.rolling(30, min_periods=30).mean()) - 1.0
            if COMP in d.columns:
                raw = pd.to_numeric(d[COMP], errors="coerce")
                swell = raw.where(raw.notna(), ratio_re)
            else:
                swell = ratio_re

            active = fc.notna() & (fc != 0)
            computable = rise.notna() & swell.notna()
            sit = (rise > 0) & (swell > 0)

            n_active += int((active & computable).sum())
            n_active_uncomputable += int((active & ~computable).sum())
            n_agree += int((active & computable & sit & (fc > 0)).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    reading = ("Situation taken as 14-bar close change > 0 with the 14/30 volume ratio above 1 "
               "(recorded vol_swell raw value, recomputed from volume where missing), expected side long, "
               "active bars whose 14-bar change cannot be computed inside the window are left out of the agreement; "
               "the grid is positions 0,14,28,... of each window, kept when regime is 'trending' and the 14-bar forward "
               "return lies inside the window, the coin's mean 14-bar return is taken over all its windows' grid bars, "
               "and the slope's t uses standard errors clustered by calendar day (UTC).")

    main_name = "OLS slope of 14-bar excess forward return on forecast, trending grid bars"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long bars with a positive "
                           "14-bar return and the 14-day volume above its 30-day mean, so the config does not do "
                           "what the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        # coin's mean 14-bar return over all windows (grid bars)
        all_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            reg = d["regime"].astype(str).values
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if reg[i] == "trending" and np.isfinite(fc[i]) and not pd.isna(ts.iloc[i]):
                    coin_rows.append((r, float(fc[i]), ts.iloc[i].strftime("%Y-%m-%d")))
        if not all_rets:
            continue
        mu = float(np.mean(all_rets))
        for r, f, day in coin_rows:
            rows.append((r - mu, f, day))

    n_regime = len(rows)
    n_pos = int(sum(1 for r in rows if r[1] > 0))
    counts = {"grid cases in the regime": n_regime, "grid cases with forecast above 0": n_pos}

    slope = None
    tstat = None
    n_days = 0
    if n_regime >= 3:
        y = np.array([r[0] for r in rows])
        x = np.array([r[1] for r in rows])
        days = np.array([r[2] for r in rows])
        n_days = len(np.unique(days))
        X = np.column_stack([np.ones_like(x), x])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) == 2 and n_days >= 2:
            XtX_inv = np.linalg.inv(XtX)
            beta = XtX_inv @ (X.T @ y)
            e = y - X @ beta
            meat = np.zeros((2, 2))
            for g in np.unique(days):
                m = days == g
                s = X[m].T @ e[m]
                meat += np.outer(s, s)
            N, K, G = len(y), 2, n_days
            corr = (G / (G - 1.0)) * ((N - 1.0) / (N - K))
            V = corr * XtX_inv @ meat @ XtX_inv
            slope = float(beta[1])
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            tstat = float(slope / se) if np.isfinite(se) and se > 0 else None
    counts["days of the regime grid cases"] = int(n_days)

    if n_pos < 100 or n_regime < 200:
        status = "not observable"
        missing = []
        if n_pos < 100:
            missing.append(f"only {n_pos} grid cases with forecast above 0 (minimum 100)")
        if n_regime < 200:
            missing.append(f"only {n_regime} grid cases in the regime (minimum 200)")
        decided_by = "Minimum count not reached: " + "; ".join(missing) + "."
    elif tstat is None or slope is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tstat >= 2:
        status = "confirmed"
        decided_by = "Confirm rule: the slope is positive with t >= 2."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided_by = "Reject rule: the slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive rule: the slope's |t| is below 2."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None),
                            "passed": bool(passed)},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "slope t, clustered by day", "value": tstat} if tstat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
