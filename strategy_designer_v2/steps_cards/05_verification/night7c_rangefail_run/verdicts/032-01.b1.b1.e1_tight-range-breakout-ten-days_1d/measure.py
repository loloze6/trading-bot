import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    FC = "forecast"
    TIGHT_PP = "debug_info.components.tight.post_pipeline_value"
    MIN_DAYS = 30

    def _ts(s):
        if pd.api.types.is_numeric_dtype(s):
            v = pd.to_numeric(s, errors="coerce")
            unit = "ms" if v.abs().max() > 1e11 else "s"
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True, errors="coerce")

    # ---------- 1. situation check ----------
    n_active_comp = 0
    n_agree = 0
    n_active_total = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce")
            hi = pd.to_numeric(d["high"], errors="coerce")
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            prior_high = hi.shift(1).rolling(60, min_periods=60).max()
            brk = (c / prior_high - 1.0) * 100.0
            er_raw = (c - c.shift(60)).abs() / c.diff().abs().rolling(60, min_periods=60).sum()
            er = er_raw.rolling(5, min_periods=5).mean()
            computable = brk.notna() & er.notna()
            situation = (brk > 0.0) & (er <= 0.3)
            active = fc != 0
            n_active_total += int(active.sum())
            m = active & computable
            n_active_comp += int(m.sum())
            n_agree += int((m & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active_comp) if n_active_comp > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean excess 10-day return of breakout cases over the coin's normal 10-day drift"
    threshold = "confirm: mean > 0 with t >= 2 and slope > 0; reject: t <= -2; else inconclusive; fewer than 30 independent cases: not observable"
    reading_situation = ("the situation is recomputed from prices (close above the max high of the 60 prior bars, "
                         "60-bar efficiency ratio smoothed by a 5-bar simple mean <= 0.3) on the active bars that have "
                         "64 prior bars inside their window, the expected side being long")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active_comp), "active bars agreeing": int(n_agree)},
            "decided_by": ("only %.1f%% of the checkable bars with a nonzero forecast are long bars of a close above the "
                           "prior 60-day high with a 60-day efficiency ratio of 0.3 or less, below the 90%% needed"
                           % (100.0 * agreement)),
            "reading": reading_situation,
        }

    # ---------- 2. criterion ----------
    # normal drift per coin: mean of non-overlapping 10-bar returns over all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    rows = []
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            tight = (pd.to_numeric(d[TIGHT_PP], errors="coerce").to_numpy(dtype=float)
                     if TIGHT_PP in d.columns else np.full(len(d), np.nan))
            ts = _ts(d["timestamp"])
            n = len(d)
            used_cells = set()
            for t in range(1, n):
                if not (fc[t - 1] == 0 and fc[t] >= 2.0):
                    continue
                cell = t // H
                if cell in used_cells:
                    continue
                used_cells.add(cell)
                if t + H >= n or not (np.isfinite(c[t]) and np.isfinite(c[t + H])) or c[t] <= 0:
                    continue
                r = c[t + H] / c[t] - 1.0
                day = ts.iloc[t]
                day = str(day.date()) if pd.notna(day) else "%s_%s_%d" % (coin, w, t)
                rows.append({"coin": coin, "day": day, "excess": r - drift[coin], "tight": tight[t]})

    cases = pd.DataFrame(rows, columns=["coin", "day", "excess", "tight"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_ex = float(cases["excess"].mean()) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["excess"] - mean_ex
        S = dev.groupby(cases["day"]).sum().to_numpy()
        K = len(S)
        se = np.sqrt((S ** 2).sum() * K / (K - 1)) / n_cases
        if se > 0:
            t_val = float(mean_ex / se)

    slope = None
    sl = cases.dropna(subset=["excess", "tight"])
    if len(sl) >= 2 and sl["tight"].nunique() >= 2:
        slope = float(stats.linregress(sl["tight"].to_numpy(float), sl["excess"].to_numpy(float)).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = "fewer than 30 independent cases (%d case days), so the result is not observable" % n_days
    elif t_val is not None and mean_ex > 0 and t_val >= 2 and slope_pass:
        status = "confirmed"
        decided = "the mean excess 10-day return is above 0 with t >= 2 and the slope on tight is above 0"
    elif t_val is not None and t_val <= -2:
        status = "rejected"
        decided = "the mean excess 10-day return has t <= -2"
    else:
        status = "inconclusive"
        if t_val is not None and t_val >= 2:
            decided = "t >= 2 but the slope on tight is 0 or below (or not computable), which the plan calls inconclusive"
        else:
            decided = "the t of the mean excess 10-day return lies between -2 and 2, which the plan calls inconclusive"

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t_val is None else {"name": "t of the mean, cases of one day summed", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {"name": "OLS slope of excess 10-day return on tight post_pipeline_value",
                             "value": slope, "passed": slope_pass},
        "counts": {"independent cases": n_days, "cases": n_cases},
        "decided_by": decided,
        "reading": (reading_situation + "; a case is a bar whose forecast is >= 2 while the previous bar's forecast "
                    "in the same window is 0 (a window's first bar cannot be one), the first case of each 10-bar grid "
                    "cell counting from the window's first row, cases without 10 bars ahead in their window left out, "
                    "and the independent cases are the distinct UTC days the cases fall on."),
    }
