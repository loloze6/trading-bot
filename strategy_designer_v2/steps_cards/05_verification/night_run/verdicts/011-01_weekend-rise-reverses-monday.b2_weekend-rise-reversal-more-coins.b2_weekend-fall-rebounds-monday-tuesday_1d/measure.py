import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.weekend_fall.last_history_value"
    H = 2
    MIN_CASES = 100

    # ---------- coin mean daily return over all windows together ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            r = (c / c.shift(1) - 1).iloc[1:]
            rets.append(r.dropna())
        if rets:
            allr = pd.concat(rets)
            coin_mu[coin] = float(allr.mean()) if len(allr) else np.nan
        else:
            coin_mu[coin] = np.nan

    # ---------- situation check and case collection ----------
    n_active = 0
    n_agree = 0
    case_vals = []
    case_excess = []
    case_fc = []

    for coin, wins in bars.items():
        mu = coin_mu.get(coin, np.nan)
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            # coming bar is Monday: bar start + 1 day falls on weekday 0
            next_is_monday = ((ts + pd.Timedelta(days=1)).dt.weekday == 0).values
            ret1_price = (close / close.shift(1) - 1).values
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").values
                ret1 = np.where(np.isnan(raw), ret1_price, raw)
            else:
                ret1 = ret1_price

            n = len(d)
            for i in range(n):
                f = float(fc.iloc[i])
                if f != 0:
                    n_active += 1
                    r = ret1[i]
                    if next_is_monday[i] and not np.isnan(r) and r < 0 and f > 0:
                        n_agree += 1
                # cases: Sunday bars with forecast > 0, 2-bar return inside window
                if f > 0 and next_is_monday[i] and i + H < n:
                    c0 = close.iloc[i]
                    c2 = close.iloc[i + H]
                    if pd.isna(c0) or pd.isna(c2) or c0 == 0 or np.isnan(mu):
                        continue
                    ex = c2 / c0 - 1 - H * mu
                    case_excess.append(float(ex))
                    case_fc.append(f)
                    case_vals.append(f / 10.0 * float(ex))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean position-weighted 2-bar excess return after weekend fall"
    threshold = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; at least 100 cases"
    sup_name = "OLS slope of excess 2-bar return on forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": int(len(case_vals))},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are Sunday bars (coming bar Monday) after a weekend fall with a long forecast, as the plan's situation requires.",
            "reading": "Sunday bar = bar whose start + 1 day is a Monday; weekend fall = raw period-1 return (last_history_value, else close-to-close) strictly below 0; expected side long.",
        }

    n_cases = len(case_vals)
    vals = np.array(case_vals, dtype=float)
    mean_v = float(vals.mean()) if n_cases > 0 else None
    t_v = None
    if n_cases > 1:
        sd = vals.std(ddof=1)
        if sd > 0:
            t_v = float(mean_v / (sd / np.sqrt(n_cases)))
    slope = None
    if n_cases > 2 and np.ptp(np.array(case_fc)) > 0:
        slope = float(stats.linregress(np.array(case_fc), np.array(case_excess)).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, below the plan's minimum of 100 cases across all coins and windows."
    elif t_v is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed, so neither confirm nor reject rule is met."
    elif mean_v > 0 and t_v >= 2 and slope_pass:
        status = "confirmed"
        decided = "Mean position-weighted excess return is positive with t >= 2 and the regression slope is above 0."
    elif mean_v < 0 and t_v <= -2:
        status = "rejected"
        decided = "Mean position-weighted excess return is negative with t <= -2."
    elif t_v >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope is 0 or below (or undefined), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_v,
            "statistic": None if t_v is None else {"name": "ordinary t of the mean", "value": t_v},
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": slope, "passed": slope_pass},
        "counts": {"cases": int(n_cases), "active bars": int(n_active)},
        "decided_by": decided,
        "reading": "Cases are all bars whose coming bar is Monday with forecast > 0 and close[t+2] in the same window (one per coin per week by construction), the coin mean daily return is pooled over all its windows, the slope is an OLS of the unweighted excess 2-bar return on forecast, and the plan's 'fewer than 100 cases' rule is reported as not observable.",
    }
