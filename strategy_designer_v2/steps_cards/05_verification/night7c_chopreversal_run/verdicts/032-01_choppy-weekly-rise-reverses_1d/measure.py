import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    REGIME = "mean_reversion"
    RAW = "debug_info.components.scaled_rise.last_history_value"

    def to_day(ts):
        s = pd.Series(ts)
        if pd.api.types.is_numeric_dtype(s):
            v = s.astype(float)
            med = np.nanmedian(v.values) if len(v) else 0
            unit = "ms" if med > 1e11 else "s"
            d = pd.to_datetime(v, unit=unit, utc=True)
        else:
            d = pd.to_datetime(s, utc=True)
        return d.dt.floor("D").dt.strftime("%Y-%m-%d").values

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            regime = df["regime"].astype(str).values
            raw = (pd.to_numeric(df[RAW], errors="coerce").values
                   if RAW in df.columns else np.full(len(df), np.nan))
            # 7-day return from prices inside the window, used where the raw value is missing
            r7 = np.full(len(df), np.nan)
            if len(df) > H:
                r7[H:] = close[H:] / close[:-H] - 1.0
            rise_sign = np.where(np.isfinite(raw), np.sign(raw), np.sign(r7))
            active = fc != 0
            in_situation = (regime == REGIME) & (rise_sign > 0)
            on_side = fc < 0  # idea expects a fall -> short
            n_active += int(active.sum())
            n_agree += int((active & in_situation & on_side).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean short-signed 7-bar unusual move (return minus coin's normal 7-bar drift)"
    threshold = "confirm t >= 2 with rank correlation > 0; reject t <= -2; else inconclusive"
    reading = ("The situation is read as bars the detector labels mean_reversion (its rules are er <= 0.3 and vp >= 0.5, "
               "the Fidelity's thresholds; the detector's components are not recorded and the 365-day percentile cannot be "
               "rebuilt from 120-bar windows) with a positive scaled 7-day rise (raw value, or the 7-day price return where "
               "missing), expected side short; cases are grid bars 0,7,14,... per window with forecast < 0 and a full 7-bar "
               "return inside the window; drift is the coin's mean 7-bar return on the same grid over all its windows; the t "
               "uses a day-clustered standard error with a G/(G-1) correction; the plan's 'fewer than 30 cases or days' rule "
               "is treated as a minimum count (not observable).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars in the mean_reversion regime "
                           "after a 7-day rise, as the Fidelity's situation and side require."
                           if n_active > 0 else "The record has no bar with a non-zero forecast."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, ret, |forecast|)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            days = to_day(df["timestamp"])
            for t in range(0, len(df) - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] < 0:
                    cases.append((coin, days[t], r, abs(fc[t])))
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

    rows = [(d, -(r - drift[c]), a) for c, d, r, a in cases if np.isfinite(drift.get(c, np.nan))]
    n_cases = len(rows)
    days_list = [r[0] for r in rows]
    n_days = len(set(days_list))
    x = np.array([r[1] for r in rows], dtype=float)
    a = np.array([r[2] for r in rows], dtype=float)

    mean_val = float(np.mean(x)) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        dev = pd.Series(x - x.mean()).groupby(pd.Series(days_list)).sum().values
        G = len(dev)
        var = (G / (G - 1.0)) * np.sum(dev ** 2) / (n_cases ** 2)
        se = np.sqrt(var)
        t_val = float(mean_val / se) if se > 0 else None

    rho = None
    if n_cases >= 3 and np.std(a) > 0 and np.std(x) > 0:
        rho = float(stats.spearmanr(a, x).correlation)
    sup_passed = None if rho is None or not np.isfinite(rho) else bool(rho > 0)

    counts = {"cases": int(n_cases), "distinct days": int(n_days)}

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = (f"The plan's minimum is not reached: {n_cases} cases on {n_days} distinct days "
                   "(needs at least 30 cases and 30 distinct days).")
    elif t_val is None:
        status = "inconclusive"
        decided = "The day-clustered t of the mean could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and sup_passed:
        status = "confirmed"
        decided = "The mean short-signed unusual move has t >= 2 and the rank correlation with |forecast| is above 0."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The mean short-signed unusual move has t >= 2 but the rank correlation with |forecast| is not above 0."
    elif t_val <= -2:
        status = "rejected"
        decided = "The mean short-signed unusual move has t <= -2: the rise continues."
    else:
        status = "inconclusive"
        decided = "The t of the mean short-signed unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t_val}
                          if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {"name": "Spearman rank correlation of |forecast| with short-signed unusual move",
                             "value": rho, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
