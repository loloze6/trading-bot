import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.close_pos.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    case_rows = []  # (day, excess_fall, abs_forecast)

    for coin, wins in bars.items():
        # coin's mean daily (1-bar) return over all windows together
        all_rets = []
        prepared = {}
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            d["_ret1"] = close.shift(-1) / close - 1.0  # inside the window only
            all_rets.append(d["_ret1"].dropna().values)
            prepared[w] = d
        allr = np.concatenate(all_rets) if all_rets else np.array([])
        mu = float(np.mean(allr)) if allr.size else np.nan

        for w, d in prepared.items():
            high = d["high"].astype(float)
            low = d["low"].astype(float)
            close = d["close"].astype(float)
            fc = d[FC].astype(float).fillna(0.0) if FC in d.columns else pd.Series(0.0, index=d.index)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)

            # wide day: range(t) / mean range of last 20 bars, t included
            rng = high - low
            mean20 = rng.rolling(20, min_periods=20).mean()
            ratio = rng / mean20.replace(0, np.nan)
            wide = ratio >= 1.0
            # where the 20-bar history is not inside the recorded window, the detector's
            # decision (regime) is the only evidence of the wide-day rule
            wide = wide.where(ratio.notna(), regime == "mean_reversion")

            # close above the middle of the day's range: raw component value > 0
            mid = (high + low) / 2.0
            above_px = close > mid
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                above = (raw > 0).where(raw.notna(), above_px)
            else:
                above = above_px

            # falling agitated profile: detector components not recorded -> its decision
            profile = regime == "mean_reversion"

            situation = wide.astype(bool) & above.astype(bool) & profile
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            # cases for the criterion
            cases = (fc < 0) & d["_ret1"].notna()
            if cases.any() and np.isfinite(mu):
                sub = d.loc[cases]
                ex = -(sub["_ret1"].astype(float) - mu)
                days = sub["timestamp"].dt.floor("D")
                for dy, e, f in zip(days, ex, fc[cases].abs()):
                    case_rows.append((dy, float(e), float(f)))

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "mean next-day excess fall (short-signed return minus coin mean daily return) on case bars"
    thr = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2"
    stat_name = "t of the mean, cases of one day taken together"
    sup_name = "OLS slope of excess fall on abs(forecast)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "distinct case days": None},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are short bars of the plan's "
                          "situation (falling agitated profile, wide day with range/20-day mean range >= 1, "
                          "close above the day's midpoint).",
            "reading": "The profile is read from the recorded regime (detector components are not recorded); "
                       "the wide-day rule is recomputed from prices where 20 bars exist in the window.",
        }

    # ---------- 2. criterion ----------
    cdf = pd.DataFrame(case_rows, columns=["day", "ex", "absf"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    mean_ex = float(cdf["ex"].mean()) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        dev = cdf["ex"] - mean_ex
        S = dev.groupby(cdf["day"]).sum().values
        D = len(S)
        var_mean = (D / (D - 1.0)) * float(np.sum(S ** 2)) / (n_cases ** 2)
        if var_mean > 0:
            t_val = float(mean_ex / np.sqrt(var_mean))

    slope = None
    if n_cases >= 2 and cdf["absf"].var(ddof=0) > 0:
        x = cdf["absf"].values
        y = cdf["ex"].values
        slope = float(np.sum((x - x.mean()) * (y - y.mean())) / np.sum((x - x.mean()) ** 2))
    slope_pass = None if slope is None else bool(slope > 0)

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days across the coins, below the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean excess fall could not be computed, so neither confirm nor reject is met."
    elif mean_ex > 0 and t_val >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "Mean excess fall above 0 with t >= 2 and a positive slope on abs(forecast): the confirm rule."
        else:
            status = "inconclusive"
            decided = "Confirming t but the slope on abs(forecast) is not positive: the inconclusive rule."
    elif mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean excess fall below 0 with t <= -2: the reject rule."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2: the inconclusive rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t_val is None else {"name": stat_name, "value": t_val},
            "threshold": thr,
        },
        "supporting_check": {"name": sup_name, "value": slope, "passed": slope_pass},
        "counts": {"distinct case days": n_days, "case bars": n_cases},
        "decided_by": decided,
        "reading": "Cases are every bar with forecast < 0 (1-bar horizon, so every bar is on the grid), the "
                   "drift is the coin's mean 1-bar return over all its windows, the day-grouped t sums the "
                   "deviations per UTC day, the slope is an ordinary least-squares slope required only to be > 0, "
                   "and the 30-day minimum maps to 'not observable'.",
    }
