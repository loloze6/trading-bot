import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.swing_move.last_history_value"
    PROFILE_REGIME = "unknown"  # the only regime with a strategy: |60-day price evolution| <= 10 (choppy)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).values
            raw = pd.to_numeric(df[RAW], errors="coerce").values if RAW in df.columns \
                else np.full(len(df), np.nan)
            active = f != 0
            n_active += int(active.sum())
            in_profile = reg == PROFILE_REGIME
            raw_sign = np.sign(np.where(np.isnan(raw), 0.0, raw))
            agree = active & in_profile & (raw_sign != 0) & (np.sign(f) == raw_sign)
            n_agree += int(agree.sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of 5-bar forward excess return (minus coin's normal drift) on forecast, day-pooled"
    threshold = "confirm: slope t >= 2 with mean directional excess > 0; reject: slope t <= -2"
    reading = ("Choppy profile read as the recorded regime 'unknown' (the only regime with a strategy) and the "
               "expected side as the sign of the raw swing-scaled return; normal drift is each coin's mean "
               "non-overlapping 5-bar return over all its windows; same-day cases are pooled by averaging their "
               "forecast and excess return, the slope t is the ordinary OLS t on those daily points, the supporting "
               "mean is over all cases, and the plan's under-100 grid-days rule is applied as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "grid days": None},
            "decided_by": ("Fewer than 90% of nonzero-forecast bars are in the choppy profile (regime 'unknown') "
                           "with the forecast's sign equal to the swing-scaled return's sign."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            days = ts.dt.floor("D").values
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if f[i] != 0:
                    coin_cases.append((days[i], f[i], r))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for d, fc, r in coin_cases:
            rows.append((d, fc, r - drift))

    n_cases = len(rows)
    if n_cases > 0:
        cases = pd.DataFrame(rows, columns=["day", "f", "ex"])
        daily = cases.groupby("day").agg(f=("f", "mean"), ex=("ex", "mean"))
        n_days = int(len(daily))
        dir_mean = float(np.mean(np.sign(cases["f"].values) * cases["ex"].values))
    else:
        daily = None
        n_days = 0
        dir_mean = None

    counts = {"independent cases (grid days) in the choppy profile": n_days, "cases": int(n_cases)}

    slope, t = None, None
    if daily is not None and n_days >= 3:
        x = daily["f"].values.astype(float)
        y = daily["ex"].values.astype(float)
        sxx = np.sum((x - x.mean()) ** 2)
        if sxx > 0:
            slope = float(np.sum((x - x.mean()) * (y - y.mean())) / sxx)
            resid = y - (y.mean() + slope * (x - x.mean()))
            s2 = np.sum(resid ** 2) / (n_days - 2)
            se = np.sqrt(s2 / sxx)
            t = float(slope / se) if se > 0 else None

    supp_passed = None if dir_mean is None else bool(dir_mean > 0)
    supporting = {"name": "mean excess 5-bar return in the forecast's direction", "value": dir_mean,
                  "passed": supp_passed}
    stat = {"name": "OLS slope t (day-pooled)", "value": t} if t is not None else None

    if n_days < 100:
        status = "not observable"
        decided = f"Only {n_days} independent cases (grid days) in the choppy profile, fewer than the plan's 100."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no spread in the forecast), so neither rule is met."
    elif t >= 2 and supp_passed:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess return in the forecast's direction is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger swing-scaled moves are followed by more reversal."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the mean in the forecast's direction is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": slope, "statistic": stat, "threshold": threshold},
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
