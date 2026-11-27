import json
import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    COMP = "broken_up_run"
    MIN_CASES = 40
    MIN_DAYS = 40
    BAND = 2.0

    def to_time(s):
        if pd.api.types.is_numeric_dtype(s):
            mx = float(np.nanmax(s.values)) if len(s) else 0.0
            unit = "ms" if mx > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    def comp_value(df, cid, key):
        flat = "debug_info.components.%s.%s" % (cid, key)
        if flat in df.columns:
            return pd.to_numeric(df[flat], errors="coerce").values.astype(float)
        out = np.full(len(df), np.nan)
        if "debug_info.components" in df.columns:
            col = df["debug_info.components"].values
            for i, v in enumerate(col):
                d = v
                if isinstance(d, str):
                    try:
                        d = json.loads(d)
                    except Exception:
                        d = None
                if isinstance(d, dict):
                    c = d.get(cid)
                    if isinstance(c, dict):
                        x = c.get(key)
                        try:
                            out[i] = float(x)
                        except (TypeError, ValueError):
                            pass
        return out

    def price_streak(close):
        # length of the up run broken by a down close at t (0 otherwise); NaN if not computable
        n = len(close)
        res = np.full(n, np.nan)
        for t in range(1, n):
            if not (close[t] < close[t - 1]):
                res[t] = 0.0
                continue
            k = 0
            j = t - 1
            while j >= 1 and close[j] > close[j - 1] and k < 30:
                k += 1
                j -= 1
            if j == 0 and k < 30:
                res[t] = np.nan if k == t - 1 else float(k)
            else:
                res[t] = float(k)
        return res

    n_active = 0
    n_agree = 0
    cases = []  # (coin, day, unusual_short, abs_forecast)

    for coin, wins in bars.items():
        # coin's normal 7-bar drift over all windows, non-overlapping grid
        grid_rets = []
        prepared = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            for p in range(0, len(df) - H, H):
                if np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] != 0:
                    grid_rets.append(close[p + H] / close[p] - 1.0)
            prepared[w] = (df, close)
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan

        for w, (df, close) in prepared.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            raw = comp_value(df, COMP, "last_history_value")
            ps = price_streak(close)
            streak = np.where(np.isfinite(raw), raw, ps)
            times = to_time(df["timestamp"])
            days = times.dt.strftime("%Y-%m-%d").values

            # situation check
            for t in range(len(df)):
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                down = (close[t] < close[t - 1]) if t > 0 else (np.isfinite(raw[t]) and raw[t] >= 2)
                sit = (np.isfinite(streak[t]) and streak[t] >= 2 and bool(down)
                       and regime[t] != "chop")
                if sit and f < 0:
                    n_agree += 1

            # bets on the short side
            ref = 0.0
            bet_bars = []
            for t in range(len(df)):
                f = fc[t]
                m = -f if (np.isfinite(f) and f < 0) else 0.0
                if m <= 0:
                    ref = 0.0
                    continue
                if m - ref >= BAND:
                    bet_bars.append(t)
                    ref = m
                else:
                    ref = min(ref, m)
            seen_cells = set()
            for t in bet_bars:
                cell = t // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if t + H >= len(df) or not np.isfinite(drift):
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H])) or close[t] == 0:
                    continue
                r = close[t + H] / close[t] - 1.0
                cases.append((coin, days[t], -(r - drift), abs(fc[t])))

    threshold = "mean > 0 with day-clustered t >= 2 to confirm (with slope > 0, t >= 2); mean < 0 with t <= -2 or slope < 0 with t <= -2 to reject"
    reading = ("Profile on a bar is read from the detector's recorded regime (not 'chop'), since its components are not recorded and "
               "their 365-bar lookback cannot be rebuilt inside a window; the streak is the recorded raw value of broken_up_run, "
               "else recomputed from closes; the case's first bet in each 7-bar grid cell is kept; the slope's t is the ordinary OLS t; "
               "the plan's 'fewer than 40 cases or days' minimum is reported as 'not observable'.")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean short-direction unusual 7-bar move", "value": None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "OLS slope of unusual move on |forecast|", "value": None, "passed": None},
            "counts": {"cases": 0, "distinct days": 0},
            "decided_by": "No active bars: fewer than 40 cases, the plan's minimum count, is not reached.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean short-direction unusual 7-bar move", "value": None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90 % of the active bars are short bets on a down close breaking an up run of 2+ days "
                          "inside the rising agitated profile, as the Fidelity states.",
            "reading": reading,
        }

    n = len(cases)
    day_list = [c[1] for c in cases]
    n_days = len(set(day_list))
    x = np.array([c[2] for c in cases], dtype=float)
    a = np.array([c[3] for c in cases], dtype=float)

    mean = float(np.mean(x)) if n else None
    t_mean = None
    if n >= 2 and n_days >= 2:
        dev = pd.Series(x - mean).groupby(pd.Series(day_list)).sum().values
        var = (n_days / (n_days - 1.0)) * float(np.sum(dev ** 2)) / (n ** 2)
        se = np.sqrt(var)
        t_mean = float(mean / se) if se > 0 else None

    slope = None
    t_slope = None
    if n >= 3 and np.std(a) > 0:
        lr = stats.linregress(a, x)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_pass = None if t_slope is None else bool(slope > 0 and t_slope >= 2)

    counts = {"cases": int(n), "distinct days": int(n_days)}
    main = {"name": "mean short-direction unusual 7-bar move", "value": mean,
            "statistic": None if t_mean is None else {"name": "t of the mean, cases of one day taken together", "value": t_mean},
            "threshold": threshold}
    sup = {"name": "OLS slope of unusual move on |forecast|", "value": slope, "passed": sup_pass}
    if t_slope is not None:
        sup["t"] = t_slope

    if n < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = "Fewer than 40 cases or cases on fewer than 40 distinct days: the plan's minimum count is not reached."
    else:
        rej_mean = t_mean is not None and mean < 0 and t_mean <= -2
        rej_slope = t_slope is not None and slope < 0 and t_slope <= -2
        conf_mean = t_mean is not None and mean > 0 and t_mean >= 2
        if rej_mean or rej_slope:
            status = "rejected"
            decided = ("Reject: the mean unusual move is negative with t <= -2." if rej_mean
                       else "Reject: the slope on |forecast| is negative with t <= -2.")
        elif conf_mean and sup_pass:
            status = "confirmed"
            decided = "Confirm: the mean unusual move is positive with t >= 2 and the slope on |forecast| is positive with t >= 2."
        else:
            status = "inconclusive"
            if conf_mean:
                decided = "Inconclusive: the mean meets the confirm rule but the supporting slope does not reach t >= 2."
            else:
                decided = "Inconclusive: the mean or slope has |t| below 2, meeting neither confirm nor reject."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
