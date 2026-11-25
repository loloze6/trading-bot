import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    FC = "forecast"
    REG = "regime"
    RAW = "debug_info.components.fall28.last_history_value"

    # ---------- 1. situation check ----------
    # The regime detector's component (vr) is not recorded, and each window (~120 bars) is too short to rebuild
    # a 28-day mean against the 365 days before it, so the detector's own decision (regime == "trending",
    # i.e. vr < 1) is taken as the thin-volume situation; the expected side is short (forecast < 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df[FC], errors="coerce")
            active = f.notna() & (f != 0)
            reg = df[REG].astype(str) if REG in df.columns else pd.Series("", index=df.index)
            situ = reg == "trending"
            n_active += int(active.sum())
            n_agree += int((active & situ & (f < 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9) if n_active > 0 else True

    main_name = "slope of 10-bar excess forward return on forecast (thin-volume short cases)"
    threshold = "confirm if cluster-by-day t >= 2 with supporting mean > 0; reject if t <= -2"
    reading_base = ("Thin-volume situation taken from the recorded regime (trending = vr<1) since vr cannot be "
                    "rebuilt in-window; coin mean 10-bar return taken on the non-overlapping grid of all its windows; "
                    "slope t from OLS with intercept and CR1 standard errors clustered by UTC day; supporting check "
                    "read as the mean of minus (return minus coin mean); the plan's 'fewer than 30 cases or 20 days' "
                    "treated as minimum counts giving 'not observable'.")

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are thin-volume (trending regime) "
                           "bars with a short forecast, so the config does not do what the Fidelity says."),
            "reading": reading_base,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            f = pd.to_numeric(d[FC], errors="coerce").values
            reg = d[REG].astype(str).values if REG in d.columns else np.array([""] * len(d))
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_rets.append(r)
                if reg[i] == "trending" and np.isfinite(f[i]) and f[i] < 0:
                    coin_cases.append((r, float(f[i]), ts.iloc[i].strftime("%Y-%m-%d")))
        if len(coin_rets) == 0:
            continue
        mu = float(np.mean(coin_rets))
        for r, fv, day in coin_cases:
            rows.append({"coin": coin, "excess": r - mu, "f": fv, "day": day})

    cases = pd.DataFrame(rows, columns=["coin", "excess", "f", "day"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    slope = None
    tval = None
    sup = None
    if n_cases >= 3 and cases["f"].nunique() > 1:
        y = cases["excess"].values.astype(float)
        X = np.column_stack([np.ones(n_cases), cases["f"].values.astype(float)])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        slope = float(beta[1])
        G = n_days
        if G >= 2:
            meat = np.zeros((2, 2))
            for _, idx in cases.groupby("day").indices.items():
                s = X[idx].T @ u[idx]
                meat += np.outer(s, s)
            adj = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - 2.0))
            V = adj * XtX_inv @ meat @ XtX_inv
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            tval = float(slope / se) if np.isfinite(se) and se > 0 else None
    if n_cases > 0:
        sup = float(np.mean(-cases["excess"].values))

    sup_pass = None if sup is None else bool(sup > 0)

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases (minimum 30) and {n_days} distinct days "
                   f"(minimum 20).")
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the supporting mean excess return in the short's direction is above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting mean is 0 or below, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": bool(passed)},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t, clustered by day", "value": tval} if tval is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 10-bar return in the short's direction",
            "value": sup,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
