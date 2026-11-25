import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    LHV = "debug_info.components.depth.last_history_value"
    PPV = "debug_info.components.depth.post_pipeline_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            # 30-day percent distance below the highest close, current bar included (recomputed inside the window)
            hh = close.rolling(30, min_periods=30).max()
            recomputed = (close / hh - 1.0) * 100.0
            if LHV in d.columns:
                depth_raw = pd.to_numeric(d[LHV], errors="coerce")
                depth_raw = depth_raw.where(depth_raw.notna(), recomputed)
            else:
                depth_raw = recomputed
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            regime = d["regime"].astype(str)
            # falling calm profile = the detector did not veto to chop (its components are not recorded)
            in_profile = regime.str.lower().eq("unknown")
            below_high = depth_raw < 0
            situation = in_profile & below_high
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "slope of 3-bar forward return minus coin's mean 3-bar return on depth post_pipeline_value (grid bars with non-zero forecast)"
    threshold = "confirm: slope > 0 with t >= 2 (and supporting check passes); reject: slope < 0 with t <= -2; |t| < 2 inconclusive; < 100 grid cases"
    reading_base = ("Profile taken from the recorded regime ('unknown' = not vetoed to chop, the detector's components are not recorded) "
                    "and depth from last_history_value; the t is an OLS slope t with standard errors clustered by UTC calendar day "
                    "(small-sample factor G/(G-1)*(n-1)/(n-2)); the coin's mean 3-bar return is over its non-overlapping grid of all bars of all windows; "
                    "the 100-case minimum counts grid cases with a non-zero forecast and a full 3-bar forward return.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars in the falling calm profile "
                           "with the close below its 30-day high, as the Fidelity's situation requires."),
            "reading": reading_base,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_all = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            n = len(d)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            ppv = pd.to_numeric(d[PPV], errors="coerce").values if PPV in d.columns else np.full(n, np.nan)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                grid_all.append(r)
                if fc[i] != 0 and np.isfinite(ppv[i]):
                    coin_cases.append((coin, ts.iloc[i].strftime("%Y-%m-%d"), r, float(ppv[i])))
        if len(grid_all) == 0:
            continue
        drift = float(np.mean(grid_all))
        for (c, day, r, x) in coin_cases:
            rows.append({"coin": c, "day": day, "y": r - drift, "x": x})

    cases = pd.DataFrame(rows, columns=["coin", "day", "y", "x"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    slope = None
    t = None
    sup_val = None
    sup_pass = None
    if n_cases >= 3 and cases["x"].nunique() > 1:
        X = np.column_stack([np.ones(n_cases), cases["x"].values])
        y = cases["y"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in cases.groupby("day").indices.items():
            s = X[idx].T @ e[idx]
            meat += np.outer(s, s)
        G = n_days
        if G > 1 and n_cases > 2:
            c = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - 2.0))
            V = c * XtX_inv @ meat @ XtX_inv
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            slope = float(beta[1])
            t = float(slope / se) if np.isfinite(se) and se > 0 else None
        else:
            slope = float(beta[1])
    if n_cases > 0:
        sup_val = float(np.mean(-cases["y"].values))  # unusual move in the short direction
        sup_pass = bool(sup_val > 0)

    counts = {"independent grid cases in a position": n_cases, "days": n_days, "active bars": n_active}

    if n_cases < 100:
        status = "not observable"
        decided = f"Fewer than 100 independent grid cases in a position ({n_cases}), the plan's minimum."
    elif t is None or slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the mean unusual 3-bar move in the short direction is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: deeper distances below the high are followed by higher returns."
    else:
        status = "inconclusive"
        decided = "The slope's |t| is below 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t, clustered by day", "value": t} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean unusual 3-bar move in the short direction (minus coin drift) > 0",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
