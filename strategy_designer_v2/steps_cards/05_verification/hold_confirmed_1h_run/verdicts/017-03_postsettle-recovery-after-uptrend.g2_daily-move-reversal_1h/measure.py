import numpy as np
import pandas as pd


def measure(bars):
    H = 24
    FC = "forecast"
    RAW = "debug_info.components.day_rev.last_history_value"

    # ---------- 1. situation check ----------
    # Fidelity: the situation is the coin's own past 24-bar return, active on every bar.
    # The expected side is opposite to that past move: short after a rise, long after a fall.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or FC not in df.columns:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d[FC], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(d), np.nan)

            # Past 24-bar return from the window's own prices where available.
            past = np.full(len(d), np.nan)
            if len(d) > H:
                past[H:] = close[H:] / close[:-H] - 1.0
            # Where the window's prices do not reach back 24 bars, use the raw
            # component value. Vol scaling is positive, so the sign is unchanged.
            move = np.where(np.isfinite(past), past, raw)

            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            ok = active & np.isfinite(move) & (move != 0) & (np.sign(fc) == -np.sign(move))
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "mean of forecast/10 x (next-24-bar return minus coin's mean 24-bar return), non-overlapping"
    threshold = ("confirm: mean > 0 with t >= 2 and supporting check passes; "
                 "reject: mean < 0 with t <= -2; at least 500 non-overlapping cases")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "non-overlapping cases": None},
            "decided_by": ("Fewer than 90% of active bars have the forecast opposite in sign to the past "
                           "24-bar move, while the Fidelity expects a position against that move."),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    # Non-overlapping grid at positions 0, 24, 48, ... of each window.
    per_coin = {}
    for coin, wins in bars.items():
        rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d[FC], errors="coerce").to_numpy(dtype=float)
            n = len(d)
            for i in range(0, n, H):
                r = close[i + H] / close[i] - 1.0 if i + H < n else np.nan
                rows.append((fc[i], r))
        per_coin[coin] = rows

    f_all = []
    p_all = []
    for coin, rows in per_coin.items():
        if not rows:
            continue
        arr = np.array(rows, dtype=float)
        rets = arr[:, 1]
        valid_r = np.isfinite(rets)
        if valid_r.sum() == 0:
            continue
        # The coin's mean over all windows, from its grid samples.
        coin_mean = float(np.mean(rets[valid_r]))
        ok = valid_r & np.isfinite(arr[:, 0])
        f = arr[ok, 0]
        prod = f / 10.0 * (rets[ok] - coin_mean)
        f_all.append(f)
        p_all.append(prod)

    if f_all:
        f_all = np.concatenate(f_all)
        p_all = np.concatenate(p_all)
    else:
        f_all = np.array([])
        p_all = np.array([])
    n_cases = int(len(p_all))

    mean = float(np.mean(p_all)) if n_cases > 0 else None
    tstat = None
    if n_cases > 1:
        sd = float(np.std(p_all, ddof=1))
        if sd > 0:
            tstat = mean / (sd / np.sqrt(n_cases))

    # Supporting check: largest-|forecast| third against smallest-|forecast| third.
    sup_val = None
    sup_pass = None
    k = n_cases // 3
    if k > 0:
        order = np.argsort(np.abs(f_all), kind="mergesort")
        low = p_all[order[:k]]
        high = p_all[order[-k:]]
        sup_val = float(np.mean(high) - np.mean(low))
        sup_pass = bool(sup_val > 0)

    counts = {"non-overlapping cases": n_cases, "active bars": int(n_active)}

    if n_cases < 500:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases, fewer than the plan's minimum of 500."
    elif tstat is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero dispersion), so neither rule is met."
    elif mean > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = ("The mean is positive with t >= 2, and the largest-|forecast| third beats "
                       "the smallest third.")
        else:
            status = "inconclusive"
            decided = "t >= 2, but the supporting check fails, which the plan calls inconclusive."
    elif mean < 0 and tstat <= -2:
        status = "rejected"
        decided = "The mean is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    reading = ("The coin's mean 24-bar return is taken over its non-overlapping grid samples in all windows; "
               "the thirds are the floor(n/3) cases with the largest and smallest |forecast| "
               "(stable sort); fewer than 500 cases is reported as 'not observable' as instructed; "
               "the situation side uses the in-window price 24-bar return, and the raw component value "
               "where the window has fewer than 24 prior bars.")

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": ({"name": "ordinary t of the mean", "value": float(tstat)}
                          if tstat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean product, top third |forecast| minus bottom third",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
