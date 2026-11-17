import numpy as np
import pandas as pd
from scipy import stats


def _to_ts(s):
    if pd.api.types.is_numeric_dtype(s):
        v = pd.to_numeric(s, errors="coerce")
        med = np.nanmedian(v.values) if len(v) else 0
        unit = "ms" if med > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True, errors="coerce")
    return pd.to_datetime(s, utc=True, errors="coerce")


def measure(bars):
    H = 2
    RAW = "debug_info.components.sun_fall.last_history_value"
    MIN_CASES = 300

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            ts = _to_ts(df["timestamp"])
            close = pd.to_numeric(df["close"], errors="coerce")
            ret1 = close / close.shift(1) - 1.0  # Saturday-close to Sunday-close on the Sunday bar, inside the window
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), ret1)
            else:
                raw = ret1
            is_sunday = ts.dt.dayofweek == 6
            active = fc.notna() & (fc != 0)
            situation = is_sunday & (raw < 0)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    situation_check = {"agreement": agreement, "passed": passed}

    main_name = "OLS slope of excess 2-bar return on forecast, Sunday-fall cases"
    threshold = "confirm: slope > 0 with t >= 2 and mean excess > 0; reject: slope < 0 with t <= -2; at least 300 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars on a Sunday fall, long": n_agree},
            "decided_by": ("No active bars were recorded." if n_active == 0 else
                           "Fewer than 90% of the bars with a non-zero forecast are Sunday bars after a Sunday fall with a long (positive) forecast, as the Fidelity's situation and side require."),
            "reading": "Sunday bar = bar whose start timestamp falls on a Sunday (UTC); a fall = negative raw sun_fall value (or negative one-bar return when not recorded); the expected side is long.",
        }

    # ---------- coin mean non-overlapping 2-bar return over all windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True).values
            for i in range(0, len(c) - H, H):
                r = c[i + H] / c[i] - 1.0
                if np.isfinite(r):
                    rets.append(r)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        cm = coin_mean.get(coin, np.nan)
        if not np.isfinite(cm):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            c = pd.to_numeric(df["close"], errors="coerce").values
            reg = df["regime"].astype(str).values
            n = len(df)
            for t in range(n - H):
                if reg[t] != "mean_reversion":
                    continue
                if not (np.isfinite(fc[t]) and fc[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r):
                    continue
                xs.append(float(fc[t]))
                ys.append(float(r - cm))

    n_cases = len(xs)
    counts = {"Sunday-fall cases": n_cases}
    reading = ("Cases are bars with regime mean_reversion and forecast > 0 whose t+2 close lies in the same window; "
               "the coin mean is over non-overlapping 2-bar returns on a grid from each window's first row, pooled over all its windows; "
               "the slope's t is the OLS slope over its standard error; fewer than 300 cases is reported as not observable.")

    slope = t_stat = mean_ex = None
    if n_cases >= 3 and np.std(xs) > 0:
        lr = stats.linregress(np.array(xs), np.array(ys))
        slope = float(lr.slope)
        t_stat = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    if n_cases > 0:
        mean_ex = float(np.mean(ys))

    support_pass = None if mean_ex is None else bool(mean_ex > 0)
    main = {"name": main_name, "value": slope,
            "statistic": None if t_stat is None else {"name": "OLS slope t", "value": t_stat},
            "threshold": threshold}
    support = {"name": "mean excess 2-bar return above 0", "value": mean_ex, "passed": support_pass}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} Sunday-fall cases, below the plan's minimum of 300."
    elif slope is None or t_stat is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t_stat >= 2 and support_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the mean excess 2-bar return is above 0."
    elif slope > 0 and t_stat >= 2:
        status = "inconclusive"
        decided = "The slope has t >= 2 but the mean excess 2-bar return is not above 0."
    elif slope < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: larger Sunday falls are followed by larger further falls relative to holding the coin."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
