import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    RAW = "debug_info.components.fall_x_vol.last_history_value"

    def prep(df):
        df = df.reset_index(drop=True).copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        # the bar's close is its start + 1 hour; settlement bars close at 00:00 or 16:00 UTC
        close_hour = (df["timestamp"] + pd.Timedelta(hours=1)).dt.hour
        df["_settle"] = close_hour.isin([0, 16])
        df["_fwd"] = df["close"].shift(-H) / df["close"] - 1.0
        df["_ret2"] = df["close"] / df["close"].shift(2) - 1.0
        df["_pos"] = np.arange(len(df))
        return df

    data = {}
    for coin, wins in bars.items():
        data[coin] = {w: prep(df) for w, df in wins.items()}

    # ---- situation check ----
    n_active = 0
    n_agree = 0
    for coin, wins in data.items():
        for w, df in wins.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                fall = raw.where(raw.notna(), df["_ret2"]) < 0
            else:
                fall = df["_ret2"] < 0
            ok = active & df["_settle"] & fall & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "t of slope of excess 24-bar return on forecast (settlement bars, forecast >= 2)"
    threshold = "confirm if t >= 2 with weighted mean > 0; reject if t <= -2 with weighted mean < 0; at least 200 independent cases"
    reading = ("Settlement bars are those whose close (start + 1h) is 00:00 or 16:00 UTC; the situation's fall is a negative raw "
               "component value (2-bar price return when missing); grid cells are positions //24 from each window's first row, "
               "the first forecast>=2 settlement bar per cell is the case and is dropped if its 24-bar return leaves the window; "
               "drift is the mean of each coin's non-overlapping 24-bar returns over all windows; the plan's 'fewer than 200 cases' "
               "is treated as the minimum count giving 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "independent cases": None},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are settlement bars (closing 00:00/16:00 UTC) "
                           "after a 2-hour fall with a long forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---- criterion ----
    xs, ys = [], []
    for coin, wins in data.items():
        grid_rets = []
        for w, df in wins.items():
            g = df.loc[df["_pos"] % H == 0, "_fwd"].dropna()
            grid_rets.extend(g.tolist())
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for w, df in wins.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            sel = df[df["_settle"] & (fc >= 2)].copy()
            if sel.empty:
                continue
            sel["_fc"] = fc.loc[sel.index]
            sel["_cell"] = sel["_pos"] // H
            first = sel.groupby("_cell", sort=True).head(1)
            first = first[first["_fwd"].notna() & first["_fc"].notna()]
            xs.extend(first["_fc"].astype(float).tolist())
            ys.extend((first["_fwd"].astype(float) - drift).tolist())

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    n = int(len(x))

    t_val = None
    slope = None
    if n >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_val = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    wmean = float(np.sum(x * y) / np.sum(x)) if n > 0 and np.sum(x) > 0 else None
    sup_pass = None if wmean is None else bool(wmean > 0)

    if n < 200:
        status = "not observable"
        decided = f"Only {n} independent cases across all coins, below the plan's minimum of 200."
    elif t_val is None or wmean is None:
        status = "inconclusive"
        decided = "The slope's t or the weighted mean could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and wmean > 0:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the forecast-weighted mean excess return is above 0."
    elif t_val <= -2 and wmean < 0:
        status = "rejected"
        decided = "The slope's t is -2 or less and the forecast-weighted mean excess return is below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2, or the slope and the weighted mean disagree in sign."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": t_val,
                         "statistic": None if t_val is None else {"name": "OLS slope t", "value": t_val},
                         "threshold": threshold},
        "supporting_check": {"name": "forecast-weighted mean excess 24-bar return > 0",
                             "value": wmean, "passed": sup_pass},
        "counts": {"independent cases": n, "active bars": n_active},
        "decided_by": decided,
        "reading": reading,
    }
