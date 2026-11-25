import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 48
    RAW = "debug_info.components.midweek_ret.last_history_value"

    def to_ts(s):
        if np.issubdtype(s.dtype, np.number):
            mx = float(np.nanmax(s.values)) if len(s) else 0.0
            unit = "ms" if mx > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    n_active = 0
    n_agree = 0
    case_x, case_y = [], []
    n_cases_total = 0

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        # the coin's normal 48-bar drift over all windows (non-overlapping grid)
        grid_rets = []
        prepared = {}
        for w in sorted(wins.keys()):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            ts = to_ts(df["timestamp"])
            prepared[w] = (df, close, ts)
            for i in range(0, len(close) - H, H):
                a, b = close[i], close[i + H]
                if np.isfinite(a) and np.isfinite(b) and a != 0:
                    grid_rets.append(b / a - 1.0)
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan

        for w in sorted(prepared.keys()):
            df, close, ts = prepared[w]
            n = len(df)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values.astype(float)
            # situation: bar whose coming bar starts Friday 00:00 UTC = Thursday 23:00 bar (start time)
            wd = ts.dt.weekday.values
            hr = ts.dt.hour.values
            situ = (wd == 3) & (hr == 23)
            # raw 48-bar return: recorded raw value, else recomputed from prices
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values.astype(float)
            else:
                raw = np.full(n, np.nan)
            back = np.full(n, np.nan)
            if n > H:
                back[H:] = close[H:] / close[:-H] - 1.0
            raw = np.where(np.isfinite(raw), raw, back)

            active = fc != 0
            n_active += int(active.sum())
            same_side = np.sign(fc) == np.sign(raw)
            n_agree += int((active & situ & same_side & np.isfinite(raw)).sum())

            # cases: Thursday-23:00 bars with non-zero forecast
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:-H] = close[H:] / close[:-H] - 1.0
            idx = np.where(situ & active)[0]
            n_cases_total += len(idx)
            for i in idx:
                if np.isfinite(fwd[i]) and np.isfinite(drift):
                    case_x.append(fc[i])
                    case_y.append(fwd[i] - drift)

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    threshold = "confirm: slope > 0 with t >= 2 and supporting mean > 0; reject: slope < 0 with t <= -2; at least 300 cases"
    main_name = "OLS slope of drift-removed 48-bar return on forecast, Thursday-23:00 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": int(len(case_x))},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are Thursday-23:00 bars with the forecast on the side of the 48-bar Wednesday-Thursday return, as the plan's Fidelity requires.",
            "reading": "The situation is the bar starting Thursday 23:00 UTC (whose next bar starts Friday 00:00), and the expected side is the sign of the raw 48-bar return.",
        }

    x = np.array(case_x, dtype=float)
    y = np.array(case_y, dtype=float)
    n_cases = int(len(x))

    slope, t_val = None, None
    if n_cases >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_val = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    sup = float(np.mean(np.sign(x) * y)) if n_cases > 0 else None
    sup_pass = (sup is not None and sup > 0)

    reading = ("Cases are bars starting Thursday 23:00 UTC with a non-zero forecast and a full 48-bar forward return inside their window; "
               "the normal drift is the coin's mean 48-bar return on the non-overlapping grid of all its windows; the fit has an intercept; "
               "fewer than 300 cases is reported as not observable.")

    if n_cases < 300:
        status = "not observable"
        decided = f"Only {n_cases} cases, below the plan's minimum of 300 cases across coins and windows."
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the supporting mean is above 0."
    elif slope < 0 and t_val <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    elif t_val >= 2 and not sup_pass:
        status = "inconclusive"
        decided = "t >= 2 but the supporting mean is not above 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": t_val} if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean drift-removed 48-bar return in the forecast's direction",
            "value": sup,
            "passed": (bool(sup_pass) if sup is not None else None),
        },
        "counts": {"cases": n_cases, "active bars": int(n_active), "situation bars with non-zero forecast": int(n_cases_total)},
        "decided_by": decided,
        "reading": reading,
    }
