import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.dryup_moderation.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            # falling profile: 60-bar price evolution (percent) below -10;
            # where 60 past bars are not in the window, the detector's decision
            evo = (close / close.shift(60) - 1.0) * 100.0
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            falling = np.where(evo.notna(), evo < -10.0, reg != "chop")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series([np.nan] * len(df))
            dry = (raw > 0).fillna(False).values
            active = (fc != 0).values
            ok = active & falling & dry & (fc < 0).values
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean unusual 5-day move of the short cases, drift removed"
    main_thr = "confirm: mean > 0 with t >= 2 over at least 30 cases; reject: mean < 0 with t <= -2 over at least 30 cases"
    sup_name = "mean unusual move, cases with |forecast| above median minus below median"
    reading = ("Falling profile taken as the 60-bar price evolution in percent below -10 (the detector's regime "
               "where 60 past bars are not in the window) and the dry-up as a raw component value above 0; "
               "a case is the first bet (short forecast rising at least 2 points from its lowest level since "
               "the last bet, from 0 after flat) in each 5-bar grid cell from each window's first row, cases "
               "without 5 bars ahead in the window are dropped, the drift is the coin's mean non-overlapping "
               "5-bar return over all windows, the day-clustered t uses summed deviations per day with a "
               "D/(D-1) correction, and cases with |forecast| equal to the median are in neither group.")

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars inside the falling "
                           "profile with volume dried up, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, timestamp, ret, |forecast|)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(df)
            for i in range(0, n - H, H):
                if np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0:
                    grid_rets.append(close[i + H] / close[i] - 1.0)
            # bets on the short side
            ref = 0.0
            bets = np.zeros(n, dtype=bool)
            for t in range(n):
                s = -fc[t] if fc[t] < 0 else 0.0
                if s <= 0:
                    ref = 0.0
                    continue
                if s - ref >= BAND:
                    bets[t] = True
                    ref = s
                else:
                    ref = min(ref, s)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for c0 in range(0, n, H):
                idx = np.where(bets[c0:c0 + H])[0]
                if len(idx) == 0:
                    continue
                t = c0 + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    continue
                cases.append((coin, ts.iloc[t], close[t + H] / close[t] - 1.0, abs(fc[t])))
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

    rows = [(c, tsv, -(r - drift[c]), a) for (c, tsv, r, a) in cases if np.isfinite(drift.get(c, np.nan))]
    n_cases = len(rows)
    if n_cases:
        u = np.array([r[2] for r in rows], dtype=float)
        absf = np.array([r[3] for r in rows], dtype=float)
        days = pd.Series([pd.Timestamp(r[1]).normalize() for r in rows])
        n_days = int(days.nunique())
    else:
        u = np.array([]); absf = np.array([]); n_days = 0

    mean_u = float(u.mean()) if n_cases else None
    t_stat = None
    if n_cases >= 2 and n_days >= 2:
        dev = pd.Series(u - u.mean()).groupby(days.values).sum().values
        var = (dev ** 2).sum() / n_cases ** 2 * (n_days / (n_days - 1))
        if var > 0:
            t_stat = float(mean_u / np.sqrt(var))

    diff = None
    if n_cases:
        med = np.median(absf)
        strong = u[absf > med]
        weak = u[absf < med]
        if len(strong) and len(weak):
            diff = float(strong.mean() - weak.mean())
    sup_passed = (diff > 0) if diff is not None else None

    counts = {"cases": int(n_cases), "days": n_days}
    stat = {"name": "t of the mean, cases of one day taken together", "value": t_stat} if t_stat is not None else None

    if n_cases < 30:
        status = "not observable"
        decided = f"Fewer than 30 cases ({n_cases}), the plan's minimum count, so the data cannot show the idea."
    elif t_stat is not None and mean_u > 0 and t_stat >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "Mean unusual move positive with t >= 2 over at least 30 cases and strong-minus-weak difference above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the strong-minus-weak difference is 0 or below (or not computable)."
    elif t_stat is not None and mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement) if agreement is not None else None, "passed": True},
        "main_measure": {"name": main_name, "value": mean_u, "statistic": stat, "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": diff,
                             "passed": bool(sup_passed) if sup_passed is not None else None},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
