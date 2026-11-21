import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    RAW = "debug_info.components.support_above.last_history_value"

    # ---------- 1. Situation check ----------
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
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            # Situation: a swing low clusters above the close (raw > 0), the coin has not
            # collapsed (regime mean_reversion = 90-bar return >= -50 %), and the side is short.
            situ = (np.nan_to_num(raw, nan=0.0) > 0) & (reg == "mean_reversion")
            ok = active & situ & (f < 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of the mean of |forecast|-weighted unusual 10-bar falls on short grid cases"
    main_thr = "confirm if t >= 2 over at least 30 cases (and supporting check passes); reject if t <= -2 over at least 30 cases"
    sup_name = "mean unusual fall, top third |forecast| minus bottom third"
    reading = ("Situation taken as raw support_above > 0 on bars whose regime is mean_reversion (the recorded decision "
               "of the 90-bar return >= -50 % rule) with a negative forecast; the coin's mean 10-bar return is taken "
               "over the non-overlapping grid of all its windows; thirds are floor(n/3) cases each by |forecast| "
               "(unweighted unusual fall); fewer than 30 cases is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the active bars are short bars with clustered swing lows above the "
                           "close in the no-collapse regime, so the config does not do what the plan's situation says."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    # coin mean 10-bar return over all windows (non-overlapping grid)
    coin_rows = {}
    coin_mean = {}
    for coin, wins in bars.items():
        all_r = []
        rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for p in range(0, n - H, H):
                c0, c1 = c[p], c[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                all_r.append(r)
                if np.isfinite(f[p]) and f[p] < 0:
                    rows.append((r, abs(float(f[p]))))
        coin_mean[coin] = float(np.mean(all_r)) if all_r else np.nan
        coin_rows[coin] = rows

    unusual = []
    weights = []
    for coin in sorted(coin_rows.keys()):
        mu = coin_mean[coin]
        if not np.isfinite(mu):
            continue
        for r, a in coin_rows[coin]:
            unusual.append(-(r - mu))
            weights.append(a)
    unusual = np.array(unusual, dtype=float)
    weights = np.array(weights, dtype=float)
    vals = unusual * weights
    n_cases = int(len(vals))

    mean_v = float(np.mean(vals)) if n_cases > 0 else None
    t = None
    if n_cases >= 2:
        sd = float(np.std(vals, ddof=1))
        if sd > 0:
            t = float(mean_v / (sd / np.sqrt(n_cases)))

    diff = None
    sup_pass = None
    k = n_cases // 3
    if k >= 1:
        order = np.argsort(weights, kind="mergesort")
        low = unusual[order[:k]]
        high = unusual[order[-k:]]
        diff = float(np.mean(high) - np.mean(low))
        sup_pass = bool(diff > 0)

    counts = {"cases": n_cases, "cases per third": int(k)}
    main = {"name": main_name, "value": mean_v,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": main_thr}
    sup = {"name": sup_name, "value": diff, "passed": sup_pass}
    sc = {"agreement": agreement, "passed": True}

    if n_cases < 30 or t is None:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 30 (or no t could be computed)."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main t is 2 or more over at least 30 cases and the top third shows a larger unusual fall than the bottom third."
    elif t >= 2:
        status = "inconclusive"
        decided = "The main t is at least 2 but the supporting check fails."
    elif t <= -2:
        status = "rejected"
        decided = "The main t is -2 or less over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
