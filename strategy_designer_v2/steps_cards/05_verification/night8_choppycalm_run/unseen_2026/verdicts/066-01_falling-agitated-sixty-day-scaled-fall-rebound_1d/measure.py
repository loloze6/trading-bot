import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    LHV = "debug_info.components.fall_vs_60d_swing.last_history_value"
    PROFILE_REGIME = "unknown"   # the only regime with a strategy: both profile vetoes passed

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            f = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            close = pd.to_numeric(d["close"], errors="coerce")
            day_ret = close / close.shift(1) - 1.0
            if LHV in d.columns:
                raw = pd.to_numeric(d[LHV], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # Use the raw scaled return; fall back to the price return when it is missing.
            fall = np.where(raw.notna(), raw < 0, day_ret < 0)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)
            in_profile = (regime == PROFILE_REGIME).values
            active = (f != 0).values
            ok = active & in_profile & fall & (f > 0).values
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "forecast-weighted mean next-day return minus coin's mean daily return"
    thr = "confirm: > 0 with t >= 2 and slope > 0; reject: t <= -2"
    reading = ("The falling agitated profile is read from the recorded regime "
               "(the only regime with a strategy, 'unknown', is the one where both profile vetoes passed). "
               "A falling day is a negative raw scaled return, or a negative close-to-close return when the raw value is missing. "
               "The coin's mean daily return is the mean of all its within-window close-to-close returns. "
               "The t of the weighted mean sums the cases' weighted deviations f*(x-m) per UTC day and uses "
               "SE = sqrt(D/(D-1) * sum of squared day sums) / sum(f). "
               "The plan's minimum counts are taken as 100 cases and 50 distinct days, and missing them gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None, "distinct days": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on a falling day "
                           "inside the falling agitated profile, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        per_win = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            coin_rets.append(nxt.dropna().values)
            per_win.append((d, nxt))
        if not coin_rets:
            continue
        allr = np.concatenate(coin_rets)
        if allr.size == 0:
            continue
        mu = float(np.mean(allr))
        for d, nxt in per_win:
            f = pd.to_numeric(d[FC], errors="coerce")
            ts = pd.to_datetime(d["timestamp"], utc=True)
            mask = (f > 0) & nxt.notna()
            for i in np.where(mask.values)[0]:
                rows.append((ts.iloc[i].normalize(), float(f.iloc[i]), float(nxt.iloc[i] - mu)))

    n_cases = len(rows)
    days = sorted(set(r[0] for r in rows))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days), "active bars": int(n_active)}

    value = None
    tval = None
    slope = None
    if n_cases > 0:
        cdf = pd.DataFrame(rows, columns=["day", "f", "x"])
        sw = cdf["f"].sum()
        value = float((cdf["f"] * cdf["x"]).sum() / sw) if sw > 0 else None
        if value is not None and n_days > 1:
            dev = cdf["f"] * (cdf["x"] - value)
            dsum = dev.groupby(cdf["day"]).sum().values
            se = np.sqrt(n_days / (n_days - 1.0) * np.sum(dsum ** 2)) / sw
            tval = float(value / se) if se > 0 else None
        if n_cases > 1 and cdf["f"].var(ddof=1) > 0:
            fx = cdf["f"].values
            xx = cdf["x"].values
            slope = float(np.sum((fx - fx.mean()) * (xx - xx.mean())) / np.sum((fx - fx.mean()) ** 2))

    slope_passed = None if slope is None else bool(slope > 0)

    if n_cases < 100 or n_days < 50:
        status = "not observable"
        decided_by = (f"The plan's minimum of 100 cases on 50 distinct days is not reached "
                      f"({n_cases} cases on {n_days} days).")
    elif tval is None or value is None:
        status = "inconclusive"
        decided_by = "The t of the weighted mean excess return could not be computed, so neither the confirm rule nor the reject rule is met."
    elif value > 0 and tval >= 2 and slope_passed:
        status = "confirmed"
        decided_by = "The forecast-weighted mean excess return is above 0 with t >= 2, and the slope is positive."
    elif tval <= -2:
        status = "rejected"
        decided_by = "The forecast-weighted mean excess return has t <= -2."
    elif tval >= 2:
        status = "inconclusive"
        decided_by = "The t is >= 2, but the slope is at or below 0 (or cannot be computed), so the result is inconclusive."
    else:
        status = "inconclusive"
        decided_by = "The t lies between -2 and 2, so the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": value,
            "statistic": None if tval is None else {"name": "t of weighted mean, same-day cases summed", "value": tval},
            "threshold": thr,
        },
        "supporting_check": {"name": "OLS slope of excess next-day return on forecast", "value": slope,
                             "passed": slope_passed},
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
