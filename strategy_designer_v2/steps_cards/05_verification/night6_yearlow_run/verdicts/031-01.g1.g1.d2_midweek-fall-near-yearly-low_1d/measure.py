import numpy as np
import pandas as pd


def measure(bars):
    FRIDAY = 4  # bar starting Friday (UTC): its close is Friday's close, the coming bar is Saturday
    raw_cols = [
        "debug_info.components.midweek_low.last_history_value",
        "debug_info.components.midweek_high.last_history_value",
    ]

    active_total = 0
    active_agree = 0
    cases = []  # (date, value, is_short_side)

    for coin, windows in bars.items():
        # coin's mean daily return over all its windows (returns stay inside each window)
        all_rets = []
        prepared = {}
        for w, df in windows.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            d["_ret_next"] = close.shift(-1) / close - 1.0
            all_rets.append(d["_ret_next"].dropna().values)
            prepared[w] = d
        if len(all_rets) == 0:
            continue
        cat = np.concatenate(all_rets) if len(all_rets) else np.array([])
        coin_mean = float(np.mean(cat)) if cat.size else np.nan

        for w, d in prepared.items():
            dates = d["timestamp"].dt.normalize()
            close_by_date = pd.Series(d["close"].astype(float).values, index=dates.values)
            close_by_date = close_by_date[~close_by_date.index.duplicated(keep="last")]
            fc = d["forecast"].astype(float)
            regime = d["regime"].astype(str)
            wd = d["timestamp"].dt.weekday

            for i in range(len(d)):
                f = fc.iloc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                # ---- situation check
                active_total += 1
                ok = wd.iloc[i] == FRIDAY
                # midweek return sign: recorded raw value first, else Thursday/Monday closes
                mw = np.nan
                for c in raw_cols:
                    if c in d.columns:
                        v = d[c].iloc[i]
                        if v is not None and np.isfinite(float(v)):
                            mw = float(v)
                            break
                if not np.isfinite(mw):
                    day = dates.iloc[i]
                    thu = day - pd.Timedelta(days=1)
                    mon = day - pd.Timedelta(days=4)
                    if thu in close_by_date.index and mon in close_by_date.index:
                        mw = close_by_date[thu] / close_by_date[mon] - 1.0
                if f > 0:
                    if np.isfinite(mw) and not (mw > 0):
                        ok = False
                else:
                    if regime.iloc[i] != "mean_reversion":
                        ok = False
                    if np.isfinite(mw) and not (mw < 0):
                        ok = False
                if ok:
                    active_agree += 1

                # ---- main measure cases: Friday bars with non-zero forecast
                if wd.iloc[i] != FRIDAY:
                    continue
                r = d["_ret_next"].iloc[i]
                if not np.isfinite(r) or not np.isfinite(coin_mean):
                    continue
                val = (f / 10.0) * (r - coin_mean)
                short_side = (regime.iloc[i] == "mean_reversion") and (f < 0)
                cases.append((dates.iloc[i], val, short_side))

    agreement = float(active_agree / active_total) if active_total > 0 else None
    passed = agreement is not None and agreement >= 0.90

    reading = (
        "The Friday is the bar whose UTC start is a Friday (its close is Friday's close, the next bar Saturday); "
        "the midweek return's sign is read from the recorded raw component, else from Thursday/Monday closes, and is "
        "skipped when neither exists; the lower half of the 365-day range is read from the recorded regime "
        "(mean_reversion), since the detector's Donchian value is not recorded and 365 days of history are not in the "
        "windows; Saturday's return is the next row's close over this close inside the window; the day-grouped t "
        "sums each day's case deviations from the mean with a G/(G-1) correction; the plan's minimum counts "
        "(100 days, 30 short-side cases) are applied first as 'not observable'."
    )

    main_name = "mean of forecast/10 x (Saturday return - coin mean daily return) on Friday active bars"
    main_threshold = "confirm: day-grouped t >= 2 over >= 100 days with short-side check > 0; reject: t <= -2 over >= 100 days"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_threshold},
            "supporting_check": None,
            "counts": {"active bars": int(active_total), "days": None, "short-side cases": None},
            "decided_by": (
                "Fewer than 90% of the non-zero forecasts sit on Friday bars with the side the Fidelity expects "
                "(long after a midweek gain, short only after a midweek fall in the lower half of the yearly range)."
            ),
            "reading": reading,
        }

    if len(cases) > 0:
        cdf = pd.DataFrame(cases, columns=["date", "val", "short"])
    else:
        cdf = pd.DataFrame({"date": [], "val": [], "short": []})
    n = int(len(cdf))
    n_days = int(cdf["date"].nunique()) if n else 0
    short_vals = cdf.loc[cdf["short"].astype(bool), "val"] if n else pd.Series(dtype=float)
    n_short = int(len(short_vals))

    mean_val = float(cdf["val"].mean()) if n else None
    t_val = None
    if n > 0 and n_days > 1:
        dev = cdf["val"] - mean_val
        dsum = dev.groupby(cdf["date"]).sum().values
        var = (n_days / (n_days - 1.0)) * float(np.sum(dsum ** 2)) / (n ** 2)
        if var > 0:
            t_val = float(mean_val / np.sqrt(var))

    sup_val = float(short_vals.mean()) if n_short > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    counts = {"days": n_days, "short-side cases": n_short, "cases": n}

    if n_days < 100 or n_short < 30:
        status = "not observable"
        missing = []
        if n_days < 100:
            missing.append(f"only {n_days} days of cases (minimum 100)")
        if n_short < 30:
            missing.append(f"only {n_short} short-side cases (minimum 30)")
        decided_by = "Minimum count not reached: " + " and ".join(missing) + "."
    elif t_val is None:
        status = "inconclusive"
        decided_by = "The day-grouped t could not be computed (zero variance), so neither confirm nor reject is met."
    elif t_val >= 2 and sup_pass:
        status = "confirmed"
        decided_by = "Confirm: the main-measure t is 2 or more over at least 100 days and the short-side check is above 0."
    elif t_val <= -2:
        status = "rejected"
        decided_by = "Reject: the main-measure t is -2 or less over at least 100 days."
    elif t_val >= 2:
        status = "inconclusive"
        decided_by = "Inconclusive: the main-measure t is 2 or more but the short-side check is at or below 0."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: the main-measure t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": ({"name": "t of the mean, cases grouped by day", "value": t_val} if t_val is not None else None),
            "threshold": main_threshold,
        },
        "supporting_check": {
            "name": "same mean on short-side cases (mean_reversion, forecast < 0) above 0",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
