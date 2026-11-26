import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    FC = "forecast"
    RAW = "debug_info.components.dryup.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if FC not in df.columns or len(df) == 0:
                continue
            close = df["close"].astype(float)
            fc = df[FC].astype(float)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            raw = df[RAW].astype(float) if RAW in df.columns else pd.Series(np.nan, index=df.index)
            ret20 = close / close.shift(20) - 1.0
            profile = regime == "trending"
            # where the 20-day return cannot be computed inside the window, the regime (which applies ret20<0) stands in
            fall20 = np.where(ret20.notna(), ret20 < 0, profile)
            shrunk = raw < 0
            situ = profile.values & fall20.astype(bool) & shrunk.fillna(False).values
            active = (fc != 0) & fc.notna()
            n_active += int(active.sum())
            n_agree += int((active.values & situ & (fc < 0).values).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "clustered-by-day t of the slope of drift-adjusted next 5-bar return on forecast, trending grid bars"
    thr = "confirm: slope > 0 with t >= 2 and supporting mean > 0; reject: slope < 0 with t <= -2; else inconclusive"
    reading = ("Grid = rows 0,5,10,... of each window; normal drift = the coin's mean non-overlapping 5-bar return over all its "
               "windows; in-regime = regime 'trending'; slope t uses day-clustered (CR1) standard errors; the situation check "
               "takes profile = regime 'trending', 20-day fall from prices (regime where not computable) and shrinkage = raw dryup < 0; "
               "fewer than the plan's minimum cases is reported as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars of the plan's situation "
                           "(falling profile, 20-day return < 0, 30-day volume shrunk against the 30 days before)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                coin_rets.append(r)
                if str(df.loc[i, "regime"]) == "trending":
                    f = float(df.loc[i, FC]) if FC in df.columns else np.nan
                    if np.isfinite(f):
                        day = pd.Timestamp(df.loc[i, "timestamp"]).floor("D")
                        coin_rows.append((coin, day, f, r))
        if len(coin_rets) == 0:
            continue
        drift = float(np.mean(coin_rets))
        for coin_, day, f, r in coin_rows:
            rows.append({"coin": coin_, "day": day, "x": f, "y": r - drift})

    data = pd.DataFrame(rows, columns=["coin", "day", "x", "y"])
    n_total = int(len(data))
    neg = data[data["x"] < 0]
    n_neg = int(len(neg))
    counts = {"in-regime grid cases": n_total, "grid cases with forecast < 0": n_neg,
              "days": int(data["day"].nunique()) if n_total else 0}

    # supporting check
    if n_neg > 0:
        sup_val = float((-neg["y"]).mean())
        sup_pass = bool(sup_val > 0)
    else:
        sup_val, sup_pass = None, None

    # slope with day-clustered SE
    slope, tval = None, None
    if n_total >= 3 and data["x"].var() > 0:
        X = np.column_stack([np.ones(n_total), data["x"].values])
        y = data["y"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        codes = pd.factorize(data["day"])[0]
        G = int(codes.max()) + 1
        for g in range(G):
            m = codes == g
            s = X[m].T @ u[m]
            meat += np.outer(s, s)
        if G > 1:
            corr = (G / (G - 1.0)) * ((n_total - 1.0) / (n_total - 2.0))
            V = corr * XtX_inv @ meat @ XtX_inv
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            slope = float(beta[1])
            tval = float(slope / se) if np.isfinite(se) and se > 0 else None
        else:
            slope = float(beta[1])

    main = {"name": main_name, "value": slope,
            "statistic": {"name": "day-clustered OLS slope t", "value": tval} if tval is not None else None,
            "threshold": thr}
    sup = {"name": "mean short-side unusual move on grid cases with forecast < 0", "value": sup_val, "passed": sup_pass}

    if n_neg < 30 or n_total < 60:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_neg} grid cases with forecast < 0 (needs 30) and "
                   f"{n_total} in-regime grid cases (needs 60).")
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Confirm rule: the slope is positive with t >= 2 and the supporting short-side mean is above 0."
        else:
            status = "inconclusive"
            decided = "A positive slope with t >= 2 but the supporting short-side mean is not above 0: inconclusive."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "Reject rule: the slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t is strictly between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
