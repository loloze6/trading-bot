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
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")

            # Situation from the components' raw values where they are recorded
            slow = pd.to_numeric(df[SLOW], errors="coerce") if SLOW in df.columns else pd.Series(np.nan, index=df.index)
            med = pd.to_numeric(df[MED], errors="coerce") if MED in df.columns else pd.Series(np.nan, index=df.index)

            # Where a value is missing, recompute the return from prices inside the window
            r60 = close / close.shift(60) - 1.0
            r20 = close / close.shift(20) - 1.0
            slow = slow.where(slow.notna(), r60)
            med = med.where(med.notna(), r20)

            # Where neither is available, fall back on the detector's own label
            reg_trend = (df["regime"].astype(str) == "trending") if "regime" in df.columns else pd.Series(False, index=df.index)
            known = slow.notna() & med.notna()
            situation = pd.Series(False, index=df.index)
            situation[known] = (slow[known] > 0) & (med[known] > 0)
            situation[~known] = reg_trend[~known]

            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of mean 20-bar forward excess return (vs coin mean) on active bars, non-overlapping, pooled"
    threshold = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; inconclusive otherwise or if fewer than 30 blocks"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are long bars where both the 60-bar and 20-bar returns are above 0, as the Fidelity's situation requires.",
            "reading": "Situation taken from the slow/medium last_history_value columns, recomputed from in-window prices where missing, and from the regime label where neither is available.",
        }

    # ---------- 2. Criterion ----------
    excess_all = []
    fc_all = []
    for coin, wins in bars.items():
        # coin's mean 20-bar return over all windows pooled (every bar with a valid forward return)
        fwd_list = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            fwd = close.shift(-H) / close - 1.0
            fwd_list.append(fwd.dropna().values)
        allf = np.concatenate(fwd_list) if fwd_list else np.array([])
        if len(allf) == 0:
            continue
        coin_mean = float(np.mean(allf))

        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").reset_index(drop=True)
            fwd = close.shift(-H) / close - 1.0
            grid = np.arange(0, len(df), H)
            for i in grid:
                f = fc.iloc[i]
                r = fwd.iloc[i]
                if pd.notna(f) and f > 0 and pd.notna(r):
                    excess_all.append(float(r - coin_mean))
                    fc_all.append(float(f))

    ex = np.array(excess_all)
    fcv = np.array(fc_all)
    n = int(len(ex))

    mean_ex = float(np.mean(ex)) if n > 0 else None
    t = None
    if n >= 2:
        sd = float(np.std(ex, ddof=1))
        t = float(mean_ex / (sd / np.sqrt(n))) if sd > 0 else (float(np.sign(mean_ex) * np.inf) if mean_ex != 0 else 0.0)

    slope = None
    slope_pass = None
    if n >= 3 and np.std(fcv) > 0:
        slope = float(stats.linregress(fcv, ex).slope)
        slope_pass = bool(slope > 0)

    counts = {"non-overlapping 20-bar active blocks": n}

    if n < 30:
        status = "not observable"
        decided = "Fewer than 30 non-overlapping 20-bar active blocks pooled across coins and windows, below the plan's minimum."
    elif mean_ex > 0 and t >= 2:
        status = "confirmed"
        decided = "The mean 20-bar excess return on active bars is above 0 with t >= 2."
    elif mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "The mean 20-bar excess return on active bars is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2, meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "OLS slope of 20-bar excess return on forecast level (active, non-overlapping)",
            "value": slope,
            "passed": slope_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "The coin's mean 20-bar return uses every bar's in-window 20-bar forward return across all its windows (overlapping), active blocks are grid bars 0, 20, 40, ... of each window with forecast > 0 and a full 20-bar forward return, and the supporting slope is reported but not used in the decision rule.",
    }
