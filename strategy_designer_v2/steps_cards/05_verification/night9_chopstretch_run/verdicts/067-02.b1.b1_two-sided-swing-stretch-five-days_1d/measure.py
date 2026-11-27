import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    STRETCH = "debug_info.components.stretch.last_history_value"

    def recompute_stretch(close):
        # MovingAverageDistance: (close - SMA20) / SMA20 / std of last 20 daily returns
        sma = close.rolling(20, min_periods=20).mean()
        vol = close.pct_change().rolling(20, min_periods=20).std()
        return (close - sma) / sma / vol

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce")
            if STRETCH in df.columns:
                raw = pd.to_numeric(df[STRETCH], errors="coerce")
                recorded = raw.notna().values
            else:
                raw = pd.Series(np.nan, index=df.index)
                recorded = np.zeros(len(df), dtype=bool)
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            # choppy profile = the regime the idea's strategy runs in ("unknown"), where stretch is recorded
            in_profile = recorded | (regime == "unknown")
            raw_full = raw.copy()
            rec = recompute_stretch(close)
            raw_full = raw_full.where(raw_full.notna(), rec).values
            active = f != 0
            side_ok = np.sign(f) == np.sign(raw_full)
            side_ok &= ~np.isnan(raw_full)
            n_active += int(active.sum())
            n_agree += int((active & in_profile & side_ok).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are bars of the choppy profile "
                           "where the forecast's sign equals the stretch's sign (long above the 20-day SMA, short below)."),
            "reading": "The choppy profile is read as the strategy's active regime (stretch component recorded, regime 'unknown'); "
                       "the side is the sign of the raw stretch, recomputed from closes where not recorded.",
        }

    # ---------- 2. criterion ----------
    # coin mean 5-day return over all windows (non-overlapping grid, all grid bars)
    coin_mean = {}
    cases = []
    for coin, wins in bars.items():
        all_r = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_r.append(r)
                if np.isfinite(f[i]) and f[i] != 0:
                    cases.append((coin, ts.iloc[i].floor("D"), float(f[i]), r))
        coin_mean[coin] = float(np.mean(all_r)) if all_r else np.nan

    rows = [(c, d, fv, r - coin_mean[c]) for (c, d, fv, r) in cases if np.isfinite(coin_mean[c])]
    total = len(rows)
    fv = np.array([r[2] for r in rows], dtype=float)
    ex = np.array([r[3] for r in rows], dtype=float)
    days = np.array([str(r[1]) for r in rows])
    n_long = int((fv > 0).sum())
    n_short = int((fv < 0).sum())

    counts = {"grid cases in total": total, "long grid cases": n_long, "short grid cases": n_short}

    slope = None
    tval = None
    if total >= 3 and np.var(fv) > 0:
        X = np.column_stack([np.ones(total), fv])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ ex
        e = ex - X @ beta
        meat = np.zeros((2, 2))
        uniq = np.unique(days)
        for d in uniq:
            m = days == d
            s = X[m].T @ e[m]
            meat += np.outer(s, s)
        G = len(uniq)
        K = 2
        corr = (G / (G - 1)) * ((total - 1) / (total - K)) if G > 1 else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        slope = float(beta[1])
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        tval = float(slope / se) if np.isfinite(se) and se > 0 else None

    long_mean = float(np.mean(ex[fv > 0])) if n_long > 0 else None
    short_mean = float(np.mean(-ex[fv < 0])) if n_short > 0 else None
    sup_pass = None
    if long_mean is not None and short_mean is not None:
        sup_pass = bool(long_mean > 0 and short_mean > 0)

    main = {
        "name": "slope of 5-day excess return on forecast (grid bars, clustered by day)",
        "value": slope,
        "statistic": {"name": "day-clustered t of slope", "value": tval} if tval is not None else None,
        "threshold": "confirm: slope > 0 with t >= 2 and both sides' signed excess > 0; reject: slope < 0 with t <= -2",
    }
    support = {
        "name": "mean signed excess 5-day return, long and short sides (min of the two)",
        "value": (min(long_mean, short_mean) if (long_mean is not None and short_mean is not None) else None),
        "passed": sup_pass,
        "long_side_mean": long_mean,
        "short_side_mean": short_mean,
    }
    reading = ("The choppy profile is the strategy's active regime (stretch recorded / regime 'unknown') and the side is the raw stretch's sign; "
               "the coin's mean 5-day return is over all its non-overlapping grid bars of all windows; the slope's t is OLS with day-clustered "
               "standard errors (with small-sample correction); the plan's 'fewer is inconclusive' is reported as 'not observable' per the workflow.")

    sc = {"agreement": (float(agreement) if agreement is not None else None), "passed": True}

    if total < 100 or n_long < 30 or n_short < 30:
        status = "not observable"
        decided = (f"Minimum counts not reached: {total} grid cases (need 100), {n_long} long and {n_short} short (need 30 each).")
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed on the grid cases."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Slope positive with t >= 2 and the signed excess 5-day return is above 0 on both long and short grid bars."
        else:
            status = "inconclusive"
            decided = "Slope positive with t >= 2 but one side's signed excess 5-day return is not above 0."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "Slope negative with t <= -2: large stretches are followed by a return toward the average."
    else:
        status = "inconclusive"
        decided = "The slope has |t| < 2, neither confirming nor rejecting."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
