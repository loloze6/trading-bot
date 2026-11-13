import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    SLOW = "debug_info.components.slow.last_history_value"
    MED = "debug_info.components.medium.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if not active.any():
                continue
            r60 = pd.to_numeric(df[SLOW], errors="coerce") if SLOW in df.columns else pd.Series(np.nan, index=df.index)
            r20 = pd.to_numeric(df[MED], errors="coerce") if MED in df.columns else pd.Series(np.nan, index=df.index)
            have = r60.notna() & r20.notna()
            sit_raw = (r60 > 0) & (r20 > 0)
            # Where the raw values are missing, fall back to the detector's decision.
            sit_reg = df["regime"].astype(str).eq("trending") if "regime" in df.columns else pd.Series(False, index=df.index)
            sit = sit_raw.where(have, sit_reg)
            ok = active & sit.astype(bool) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean 20-bar forward excess return over coin mean, active bars, non-overlapping"
    threshold = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; else inconclusive; at least 30 non-overlapping active blocks"
    reading = ("The coin's mean 20-bar return is taken over every bar of all its windows (overlapping, within windows); "
               "the active blocks are the active bars (forecast > 0) on the grid 0, 20, 40, ... of each window; "
               "the situation is checked on the raw slow/medium returns, using the regime label where they are missing.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars where both the 60-bar "
                           "and 20-bar returns are positive, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    excess = []
    fcs = []
    for coin, wins in bars.items():
        # coin mean 20-bar return across all its windows
        allr = []
        frames = {}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fwd = close.shift(-H) / close - 1.0
            frames[w] = (df, fwd)
            allr.append(fwd.dropna().values)
        allr = np.concatenate(allr) if allr else np.array([])
        if allr.size == 0:
            continue
        cmean = float(np.mean(allr))
        for w, (df, fwd) in frames.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            idx = np.arange(0, len(df), H)
            for i in idx:
                f = fc.iloc[i]
                r = fwd.iloc[i]
                if pd.notna(f) and f > 0 and pd.notna(r):
                    excess.append(float(r) - cmean)
                    fcs.append(float(f))

    excess = np.array(excess)
    fcs = np.array(fcs)
    n = int(excess.size)
    counts = {"non-overlapping 20-bar active blocks": n}

    mean_ex = float(np.mean(excess)) if n > 0 else None
    tval = None
    if n > 1:
        sd = float(np.std(excess, ddof=1))
        if sd > 0:
            tval = float(mean_ex / (sd / np.sqrt(n)))

    slope = None
    sup_pass = None
    if n > 2 and np.std(fcs) > 0:
        slope = float(stats.linregress(fcs, excess).slope)
        sup_pass = bool(slope > 0)

    if n < 30:
        status = "not observable"
        decided = f"Only {n} non-overlapping 20-bar active blocks, fewer than the plan's minimum of 30."
    elif tval is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (zero dispersion), so neither confirm nor reject is met."
    elif mean_ex > 0 and tval >= 2:
        status = "confirmed"
        decided = "The mean 20-bar excess return on active bars is above 0 with t >= 2."
    elif mean_ex < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean 20-bar excess return on active bars is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2, meeting the plan's inconclusive rule."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": tval} if tval is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "slope of 20-bar excess return on forecast level (non-overlapping active blocks)",
            "value": slope,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
