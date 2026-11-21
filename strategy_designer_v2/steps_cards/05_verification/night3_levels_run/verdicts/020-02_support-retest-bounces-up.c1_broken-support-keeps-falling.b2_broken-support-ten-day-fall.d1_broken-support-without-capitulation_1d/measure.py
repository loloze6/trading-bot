import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    MIN_CASES = 30
    COL_SHORT = "debug_info.components.support_above_short.last_history_value"
    COL_REB = "debug_info.components.support_above_rebound.last_history_value"

    def num(df, col):
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        return pd.Series(np.nan, index=df.index)

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            fc = num(df, "forecast").fillna(0.0).values
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array(["unknown"] * len(df))
            raw_s = num(df, COL_SHORT).values
            raw_r = num(df, COL_REB).values
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active += 1
                if regime[i] == "mean_reversion":
                    raw, side = raw_r[i], 1.0
                else:
                    raw, side = raw_s[i], -1.0
                if np.isfinite(raw) and raw > 0 and np.sign(fc[i]) == side:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "pooled mean of forecast/10 x (10-bar return minus coin's mean 10-bar return), before costs"
    thr = "mean > 0 with t >= 2 over at least 30 cases (confirm); mean < 0 with t <= -2 over at least 30 cases (reject)"
    sup_name = "mean signed excess return, upper half of |forecast| minus lower half"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the non-zero forecast bars have a swing low above the close (raw component > 0) "
                           "with a short outside the 90-day <= -30% regime and a long inside it, as the Fidelity states."),
            "reading": "The deep-fall regime is read from the recorded `regime` column (mean_reversion = 90-day return <= -30%), "
                       "and the situation is a positive raw value of the active regime's component.",
        }

    # ---------- 2. Criterion ----------
    # per coin: grid returns on all windows (for the coin's mean), and cells with non-zero forecast
    rows = []
    for coin in sorted(bars.keys()):
        all_rets = []
        cells = []
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            close = num(df, "close").values
            fc = num(df, "forecast").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    continue
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] != 0:
                    cells.append((fc[t], r))
        if len(all_rets) == 0:
            continue
        mu = float(np.mean(all_rets))
        for f, r in cells:
            rows.append((f, f / 10.0 * (r - mu)))

    n_cases = len(rows)
    counts = {"non-zero grid cases": int(n_cases)}

    if n_cases > 0:
        vals = np.array([v for _, v in rows], dtype=float)
        absf = np.array([abs(f) for f, _ in rows], dtype=float)
        mean = float(np.mean(vals))
        if n_cases > 1:
            sd = float(np.std(vals, ddof=1))
            tstat = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0
        else:
            tstat = None
        med = float(np.median(absf))
        up = vals[absf > med]
        lo = vals[absf <= med]
        counts["upper half cases"] = int(len(up))
        counts["lower half cases"] = int(len(lo))
        if len(up) > 0 and len(lo) > 0:
            diff = float(np.mean(up) - np.mean(lo))
            sup_pass = bool(diff > 0)
        else:
            diff, sup_pass = None, None
    else:
        mean, tstat, diff, sup_pass = None, None, None, None

    reading = ("The coin's mean 10-bar return is taken over all grid cells (0, 10, 20, ... of each window, return inside the window) "
               "of all its windows; the upper half of |forecast| is the cells strictly above its median and the lower half those at or below; "
               "the regime side is read from the recorded `regime` column.")

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} non-zero grid cases, fewer than the plan's minimum of 30."
    elif tstat is not None and mean > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean is above 0 with t >= 2 over at least 30 cases, and the upper half of |forecast| earns more than the lower half."
        else:
            status = "inconclusive"
            decided = "The mean is above 0 with t >= 2, but the supporting check (upper minus lower half above 0) fails."
    elif tstat is not None and mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "The mean is below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": ({"name": "t of the mean", "value": tstat} if tstat is not None else None),
            "threshold": thr,
        },
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
