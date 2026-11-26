import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    MIN_POS = 100
    RAW = "debug_info.components.scaled_rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("unknown", index=df.index)
            # rising-market profile: the idea's regime ran (component recorded) and the detector did not veto to chop
            in_profile = raw.notna() & (regime != "chop")
            # 3-day scaled rise: the raw component value > 0 (fallback: the 3-bar price return inside the window)
            close = pd.to_numeric(df["close"], errors="coerce")
            ret3_past = close / close.shift(H) - 1
            rise = (raw > 0) | (raw.isna() & (ret3_past > 0))
            situation = in_profile & rise
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.90
    else:
        agreement = None
        passed = True

    main_name = "slope of excess 3-bar forward return on forecast (in-profile grid bars)"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2 (t clustered by day)"
    sup_name = "mean excess 3-bar return on grid bars with forecast > 0 is above 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars in the rising profile "
                          "after a positive 3-day scaled rise, as the plan's Fidelity requires.",
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        # coin's mean 3-bar return over all windows (holding the coin), on the non-overlapping grid
        all_rets = []
        coin_rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            raw = pd.to_numeric(df[RAW], errors="coerce").values if RAW in df.columns else np.full(n, np.nan)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                r = close[i + H] / close[i] - 1
                if not np.isfinite(r):
                    continue
                all_rets.append(r)
                if np.isfinite(raw[i]) and np.isfinite(fc[i]):
                    coin_rows.append((ts.iloc[i].floor("D"), fc[i], r))
        if not all_rets:
            continue
        mu = float(np.mean(all_rets))
        for d, f, r in coin_rows:
            rows.append((d, f, r - mu))

    if rows:
        data = pd.DataFrame(rows, columns=["day", "f", "ex"])
    else:
        data = pd.DataFrame(columns=["day", "f", "ex"])

    n_grid = int(len(data))
    pos = data[data["f"] > 0] if n_grid else data
    n_pos = int(len(pos))
    n_pos_days = int(pos["day"].nunique()) if n_pos else 0

    slope = None
    t = None
    if n_grid >= 3 and data["f"].nunique() > 1:
        X = np.column_stack([np.ones(n_grid), data["f"].values.astype(float)])
        y = data["ex"].values.astype(float)
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        codes = pd.factorize(data["day"])[0]
        G = int(codes.max()) + 1
        meat = np.zeros((2, 2))
        for g in range(G):
            m = codes == g
            s = X[m].T @ u[m]
            meat += np.outer(s, s)
        K = 2
        corr = (G / (G - 1)) * ((n_grid - 1) / (n_grid - K)) if G > 1 else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t = float(slope / se) if np.isfinite(se) and se > 0 else None

    sup_val = float(pos["ex"].mean()) if n_pos else None
    sup_pass = (sup_val is not None and sup_val > 0) if n_pos else None

    counts = {"grid bars with forecast > 0": n_pos,
              "in-profile grid bars": n_grid,
              "days of grid bars with forecast > 0": n_pos_days}

    if n_pos < MIN_POS:
        status = "not observable"
        decided = f"Only {n_pos} grid bars with forecast > 0, fewer than the plan's minimum of 100."
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2, the mean excess return on forecast > 0 bars is above 0, with at least 100 such bars."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting check (mean excess return on forecast > 0 bars above 0) fails."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2, with at least 100 grid bars with forecast > 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": None if t is None else {"name": "OLS t, standard errors clustered by day", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "In-profile bars are grid bars where the scaled_rise raw value is recorded, the regression has an "
                   "intercept with CR1 day-clustered errors, the coin's mean 3-bar return is taken over all grid bars of "
                   "all its windows, and the supporting check needs only a mean above 0 (no t), as written.",
    }
