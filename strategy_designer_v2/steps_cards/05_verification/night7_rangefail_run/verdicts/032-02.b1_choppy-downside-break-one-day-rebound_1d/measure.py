import numpy as np
import pandas as pd


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        mx = s.dropna().abs().max() if s.notna().any() else 0
        unit = "ms" if mx > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    raw_col = "debug_info.components.depth.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    case_rows = []          # (day, unusual move, forecast)
    for coin, wins in bars.items():
        # the coin's mean daily return over all its windows (returns never cross windows)
        all_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["_ts"] = _to_utc(d["timestamp"]).values
            d = d.sort_values("_ts").reset_index(drop=True)
            close = d["close"].astype(float)
            low = d["low"].astype(float)
            d["_ret1"] = close.shift(-1) / close - 1.0
            all_rets.append(d["_ret1"].dropna().values)
            # raw distance from prior 20-bar low, recomputed inside the window
            prior_low = low.shift(1).rolling(20, min_periods=20).min()
            d["_dist_px"] = (close / prior_low - 1.0) * 100.0
            prepared.append(d)
        rets = np.concatenate(all_rets) if all_rets else np.array([])
        mu = float(np.mean(rets)) if len(rets) else np.nan

        for d in prepared:
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            if raw_col in d.columns:
                raw = pd.to_numeric(d[raw_col], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            raw = raw.where(raw.notna(), d["_dist_px"])
            situation = raw < 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

            cases = (fc > 0) & d["_ret1"].notna()
            for i in np.flatnonzero(cases.values):
                case_rows.append((d["_ts"].iloc[i].floor("D"),
                                  float(d["_ret1"].iloc[i]) - mu,
                                  float(fc.iloc[i])))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean next-day unusual move (return minus coin's mean daily return) over bars with forecast > 0"
    threshold = "confirm: mean > 0 with t >= 2.0 and slope > 0; reject: mean < 0 with t <= -2.0; else inconclusive; fewer than 30 distinct days: inconclusive"
    reading = ("The situation is checked as close < min(low of prior 20 bars) (raw depth value < 0, recomputed from prices "
               "where not recorded) on the long side, without re-testing the choppy profile the code adds; the next-day "
               "return of a window's last bar is left out; the day-clustered t sums the cases' deviations per UTC day with "
               "a D/(D-1) correction; the plan's own 'fewer than 30 distinct days' rule is treated as the minimum count "
               "and reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long bars where the close is under "
                           "the prior 20-day low, which the Fidelity says the test holds."
                           if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    n_cases = len(case_rows)
    if n_cases:
        cdf = pd.DataFrame(case_rows, columns=["day", "u", "f"])
        n_days = int(cdf["day"].nunique())
    else:
        cdf = pd.DataFrame(columns=["day", "u", "f"])
        n_days = 0

    mean_u = float(cdf["u"].mean()) if n_cases else None
    t = None
    if n_cases and n_days >= 2:
        dev = cdf["u"] - mean_u
        s = dev.groupby(cdf["day"]).sum().values
        var = float(np.sum(s ** 2)) * n_days / (n_days - 1) / (n_cases ** 2)
        if var > 0:
            t = mean_u / np.sqrt(var)
    slope = None
    if n_cases >= 2 and float(np.var(cdf["f"].values)) > 0:
        slope = float(np.polyfit(cdf["f"].values.astype(float), cdf["u"].values.astype(float), 1)[0])
    slope_pass = None if slope is None else bool(slope > 0)

    counts = {"cases": n_cases, "distinct days": n_days}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days across all coins and windows, below the plan's 30."
    elif t is not None and mean_u > 0 and t >= 2.0 and slope_pass:
        status = "confirmed"
        decided = "The mean unusual move is > 0 with t >= 2.0 and the slope on the forecast is > 0."
    elif t is not None and mean_u < 0 and t <= -2.0:
        status = "rejected"
        decided = "The mean unusual move is < 0 with t <= -2.0."
    elif t is not None and t >= 2.0:
        status = "inconclusive"
        decided = "The t is >= 2.0 but the supporting slope is not > 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2.0 and 2.0 (or cannot be computed), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": mean_u,
                         "statistic": None if t is None else {"name": "t of the mean, cases of one day together",
                                                              "value": float(t)},
                         "threshold": threshold},
        "supporting_check": {"name": "OLS slope of next-day unusual move on forecast",
                             "value": slope, "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
