import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 48
    RAW = "debug_info.components.thin_weekend_move.last_history_value"
    MIN_CASES = 300

    # ---------- normal 48-bar drift per coin (non-overlapping grid, all windows together) ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                rets.extend(r[np.isfinite(r)].tolist())
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- situation check and cases ----------
    n_active = 0
    n_agree = 0
    cases = []  # (coin, forecast, unusual return)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            bar_end = ts + pd.Timedelta(hours=1)
            # bar closing Sunday 24:00 UTC = bar ending Monday 00:00
            situ = ((bar_end.dt.dayofweek == 0) & (bar_end.dt.hour == 0) &
                    (bar_end.dt.minute == 0)).to_numpy()
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(df), np.nan)
            n = len(df)
            for i in np.nonzero(f != 0)[0]:
                n_active += 1
                rv = raw[i]
                if not np.isfinite(rv):
                    rv = (c[i] / c[i - H] - 1.0) if i - H >= 0 else np.nan
                if situ[i] and np.isfinite(rv) and rv != 0 and np.sign(f[i]) == -np.sign(rv):
                    n_agree += 1
            for i in np.nonzero(situ & (f != 0))[0]:
                if i + H < n and np.isfinite(c[i]) and np.isfinite(c[i + H]) and np.isfinite(drift[coin]):
                    cases.append((coin, f[i], c[i + H] / c[i] - 1.0 - drift[coin]))

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    reading = ("The Sunday-close bar is the 1h bar whose end (start + 1 h) is Monday 00:00 UTC and its expected side "
               "is opposite to the sign of the raw component (the weekend's 48-bar move); cases are those bars with a "
               "non-zero forecast and a full 48-bar forward return in the same window, pooled across coins in one OLS "
               "of unusual return on forecast; the top 20 % by |forecast| is the ceiling of 0.2 x cases; the plan's "
               "'fewer than 300 cases' is reported as not observable.")

    main_name = "OLS slope of 48-bar drift-removed return on Sunday-close forecast"
    main_thr = "slope > 0 with t >= 2 confirms (with supporting check); slope < 0 with t <= -2 rejects"

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on expected side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are Sunday-close bars betting against "
                           "the weekend's 48-bar move, as the Fidelity's situation and side require."),
            "reading": reading,
        }

    n_cases = len(cases)
    counts = {"cases with a non-zero forecast": int(n_cases)}
    sit = {"agreement": agreement, "passed": passed}

    slope = t = None
    sup_val = None
    sup_pass = None
    if n_cases >= 3:
        x = np.array([cc[1] for cc in cases], dtype=float)
        y = np.array([cc[2] for cc in cases], dtype=float)
        if np.std(x) > 0:
            lr = stats.linregress(x, y)
            slope = float(lr.slope)
            t = float(lr.slope / lr.stderr) if lr.stderr > 0 else (np.inf if lr.slope > 0 else -np.inf)
            t = float(t)
        k = int(np.ceil(0.2 * n_cases))
        order = np.argsort(-np.abs(x), kind="mergesort")[:k]
        signed = np.sign(x[order]) * y[order]
        sup_val = float(np.mean(signed))
        sup_pass = bool(sup_val > 0)
        counts["top 20 % cases"] = int(k)

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t} if t is not None else None),
            "threshold": main_thr}
    sup = {"name": "mean signed unusual move of top 20 % |forecast| cases", "value": sup_val, "passed": sup_pass}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases with a non-zero forecast across all coins, below the plan's minimum of 300."
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope could not be estimated (no variation in the forecast), so neither rule is met."
    elif slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the top 20 % |forecast| cases show a positive mean signed unusual move."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: larger thin-weekend moves continue rather than reverse."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check failed, which the plan counts as inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan counts as inconclusive."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
