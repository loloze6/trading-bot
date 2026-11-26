import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.depth.last_history_value"
    H = 1
    MIN_DAYS = 100

    # ---------- per-coin mean daily return over all windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp") if "timestamp" in df.columns else df
            c = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) > H:
                r = c[H:] / c[:-H] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if allr.size else np.nan

    # ---------- situation check + case collection ----------
    n_active = 0
    n_agree = 0
    case_x, case_y, case_day = [], [], []

    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.copy()
            if "timestamp" in d.columns:
                d["_ts"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
                d = d.sort_values("_ts").reset_index(drop=True)
            else:
                d = d.reset_index(drop=True)
                d["_ts"] = pd.NaT
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            raw = (pd.to_numeric(d[RAW], errors="coerce").to_numpy(dtype=float)
                   if RAW in d.columns else np.full(len(d), np.nan))
            regime = d["regime"].astype(str).to_numpy() if "regime" in d.columns else np.array([""] * len(d))
            n = len(d)

            # up day from prices (1-bar return > 0); first bar of a window: detector's decision
            prev = np.r_[np.nan, close[:-1]]
            ret1 = close / prev - 1.0
            up = np.where(np.isfinite(ret1), ret1 > 0, regime == "mean_reversion")
            # agitated profile: detector components not recorded -> its decision (not vetoed to chop,
            # and the up-day rule's regime)
            agitated = regime == "mean_reversion"
            # depth: close below 20-day high (raw distance negative)
            below = np.isfinite(raw) & (raw < 0)
            situation = up & agitated & below

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            # next-day return within the window
            nxt = np.r_[close[H:], np.full(H, np.nan)]
            fwd = nxt / close - 1.0
            mu = coin_mean.get(coin, np.nan)
            for i in range(n):
                if fc[i] < 0 and np.isfinite(fwd[i]) and np.isfinite(mu):
                    case_x.append(abs(fc[i]))
                    case_y.append(fwd[i] - mu)
                    ts = d["_ts"].iloc[i]
                    case_day.append(str(ts.date()) if pd.notna(ts) else f"{coin}_{w}_{i}")

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    threshold_txt = ("confirm: slope < 0 with t <= -2 and supporting check passes; "
                     "reject: slope > 0 with t >= +2; otherwise inconclusive; at least 100 distinct case days")
    main_name = "slope of next-day excess return on abs(forecast), cases forecast < 0"
    reading = ("Profile and the up-day rule on a window's first bar are taken from the recorded regime "
               "(the detector's components are not recorded), the up day elsewhere from the 1-bar close return, "
               "the depth from the raw component being below 0; the slope t uses a day-clustered (by UTC date) "
               "OLS standard error with the usual small-sample correction, the coin's mean is over all 1-bar "
               "returns of all its windows, and the 100-case-day minimum is treated as a minimum count "
               "(not observable when missed).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are short bars on an up-day close "
                           "below the 20-day high inside the agitated profile, as the Fidelity's situation and side require."),
            "reading": reading,
        }

    x = np.asarray(case_x, dtype=float)
    y = np.asarray(case_y, dtype=float)
    days = np.asarray(case_day)
    n_cases = int(len(x))
    n_days = int(len(np.unique(days))) if n_cases else 0

    slope = None
    t_slope = None
    if n_cases >= 3 and np.ptp(x) > 0:
        X = np.column_stack([np.ones(n_cases), x])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ (X.T @ y)
        u = y - X @ beta
        meat = np.zeros((2, 2))
        uniq, inv = np.unique(days, return_inverse=True)
        G = len(uniq)
        sg = np.zeros((G, 2))
        np.add.at(sg, inv, X * u[:, None])
        meat = sg.T @ sg
        V = XtX_inv @ meat @ XtX_inv
        if G > 1 and n_cases > 2:
            V = V * (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - 2.0))
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t_slope = float(slope / se) if np.isfinite(se) and se > 0 else None

    sup_val = float(np.mean(-y)) if n_cases else None
    sup_pass = (sup_val is not None and sup_val > 0)

    counts = {"distinct case days": n_days, "cases": n_cases}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Only {n_days} distinct case days across coins and windows, below the plan's minimum of 100."
    elif slope is None or t_slope is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed on the cases, so neither confirm nor reject is met."
    elif slope < 0 and t_slope <= -2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is negative with t <= -2 and the mean short-direction excess return is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is negative with t <= -2 but the supporting check (mean short-direction excess > 0) fails."
    elif slope > 0 and t_slope >= 2:
        status = "rejected"
        decided = "The slope is positive with t >= +2: deeper up-day closes are followed by stronger next-day moves."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "day-clustered OLS slope t", "value": t_slope} if t_slope is not None else None),
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "mean next-day excess return in short direction > 0",
            "value": sup_val,
            "passed": (bool(sup_pass) if sup_val is not None else None),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
