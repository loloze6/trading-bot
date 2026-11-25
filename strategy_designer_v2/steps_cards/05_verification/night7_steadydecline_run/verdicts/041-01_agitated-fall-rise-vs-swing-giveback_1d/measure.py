import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.scaled_rise.last_history_value"
    MIN_CASES = 100
    T_THR = 2.0

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(d[FC], errors="coerce")
            active = fc.notna() & (fc != 0)
            if active.sum() == 0:
                continue
            # profile: the detector's vetoes send bars outside "falling agitated" to "chop";
            # the profile holds where the default regime "unknown" survives
            reg = d["regime"].astype(str).str.strip().str.lower()
            in_profile = reg == "unknown"
            # the rise: scaled return of the day > 0 (raw value), else the day's own return
            close = pd.to_numeric(d["close"], errors="coerce")
            day_ret = close / close.shift(1) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                rise = raw.where(raw.notna(), day_ret) > 0
            else:
                rise = day_ret > 0
            situation = in_profile & rise.fillna(False) & (fc < 0)  # short side
            n_active += int(active.sum())
            n_agree += int((active & situation).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "clustered-by-day t of the slope of next-bar excess return on abs(forecast), forecast < 0"
    threshold = "confirm: slope <= 0 with t <= -2 (and mean excess < 0, >= 100 cases); reject: t >= +2"
    reading = ("The profile is read from the recorded regime (default 'unknown' = falling agitated, vetoes give 'chop') "
               "since its 365-bar detector cannot be rebuilt inside 120-bar windows, the rise from the raw scaled return > 0; "
               "the coin's drift is the mean of all its in-window 1-bar returns over all windows, every bar is a case at a 1-bar horizon, "
               "the slope's t uses day-clustered standard errors, and the plan's 'fewer than 100 cases' is treated as the minimum count (not observable).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the active bars are short bars on an up day inside the falling agitated profile "
                           "(regime 'unknown'), so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    ys, xs, days = [], [], []
    for coin, wins in bars.items():
        # coin drift over all windows
        allr = []
        frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            allr.append(nxt.dropna().values)
            frames.append((d, nxt))
        if not allr:
            continue
        allr = np.concatenate(allr)
        if len(allr) == 0:
            continue
        drift = float(np.mean(allr))
        for d, nxt in frames:
            fc = pd.to_numeric(d[FC], errors="coerce")
            m = (fc < 0) & nxt.notna()
            if m.sum() == 0:
                continue
            ys.extend((nxt[m] - drift).tolist())
            xs.extend(fc[m].abs().tolist())
            days.extend(pd.to_datetime(d.loc[m, "timestamp"], utc=True).dt.floor("D").astype(str).tolist())

    y = np.asarray(ys, float)
    x = np.asarray(xs, float)
    days = np.asarray(days)
    n = len(y)
    n_days = int(len(np.unique(days))) if n else 0
    mean_ex = float(np.mean(y)) if n else None
    counts = {"cases (bars with forecast < 0)": int(n), "days": n_days}

    slope, t_slope = None, None
    if n >= 3 and np.var(x) > 0:
        X = np.column_stack([np.ones(n), x])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        resid = y - X @ beta
        meat = np.zeros((2, 2))
        uniq = np.unique(days)
        for g in uniq:
            idx = days == g
            s = X[idx].T @ resid[idx]
            meat += np.outer(s, s)
        G = len(uniq)
        k = 2
        corr = (G / (G - 1)) * ((n - 1) / (n - k)) if G > 1 and n > k else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t_slope = float(slope / se) if np.isfinite(se) and se > 0 else None

    sup_pass = (mean_ex < 0) if mean_ex is not None else None
    supporting = {"name": "mean next-bar return minus coin drift on forecast < 0 bars, before costs, below 0",
                  "value": mean_ex, "passed": sup_pass}
    statistic = {"name": "slope t, clustered by day", "value": t_slope} if t_slope is not None else None
    main = {"name": main_name, "value": slope, "statistic": statistic, "threshold": threshold}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} bars with forecast < 0, under the plan's minimum of 100 cases."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in abs(forecast)), so it meets neither rule."
    elif t_slope <= -T_THR and slope <= 0:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is <= 0 with t <= -2 and the mean next-day excess return is below 0, with at least 100 cases."
        else:
            status = "inconclusive"
            decided = "A slope t <= -2 whose mean next-day excess return is not below 0 is inconclusive."
    elif t_slope >= T_THR:
        status = "rejected"
        decided = "The slope has t >= +2: larger scaled rises are followed by relatively higher next-day returns."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
