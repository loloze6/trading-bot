import numpy as np
import pandas as pd


def measure(bars):
    # ---------- helpers ----------
    FC = "forecast"
    RAW = "debug_info.components.fall_low.last_history_value"

    def _ts(df):
        return pd.to_datetime(df["timestamp"], utc=True, errors="coerce")

    # ---------- 1. situation check ----------
    # Situation (Fidelity): a one-day fall of at least 2 usual moves (return / 20-day std of daily returns <= -2);
    # expected side: long (outcome is a rise).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0)
            r = close / close.shift(1) - 1.0
            std_incl = r.rolling(20, min_periods=20).std(ddof=1)
            std_prev = r.shift(1).rolling(20, min_periods=20).std(ddof=1)
            z_incl = r / std_incl
            z_prev = r / std_prev
            tol = 1e-9
            sit = (z_incl <= -2.0 + tol) | (z_prev <= -2.0 + tol)
            # where the prices of the window cannot give the 20-day std (start of a window),
            # fall back to the detector's recorded decision and the component's raw fall value
            cannot = z_incl.isna() & z_prev.isna()
            if "regime" in df.columns:
                reg_ok = df["regime"].astype(str) == "mean_reversion"
            else:
                reg_ok = pd.Series(False, index=df.index)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw_ok = raw > 0
            else:
                raw_ok = pd.Series(True, index=df.index)
            sit = sit.where(~cannot, reg_ok & raw_ok)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean excess next-day return on bars with forecast > 0 (vs coin's all-window mean daily return)"
    thr = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; at least 100 independent case-days"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("no active bars in the record" if n_active == 0 else
                           "fewer than 90% of bars with a non-zero forecast are long bars on a one-day fall of at "
                           "least 2 usual moves (20-day return std), as the plan's situation requires"),
            "reading": "situation recomputed from the closes as the day's return over the 20-day std of daily returns "
                       "(current bar included or excluded, either accepted), falling back on the recorded regime where "
                       "a window's first bars cannot give that std",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        all_r = []
        per_win = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fwd = close.shift(-1) / close - 1.0  # inside the window only
            all_r.append(fwd.dropna().values)
            per_win.append((df, fwd))
        if not all_r:
            continue
        allv = np.concatenate(all_r)
        if allv.size == 0:
            continue
        mu = float(np.mean(allv))
        for df, fwd in per_win:
            fc = pd.to_numeric(df[FC], errors="coerce")
            ts = _ts(df)
            m = (fc > 0) & fwd.notna() & ts.notna()
            for i in np.where(m.values)[0]:
                rows.append((ts.iloc[i].floor("D"), float(fwd.iloc[i] - mu), float(fc.iloc[i])))

    n_cases = len(rows)
    if n_cases > 0:
        d = pd.DataFrame(rows, columns=["day", "x", "f"])
        x = d["x"].values
        f = d["f"].values
        mean_x = float(np.mean(x))
        n_days = int(d["day"].nunique())
        dev = d.assign(dev=d["x"] - mean_x).groupby("day")["dev"].sum().values
        if n_days > 1:
            se = np.sqrt(np.sum(dev ** 2) * n_days / (n_days - 1)) / n_cases
            t = float(mean_x / se) if se > 0 else None
        else:
            t = None
        wmean = float(np.sum(x * f) / np.sum(f)) if np.sum(f) > 0 else None
        sup_pass = bool(wmean is not None and wmean >= mean_x)
    else:
        mean_x, t, wmean, sup_pass, n_days = None, None, None, None, 0

    counts = {"independent case-days": int(n_days), "cases": int(n_cases)}
    reading = ("situation recomputed from the closes (20-day std with or without the current bar accepted, regime "
               "fallback at window starts); the coin's mean daily return is over all its windows' next-day returns; "
               "the t uses day-clustered deviations from the mean (deviations summed per UTC day, D/(D-1) correction) "
               "and the 100 minimum is read on distinct UTC days with a case")

    if n_days < 100:
        status = "not observable"
        decided = f"fewer than 100 independent case-days across all coins and windows ({n_days})."
    elif t is None:
        status = "inconclusive"
        decided = "the t of the mean excess could not be computed."
    elif mean_x > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "mean excess next-day return above 0 with t >= 2, and the forecast-weighted mean is at least the unweighted mean."
    elif mean_x < 0 and t <= -2:
        status = "rejected"
        decided = "mean excess next-day return below 0 with t <= -2."
    elif t >= 2 and not sup_pass:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails (forecast-weighted mean below the unweighted mean)."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name,
                         "value": None if mean_x is None else float(mean_x),
                         "statistic": None if t is None else {"name": "t of the mean, cases of one day summed", "value": float(t)},
                         "threshold": thr},
        "supporting_check": {"name": "forecast-weighted mean excess >= unweighted mean",
                             "value": None if wmean is None else float(wmean),
                             "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
