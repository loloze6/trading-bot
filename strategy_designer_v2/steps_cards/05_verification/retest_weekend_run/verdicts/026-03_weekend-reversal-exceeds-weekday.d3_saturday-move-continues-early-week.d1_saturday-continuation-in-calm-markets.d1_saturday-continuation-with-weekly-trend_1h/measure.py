import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 48
    SAT_RAW = "debug_info.components.sat.last_history_value"
    WK_RAW = "debug_info.components.week.last_history_value"

    active_total = 0
    active_agree = 0
    entry_rows = []  # (coin, forecast, ret48)
    coin_grid_returns = {}

    for coin, windows in bars.items():
        grid = []
        for wname, df in windows.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            n = len(df)
            ts = pd.to_datetime(df["timestamp"], utc=True)

            # Forward 48-bar return inside the window only
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0

            # Non-overlapping grid: positions 0, 48, 96, ... from the window's first row
            for p in range(0, n - H, H):
                if np.isfinite(fwd[p]):
                    grid.append(fwd[p])

            # Situation recomputation from prices (fallback where raw values are not recorded)
            cs = pd.Series(close)
            sat_px = (cs.shift(24) / cs.shift(48) - 1.0).to_numpy()
            wk_px = (cs / cs.shift(168) - 1.0).to_numpy()
            sat_raw = (pd.to_numeric(df[SAT_RAW], errors="coerce").to_numpy(dtype=float)
                       if SAT_RAW in df.columns else np.full(n, np.nan))
            wk_raw = (pd.to_numeric(df[WK_RAW], errors="coerce").to_numpy(dtype=float)
                      if WK_RAW in df.columns else np.full(n, np.nan))
            sat_v = np.where(np.isfinite(sat_raw), sat_raw, sat_px)
            wk_v = np.where(np.isfinite(wk_raw), wk_raw, wk_px)

            # Timing: decision read at Monday 00:00 (bar closing at it, or bar opening at it)
            close_t = ts + pd.Timedelta(hours=1)
            t_close = ((close_t.dt.dayofweek == 0) & (close_t.dt.hour == 0)
                       & (close_t.dt.minute == 0)).to_numpy()
            t_open = ((ts.dt.dayofweek == 0) & (ts.dt.hour == 0)
                      & (ts.dt.minute == 0)).to_numpy()
            timing = t_close | t_open

            # Calm-market condition: detector component not recorded, 8760-bar lookback
            # exceeds the window, so it is taken from the detector's decision.
            calm = (df["regime"].astype(str) == "trending").to_numpy()

            long_sit = timing & calm & (sat_v > 0) & (wk_v > 0)
            short_sit = timing & calm & (sat_v < 0) & (wk_v < 0)

            act = fc != 0
            active_total += int(act.sum())
            agree = (act & (fc > 0) & long_sit) | (act & (fc < 0) & short_sit)
            active_agree += int(agree.sum())

            for i in np.where(act)[0]:
                if np.isfinite(fwd[i]):
                    entry_rows.append((coin, fc[i], fwd[i]))
        coin_grid_returns[coin] = grid

    agreement = (active_agree / active_total) if active_total > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "slope of excess 48-bar return on entry forecast, pooled"
    threshold = "slope t >= 2 with >= 100 cases (and mean directional excess > 0) confirms; t <= -2 with >= 100 cases rejects"
    reading = ("The decision bar is taken as the bar read at Monday 00:00 UTC (closing at it, per the plan, or opening at it); "
               "the calm-market rule is taken from regime == 'trending' because the 8760-bar percentile cannot be rebuilt inside a window; "
               "Saturday/weekly signs use the recorded raw values, else recomputed from prices; each coin's mean 48-bar return uses "
               "non-overlapping grid stretches of all its windows; the slope t is the OLS t over all entry bars with a full 48-bar return.")

    if active_total > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"entry cases": len(entry_rows), "active bars": active_total},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are Monday 00:00 bars in calm markets "
                           "with Saturday's return and the 7-day return of the forecast's sign."),
            "reading": reading,
        }

    coin_mean = {c: (float(np.mean(g)) if len(g) else np.nan) for c, g in coin_grid_returns.items()}
    x, y = [], []
    for coin, f, r in entry_rows:
        m = coin_mean.get(coin, np.nan)
        if np.isfinite(m):
            x.append(f)
            y.append(r - m)
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n_cases = int(len(x))

    slope = None
    t_val = None
    if n_cases >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_val = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    supp_val = float(np.mean(np.sign(x) * y)) if n_cases > 0 else None
    supp_pass = (supp_val > 0) if supp_val is not None else None

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} entry cases, below the plan's minimum of 100."
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast)."
    elif t_val >= 2 and supp_pass:
        status = "confirmed"
        decided = "Slope t is 2 or more with at least 100 cases and the mean directional excess return is above 0."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "Slope t is 2 or more but the mean directional excess return is 0 or below."
    elif t_val <= -2:
        status = "rejected"
        decided = "Slope t is -2 or less with at least 100 cases."
    else:
        status = "inconclusive"
        decided = "Slope t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t_val} if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 48-bar return in forecast direction",
            "value": supp_val,
            "passed": (bool(supp_pass) if supp_pass is not None else None),
        },
        "counts": {"entry cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
