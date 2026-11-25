import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    LH = "debug_info.components.thin_volume.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            lh = pd.to_numeric(df[LH], errors="coerce").values if LH in df.columns else np.full(len(df), np.nan)
            reg = df["regime"].astype(str).values
            n = len(df)
            ret28 = np.full(n, np.nan)
            if n > 28:
                ret28[28:] = close[28:] / close[:-28] - 1.0
            for i in range(n):
                if not np.isfinite(fc[i]) or fc[i] == 0:
                    continue
                n_active += 1
                if np.isfinite(ret28[i]):
                    decline = ret28[i] < 0
                else:
                    decline = reg[i] == "trending"
                thin = np.isfinite(lh[i]) and lh[i] < 0
                if decline and thin and fc[i] < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    mm_name = "clustered OLS slope of 5-bar excess return on forecast, trending grid cells"
    mm_thr = "confirm: slope > 0 with t >= 2 (and supporting check); reject: slope < 0 with t <= -2; else inconclusive"
    reading = ("Situation bars are those with a negative 28-bar close-to-close return inside the window (the recorded regime "
               "where 28 prior bars are not in the window), raw log volume ratio below 0 and a negative forecast; the slope's t "
               "uses an OLS with intercept and standard errors clustered by calendar day (UTC); the coin's mean 5-bar return "
               "uses all grid cells of all its windows; the plan's 'inconclusive with fewer cases' is reported as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": mm_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the active bars are 28-day-decline bars with volume below its usual level "
                           "and a short forecast, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        all_rets = []
        cells = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                all_rets.append(r)
                cells.append((df.loc[i, "regime"], df.loc[i, "forecast"], df.loc[i, "timestamp"], r))
        if not all_rets:
            continue
        mu = float(np.mean(all_rets))
        for reg, f, ts, r in cells:
            f = pd.to_numeric(f, errors="coerce")
            if str(reg) != "trending" or not np.isfinite(f):
                continue
            day = pd.Timestamp(ts)
            if day.tzinfo is not None:
                day = day.tz_convert("UTC").tz_localize(None)
            rows.append((coin, day.normalize(), float(f), r - mu))

    d = pd.DataFrame(rows, columns=["coin", "day", "f", "ex"])
    n_reg = int(len(d))
    strong = d[d["f"] <= -2] if n_reg else d
    n_strong = int(len(strong))
    counts = {"regime grid cells": n_reg, "grid cells with forecast <= -2": n_strong,
              "days of regime grid cells": int(d["day"].nunique()) if n_reg else 0}

    sup_val = float((-strong["ex"]).mean()) if n_strong > 0 else None
    sup_pass = (sup_val is not None and sup_val > 0) if n_strong > 0 else None

    slope = None
    tval = None
    if n_reg >= 3 and d["f"].nunique() > 1:
        X = np.column_stack([np.ones(n_reg), d["f"].values])
        y = d["ex"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        groups = d["day"].values
        G = 0
        for g in pd.unique(groups):
            m = groups == g
            s = X[m].T @ u[m]
            meat += np.outer(s, s)
            G += 1
        k = 2
        corr = (G / (G - 1)) * ((n_reg - 1) / (n_reg - k)) if G > 1 else 1.0
        V = XtX_inv @ meat @ XtX_inv * corr
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        tval = float(slope / se) if np.isfinite(se) and se > 0 else None

    main = {"name": mm_name, "value": slope,
            "statistic": {"name": "day-clustered OLS t", "value": tval} if tval is not None else None,
            "threshold": mm_thr}
    sup = {"name": "mean negated excess 5-bar return, cells with forecast <= -2", "value": sup_val, "passed": sup_pass}

    if n_reg < 100 or n_strong < 30:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_reg} regime grid cells (100 needed) and "
                   f"{n_strong} cells with forecast <= -2 (30 needed).")
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: thinner-volume declines fall less than heavy-volume ones."
    else:
        status = "inconclusive"
        decided = "The slope's |t| is below 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
