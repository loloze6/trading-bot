import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    MIN_CASES = 40
    RAW = "debug_info.components.scaled_week_rise.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if "forecast" not in df.columns or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            ret7 = close / close.shift(H) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), ret7)
            else:
                raw = ret7
            if "regime" in df.columns:
                calm = df["regime"].astype(str) == "unknown"
            else:
                calm = pd.Series(False, index=df.index)
            situation = calm & (raw > 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    if n_active > 0:
        agreement = n_agree / n_active
    else:
        agreement = None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("The choppy calm profile is read from the recorded regime ('unknown' = no veto, since the 365-bar "
               "volatility percentile cannot be rebuilt from the windows) and the rise from the raw component value "
               "(or the 7-bar close return where it is missing); the normal drift is each coin's mean 7-bar return on "
               "the non-overlapping grid of all its windows; the slope's t is the ordinary OLS t over all cases pooled; "
               "the mean's day-clustered t uses a G/(G-1) correction; fewer than 40 cases is reported as not observable "
               "as the workflow requires.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars in the choppy calm "
                           "profile with a positive 7-bar scaled return, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_all = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values if "forecast" in df.columns \
                else np.full(len(df), np.nan)
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_all.append(r)
                f = fc[i]
                if np.isfinite(f) and f > 0:
                    day = ts.iloc[i]
                    day = str(day.floor("D")) if pd.notna(day) else f"{coin}-{w}-{i}"
                    coin_cases.append((f, r, day))
        if len(grid_all) == 0:
            continue
        drift = float(np.mean(grid_all))
        for f, r, day in coin_cases:
            rows.append({"coin": coin, "forecast": f, "excess": r - drift, "day": day})

    cases = pd.DataFrame(rows, columns=["coin", "forecast", "excess", "day"])
    n = len(cases)
    n_days = int(cases["day"].nunique()) if n else 0

    slope = None
    slope_t = None
    mean_ex = None
    mean_t = None
    if n >= 3:
        x = cases["forecast"].values.astype(float)
        y = cases["excess"].values.astype(float)
        if np.var(x) > 0:
            lr = stats.linregress(x, y)
            slope = float(lr.slope)
            slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    if n >= 1:
        y = cases["excess"].values.astype(float)
        mean_ex = float(np.mean(y))
        dev = cases.assign(d=y - mean_ex).groupby("day")["d"].sum().values
        G = len(dev)
        if G > 1:
            var = (G / (G - 1)) * np.sum(dev ** 2) / (n ** 2)
            se = np.sqrt(var)
            mean_t = float(mean_ex / se) if se > 0 else None

    sup_passed = None if mean_ex is None else bool(mean_ex > 0)

    if n < MIN_CASES:
        status = "not observable"
        decided_by = f"Only {n} cases with forecast > 0 on the 7-bar grid, fewer than the plan's minimum of 40."
    elif slope_t is not None and slope_t >= 2 and mean_ex is not None and mean_ex > 0:
        status = "confirmed"
        decided_by = "Confirm: the slope's t is 2 or more and the mean excess return is above 0, with at least 40 cases."
    elif (slope_t is not None and slope_t <= -2) or (mean_t is not None and mean_t <= -2):
        status = "rejected"
        decided_by = ("Reject: the slope's t is -2 or less, or the mean excess return's t is -2 or less, "
                      "with at least 40 cases.")
    else:
        status = "inconclusive"
        if slope_t is not None and slope_t >= 2:
            decided_by = ("Inconclusive: the slope's t is 2 or more but the mean excess return is not above 0 "
                          "(supporting check failed).")
        else:
            decided_by = "Inconclusive: at least 40 cases, but neither the confirm nor the reject rule is met."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "slope of 7-bar excess return on forecast",
            "value": slope,
            "statistic": None if slope_t is None else {"name": "OLS slope t", "value": slope_t},
            "threshold": "slope t >= 2 confirms (with mean excess > 0); slope t <= -2 rejects",
        },
        "supporting_check": {
            "name": "mean excess 7-bar return above 0 (day-clustered t, reject if t <= -2)",
            "value": mean_ex,
            "passed": sup_passed,
            "t": mean_t,
        },
        "counts": {"cases with forecast > 0 on the grid": int(n), "days": n_days},
        "decided_by": decided_by,
        "reading": reading,
    }
