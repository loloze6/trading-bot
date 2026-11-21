import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.vol_power_reversed.last_history_value"
    POS = "postRebalance_current_allocation"

    # ---------- 1. situation check ----------
    # Situation: raw value w_vol x z_vol is non-zero (past relation gives a direction).
    # Expected side: against the past relation, i.e. sign(forecast) == -sign(raw).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            ok = active & raw.notna() & (raw != 0) & (np.sign(f) == -np.sign(raw))
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "mean timing gain per case, 5-bar non-overlapping grid, before costs"
    main_thr = "confirm: mean > 0 with t >= 2 (and supporting check); reject: mean < 0 with t <= -2"
    sup_name = "mean timing gain positive in at least 4 of the 6 coins"
    reading = ("A case is a grid bar (positions 0,5,10,... of each window) with non-zero post-trade position "
               "and a full 5-bar forward return inside the window; the coin's mean 5-bar return is the mean over "
               "the same grid in all its windows; a coin with no cases counts as not positive; the plan's "
               "'fewer than 300 cases' is reported as not observable, per the workflow's rule on minimum counts; "
               "the situation check counts active bars with non-zero raw value whose forecast sign is opposite to it.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the active bars have a forecast opposite in sign to the non-zero raw "
                           "w_vol x z_vol value, so the config does not bet against the past volatility relation as "
                           "the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    gains_all = []
    coin_means = {}
    coin_counts = {}
    for coin, wins in bars.items():
        # coin's mean 5-bar return over all windows, on the grid
        rets = []
        cells = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            p = pd.to_numeric(df[POS], errors="coerce").to_numpy(dtype=float) if POS in df.columns \
                else np.full(len(df), np.nan)
            n = len(c)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                rets.append(r)
                cells.append((p[i], r))
        if len(rets) == 0:
            coin_means[coin] = None
            coin_counts[coin] = 0
            continue
        mu = float(np.mean(rets))
        g = [pi * (r - mu) for pi, r in cells if np.isfinite(pi) and pi != 0]
        coin_counts[coin] = len(g)
        coin_means[coin] = float(np.mean(g)) if len(g) > 0 else None
        gains_all.extend(g)

    gains = np.array(gains_all, dtype=float)
    n_cases = int(len(gains))
    mean_gain = float(gains.mean()) if n_cases > 0 else None
    if n_cases > 1:
        sd = float(gains.std(ddof=1))
        t = float(mean_gain / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0
    else:
        t = None

    n_pos_coins = int(sum(1 for v in coin_means.values() if v is not None and v > 0))
    sup_pass = bool(n_pos_coins >= 4)

    counts = {"non-overlapping cases across all coins and windows": n_cases}
    for coin in coin_counts:
        counts["cases " + str(coin)] = int(coin_counts[coin])
    counts["coins with positive mean timing gain"] = n_pos_coins

    if n_cases < 300 or t is None:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases, below the plan's minimum of 300."
    elif mean_gain > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean timing gain above 0 with t >= 2 and positive in at least 4 of the 6 coins."
    elif mean_gain < 0 and t <= -2:
        status = "rejected"
        decided = "Mean timing gain below 0 with t <= -2: the past volatility relation persists."
    elif t >= 2 and not sup_pass:
        status = "inconclusive"
        decided = "t >= 2 but the mean timing gain is positive in fewer than 4 of the 6 coins."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_gain,
            "statistic": {"name": "ordinary t of the mean", "value": t} if t is not None else None,
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": n_pos_coins, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
