import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    RAW = "debug_info.components.scaled_rise.last_history_value"
    PROFILE_REGIME = "unknown"  # the only regime with a strategy: no veto fired = falling calm profile

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            ret14 = close / close.shift(14) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # the coin rose over 14 days: raw scaled return > 0 (its sign is the 14-day return's sign);
            # where not recorded, recomputed from prices
            rose = np.where(raw.notna(), raw > 0, ret14 > 0)
            in_profile = (df["regime"].astype(str) == PROFILE_REGIME).values
            active = (fc != 0).values
            ok = active & in_profile & rose & (fc > 0).values
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    sit = {"agreement": agreement, "passed": passed}

    main_name = "mean 7-bar excess return of forecast>0 cases over the coin's mean 7-bar return"
    thr = "confirm: mean > 0 with t >= 2 and slope > 0; reject: t <= -2; else inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of a coin that rose "
                           "over 14 days inside the falling calm profile (regime 'unknown'), so the config does "
                           "not do what the Fidelity says." if n_active > 0 else
                           "The record has no bar with a non-zero forecast, so the situation cannot be checked."),
            "reading": "Situation = regime 'unknown' (no profile veto fired) and the raw scaled 14-day return > 0, side long.",
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, forecast, fwd_ret)
    coin_grid_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                allr.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    cases.append((coin, ts[i].strftime("%Y-%m-%d"), float(fc[i]), r))
        coin_grid_rets[coin] = float(np.mean(allr)) if allr else np.nan

    rows = [(c, d, f, r - coin_grid_rets[c]) for (c, d, f, r) in cases if np.isfinite(coin_grid_rets[c])]
    n_cases = len(rows)
    days = sorted(set(r[1] for r in rows))
    n_days = len(days)
    counts = {"independent cases (days)": int(n_days), "cases": int(n_cases)}

    mean_ex = None
    t_val = None
    slope = None
    if n_cases > 0:
        ex = np.array([r[3] for r in rows])
        fcs = np.array([r[2] for r in rows])
        mean_ex = float(ex.mean())
        dev = pd.Series(ex - mean_ex).groupby([r[1] for r in rows]).sum().values
        if n_days > 1:
            se = np.sqrt(n_days / (n_days - 1) * np.sum(dev ** 2)) / n_cases
            t_val = float(mean_ex / se) if se > 0 else None
        if n_cases > 1 and np.std(fcs) > 0:
            slope = float(stats.linregress(fcs, ex).slope)

    stat = {"name": "t of the mean, cases of one day pooled (day-clustered)", "value": t_val} if t_val is not None else None
    slope_pass = None if slope is None else bool(slope > 0)
    supp = {"name": "OLS slope of 7-bar excess return on forecast", "value": slope, "passed": slope_pass}
    mm = {"name": main_name, "value": mean_ex, "statistic": stat, "threshold": thr}

    reading = ("Cases are grid bars (positions 0,7,14,... of each window, with a full 7-bar forward return inside it) "
               "with forecast > 0; the coin's mean 7-bar return is taken on the same grid over all its windows; the t "
               "sums each day's case deviations into one (day-clustered standard error); the plan's 'fewer than 30 "
               "days' rule is applied as the minimum count, giving 'not observable'.")

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} independent days of cases, below the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean excess return could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val <= -2:
        status = "rejected"
        decided = "The mean excess return has t <= -2 (reject rule)."
    elif mean_ex > 0 and t_val >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "The mean excess return is above 0 with t >= 2 and the slope on the forecast is positive (confirm rule)."
        else:
            status = "inconclusive"
            decided = "A confirming t with a slope at or below 0 (or not computable) is inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": mm,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
