import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 4
    BAND = 2.0
    RAW = "debug_info.components.vol_surge_up.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            ret = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # situation: an up hour with traded volume, i.e. raw graded product > 0
            # (recomputed from the price where the raw value is missing)
            vol = pd.to_numeric(df["volume"], errors="coerce")
            sit_price = (ret > 0) & (vol > 0)
            sit = np.where(raw.notna(), raw > 0, sit_price)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & pd.Series(sit, index=df.index) & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean excess 4-bar return per bet case (coin drift removed)"
    thr = "confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading = ("Situation bars are those whose raw component value is positive (an up hour on traded volume), "
               "long side; a bet is a rise of a positive forecast of at least 2 points from its lowest positive level "
               "since the last bet (from 0 after a flat), the first bet bar of each non-overlapping 4-bar cell counted "
               "from each window's first row is the case, cells whose signal bar lacks 4 later bars in the window are "
               "left out, and the coin's drift is the mean 4-bar return on the same grid over all its windows.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are up hours with a long forecast, "
                           "so the config does not trade the plan's heavy-volume up-surge situation on the long side."
                           if n_active > 0 else "The record has no active bar, so the config never takes the plan's position."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    excess_all = []
    weights_all = []
    for coin, wins in bars.items():
        # coin's normal drift: mean non-overlapping 4-bar return over all windows
        grid_rets = []
        per_window = {}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for t in range(0, n - H, H):
                r = close[t + H] / close[t] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            per_window[w] = df
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in per_window.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                fi = f[i]
                if not np.isfinite(fi) or fi <= 0:
                    ref = 0.0
                    continue
                if fi - ref >= BAND:
                    bet[i] = True
                    ref = fi
                else:
                    ref = min(ref, fi)
            for c0 in range(0, n, H):
                idx = np.where(bet[c0:c0 + H])[0]
                if len(idx) == 0:
                    continue
                t = c0 + int(idx[0])
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r):
                    continue
                excess_all.append(r - drift)
                weights_all.append(f[t])

    ex = np.asarray(excess_all, dtype=float)
    wt = np.asarray(weights_all, dtype=float)
    n_cases = int(len(ex))

    mean_ex = float(np.mean(ex)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(ex, ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n_cases)))
    wmean = None
    if n_cases > 0 and np.sum(wt) > 0:
        wmean = float(np.sum(ex * wt) / np.sum(wt))
    sup_pass = (wmean > 0) if wmean is not None else None

    main = {"name": main_name, "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": t_stat} if t_stat is not None else None),
            "threshold": thr}
    sup = {"name": "forecast-weighted mean excess 4-bar return > 0", "value": wmean, "passed": sup_pass}

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases across both coins and all windows, below the plan's minimum of 30."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean cannot be computed (no spread in excess returns), so neither rule is met."
    elif mean_ex > 0 and t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean excess 4-bar return is positive with t >= 2 over at least 30 cases and the forecast-weighted mean is above 0."
    elif mean_ex < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean excess 4-bar return is negative with t <= -2 over at least 30 cases."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check (forecast-weighted mean above 0) fails."
    else:
        status = "inconclusive"
        decided = "-2 < t < 2 over at least 30 cases: neither the confirm nor the reject rule is met."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
