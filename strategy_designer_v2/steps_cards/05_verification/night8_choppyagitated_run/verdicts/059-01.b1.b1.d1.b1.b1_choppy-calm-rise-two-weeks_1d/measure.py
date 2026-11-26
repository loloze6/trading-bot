import numpy as np
import pandas as pd


def measure(bars):
    H = 14
    RAW = "debug_info.components.scaled_rise.last_history_value"

    # ---------- 1. Situation check: choppy-calm profile, past 7-day rise, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # where the raw value is not recorded, fall back on the 7-day return from prices (same sign)
            ret7 = close / close.shift(7) - 1.0
            rise_sign = raw.where(raw.notna(), ret7)
            regime = df["regime"].astype(str).str.strip().str.lower()
            profile = regime == "unknown"  # the only regime with a strategy: no veto fired = choppy calm
            active = fc.notna() & (fc != 0)
            situ = profile & (rise_sign > 0) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars in the "
                           "choppy-calm profile (regime 'unknown') after a 7-day rise, as the Fidelity states."),
            "reading": "The choppy-calm profile is read from the recorded regime 'unknown' (no veto fired), "
                       "and the rise from the sign of the raw scaled 7-day return.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_all = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_all.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    day = ts.iloc[i].floor("D") if pd.notna(ts.iloc[i]) else None
                    coin_rows.append((coin, day, float(fc[i]), r))
        if len(grid_all) == 0:
            continue
        drift = float(np.mean(grid_all))
        for (c, day, f, r) in coin_rows:
            rows.append({"coin": c, "day": str(day), "f": f, "y": r - drift})

    n_cases = len(rows)
    days = sorted(set(r["day"] for r in rows))
    n_days = len(days)

    slope = None
    t_slope = None
    mean_unusual = None
    if n_cases > 0:
        d = pd.DataFrame(rows)
        mean_unusual = float(d["y"].mean())
        if n_cases >= 3 and d["f"].var() > 0:
            X = np.column_stack([np.ones(n_cases), d["f"].values])
            y = d["y"].values
            XtX_inv = np.linalg.inv(X.T @ X)
            beta = XtX_inv @ X.T @ y
            e = y - X @ beta
            slope = float(beta[1])
            G = d["day"].nunique()
            if G >= 2:
                meat = np.zeros((2, 2))
                for _, idx in d.groupby("day").indices.items():
                    s = X[idx].T @ e[idx]
                    meat += np.outer(s, s)
                k = 2
                corr = (G / (G - 1.0)) * ((n_cases - 1.0) / (n_cases - k))
                V = corr * XtX_inv @ meat @ XtX_inv
                se = np.sqrt(V[1, 1]) if V[1, 1] > 0 else np.nan
                if np.isfinite(se) and se > 0:
                    t_slope = float(slope / se)

    sup_pass = None if mean_unusual is None else bool(mean_unusual > 0)

    if n_cases < 30:
        status = "not observable"
        decided_by = f"Only {n_cases} grid cases with forecast > 0, fewer than the plan's minimum of 30."
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided_by = "The slope is positive with t >= 2 and the mean unusual move is above 0."
    elif slope < 0 and t_slope <= -2:
        status = "rejected"
        decided_by = "The slope is negative with t <= -2."
    elif t_slope >= 2:
        status = "inconclusive"
        decided_by = "The slope has t >= 2 but the mean unusual move is <= 0."
    else:
        status = "inconclusive"
        decided_by = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": "slope of drift-removed 14-bar forward return on forecast, grid bars with forecast > 0",
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t, clustered by day", "value": t_slope},
            "threshold": "confirm: slope > 0 with t >= 2 (and mean unusual move > 0); reject: slope < 0 with t <= -2",
        },
        "supporting_check": {"name": "mean unusual move of the cases (long side)",
                             "value": mean_unusual, "passed": sup_pass},
        "counts": {"grid cases with forecast > 0": int(n_cases), "days": int(n_days)},
        "decided_by": decided_by,
        "reading": ("The profile is the recorded regime 'unknown'; the cases are each window's 0,14,28,... bars "
                    "with forecast > 0 and a full 14-bar forward return in the window; the coin's mean 14-bar return "
                    "(its normal drift) is taken over all its windows' grid bars; 'cases of one day taken together' "
                    "is read as a day-clustered (CR1) standard error of the slope; the plan's 'fewer than 30 cases' "
                    "rule is applied as the minimum count giving 'not observable'."),
    }
