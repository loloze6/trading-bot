import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.fall_vs_year_swing.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    rows = []
    for coin, wins in bars.items():
        # coin's mean daily return over all its windows (never across windows)
        all_r = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            if len(c) > 1:
                all_r.append(c[1:] / c[:-1] - 1.0)
        all_r = np.concatenate(all_r) if all_r else np.array([])
        all_r = all_r[np.isfinite(all_r)]
        mu = float(np.mean(all_r)) if len(all_r) else np.nan

        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values.astype(float)
            else:
                raw = np.full(len(df), np.nan)
            # fall on the day: raw value < 0; where not recorded, the price return
            prev = np.r_[np.nan, c[:-1]]
            day_ret = c / prev - 1.0
            fall = np.where(np.isfinite(raw), raw < 0, np.isfinite(day_ret) & (day_ret < 0))
            profile = reg == "unknown"
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & profile & fall & (fc > 0)).sum())

            ts = pd.to_datetime(df["timestamp"], utc=True)
            nxt = np.r_[c[1:], np.nan]
            r_next = nxt / c - 1.0
            for i in range(len(df)):
                if np.isfinite(fc[i]) and fc[i] > 0 and np.isfinite(r_next[i]) and np.isfinite(mu):
                    rows.append((ts.iloc[i].strftime("%Y-%m-%d"), fc[i], r_next[i] - mu))

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    reading = ("The falling agitated profile is read from the recorded `regime` (bars left 'unknown' by the two chop "
               "vetoes, since the detector's components are not recorded and cannot be rebuilt inside ~120-bar windows), "
               "a fall is a negative raw scaled return, the slope's t is an OLS t with standard errors clustered by UTC "
               "day, and bars without a next close in the same window are left out.")
    main_name = "OLS slope of next-day excess return on forecast, over bars with forecast > 0"
    thr = "slope t >= 2 (with mean excess > 0) confirms; slope t <= -2 rejects"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"bars with forecast > 0": None, "distinct days": None, "active bars": n_active},
            "decided_by": ("Fewer than 90% of the active bars are long bars on a one-day fall inside the falling "
                           "agitated profile (agreement %.3f)." % agreement),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    d = pd.DataFrame(rows, columns=["day", "x", "y"])
    n = int(len(d))
    n_days = int(d["day"].nunique()) if n else 0
    counts = {"bars with forecast > 0": n, "distinct days": n_days}

    slope = None
    tstat = None
    mean_ex = float(d["y"].mean()) if n else None
    if n >= 3 and n_days >= 2 and d["x"].nunique() > 1:
        X = np.column_stack([np.ones(n), d["x"].values])
        y = d["y"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        e = y - X @ beta
        meat = np.zeros((2, 2))
        for _, idx in d.groupby("day").indices.items():
            s = X[idx].T @ e[idx]
            meat += np.outer(s, s)
        G = n_days
        k = 2
        corr = (G / (G - 1.0)) * ((n - 1.0) / (n - k)) if n > k else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        tstat = float(slope / se) if np.isfinite(se) and se > 0 else None

    sup_pass = (mean_ex > 0) if mean_ex is not None else None
    supporting = {"name": "mean next-day excess return over bars with forecast > 0 above 0",
                  "value": mean_ex, "passed": sup_pass}
    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "slope t, cases of one day pooled (clustered by day)", "value": tstat}
                          if tstat is not None else None),
            "threshold": thr}

    if n < 100 or n_days < 60:
        status = "not observable"
        decided = ("Minimum count not reached: %d bars with forecast > 0 (need 100) on %d distinct days (need 60)."
                   % (n, n_days))
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess return is above 0."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "A positive slope (t >= 2) with a mean excess return at or below 0 is inconclusive."
    elif tstat <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
