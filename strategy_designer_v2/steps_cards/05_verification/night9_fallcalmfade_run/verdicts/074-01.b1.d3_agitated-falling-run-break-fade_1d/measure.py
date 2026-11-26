import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.run_depth.last_history_value"

    # ---------- coin mean daily return over all windows ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            r = c[1:] / c[:-1] - 1.0
            rets.append(r[np.isfinite(r)])
        rets = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(rets)) if len(rets) else np.nan

    # ---------- situation check and case collection ----------
    n_active = 0
    n_agree = 0
    case_vals, case_absf, case_days = [], [], []

    for coin, wins in bars.items():
        mu = coin_mu.get(coin, np.nan)
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            reg = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))
            raw = (pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
                   if RAW in df.columns else np.full(len(df), np.nan))
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            n = len(df)

            for t in range(n):
                if f[t] == 0 or not np.isfinite(f[t]):
                    continue
                n_active += 1
                # run break from prices: up close after >= 2 down closes
                if t >= 3 and np.all(np.isfinite(c[t - 3:t + 1])):
                    run_break = (c[t] > c[t - 1]) and (c[t - 1] < c[t - 2]) and (c[t - 2] < c[t - 3])
                else:
                    # not enough in-window history: fall back on the recorded run-depth raw value
                    run_break = bool(np.isfinite(raw[t]) and raw[t] > 0)
                # falling agitated profile: the detector's decision (vetoes give "chop")
                profile_ok = reg[t] == "mean_reversion"
                if run_break and profile_ok and f[t] < 0:
                    n_agree += 1

                # case for the main measure: next-day return inside the window
                if t + 1 < n and np.isfinite(c[t]) and np.isfinite(c[t + 1]) and np.isfinite(mu):
                    r = c[t + 1] / c[t] - 1.0
                    case_vals.append(-(r - mu))
                    case_absf.append(abs(f[t]))
                    case_days.append(ts.iloc[t].floor("D") if pd.notna(ts.iloc[t]) else pd.NaT)

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    reading = ("The run break is recomputed from in-window closes (up close after at least two down closes, "
               "falling back on a positive recorded run_depth raw value on the first three bars of a window) and the "
               "falling-agitated profile is read from the recorded regime being 'mean_reversion' since the 365-day "
               "volatility percentile cannot be rebuilt from ~120-bar windows; the main value is the mean per case, "
               "its t is the ordinary t of the per-day sums, and the slope is an OLS of per-case short-signed excess "
               "on absolute forecast.")

    main_name = "mean next-day short-signed excess return on nonzero-forecast bars"
    threshold = "confirm: mean > 0 with t >= 2 and slope > 0; reject: t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": (f"Only {agreement:.1%} of active bars are short forecasts on run-break bars inside the "
                           "falling-agitated profile, below the 90% the plan's situation requires."),
            "reading": reading,
        }

    vals = np.array(case_vals, dtype=float)
    absf = np.array(case_absf, dtype=float)
    days = pd.Series(case_days)
    ok = np.isfinite(vals) & days.notna().to_numpy()
    vals, absf, days = vals[ok], absf[ok], days[ok].reset_index(drop=True)

    n_cases = int(len(vals))
    n_days = int(days.nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_case = float(np.mean(vals)) if n_cases else None
    t_val = None
    if n_days >= 2:
        day_sums = pd.Series(vals).groupby(days.values).sum().to_numpy(dtype=float)
        sd = np.std(day_sums, ddof=1)
        if sd > 0:
            t_val = float(np.mean(day_sums) / (sd / np.sqrt(len(day_sums))))
        else:
            t_val = 0.0

    slope = None
    if n_cases >= 3 and np.unique(absf).size >= 2:
        slope = float(stats.linregress(absf, vals).slope)
    slope_passed = None if slope is None else bool(slope > 0)

    main = {"name": main_name, "value": mean_case,
            "statistic": None if t_val is None else {"name": "t of the mean (cases summed per day)", "value": t_val},
            "threshold": threshold}
    supp = {"name": "OLS slope of short-signed excess on |forecast|", "value": slope, "passed": slope_passed}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = (f"The plan's minimum of 30 cases on 30 distinct days is not reached "
                   f"({n_cases} cases, {n_days} days).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and mean_case is not None and mean_case > 0 and slope_passed:
        status = "confirmed"
        decided = "The mean short-signed excess return is above 0 with t >= 2 and the supporting slope is above 0."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The t is >= 2 but the supporting slope is not above 0, which the plan calls inconclusive."
    elif t_val <= -2:
        status = "rejected"
        decided = "The mean short-signed excess return has t <= -2: the day after a run break rises more than usual."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
