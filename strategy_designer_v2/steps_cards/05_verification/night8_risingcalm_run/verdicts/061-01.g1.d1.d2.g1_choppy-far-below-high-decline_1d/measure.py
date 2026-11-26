import numpy as np
import pandas as pd

GAP_COL = "debug_info.components.gap_below_high.last_history_value"
H = 5


def _gap_from_prices(close):
    # DistanceFromHigh, period 20, close source, current bar included, percent form (inside the window only)
    hi = close.rolling(20, min_periods=1).max()
    return (close / hi - 1.0) * 100.0


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for win in sorted(bars[coin]):
            df = bars[coin][win].reset_index(drop=True)
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            if GAP_COL in df.columns:
                gap = pd.to_numeric(df[GAP_COL], errors="coerce")
                gap = gap.where(gap.notna(), _gap_from_prices(close))
            else:
                gap = _gap_from_prices(close)
            # choppy profile: the detector's default regime "unknown" (|60-bar evolution| <= 10)
            choppy = df["regime"].astype(str) == "unknown"
            situation = choppy & (gap < 0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "|forecast|-weighted mean excess 5-bar short return over grid cases with forecast < 0"
    threshold = "confirm: mean > 0 with t >= 2 (day-clustered) and larger-gap half beats smaller-gap half; reject: mean < 0 with t <= -2"
    reading_base = ("Choppy bars are read from the recorded regime 'unknown' (the detector's default when the 60-bar "
                    "evolution is within +/-10), the gap from last_history_value (recomputed from closes where missing); ")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are choppy bars with the close below "
                           "its 20-day closing high carrying a short forecast, as the Fidelity requires."),
            "reading": reading_base + "agreement counts active bars meeting all three conditions.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin in sorted(bars):
        grid_rets = []
        coin_cases = []
        for win in sorted(bars[coin]):
            df = bars[coin][win].reset_index(drop=True)
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                f = fc[i]
                if np.isfinite(f) and f < 0 and not pd.isna(ts.iloc[i]):
                    coin_cases.append((r, f, ts.iloc[i].strftime("%Y-%m-%d")))
        if len(grid_rets) == 0:
            continue
        mu = float(np.mean(grid_rets))
        for r, f, d in coin_cases:
            rows.append({"coin": coin, "excess_short": -(r - mu), "absf": abs(f), "day": d})

    cases = pd.DataFrame(rows, columns=["coin", "excess_short", "absf", "day"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"grid cases": n_cases, "distinct days with a case": n_days}

    reading = (reading_base +
               "the coin's mean 5-bar return is over all its windows' non-overlapping grid returns; the t uses per-day "
               "summed deviations of the weighted values (with D/(D-1) correction); the larger-gap half is |forecast| "
               "strictly above the median and the halves compare unweighted mean excess short returns; "
               "too few cases gives 'not observable' as the workflow requires.")

    mean_val = None
    t_val = None
    diff = None
    if n_cases > 0:
        w = cases["absf"].values / cases["absf"].mean()
        x = w * cases["excess_short"].values
        mean_val = float(np.mean(x))
        dev = pd.Series(x - mean_val).groupby(cases["day"].values).sum().values
        D = len(dev)
        if D > 1:
            se = np.sqrt(np.sum(dev ** 2) * D / (D - 1)) / n_cases
            t_val = float(mean_val / se) if se > 0 else None
        med = float(np.median(cases["absf"].values))
        big = cases["absf"].values > med
        small = ~big
        if big.sum() > 0 and small.sum() > 0:
            diff = float(cases["excess_short"].values[big].mean() - cases["excess_short"].values[small].mean())

    sup_pass = None if diff is None else bool(diff > 0)
    main = {"name": main_name, "value": mean_val,
            "statistic": None if t_val is None else {"name": "t of the mean, cases of one day summed", "value": t_val},
            "threshold": threshold}
    supporting = {"name": "larger-gap half minus smaller-gap half mean excess short return",
                  "value": diff, "passed": sup_pass}

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} grid cases (need 100) and {n_days} distinct days "
                   f"(need 60).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_val > 0 and t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "Weighted mean excess short return above 0 with t >= 2 and the larger-gap half beats the smaller-gap half."
    elif mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "Weighted mean excess short return below 0 with t <= -2."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the larger-gap half does not beat the smaller-gap half."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
