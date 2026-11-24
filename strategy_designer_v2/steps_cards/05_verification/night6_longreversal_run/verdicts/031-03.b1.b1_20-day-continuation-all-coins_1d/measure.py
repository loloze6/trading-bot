import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.ret20.last_history_value"
    MIN_CASES = 300
    MIN_DAYS = 100

    # ---------- 1. Situation check ----------
    # The situation holds on every bar with a nonzero 20-day return (the plan keeps all bars).
    # The idea expects continuation: long after a rise, short after a fall.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            f = pd.to_numeric(d["forecast"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            recomputed = close / close.shift(20) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            ok = active & raw.notna() & (raw != 0) & (np.sign(raw) == np.sign(f))
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of forecast/10 x coin's excess 10-bar return, non-overlapping grid"
    threshold = "confirm: mean > 0 with day-clustered t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a nonzero forecast have the sign of the coin's 20-day return, "
                          "so the config does not take the continuation side on the plan's situation.",
            "reading": "Situation taken as every bar with a nonzero raw 20-day return, expected side = its sign (continuation).",
        }

    # ---------- 2. Cases on the non-overlapping 10-bar grid ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_rets.append(r)
                if np.isfinite(f[t]) and f[t] != 0:
                    coin_cases.append((coin, ts.iloc[t].floor("D"), f[t], r))
        if len(coin_rets) == 0:
            continue
        mu = float(np.mean(coin_rets))
        for (c, day, fc, r) in coin_cases:
            rows.append({"coin": c, "day": day, "f": fc, "ex": r - mu})

    cases = pd.DataFrame(rows, columns=["coin", "day", "f", "ex"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases > 0 else 0
    counts = {"cases with a nonzero forecast": n_cases, "distinct days": n_days}

    # Main measure
    mean_val = None
    t_val = None
    if n_cases > 0:
        prod = (cases["f"] / 10.0) * cases["ex"]
        mean_val = float(prod.mean())
        dev = prod - mean_val
        per_day = dev.groupby(cases["day"]).sum()
        G = len(per_day)
        if G > 1:
            var = (G / (G - 1)) * float((per_day ** 2).sum()) / (n_cases ** 2)
            se = np.sqrt(var)
            t_val = float(mean_val / se) if se > 0 else None

    # Supporting check: top third vs bottom third by |forecast|
    sup_val = None
    sup_pass = None
    sup_t = None
    if n_cases >= 3:
        k = n_cases // 3
        absf = cases["f"].abs().to_numpy()
        order = np.argsort(absf, kind="mergesort")
        direc = (cases["ex"] * np.sign(cases["f"])).to_numpy()
        bottom = direc[order[:k]]
        top = direc[order[-k:]]
        if k >= 1:
            sup_val = float(np.mean(top) - np.mean(bottom))
            sup_pass = bool(sup_val > 0)
            if k >= 2:
                tt = stats.ttest_ind(top, bottom, equal_var=False)
                sup_t = float(tt.statistic) if np.isfinite(tt.statistic) else None

    supporting = {
        "name": "Welch difference of directional excess return, top third minus bottom third by |forecast|"
                + (f" (Welch t {sup_t:.3f})" if sup_t is not None else ""),
        "value": sup_val,
        "passed": sup_pass,
    }

    # ---------- 3. Decision ----------
    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = (f"The minimum of {MIN_CASES} cases with a nonzero forecast on at least {MIN_DAYS} distinct days "
                   f"is not reached ({n_cases} cases, {n_days} days).")
    elif t_val is None or mean_val is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_val > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean is positive with t >= 2 and the top third by |forecast| beats the bottom third."
        else:
            status = "inconclusive"
            decided = "The mean is positive with t >= 2 but the supporting check fails, which the plan calls inconclusive."
    elif mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean is negative with t <= -2: the coins move back against their 20-day move."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": ({"name": "t of the mean, cases of one day summed as one piece of evidence", "value": t_val}
                          if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are the grid bars (positions 0, 10, 20, ... of each window, with t+10 inside the window) "
                    "with a nonzero forecast, the coin's mean 10-bar return is taken over all grid bars of all its "
                    "windows, the thirds are the n//3 cases with the smallest and largest |forecast| by stable rank, "
                    "and the day-clustered t sums the cases' deviations per UTC day."),
    }
