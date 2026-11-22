import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 6
    BAND = 2.0
    RISE = "debug_info.components.rise.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            active = f != 0
            if not active.any():
                continue
            reg = df["regime"].astype(str).values
            gate = reg == "mean_reversion"  # detector's decision: volume ratio 0.5..1.5 of its 720-bar mean
            if RISE in df.columns:
                rise = pd.to_numeric(df[RISE], errors="coerce").values
            else:
                rise = np.full(len(df), np.nan)
            up = np.where(np.isnan(rise), False, rise > 0)
            sit = gate & up & (f < 0)
            n_active += int(active.sum())
            n_agree += int((active & sit).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The volume gate is read from the recorded regime (mean_reversion = volume ratio 0.5 to 1.5, the detector's "
               "components are not recorded) and an up-hour as rise last_history_value > 0; a case is the first short bet "
               "(the forecast's magnitude rising by >= 2 points from its lowest short level since the last bet, from 0 after "
               "a flat) in each 6-bar grid cell of a window with a full 6-bar return inside the window; the median split "
               "puts |forecast| above the median in the larger half and the rest in the smaller half; the plan's "
               "'fewer than 100 independent cases' minimum is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "independent cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars after an up-hour in the "
                           "quiet-volume regime, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    gives = []
    sizes = []
    counts_by_coin = {}
    for coin, wins in bars.items():
        # normal 6-bar drift over all windows (non-overlapping grid)
        drift_samples = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    drift_samples.append(c[i + H] / c[i] - 1.0)
        drift = float(np.mean(drift_samples)) if drift_samples else np.nan

        ncoin = 0
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(f)
            bet = np.zeros(n, dtype=bool)
            anchor = 0.0
            for i in range(n):
                if f[i] < 0:
                    m = -f[i]
                    if m - anchor >= BAND:
                        bet[i] = True
                        anchor = m
                    else:
                        anchor = min(anchor, m)
                else:
                    anchor = 0.0
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0) or not np.isfinite(drift):
                    continue
                r = c[t + H] / c[t] - 1.0
                gives.append(-(r - drift))
                sizes.append(abs(f[t]))
                ncoin += 1
        counts_by_coin[coin] = ncoin

    gives = np.array(gives, dtype=float)
    sizes = np.array(sizes, dtype=float)
    n_cases = int(len(gives))

    mean_g = float(np.mean(gives)) if n_cases > 0 else None
    t_g = None
    if n_cases > 1:
        sd = float(np.std(gives, ddof=1))
        t_g = float(mean_g / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    diff = None
    if n_cases >= 2:
        med = float(np.median(sizes))
        large = gives[sizes > med]
        small = gives[sizes <= med]
        if len(large) > 0 and len(small) > 0:
            diff = float(np.mean(large) - np.mean(small))
    check_pass = None if diff is None else bool(diff > 0)

    counts = {"independent cases across both coins": n_cases}
    for k, v in counts_by_coin.items():
        counts["cases " + str(k)] = int(v)

    if n_cases < 100 or t_g is None:
        status = "not observable"
        decided = f"Only {n_cases} independent cases across both coins, below the plan's minimum of 100."
    elif mean_g > 0 and t_g >= 2 and check_pass:
        status = "confirmed"
        decided = "Mean 6-bar giveback above 0 with t >= 2 and the larger-half minus smaller-half difference above 0."
    elif t_g >= 2:
        status = "inconclusive"
        decided = "Main t >= 2 but the larger-half minus smaller-half difference is <= 0, which the plan calls inconclusive."
    elif mean_g < 0 and t_g <= -2:
        status = "rejected"
        decided = "Mean giveback below 0 with t <= -2: the price continues upward after quiet-volume rises."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean 6-bar giveback after short bets, drift removed, signed short, before costs",
            "value": mean_g,
            "statistic": None if t_g is None else {"name": "t of the mean", "value": t_g},
            "threshold": "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "giveback of larger-|forecast| half minus smaller half",
            "value": diff,
            "passed": check_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
