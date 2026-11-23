import numpy as np
import pandas as pd
from scipy import stats


def _to_time(ts):
    if pd.api.types.is_numeric_dtype(ts):
        v = pd.to_numeric(ts, errors="coerce")
        unit = "ms" if v.dropna().abs().median() > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(ts, utc=True, errors="coerce")


def measure(bars):
    H = 3
    MIN_CASES = 200
    raw_col = "debug_info.components.wkend_fall_volratio.last_history_value"

    n_active = 0
    n_agree = 0
    case_rows = []  # (coin, forecast, ret)
    coin_grid_returns = {}

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        grid = []
        for w in sorted(wins.keys()):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.copy()
            t = _to_time(df["timestamp"])
            df = df.assign(_t=t.values).sort_values("_t").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            wd = pd.DatetimeIndex(df["_t"]).weekday.to_numpy()
            is_sun = wd == 6
            n = len(df)

            # raw component value; recompute sign from prices where not recorded
            if raw_col in df.columns:
                raw = pd.to_numeric(df[raw_col], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(n, np.nan)
            ret1 = np.full(n, np.nan)
            if n > 1:
                ret1[1:] = close[1:] / close[:-1] - 1.0
            raw_eff = np.where(np.isnan(raw), ret1, raw)
            fell = raw_eff < 0

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & is_sun & fell & (fc > 0)).sum())

            # forward 3-bar returns inside window
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:-H] = close[H:] / close[:-H] - 1.0

            # non-overlapping grid: positions 0, 3, 6, ...
            for i in range(0, n, H):
                if np.isfinite(fwd[i]):
                    grid.append(fwd[i])

            for i in range(n):
                if is_sun[i] and fc[i] > 0 and np.isfinite(fwd[i]):
                    case_rows.append((coin, fc[i], fwd[i]))
        coin_grid_returns[coin] = float(np.mean(grid)) if len(grid) else np.nan

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "OLS slope of excess 3-bar return on forecast, Sunday bars with forecast > 0"
    threshold = "confirm: slope t >= 2 and mean excess > 0; reject: slope t <= -2; at least 200 cases"
    reading = ("Sunday bars are bars whose UTC start is a Sunday (the next bar is Monday), a weekend fall is a negative "
               "raw component value (the Sunday one-bar return where not recorded), cases are those with a full 3-bar "
               "return inside the window, the slope's t is the ordinary OLS t, and the plan's 'below 200 cases' rule "
               "is applied as the minimum count giving 'not observable'.")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "mean excess 3-bar return > 0", "value": None, "passed": None},
            "counts": {"cases": 0},
            "decided_by": "No bar has a non-zero forecast, so fewer than the plan's minimum of 200 cases.",
            "reading": reading,
        }

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are Sunday bars after a weekend fall "
                           "with a long forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    x, y = [], []
    for coin, f, r in case_rows:
        m = coin_grid_returns.get(coin, np.nan)
        if np.isfinite(m) and np.isfinite(f) and np.isfinite(r):
            x.append(f)
            y.append(r - m)
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n_cases = int(len(x))

    slope = None
    t_slope = None
    mean_ex = float(np.mean(y)) if n_cases > 0 else None
    if n_cases >= 3 and np.std(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    sup_pass = (mean_ex > 0) if mean_ex is not None else None
    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t_slope} if t_slope is not None else None),
            "threshold": threshold}
    sup = {"name": "mean excess 3-bar return > 0", "value": mean_ex, "passed": sup_pass}
    counts = {"cases": n_cases}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, below the plan's minimum of 200 cases."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope of excess return on the forecast has t >= 2 and the mean excess return is positive."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope of excess return on the forecast has t <= -2."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope t is >= 2 but the mean excess return is at or below 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
