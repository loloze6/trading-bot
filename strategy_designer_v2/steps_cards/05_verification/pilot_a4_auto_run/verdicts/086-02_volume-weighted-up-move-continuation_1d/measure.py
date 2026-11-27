import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.up_volume.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            active = f != 0
            if not active.any():
                continue
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            in_profile = reg == "unknown"  # falling calm: neither veto (trend >= -10, swing > 0.5) fired
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            up_move = np.where(np.isnan(raw), False, raw > 0)
            situ = in_profile & up_move & (f > 0)
            n_active += int(active.sum())
            n_agree += int((situ & active).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean unusual 5-bar move of the signals (return minus normal 5-bar drift)"
    main_thr = "confirm: mean > 0 with t >= 2 (and supporting difference > 0); reject: mean < 0 with t <= -2"
    reading = ("The falling-calm profile is read from the recorded regime ('unknown' = no veto fired), since its "
               "components are not recorded and their 365-bar lookback cannot be rebuilt in a window, and an up day as "
               "a positive raw value; cases are the first long bet (forecast rise >= 2 points from its lowest level "
               "since the last bet, reset to 0 after a flat) in each 5-bar grid cell of each window with a 5-bar "
               "return inside the window, on every coin of the record; the day-clustered t sums the deviations per UTC "
               "day with a D/(D-1) correction; the median split excludes cases equal to the median; the plan's "
               "minimum of 30 cases on 30 days, when not reached, gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases": None, "distinct days": None},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are positive-forecast bars of an up "
                           "day inside the falling-calm profile, as the plan's situation and long side require."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_ret, case_coin, case_day, case_fc = [], [], [], []
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            days = ts.dt.strftime("%Y-%m-%d").values
            n = len(df)
            # normal drift grid
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    grid_rets.append(c1 / c0 - 1.0)
            # bets
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for t in range(n):
                ft = f[t]
                if ft <= 0:
                    ref = 0.0
                    continue
                if ft - ref >= BAND:
                    bet[t] = True
                    ref = ft
                else:
                    ref = min(ref, ft)
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0):
                    continue
                coin_cases.append((c1 / c0 - 1.0, days[t], float(f[t])))
        drift[coin] = float(np.mean(grid_rets)) if len(grid_rets) > 0 else np.nan
        for r, d, fc in coin_cases:
            if np.isfinite(drift[coin]):
                case_ret.append(r - drift[coin])
                case_coin.append(coin)
                case_day.append(d)
                case_fc.append(fc)

    u = np.array(case_ret, dtype=float)
    fcs = np.array(case_fc, dtype=float)
    N = len(u)
    D = len(set(case_day))
    counts = {"cases": int(N), "distinct days": int(D)}

    mean_u = float(np.mean(u)) if N > 0 else None
    t_stat = None
    if N > 1 and D > 1:
        dev = pd.Series(u - mean_u).groupby(np.array(case_day)).sum().values
        var = (D / (D - 1.0)) * np.sum(dev ** 2) / (N ** 2)
        if var > 0:
            t_stat = float(mean_u / np.sqrt(var))

    diff = None
    if N > 0:
        med = np.median(fcs)
        hi = u[fcs > med]
        lo = u[fcs < med]
        if len(hi) > 0 and len(lo) > 0:
            diff = float(np.mean(hi) - np.mean(lo))
    sup_pass = None if diff is None else bool(diff > 0)

    if N < 30 or D < 30:
        status = "not observable"
        decided = f"The plan needs at least 30 cases on at least 30 distinct days; the record has {N} cases on {D} days."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_stat >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the above-median minus below-median difference is above 0."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "The t is 2 or more but the supporting difference is at or below 0 (or not computable), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_stat is None else {"name": "t of the mean, cases of one day together", "value": t_stat},
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "mean unusual move above-median forecast minus below-median",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
