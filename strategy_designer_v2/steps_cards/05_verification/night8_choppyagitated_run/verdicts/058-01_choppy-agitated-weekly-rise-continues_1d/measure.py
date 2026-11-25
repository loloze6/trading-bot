import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    RAW = "debug_info.components.scaled_rise.last_history_value"
    PROFILE_REGIME = "unknown"  # the only regime with a strategy; the vetoes send bars outside the profile to "chop"

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
            # 7-day return as rise: from the raw value when recorded, else from prices within the window
            ret7 = close / close.shift(H) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            rise = pd.Series(np.where(raw.notna(), raw > 0, ret7 > 0), index=df.index)
            in_profile = df["regime"].astype(str) == PROFILE_REGIME
            situation = in_profile & rise
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    main_name = "mean excess 7-bar forward return of grid cases with forecast > 0 (vs coin's mean 7-bar return)"
    threshold = "confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2"
    sup_name = "Spearman correlation between forecast and excess 7-bar return"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("fewer than 90% of the active bars (forecast != 0) are long bars inside the choppy "
                           "agitated profile (regime 'unknown') with a positive 7-day return"
                           if n_active > 0 else "no active bar in the record"),
            "reading": "the profile is read from the recorded regime ('unknown' = inside the profile), the rise from the raw component value's sign (prices when not recorded).",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_grid_rets = []
        coin_cases = []
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
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                coin_grid_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    coin_cases.append((fc[i], r, ts.iloc[i].strftime("%Y-%m-%d")))
        if len(coin_grid_rets) == 0:
            continue
        drift = float(np.mean(coin_grid_rets))
        for f, r, d in coin_cases:
            rows.append({"coin": coin, "forecast": f, "excess": r - drift, "day": d})

    cases = pd.DataFrame(rows, columns=["coin", "forecast", "excess", "day"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"grid cases": n_cases, "distinct days": n_days}

    mean_ex = float(cases["excess"].mean()) if n_cases else None
    t = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["excess"] - mean_ex
        S = dev.groupby(cases["day"]).sum().values
        D = len(S)
        var = (D / (D - 1)) * float(np.sum(S ** 2)) / (n_cases ** 2)
        se = np.sqrt(var)
        t = float(mean_ex / se) if se > 0 else None
    rho = None
    if n_cases >= 3:
        rr = stats.spearmanr(cases["forecast"].values, cases["excess"].values)
        rv = float(rr.correlation if hasattr(rr, "correlation") else rr[0])
        rho = rv if np.isfinite(rv) else None
    sup_pass = None if rho is None else bool(rho > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"fewer than 30 grid cases ({n_cases})."
    elif n_days < 30:
        status = "not observable"
        decided = f"the cases fall on fewer than 30 distinct days ({n_days})."
    elif t is not None and mean_ex > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "mean excess 7-bar return positive with t >= 2 and Spearman correlation above 0."
    elif t is not None and mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "mean excess 7-bar return negative with t <= -2."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the Spearman correlation is 0 or below."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {"name": main_name, "value": mean_ex,
                         "statistic": None if t is None else {"name": "t of the mean, cases of one day taken together", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": rho, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("grid bars at positions 0,7,14,... of each window with a full 7-bar forward return inside the window; "
                    "the coin's mean 7-bar return is the mean over that grid of all its windows; the day-clustered t uses "
                    "per-day sums of deviations with a D/(D-1) correction; minimum counts are reported as 'not observable'."),
    }
