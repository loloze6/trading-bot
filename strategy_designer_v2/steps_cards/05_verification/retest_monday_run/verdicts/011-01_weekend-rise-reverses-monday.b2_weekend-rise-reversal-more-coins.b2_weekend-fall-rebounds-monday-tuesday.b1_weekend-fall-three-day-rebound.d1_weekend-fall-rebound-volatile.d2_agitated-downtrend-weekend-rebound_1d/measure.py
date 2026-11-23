import numpy as np
import pandas as pd

RAW_COL = "debug_info.components.wkend_fall_volratio.last_history_value"


def _to_ts(s):
    if np.issubdtype(s.dtype, np.number):
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
    H = 3
    active_total = 0
    active_agree = 0
    cases = []  # (forecast, excess)

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        prepared = []
        stretch_rets = []
        for w in sorted(wins.keys(), key=lambda k: (len(str(k)), str(k))):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.copy()
            df["_ts"] = _to_ts(df["timestamp"])
            df = df.sort_values("_ts").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").astype(float)
            # Non-overlapping 3-bar stretches from the window's first row
            for i in range(0, len(df) - H, H):
                c0, c1 = close.iloc[i], close.iloc[i + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    stretch_rets.append(c1 / c0 - 1.0)
            prepared.append((df, close, fc))

        drift = float(np.mean(stretch_rets)) if len(stretch_rets) > 0 else np.nan

        for df, close, fc in prepared:
            n = len(df)
            is_sun = (df["_ts"].dt.dayofweek == 6).values
            ret20 = (close / close.shift(20) - 1.0).values
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * n)
            ret1 = (close / close.shift(1) - 1.0).values
            if RAW_COL in df.columns:
                raw = pd.to_numeric(df[RAW_COL], errors="coerce").astype(float).values
            else:
                raw = np.full(n, np.nan)
            fcv = fc.values
            closev = close.values

            for i in range(n):
                f = fcv[i]
                if not np.isfinite(f):
                    continue
                # Situation check on active bars
                if f != 0:
                    active_total += 1
                    if np.isfinite(ret20[i]):
                        down20 = ret20[i] < 0
                    else:
                        down20 = regime[i] == "mean_reversion"
                    if np.isfinite(raw[i]):
                        fall = raw[i] < 0
                    elif np.isfinite(ret1[i]):
                        fall = ret1[i] < 0
                    else:
                        fall = False
                    if is_sun[i] and down20 and fall and f > 0:
                        active_agree += 1
                # Cases: Sunday bar with forecast >= 2
                if is_sun[i] and f >= 2 and i + H < n and np.isfinite(drift):
                    c0, c1 = closev[i], closev[i + H]
                    if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                        cases.append((float(f), float(c1 / c0 - 1.0 - drift)))

    agreement = float(active_agree / active_total) if active_total > 0 else 0.0
    passed = bool(active_total > 0 and agreement >= 0.9)

    main_name = "forecast-weighted mean excess 3-day return of Sunday cases (forecast >= 2)"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check; reject: mean < 0 with t <= -2; at least 100 cases"
    reading = ("Sunday bars are those whose bar start (UTC) is a Sunday; the 20-day return is close[t]/close[t-20]-1 "
               "inside the window (the recorded regime where 20 prior bars are not in the window); the weekend fall is "
               "the raw component < 0 (else Sunday's close-to-close return); the weighted t uses the heteroskedasticity-"
               "robust standard error sqrt(n/(n-1) * sum(w^2 (x-m)^2)) / sum(w); top and bottom halves are the upper and "
               "lower n//2 cases by forecast (stable sort, middle case dropped if n is odd), compared by unweighted means; "
               "the plan's fewer-than-100-cases rule is applied as a minimum count (not observable).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(active_total), "cases": int(len(cases))},
            "decided_by": ("Only {:.1%} of bars with a non-zero forecast are Sunday bars of a falling weekend with a negative "
                           "20-day return and a long forecast, below the 90 % the plan's situation requires.").format(agreement),
            "reading": reading,
        }

    n = len(cases)
    counts = {"cases": int(n)}
    mean_w = None
    t_val = None
    diff = None
    if n > 0:
        f = np.array([c[0] for c in cases])
        x = np.array([c[1] for c in cases])
        sw = f.sum()
        mean_w = float((f * x).sum() / sw)
        if n > 1:
            var = (n / (n - 1.0)) * np.sum((f ** 2) * (x - mean_w) ** 2) / (sw ** 2)
            se = float(np.sqrt(var))
            t_val = float(mean_w / se) if se > 0 else None
        if n >= 2:
            order = np.argsort(f, kind="mergesort")
            half = n // 2
            bottom = x[order[:half]]
            top = x[order[n - half:]]
            diff = float(top.mean() - bottom.mean())

    supp_passed = None if diff is None else bool(diff > 0)
    supporting = {"name": "mean excess return, top half minus bottom half of forecast",
                  "value": diff, "passed": supp_passed}
    statistic = {"name": "t of the forecast-weighted mean", "value": t_val} if t_val is not None else None

    if n < 100:
        status = "not observable"
        decided = "Fewer than 100 cases ({}) across all coins and windows: the minimum count is not reached.".format(n)
    elif t_val is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_w > 0 and t_val >= 2 and supp_passed:
        status = "confirmed"
        decided = "The forecast-weighted mean excess 3-day return is positive with t >= 2 and the top-half minus bottom-half difference is above 0."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the top-half minus bottom-half difference is 0 or below, which the plan calls inconclusive."
    elif mean_w < 0 and t_val <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess 3-day return is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_w, "statistic": statistic, "threshold": threshold},
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
