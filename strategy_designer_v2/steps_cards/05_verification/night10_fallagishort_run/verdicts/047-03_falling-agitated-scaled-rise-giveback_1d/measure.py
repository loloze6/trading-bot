import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.scaled_rise.last_history_value"
    T_CONF, T_REJ = -2.0, 2.0
    MIN_SHORT, MIN_DAYS = 100, 60

    # ---------- per-coin mean daily return over all windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp")
            c = d["close"].astype(float).values
            if len(c) > 1:
                rets.append(c[1:] / c[:-1] - 1.0)
        allr = np.concatenate(rets) if rets else np.array([])
        allr = allr[np.isfinite(allr)]
        coin_mean[coin] = float(allr.mean()) if allr.size else np.nan

    # ---------- situation check and collection of short bars ----------
    n_active = 0
    n_agree = 0
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            prev_ret = close / close.shift(1) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # up day: raw scaled return > 0 where recorded, else from prices
            up = np.where(raw.notna(), raw > 0, prev_ret > 0)
            up = pd.Series(up, index=d.index).astype(bool)
            in_profile = d["regime"].astype(str) == "unknown"
            active = fc != 0
            agree = active & in_profile & up & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            nxt = close.shift(-1) / close - 1.0
            ts = pd.to_datetime(d["timestamp"], utc=True).dt.floor("D")
            sel = (fc < 0) & nxt.notna()
            for i in np.where(sel.values)[0]:
                rows.append((coin, ts.iloc[i], abs(float(fc.iloc[i])),
                             float(nxt.iloc[i]) - coin_mean[coin]))

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of next-day excess return on abs(forecast), short bars"
    thr = "confirm if slope t <= -2 (with mean excess < 0); reject if slope t >= +2"
    reading = ("Profile bars are those with regime 'unknown' (the detector's only non-vetoed regime, i.e. falling and "
               "agitated), up days are a positive raw scaled return (price change when unrecorded), every short bar with "
               "a next close in its window is used (1-bar horizon grid), and the slope's t uses cluster-robust (CR1) "
               "standard errors clustered by UTC day.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars on up days inside the "
                           "falling agitated profile, as the Fidelity requires."),
            "reading": reading,
        }

    data = pd.DataFrame(rows, columns=["coin", "day", "x", "y"])
    n_short = int(len(data))
    n_days = int(data["day"].nunique()) if n_short else 0
    counts = {"short bars": n_short, "distinct days": n_days}

    slope = None
    tval = None
    mean_ex = None
    if n_short >= 3:
        x = data["x"].values
        y = data["y"].values
        X = np.column_stack([np.ones(n_short), x])
        XtX = X.T @ X
        if np.linalg.matrix_rank(XtX) == 2:
            XtX_inv = np.linalg.inv(XtX)
            beta = XtX_inv @ X.T @ y
            resid = y - X @ beta
            meat = np.zeros((2, 2))
            codes = pd.factorize(data["day"])[0]
            G = codes.max() + 1
            for g in range(G):
                m = codes == g
                s = X[m].T @ resid[m]
                meat += np.outer(s, s)
            corr = (G / (G - 1)) * ((n_short - 1) / (n_short - 2)) if G > 1 else np.nan
            V = corr * XtX_inv @ meat @ XtX_inv
            se = float(np.sqrt(V[1, 1])) if np.isfinite(V[1, 1]) and V[1, 1] > 0 else np.nan
            slope = float(beta[1])
            tval = float(slope / se) if np.isfinite(se) and se > 0 else None
    if n_short:
        mean_ex = float(data["y"].mean())

    sup_pass = None if mean_ex is None else bool(mean_ex < 0)
    main = {"name": main_name, "value": slope,
            "statistic": None if tval is None else {"name": "slope t (day-clustered)", "value": tval},
            "threshold": thr}
    sup = {"name": "mean next-day excess return on short bars", "value": mean_ex, "passed": sup_pass}

    if n_short < MIN_SHORT or n_days < MIN_DAYS:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_short} short bars (need 100) and {n_days} distinct days "
                   f"(need 60).")
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval <= T_CONF and sup_pass:
        status = "confirmed"
        decided = "The slope's t is -2 or less and the mean excess next-day return is below 0."
    elif tval >= T_REJ:
        status = "rejected"
        decided = "The slope's t is +2 or more: larger scaled rises are followed by larger next-day gains."
    elif tval <= T_CONF:
        status = "inconclusive"
        decided = "The slope's t is -2 or less but the mean excess next-day return is not below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
