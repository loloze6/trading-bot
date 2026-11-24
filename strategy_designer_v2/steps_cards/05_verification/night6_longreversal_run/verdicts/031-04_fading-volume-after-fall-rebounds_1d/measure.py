import json
import numpy as np
import pandas as pd


def measure(bars):
    H = 30
    REGIME = "mean_reversion"
    COMP = "vol_dry"

    def get_raw(df):
        col = "debug_info.components.%s.last_history_value" % COMP
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").to_numpy(dtype=float)
        out = np.full(len(df), np.nan)
        if "debug_info.components" in df.columns:
            for i, v in enumerate(df["debug_info.components"].tolist()):
                d = v
                if isinstance(d, str):
                    try:
                        d = json.loads(d)
                    except Exception:
                        d = None
                if isinstance(d, dict):
                    c = d.get(COMP)
                    if isinstance(c, dict):
                        x = c.get("last_history_value")
                        try:
                            out[i] = float(x)
                        except (TypeError, ValueError):
                            pass
        return out

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            reg = df["regime"].astype(str).to_numpy()
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            raw = get_raw(df)
            for i in range(len(df)):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                ok = (reg[i] == REGIME) and (f > 0)
                # volume below its 90-day mean: raw log ratio < 0
                ok = ok and np.isfinite(raw[i]) and raw[i] < 0
                # where 90 prior bars exist in the window, the 90-day return must be negative
                if ok and i >= 90 and np.isfinite(close[i]) and np.isfinite(close[i - 90]) and close[i - 90] > 0:
                    ok = (close[i] / close[i - 90] - 1.0) < 0
                if ok:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of 30-day forward return minus coin drift on forecast, regime grid bars"
    thr = "slope t >= 2 (with supporting check) confirms; t <= -2 rejects; between is inconclusive"
    reading = ("The situation is read from the recorded regime (the detector's 365-day volatility cannot be rebuilt "
               "inside ~120-bar windows), required long, with the vol_dry raw log ratio below 0 and, where 90 bars of "
               "the window exist, a negative 90-day return; the drift is the coin's mean 30-bar return on the "
               "non-overlapping grid of all its windows; the slope is pooled OLS with intercept over all coins with "
               "CR1 standard errors clustered by calendar day.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars in the mean_reversion "
                           "fall regime with volume below its 90-day mean, as the Fidelity's situation requires."),
            "reading": reading,
        }

    # ---------- criterion ----------
    rows = []
    drift = {}
    for coin, wins in bars.items():
        allret = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            reg = df["regime"].astype(str).to_numpy()
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                allret.append(r)
                if reg[i] == REGIME and np.isfinite(fc[i]) and not pd.isna(ts.iloc[i]):
                    rows.append((coin, r, float(fc[i]), ts.iloc[i].strftime("%Y-%m-%d")))
        drift[coin] = float(np.mean(allret)) if allret else np.nan

    data = pd.DataFrame(rows, columns=["coin", "ret", "fc", "day"])
    if len(data):
        data["ex"] = data["ret"] - data["coin"].map(drift)
        data = data[np.isfinite(data["ex"])]
    n_cases = int(len(data))
    pos = data[data["fc"] > 0] if n_cases else data
    n_pos = int(len(pos))
    counts = {"grid cases in the regime": n_cases, "grid cases with a forecast above 0": n_pos,
              "days clustered": int(data["day"].nunique()) if n_cases else 0}

    sup_val = float(pos["ex"].mean()) if n_pos > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None
    supporting = {"name": "mean 30-day return minus drift, regime grid cases with forecast > 0",
                  "value": sup_val, "passed": sup_pass}

    slope = None
    tval = None
    if n_cases >= 3 and np.var(data["fc"].to_numpy()) > 0:
        X = np.column_stack([np.ones(n_cases), data["fc"].to_numpy(dtype=float)])
        y = data["ex"].to_numpy(dtype=float)
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        resid = y - X @ beta
        slope = float(beta[1])
        groups = data["day"].to_numpy()
        G = len(np.unique(groups))
        if G >= 2:
            meat = np.zeros((2, 2))
            for g in np.unique(groups):
                m = groups == g
                s = X[m].T @ resid[m]
                meat += np.outer(s, s)
            K = 2
            corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - K)) if n_cases > K else 1.0
            V = corr * XtX_inv @ meat @ XtX_inv
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else 0.0
            if se > 0:
                tval = float(slope / se)

    main = {"name": main_name, "value": slope,
            "statistic": {"name": "slope t, SE clustered by day", "value": tval} if tval is not None else None,
            "threshold": thr}

    if n_cases < 20 or n_pos < 10:
        status = "not observable"
        decided = ("Minimum count not reached: %d grid cases in the regime (need 20) and %d with a forecast above 0 "
                   "(need 10)." % (n_cases, n_pos))
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no forecast variation or a single day cluster), so it meets neither rule."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm rule met: the slope's t is 2 or more and the supporting check passes."
    elif tval <= -2:
        status = "rejected"
        decided = "Reject rule met: the slope's t is -2 or less."
    elif tval >= 2:
        status = "inconclusive"
        decided = "Inconclusive rule: the slope's t is 2 or more but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
