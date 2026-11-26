import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    FC = "forecast"

    # ---------- helpers ----------
    def _ts(df):
        return pd.to_datetime(df["timestamp"], utc=True)

    def _fwd(close, h):
        c = close.to_numpy(dtype=float)
        out = np.full(len(c), np.nan)
        if len(c) > h:
            out[:-h] = c[h:] / c[:-h] - 1.0
        return out

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).to_numpy()
            fc = pd.to_numeric(df[FC], errors="coerce").to_numpy()
            reg = df["regime"].astype(str).to_numpy()
            n = len(df)
            ret30 = np.full(n, np.nan)
            if n > 30:
                ret30[30:] = close[30:] / close[:-30] - 1.0
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                if np.isfinite(ret30[i]):
                    in_fall = ret30[i] < 0
                else:
                    # 30-day return not computable inside the window: use the detector's decision
                    in_fall = reg[i] == "trending"
                if in_fall and f < 0:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "slope of drift-adjusted 5-bar forward return on forecast, fall-regime grid bars"
    threshold = "confirm: slope > 0 with day-clustered t >= 2 (and supporting check passes); reject: slope < 0 with t <= -2"
    reading = ("The 30-day fall is close[t]/close[t-30]-1 < 0 within the window, using the recorded regime where the window "
               "has fewer than 30 prior bars; the regime sample uses the recorded regime 'trending'; the drift is the coin's mean "
               "5-bar return on the non-overlapping grid of all its windows; the slope's t is cluster-robust (CR1) by UTC day; "
               "the plan's 'fewer cases' rule is reported as 'not observable' per the workflow.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active_bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars during a 30-day fall, "
                           "so the config does not do what the Fidelity's situation and side say."
                           if n_active > 0 else "No bar has a non-zero forecast, so the plan's situation is never traded."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fwd = _fwd(df["close"].astype(float), H)
            ts = _ts(df)
            fc = pd.to_numeric(df[FC], errors="coerce").to_numpy()
            reg = df["regime"].astype(str).to_numpy()
            for i in range(0, len(df), H):
                if not np.isfinite(fwd[i]):
                    continue
                coin_rets.append(fwd[i])
                coin_rows.append((ts.iloc[i].floor("D"), fwd[i], fc[i], reg[i]))
        if not coin_rets:
            continue
        drift = float(np.mean(coin_rets))
        for d, r, f, rg in coin_rows:
            if rg == "trending" and np.isfinite(f):
                rows.append((d, r - drift, float(f)))

    n_reg = len(rows)
    strong = [r for r in rows if r[2] <= -2]
    n_strong = len(strong)
    n_days = len(set(r[0] for r in strong))
    counts = {
        "grid bars in the fall regime": int(n_reg),
        "grid bars in the fall regime with a forecast of -2 or lower": int(n_strong),
        "distinct days of those bars": int(n_days),
    }

    # supporting check
    if n_strong > 0:
        sup_val = float(np.mean([-r[1] for r in strong]))
        sup_pass = bool(sup_val > 0)
    else:
        sup_val, sup_pass = None, None
    supporting = {"name": "mean drift-adjusted 5-bar return in the short direction, forecast <= -2",
                  "value": sup_val, "passed": sup_pass}

    # regression with day-clustered t
    slope, tval = None, None
    if n_reg >= 3:
        y = np.array([r[1] for r in rows])
        x = np.array([r[2] for r in rows])
        days = np.array([r[0].value for r in rows])
        X = np.column_stack([np.ones(n_reg), x])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) == 2:
            XtX_inv = np.linalg.inv(XtX)
            beta = XtX_inv @ X.T @ y
            e = y - X @ beta
            meat = np.zeros((2, 2))
            uniq = np.unique(days)
            for g in uniq:
                m = days == g
                s = X[m].T @ e[m]
                meat += np.outer(s, s)
            G = len(uniq)
            if G > 1:
                corr = (G / (G - 1.0)) * ((n_reg - 1.0) / (n_reg - 2.0))
                V = corr * XtX_inv @ meat @ XtX_inv
                slope = float(beta[1])
                se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else 0.0
                tval = float(slope / se) if se > 0 else None
            else:
                slope = float(beta[1])

    main = {"name": main_name, "value": slope,
            "statistic": None if tval is None else {"name": "day-clustered OLS slope t", "value": tval},
            "threshold": threshold}

    if n_strong < 100 or n_days < 30:
        status = "not observable"
        decided = ("The plan's minimum of 100 fall-regime grid bars with a forecast of -2 or lower over at least 30 distinct "
                   f"days is not reached ({n_strong} bars, {n_days} days).")
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the supporting check passes (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting check fails (inconclusive rule)."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
