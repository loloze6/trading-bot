import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    BAND = 2.0
    REGIME = "mean_reversion"
    RAW = "debug_info.components.rally.last_history_value"

    def to_days(ts):
        s = pd.Series(ts)
        if pd.api.types.is_numeric_dtype(s):
            v = s.astype(float)
            mx = np.nanmax(np.abs(v.values)) if len(v) else 0
            unit = "ns" if mx > 1e17 else ("us" if mx > 1e14 else ("ms" if mx > 1e11 else "s"))
            d = pd.to_datetime(v, unit=unit, utc=True)
        else:
            d = pd.to_datetime(s, utc=True)
        return d.dt.strftime("%Y-%m-%d").values

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            raw = (pd.to_numeric(df[RAW], errors="coerce").values if RAW in df.columns
                   else np.full(len(df), np.nan))
            active = np.isfinite(f) & (f != 0)
            situ = (reg == REGIME) & np.isfinite(raw) & (raw > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ & (f < 0)).sum())

    reading = ("The regime part of the situation (distance from the 365-day closing low at or below its median) is read "
               "from the recorded `regime` == 'mean_reversion' since the detector's component is not recorded and 365 "
               "days cannot be rebuilt from ~120-bar windows, the rally part as a recorded raw 60-day return > 0, the "
               "side as short; a case is the first short bet (rise of |forecast| of at least 2 points) in each 20-bar "
               "grid cell of a window, the day-clustered t uses the cluster-robust standard error with a G/(G-1) "
               "correction, the minimum is the number of distinct days of the cases, and the supporting check's thirds "
               "are the top and bottom floor(n/3) grid bars (positions 0, 20, 40, ...) in regime with nonzero forecast, "
               "pooled across coins and windows, sorted by |forecast|, on the raw 20-bar return.")

    main_name = "mean unusual 20-day move of short cases (return minus drift, short direction)"
    thr = "confirm: mean > 0 with day-clustered t >= 2 and supporting check passed; reject: mean < 0 with t <= -2"
    sup_name = "20-day return after largest-third |forecast| minus after smallest third (must be < 0)"

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": {"cases on distinct days": 0},
            "decided_by": "No bar carries a nonzero forecast, so no case on distinct days exists (fewer than 30).",
            "reading": reading,
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a nonzero forecast are short forecasts on bars in the "
                           "near-yearly-low regime after a 60-day rise, as the Fidelity's situation and outcome require."),
            "reading": reading,
        }

    # ---------- 2. drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    case_vals = []
    case_days = []
    sup_abs = []
    sup_ret = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            days = to_days(df["timestamp"])
            n = len(df)

            # bets on the short side
            ref = 0.0
            side = 0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                fi = f[i]
                s = int(np.sign(fi))
                if s == 0:
                    ref = 0.0
                    side = 0
                    continue
                if s != side:
                    ref = 0.0
                    side = s
                a = abs(fi)
                if a - ref >= BAND:
                    if s < 0:
                        bet[i] = True
                    ref = a
                else:
                    ref = min(ref, a)

            d = drift.get(coin, np.nan)
            for cell_start in range(0, n, H):
                idx = np.where(bet[cell_start:cell_start + H])[0]
                if len(idx) == 0:
                    continue
                t = cell_start + int(idx[0])
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0 and np.isfinite(d)):
                    continue
                r = c[t + H] / c[t] - 1
                case_vals.append(-(r - d))
                case_days.append(days[t])

            # supporting check grid
            for p in range(0, n, H):
                if p + H >= n:
                    continue
                if reg[p] != REGIME or f[p] == 0:
                    continue
                if not (np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0):
                    continue
                sup_abs.append(abs(f[p]))
                sup_ret.append(c[p + H] / c[p] - 1)

    x = np.array(case_vals, dtype=float)
    n_cases = len(x)
    n_days = len(set(case_days))
    mean_u = float(np.mean(x)) if n_cases else None

    tstat = None
    if n_cases >= 2 and n_days >= 2:
        dev = pd.Series(x - x.mean()).groupby(np.array(case_days)).sum().values
        G = len(dev)
        se = np.sqrt(np.sum(dev ** 2) * G / (G - 1)) / n_cases
        if se > 0:
            tstat = float(x.mean() / se)

    # supporting check
    sup_val = None
    sup_pass = None
    m = len(sup_abs)
    k = m // 3
    if k >= 1:
        order = np.argsort(np.array(sup_abs), kind="mergesort")
        rr = np.array(sup_ret)
        small = rr[order[:k]]
        large = rr[order[m - k:]]
        sup_val = float(np.mean(large) - np.mean(small))
        sup_pass = bool(sup_val < 0)

    counts = {"cases": int(n_cases), "cases on distinct days": int(n_days),
              "supporting check bars": int(m)}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} cases on distinct days across all coins and windows, fewer than the plan's 30."
    elif tstat is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed (zero spread), so the result meets neither rule."
    elif mean_u > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with a day-clustered t of 2 or more and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "A confirming t whose supporting check fails (largest third not lower than smallest) is inconclusive."
    elif mean_u < 0 and tstat <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with a day-clustered t of -2 or less."
    else:
        status = "inconclusive"
        decided = "The day-clustered t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": ({"name": "day-clustered t", "value": tstat} if tstat is not None else None),
            "threshold": thr,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
