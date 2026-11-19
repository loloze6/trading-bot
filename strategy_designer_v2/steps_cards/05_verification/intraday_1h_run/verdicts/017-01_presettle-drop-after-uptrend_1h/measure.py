import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.rise72.last_history_value"

    def to_time(s):
        if pd.api.types.is_numeric_dtype(s):
            v = pd.to_numeric(s, errors="coerce")
            med = np.nanmedian(np.abs(v.values)) if len(v) else 0
            unit = "ms" if med > 1e11 else "s"
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True, errors="coerce")

    # ---------- situation check ----------
    # Two conventions for "the 2 hours before settlement": decision bars stamped
    # 21h/22h (closes at 22h/23h) or stamped 22h/23h (the plan's Forecast line).
    conv_sets = [{5, 6}, {6, 7}]  # hour % 8
    n_active = 0
    hits = [0, 0]

    # ---------- criterion ----------
    case_values, case_excess, case_absf = [], [], []

    for coin, wins in bars.items():
        # coin's mean 2-bar return over all its windows (non-overlapping grid 0,2,4,...)
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values.astype(float)
            n = len(close)
            if n >= 3:
                idx = np.arange(0, n - 2, 2)
                r = close[idx + 2] / close[idx] - 1.0
                r = r[np.isfinite(r)]
                grid_rets.extend(r.tolist())
            prepared.append((d, close))
        mu = float(np.mean(grid_rets)) if len(grid_rets) else np.nan

        for d, close in prepared:
            n = len(close)
            ts = to_time(d["timestamp"])
            hour = ts.dt.hour.values
            minute = ts.dt.minute.values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values.astype(float)

            # raw 72-bar rise: recorded value, else recomputed from prices inside the window
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").values.astype(float)
            else:
                raw = np.full(n, np.nan)
            recomputed = pd.Series(close).pct_change(72).values * 100.0
            raw = np.where(np.isfinite(raw), raw, recomputed)

            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            for k, hs in enumerate(conv_sets):
                in_clock = np.isin(hour % 8, list(hs)) & (minute == 0)
                sit = in_clock & np.isfinite(raw) & (raw > 0) & (fc < 0)
                hits[k] += int((active & sit).sum())

            # cases: bars stamped 21:00, 05:00, 13:00 with forecast < 0
            start = (np.isin(hour, [21, 5, 13])) & (minute == 0) & np.isfinite(fc) & (fc < 0)
            for t in np.where(start)[0]:
                if t + 2 >= n:
                    continue
                r = close[t + 2] / close[t] - 1.0
                if not np.isfinite(r) or not np.isfinite(mu):
                    continue
                ex = r - mu
                case_values.append((-fc[t] / 10.0) * ex)
                case_excess.append(ex)
                case_absf.append(abs(fc[t]))

    agreement = (max(hits) / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The situation is a pre-settlement clock bar (hour mod 8 in {5,6} or in {6,7}, the better of the two "
               "stamp conventions), a positive raw 72-bar rise and a negative forecast; cases are the bars stamped "
               "21:00/05:00/13:00 with forecast < 0 whose t+2 close lies in the same window, the coin mean is over its "
               "non-overlapping 2-bar grid across all windows, and the thirds are the n//3 largest and n//3 smallest |forecast| cases.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars in the 2 hours before a "
                           "settlement after a positive 72-bar rise, as the plan's situation requires."),
            "reading": reading,
        }

    vals = np.array(case_values, dtype=float)
    exc = np.array(case_excess, dtype=float)
    absf = np.array(case_absf, dtype=float)
    n_cases = int(len(vals))

    mean_v = float(np.mean(vals)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(vals, ddof=1))
        t_stat = float(mean_v / (sd / np.sqrt(n_cases))) if sd > 0 else None

    diff = None
    check_passed = None
    k = n_cases // 3
    if k >= 1:
        order = np.argsort(absf, kind="mergesort")
        bottom = exc[order[:k]]
        top = exc[order[-k:]]
        diff = float(np.mean(top) - np.mean(bottom))
        check_passed = bool(diff < 0)

    main = {
        "name": "mean of (-forecast/10) x excess 2-bar return over settlement episodes",
        "value": mean_v,
        "statistic": {"name": "ordinary t", "value": t_stat} if t_stat is not None else None,
        "threshold": "confirm if t >= 2 (with check difference < 0); reject if t <= -2",
    }
    support = {
        "name": "mean excess 2-bar return, top third minus bottom third by |forecast|",
        "value": diff,
        "passed": check_passed,
    }
    counts = {"episodes with forecast < 0": n_cases}

    if n_cases < 200:
        status = "not observable"
        decided = f"Only {n_cases} episodes with forecast < 0 inside windows, below the required 200."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The main-measure t could not be computed (zero dispersion), so neither confirm nor reject is met."
    elif t_stat >= 2 and check_passed:
        status = "confirmed"
        decided = "The main-measure t is >= 2 and the top-minus-bottom-third difference is below 0."
    elif t_stat <= -2:
        status = "rejected"
        decided = "The main-measure t is <= -2: the pre-settlement return rises with the 3-day run-up."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "The main-measure t is >= 2 but the supporting check fails (difference not below 0)."
    else:
        status = "inconclusive"
        decided = "The main-measure t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
