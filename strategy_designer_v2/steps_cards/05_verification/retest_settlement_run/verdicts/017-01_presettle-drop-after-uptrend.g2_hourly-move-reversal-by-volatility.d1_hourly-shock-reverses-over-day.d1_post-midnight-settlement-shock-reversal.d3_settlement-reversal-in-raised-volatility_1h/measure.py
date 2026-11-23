import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    RAW = "debug_info.components.settle_fade.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            ts = pd.to_datetime(df["timestamp"], utc=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            close = pd.to_numeric(df["close"], errors="coerce")
            ret1 = (close / close.shift(1) - 1.0).to_numpy()
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy()
            else:
                raw = np.full(len(df), np.nan)
            move = np.where(np.isfinite(raw), raw, ret1)
            hour0 = (ts.dt.hour == 0).to_numpy()
            active = f != 0
            expected_side = -np.sign(move)  # fade of the settlement-hour move
            ok = hour0 & np.isfinite(move) & (np.sign(f) == expected_side) & (expected_side != 0)
            n_active += int(active.sum())
            n_agree += int((active & ok).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9
    reading = ("The situation is the bar whose timestamp (start) is 00:00 UTC with the forecast's sign opposite to the "
               "sign of the raw settle_fade value (price return where missing); the slope is an OLS with intercept of "
               "excess 24-bar return on forecast; the coin's mean 24-bar return uses the non-overlapping grid 0,24,48,... "
               "of each window pooled over its windows; s24 is the ddof-1 std of 24 hourly returns, its 720-bar mean "
               "includes bar t, both inside the window, cases without a ratio are left out of the check; the high half "
               "is ratio above the median, the low half at or below it.")

    main_name = "pooled OLS slope of excess 24-bar return on forecast"
    thr = "slope > 0 with t >= 2 confirms, slope < 0 with t <= -2 rejects, over at least 1000 cases"

    if agreement is None:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": "No bar has a non-zero forecast, so the minimum of 1000 cases is not reached.",
            "reading": reading,
        }
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active_bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the non-zero forecasts sit on the 00:00 UTC settlement bar with a sign "
                           "opposite to that bar's return, as the Fidelity's fade of the settlement hour requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    X, Y, R = [], [], []
    for coin, wins in bars.items():
        grid_rets = []
        per_win = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            idx = np.arange(0, n - H, H)
            if len(idx):
                g = close[idx + H] / close[idx] - 1.0
                grid_rets.extend(list(g[np.isfinite(g)]))
            per_win.append((df, close))
        if not grid_rets:
            continue
        mu = float(np.mean(grid_rets))
        for df, close in per_win:
            n = len(close)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy()
            reg = df["regime"].astype(str).to_numpy()
            cs = pd.Series(close)
            r1 = cs / cs.shift(1) - 1.0
            s24 = r1.rolling(24, min_periods=24).std(ddof=1)
            ms = s24.rolling(720, min_periods=720).mean()
            ratio = (s24 / ms).to_numpy()
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:n - H] = close[H:] / close[:n - H] - 1.0
            sel = (reg == "mean_reversion") & (f != 0) & np.isfinite(fwd)
            for i in np.where(sel)[0]:
                X.append(f[i])
                Y.append(fwd[i] - mu)
                R.append(ratio[i])

    X = np.asarray(X, float)
    Y = np.asarray(Y, float)
    R = np.asarray(R, float)
    n_cases = int(len(X))

    slope = t = None
    if n_cases >= 3 and np.std(X) > 0:
        lr = stats.linregress(X, Y)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # supporting check
    diff = None
    n_hi = n_lo = 0
    m = np.isfinite(R)
    if m.sum() >= 2:
        gain = np.sign(X[m]) * Y[m] * np.abs(X[m]) / 10.0
        med = np.median(R[m])
        hi = R[m] > med
        lo = ~hi
        n_hi, n_lo = int(hi.sum()), int(lo.sum())
        if n_hi > 0 and n_lo > 0:
            diff = float(gain[hi].mean() - gain[lo].mean())
    sup_pass = (diff > 0) if diff is not None else None

    counts = {"cases": n_cases, "cases_with_ratio": int(m.sum()),
              "high_ratio_cases": n_hi, "low_ratio_cases": n_lo}

    if n_cases < 1000:
        status = "not observable"
        decided = f"Only {n_cases} cases, below the plan's minimum of 1000 cases."
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Slope positive with t >= 2 over at least 1000 cases and the high-ratio half's fade gain above the low-ratio half's."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the high-ratio half's fade gain is not above the low-ratio half's."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "Slope negative with t <= -2 over at least 1000 cases: settlement-hour moves continue rather than reverse."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2 over at least 1000 cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean fade gain, high-ratio half minus low-ratio half",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
