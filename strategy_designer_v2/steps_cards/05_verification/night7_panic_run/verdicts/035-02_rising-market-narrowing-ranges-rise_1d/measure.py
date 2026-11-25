import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RAW = "debug_info.components.range_calm.last_history_value"
    PROFILE_REGIME = "unknown"  # the config's only strategy regime: not vetoed to chop by the 60-bar price evolution

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            reg = df["regime"].astype(str)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            in_sit = (reg == PROFILE_REGIME) & raw.notna() & np.isfinite(raw) & (raw > 0)
            agree = active & in_sit & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    reading = ("The rising-market profile is read from the recorded regime (the detector's decision, 'unknown' = not vetoed "
               "to chop), the situation also needs a recorded positive range ratio, the side is long; the coin's mean 3-day "
               "return uses the non-overlapping grid of all its bars in all windows; thirds are the lowest and highest "
               "floor(n/3) cases of the forecast pooled over all coins and windows (ties broken by record order); fewer "
               "than 100 cases in a third is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "Welch t of excess 3-day return, top third minus bottom third of forecast",
                             "value": None, "statistic": None,
                             "threshold": "confirm t >= 2 with top-third mean excess > 0; reject t <= -2"},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars inside the rising-market "
                           "profile with a recorded range ratio, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin mean 3-day return over all windows (non-overlapping grid)
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (forecast, excess)
    for coin in sorted(bars.keys()):
        wins = bars[coin]
        for w in sorted(wins.keys(), key=lambda s: (len(str(s)), str(s))):
            df = wins[w]
            if df is None or len(df) == 0 or not np.isfinite(coin_mean.get(coin, np.nan)):
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            reg = df["regime"].astype(str).to_numpy()
            for i in range(0, len(c) - H, H):
                if reg[i] != PROFILE_REGIME:
                    continue
                if not (np.isfinite(fc[i]) and fc[i] > 0):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                cases.append((float(fc[i]), r - coin_mean[coin]))

    n = len(cases)
    k = n // 3
    if k > 0:
        arr = np.array(cases)
        order = np.argsort(arr[:, 0], kind="stable")
        bottom = arr[order[:k], 1]
        top = arr[order[n - k:], 1]
    else:
        bottom = np.array([])
        top = np.array([])

    counts = {"grid cases": n, "top-third cases": int(len(top)), "bottom-third cases": int(len(bottom))}
    main_name = "Welch t of excess 3-day return, top third minus bottom third of forecast"
    threshold = "confirm t >= 2 with top-third mean excess > 0; reject t <= -2; at least 100 grid cases per third"

    if len(top) < 100 or len(bottom) < 100:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name,
                             "value": float(top.mean() - bottom.mean()) if k > 1 else None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "top-third mean excess 3-day return > 0",
                                 "value": float(top.mean()) if len(top) else None, "passed": None},
            "counts": counts,
            "decided_by": "The plan's minimum of 100 grid cases per third is not reached.",
            "reading": reading,
        }

    diff = float(top.mean() - bottom.mean())
    t = float(stats.ttest_ind(top, bottom, equal_var=False).statistic)
    top_mean = float(top.mean())
    sup_pass = bool(top_mean > 0)

    if t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Welch t >= 2 (top minus bottom) and the top-third mean excess 3-day return is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "Welch t <= -2: bottom-third cases rise more than top-third cases."
    elif t >= 2:
        status = "inconclusive"
        decided = "Welch t >= 2 but the supporting check (top-third mean excess above 0) fails."
    else:
        status = "inconclusive"
        decided = "Welch t is between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": diff,
                         "statistic": {"name": "Welch t", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": "top-third mean excess 3-day return > 0", "value": top_mean, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
