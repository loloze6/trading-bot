import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    WIDTH_COL = "debug_info.components.wide_day.last_history_value"

    sit_total = 0
    sit_agree = 0
    case_rows = []

    for coin, wins in bars.items():
        # Normal drift: the coin's mean 1-day return over all its windows (returns inside each window only)
        all_rets = []
        prepared = {}
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True).copy()
            close = d["close"].astype(float)
            d["_fwd"] = close.shift(-1) / close - 1.0
            all_rets.append(d["_fwd"].dropna().values)
            prepared[w] = d
        if len(all_rets) == 0:
            continue
        cat = np.concatenate(all_rets) if len(all_rets) else np.array([])
        drift = float(np.mean(cat)) if cat.size else np.nan

        for w, d in prepared.items():
            high = d["high"].astype(float)
            low = d["low"].astype(float)
            close = d["close"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)

            # width: recorded raw value where present, else recomputed from prices inside the window
            ret = close.pct_change()
            std30 = ret.rolling(30, min_periods=30).std()
            width_calc = (high - low) / close / std30
            if WIDTH_COL in d.columns:
                width = pd.to_numeric(d[WIDTH_COL], errors="coerce")
                width = width.where(width.notna(), width_calc)
            else:
                width = width_calc
            rng = (high - low)
            loc = (high - close) / rng.where(rng > 0)
            profile_ok = d["regime"].astype(str) == "mean_reversion"
            situation = (width >= 2.0) & (loc > 0.5) & profile_ok

            active = fc != 0
            sit_total += int(active.sum())
            sit_agree += int((active & situation & (fc > 0)).sum())

            cases = d[(fc > 0) & d["_fwd"].notna()]
            for _, r in cases.iterrows():
                case_rows.append({
                    "day": pd.Timestamp(r["timestamp"]).tz_localize(None).normalize()
                    if pd.Timestamp(r["timestamp"]).tzinfo is not None
                    else pd.Timestamp(r["timestamp"]).normalize(),
                    "excess": float(r["_fwd"]) - drift,
                    "forecast": float(r["forecast"]),
                })

    agreement = (sit_agree / sit_total) if sit_total > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean next-day excess return over coin drift on bars with forecast > 0"
    threshold = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2"
    reading = ("The rising-calm profile cannot be recomputed from the recorded bars (365-bar lookback), so the situation is "
               "width >= 2 and (high-close)/(high-low) > 0.5 on bars whose regime is mean_reversion (profile vetoes not hit); "
               "the same-day t uses deviations summed per UTC day with a G/(G-1) correction, the drift is each coin's mean "
               "1-day return over all its windows, and the plan's 30-day minimum is treated as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(sit_total), "active bars in situation on long side": int(sit_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are wide, lower-close days in the "
                           "rising-calm regime with a long forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    cdf = pd.DataFrame(case_rows)
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    mean = None
    tval = None
    slope = None
    if n_cases > 0:
        x = cdf["excess"].values
        mean = float(np.mean(x))
        dev = cdf.assign(dev=x - mean).groupby("day")["dev"].sum().values
        G = len(dev)
        if G > 1:
            var = (G / (G - 1.0)) * np.sum(dev ** 2) / (n_cases ** 2)
            se = np.sqrt(var)
            tval = float(mean / se) if se > 0 else None
        f = cdf["forecast"].values
        if n_cases > 1 and np.std(f) > 0:
            slope = float(stats.linregress(f, x).slope)

    slope_pass = None if slope is None else bool(slope > 0)

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct days with cases, below the plan's minimum of 30."
    elif mean is not None and tval is not None and mean > 0 and tval >= 2 and slope_pass:
        status = "confirmed"
        decided = "Mean next-day excess return above 0 with t >= 2 and a slope above 0 (confirm rule)."
    elif mean is not None and tval is not None and mean < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean next-day excess return below 0 with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        if mean is not None and tval is not None and mean > 0 and tval >= 2 and not slope_pass:
            decided = "Positive mean with t >= 2 but a slope at or below 0 (inconclusive rule)."
        else:
            decided = "t between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": None if tval is None else {"name": "t of the mean, same-day cases taken together", "value": tval},
            "threshold": threshold,
        },
        "supporting_check": {"name": "OLS slope of next-day excess return on forecast > 0",
                             "value": slope, "passed": slope_pass},
        "counts": {"distinct days with cases": n_days, "cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
