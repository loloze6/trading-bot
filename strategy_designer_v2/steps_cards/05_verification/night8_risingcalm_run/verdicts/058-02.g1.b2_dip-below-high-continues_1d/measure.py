import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.dip_depth.last_history_value"

    def raw_from_prices(df):
        # (close - highest close of the last 5 days incl. today) / that high / std of last 30 daily returns
        c = df["close"].astype(float)
        hi = c.rolling(5, min_periods=5).max()
        vol = c.pct_change().rolling(30, min_periods=30).std()
        return (c - hi) / hi / vol

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                fallback = raw_from_prices(df)
                raw = raw.where(raw.notna(), fallback)
            else:
                raw = raw_from_prices(df)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # situation: close below its 5-day high (raw depth < 0), expected side: short
            agree = active & (raw < 0) & (fc < 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "pooled OLS slope of 5-bar excess return on forecast"
    threshold = "confirm: slope > 0 with t >= 2 (and check passes); reject: slope < 0 with t <= -2; at least 300 independent cases"
    sup_name = "mean excess 5-bar return of the 20% most negative-forecast cases below 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are bars below the 5-day high with a short forecast, as the Fidelity's situation and side require.",
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    rows = []
    drifts = {}
    for coin, wins in bars.items():
        coin_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                coin_rets.append(r)
                if np.isfinite(fc[i]):
                    coin_rows.append((coin, ts.iloc[i].floor("D"), float(fc[i]), r))
        if len(coin_rets) == 0:
            continue
        drifts[coin] = float(np.mean(coin_rets))
        for (cn, day, f, r) in coin_rows:
            rows.append({"coin": cn, "day": day, "f": f, "ex": r - drifts[cn]})

    data = pd.DataFrame(rows, columns=["coin", "day", "f", "ex"])
    n_cases = int(len(data))
    n_days = int(data["day"].nunique()) if n_cases else 0
    counts = {"independent cases": n_cases, "days": n_days}

    reading = ("Cases are all bars of each window's non-overlapping 5-bar grid (positions 0, 5, 10, ...) with a forward return, "
               "including forecast-0 bars; the 300 minimum is counted on these cases; the slope's t uses day-clustered (CR1) "
               "standard errors in an OLS with intercept; the deepest fifth is the ceil(20%) cases with the lowest forecast.")

    slope = None
    tstat = None
    sup_val = None
    sup_pass = None

    if n_cases >= 3 and data["f"].nunique() > 1:
        X = np.column_stack([np.ones(n_cases), data["f"].values])
        y = data["ex"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        groups = data["day"].values
        codes, uniq = pd.factorize(groups)
        G = len(uniq)
        for g in range(G):
            idx = codes == g
            s = X[idx].T @ u[idx]
            meat += np.outer(s, s)
        if G > 1:
            corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - 2.0))
        else:
            corr = 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        slope = float(beta[1])
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else float("nan")
        tstat = float(slope / se) if np.isfinite(se) and se > 0 else None

    if n_cases > 0:
        k = int(np.ceil(0.2 * n_cases))
        k = max(k, 1)
        deep = data.sort_values("f", kind="mergesort").iloc[:k]
        sup_val = float(deep["ex"].mean())
        sup_pass = bool(sup_val < 0)

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "day-clustered OLS slope t", "value": tstat} if tstat is not None else None),
            "threshold": threshold}
    sup = {"name": sup_name, "value": sup_val, "passed": sup_pass}

    if n_cases < 300:
        status = "not observable"
        decided = f"The plan needs at least 300 independent cases; only {n_cases} are in the record."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the deepest fifth's mean excess return is below 0 (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the deepest fifth's mean excess return is not below 0 (inconclusive rule)."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: deeper dips are followed by larger rises than drift (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
