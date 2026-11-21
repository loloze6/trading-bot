import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.vs_fall.last_history_value"

    # ---------- 1. Situation check ----------
    # The plan's situation is a 1-bar fall, measured in units of the 20-day volatility.
    # The side it expects is long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            ret1 = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # When the raw value is missing, take the sign of the fall from the prices.
            fall_val = raw.where(raw.notna(), ret1)
            active = fc.notna() & (fc != 0)
            situ = fall_val < 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "one-sample t of mean excess next-day return on bars with forecast >= 5"
    thr = "confirm if t >= 2 with >= 30 cases and convexity check passes; reject if t <= -2 with >= 30 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are 1-bar falls "
                          "(raw vol-scaled return < 0) with a long forecast, which the plan's Fidelity says they must be.",
            "reading": "The situation is taken as the raw vol-scaled 1-bar return < 0, and the 1-bar price return "
                       "is used where the raw value is not recorded.",
        }

    # ---------- 2. Criterion ----------
    hi_ex, hi_fc, lo_ex, lo_fc = [], [], [], []
    for coin, wins in bars.items():
        # The coin's mean daily return over all its windows, never across a window boundary.
        all_r = []
        per_win = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fwd = close.shift(-1) / close - 1.0
            all_r.append(fwd.dropna().values)
            per_win.append((pd.to_numeric(df["forecast"], errors="coerce"), fwd))
        allr = np.concatenate(all_r) if all_r else np.array([])
        if allr.size == 0:
            continue
        mu = float(np.mean(allr))
        for fc, fwd in per_win:
            ok = fc.notna() & fwd.notna()
            ex = (fwd - mu)[ok]
            f = fc[ok]
            hi = f >= 5
            lo = (f > 0) & (f < 5)
            hi_ex.extend(ex[hi].tolist())
            hi_fc.extend(f[hi].tolist())
            lo_ex.extend(ex[lo].tolist())
            lo_fc.extend(f[lo].tolist())

    hi_ex = np.array(hi_ex, dtype=float)
    hi_fc = np.array(hi_fc, dtype=float)
    lo_ex = np.array(lo_ex, dtype=float)
    lo_fc = np.array(lo_fc, dtype=float)
    n_hi = int(hi_ex.size)
    n_lo = int(lo_ex.size)

    mean_hi = float(np.mean(hi_ex)) if n_hi > 0 else None
    t = None
    if n_hi >= 2:
        sd = float(np.std(hi_ex, ddof=1))
        if sd > 0:
            t = float(mean_hi / (sd / np.sqrt(n_hi)))

    per_hi = float(np.mean(hi_ex) / np.mean(hi_fc)) if n_hi > 0 and np.mean(hi_fc) != 0 else None
    per_lo = float(np.mean(lo_ex) / np.mean(lo_fc)) if n_lo > 0 and np.mean(lo_fc) != 0 else None
    if per_hi is not None and per_lo is not None:
        sup_val = float(per_hi - per_lo)
        sup_pass = bool(per_hi > per_lo)
    else:
        sup_val = None
        sup_pass = None

    if n_hi < 30:
        status = "not observable"
        decided = (f"Only {n_hi} bars have a forecast of 5 or more, "
                   "fewer than the plan's minimum of 30 cases.")
    elif t is None:
        status = "inconclusive"
        decided = "The main t could not be computed (zero dispersion), so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The main t is 2 or more with at least 30 cases, and the convexity check passes."
    elif t <= -2:
        status = "rejected"
        decided = "The main t is -2 or less with at least 30 cases."
    elif t >= 2:
        status = "inconclusive"
        decided = "The main t is 2 or more, but the convexity check fails."
    else:
        status = "inconclusive"
        decided = "The main t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_hi,
            "statistic": {"name": "one-sample t of the mean", "value": t} if t is not None else None,
            "threshold": thr,
        },
        "supporting_check": {
            "name": "per-unit-forecast mean excess return, group >= 5 minus group 0 < f < 5",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {
            "bars with forecast >= 5": n_hi,
            "bars with forecast between 0 and 5": n_lo,
        },
        "decided_by": decided,
        "reading": ("The per-unit-forecast return of each group is taken as the group's mean excess return divided "
                    "by its mean forecast; 'between 0 and 5' is read as 0 < forecast < 5; every bar is a case, "
                    "since the 1-bar horizon grid holds every bar; and the coin's mean is that of all its "
                    "within-window daily returns."),
    }
