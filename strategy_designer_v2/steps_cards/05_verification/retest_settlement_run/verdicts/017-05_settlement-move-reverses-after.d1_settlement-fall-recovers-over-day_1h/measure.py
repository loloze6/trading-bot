import numpy as np
import pandas as pd


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype(float)
        med = np.nanmedian(np.abs(v.values)) if len(v) else 0.0
        if med > 1e17:
            unit = "ns"
        elif med > 1e14:
            unit = "us"
        elif med > 1e11:
            unit = "ms"
        else:
            unit = "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 24
    RAW = "debug_info.components.fall2h.last_history_value"

    n_active = 0
    n_agree = 0
    case_rows = []  # (forecast, excess)

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        # coin's normal 24-bar drift: non-overlapping grid returns over all windows
        grid_rets = []
        prepared = {}
        for w in sorted(wins.keys(), key=lambda k: (len(str(k)), str(k))):
            df = wins[w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            n = len(close)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    grid_rets.append(c1 / c0 - 1.0)
            prepared[w] = (df, close)
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan

        for w, (df, close) in prepared.items():
            n = len(close)
            ts = _to_utc(df["timestamp"]).reset_index(drop=True)
            next_hour = (ts + pd.Timedelta(hours=1)).dt.hour.values
            settle = np.isin(next_hour, [0, 16])

            # raw 2-hour scaled move into settlement: recorded raw value, else price return
            ret2 = np.full(n, np.nan)
            if n > 2:
                ret2[2:] = close[2:] / close[:-2] - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values.astype(float)
                raw = np.where(np.isfinite(raw), raw, ret2)
            else:
                raw = ret2
            fall = np.isfinite(raw) & (raw < 0)
            situation = settle & fall

            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

            # cases: settlement bar with forecast > 0, first one per 24-bar grid cell
            for start in range(0, n, H):
                end = min(start + H, n)
                for t in range(start, end):
                    if settle[t] and np.isfinite(fc[t]) and fc[t] > 0:
                        if t + H < n and np.isfinite(close[t]) and np.isfinite(close[t + H]) \
                                and close[t] > 0 and np.isfinite(drift):
                            r = close[t + H] / close[t] - 1.0
                            case_rows.append((float(fc[t]), float(r - drift)))
                        break

    reading = ("Settlement bars are those stamped 23:00 or 15:00 UTC (the next bar opens at 00:00 or 16:00) and a fall "
               "is a negative fall2h raw value (2-bar price return when not recorded); a case is the first settlement "
               "bar with forecast > 0 in each 24-bar grid cell of a window, with a full 24-bar forward return; the t of "
               "the forecast-weighted mean uses the weighted (sandwich) standard error with n/(n-1) correction; top and "
               "bottom halves are the upper and lower n//2 cases sorted by forecast (the middle case dropped if n is odd), "
               "compared on unweighted mean excess returns; the plan's 100-case minimum gives 'not observable'.")

    threshold = "confirm: weighted mean > 0 with t >= 2 and supporting check passes; reject: weighted mean < 0 with t <= -2"
    mm_name = "forecast-weighted mean 24-bar excess return over normal drift"

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"independent cases": 0},
            "decided_by": "No active bars (forecast never non-zero), so the record holds no case of the idea.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"independent cases": len(case_rows)},
            "decided_by": ("Fewer than 90% of active bars are long bars on a 00:00/16:00 settlement after a 2-hour fall, "
                           "so the forecast does not follow the plan's situation and side."),
            "reading": reading,
        }

    n_cases = len(case_rows)
    if n_cases == 0:
        f = np.array([]); x = np.array([])
    else:
        f = np.array([c[0] for c in case_rows]); x = np.array([c[1] for c in case_rows])

    wmean = None; tval = None
    if n_cases >= 2 and f.sum() > 0:
        sw = f.sum()
        m = float((f * x).sum() / sw)
        se = np.sqrt(np.sum(f ** 2 * (x - m) ** 2)) / sw * np.sqrt(n_cases / (n_cases - 1))
        wmean = m
        tval = float(m / se) if se > 0 else None
    elif n_cases == 1:
        wmean = float(x[0])

    sup_val = None; sup_pass = None
    if n_cases >= 2:
        order = np.argsort(f, kind="mergesort")
        k = n_cases // 2
        bottom = x[order[:k]]
        top = x[order[n_cases - k:]]
        sup_val = float(top.mean() - bottom.mean())
        sup_pass = bool(sup_val > 0)

    result = {
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": mm_name, "value": wmean,
                         "statistic": ({"name": "t of weighted mean", "value": tval} if tval is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "top-half minus bottom-half forecast mean excess return",
                             "value": sup_val, "passed": sup_pass},
        "counts": {"independent cases": int(n_cases)},
        "reading": reading,
    }

    if n_cases < 100:
        result["status"] = "not observable"
        result["decided_by"] = f"Only {n_cases} independent cases, fewer than the plan's minimum of 100."
        return result

    if tval is None or wmean is None:
        result["status"] = "inconclusive"
        result["decided_by"] = "The t of the weighted mean could not be computed (zero dispersion), meeting neither rule."
        return result

    if wmean > 0 and tval >= 2:
        if sup_pass:
            result["status"] = "confirmed"
            result["decided_by"] = "Weighted mean excess return above 0 with t >= 2 and the top-minus-bottom half check above 0."
        else:
            result["status"] = "inconclusive"
            result["decided_by"] = "Weighted mean excess return above 0 with t >= 2 but the supporting check fails."
    elif wmean < 0 and tval <= -2:
        result["status"] = "rejected"
        result["decided_by"] = "Weighted mean excess return below 0 with t <= -2."
    else:
        result["status"] = "inconclusive"
        result["decided_by"] = "The t of the weighted mean excess return lies strictly between -2 and 2."
    return result
