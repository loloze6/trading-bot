import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    LHV = "debug_info.components.rsi_low.last_history_value"

    # ---------- 1. Situation check ----------
    # The situation is RSI below 50, so last_history_value = (50 - RSI) * 0.4 is above 0.
    # The expected side is long, so the forecast should be above 0.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["forecast", LHV]].dropna()
            act = d["forecast"] != 0
            n_active += int(act.sum())
            ok = act & (d[LHV] > 0) & (d["forecast"] > 0)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled mean 5-bar excess return (vs coin's window hold average) after top-quintile forecasts"
    thr_text = "t >= 2 with supporting check to confirm; t <= -2 to reject"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_text},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active (non-zero forecast) bars have RSI below 50 with a long forecast, "
                          "so the config does not trade the plan's 'RSI low -> long' situation.",
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    pooled_top = []
    per_coin_top_n = {}
    per_coin_diff = {}
    for coin, wins in bars.items():
        # Top-quintile cut-off: the 80th percentile of this coin's non-zero forecasts, over all its windows.
        fc_all = pd.concat([df["forecast"] for df in wins.values()]).dropna()
        nz = fc_all[fc_all != 0]
        if len(nz) == 0:
            per_coin_top_n[coin] = 0
            per_coin_diff[coin] = None
            continue
        cut = float(np.quantile(nz.values, 0.8))

        top_ex, zero_ex = [], []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            grid = np.arange(0, n, H)
            grid = grid[grid + H < n]
            if len(grid) == 0:
                continue
            fwd = close[grid + H] / close[grid] - 1.0
            fcg = fc[grid]
            valid = np.isfinite(fwd)
            if valid.sum() == 0:
                continue
            base = float(np.mean(fwd[valid]))  # hold baseline: the window's mean 5-bar return on the grid
            ex = fwd - base
            mtop = valid & np.isfinite(fcg) & (fcg != 0) & (fcg >= cut)
            mzero = valid & np.isfinite(fcg) & (fcg == 0)
            top_ex.extend(ex[mtop].tolist())
            zero_ex.extend(ex[mzero].tolist())

        per_coin_top_n[coin] = len(top_ex)
        pooled_top.extend(top_ex)
        if len(top_ex) > 0 and len(zero_ex) > 0:
            per_coin_diff[coin] = float(np.mean(top_ex) - np.mean(zero_ex))
        else:
            per_coin_diff[coin] = None

    arr = np.array(pooled_top, dtype=float)
    n_top = int(len(arr))
    mean_ex = float(arr.mean()) if n_top > 0 else None
    t = None
    if n_top >= 2:
        sd = float(arr.std(ddof=1))
        if sd > 0:
            t = float(mean_ex / (sd / np.sqrt(n_top)))

    n_pos = int(sum(1 for v in per_coin_diff.values() if v is not None and v > 0))
    support_ok = n_pos >= 2

    counts = {"pooled non-overlapping top-quintile cases": n_top}
    for c, k in per_coin_top_n.items():
        counts[f"top-quintile cases {c}"] = int(k)
    counts["coins with positive top-minus-neutral excess"] = n_pos

    too_few = n_top < 30 or any(k < 8 for k in per_coin_top_n.values())
    if too_few:
        status = "inconclusive"
        decided = "Inconclusive: fewer than 30 non-overlapping top-quintile cases pooled or fewer than 8 for some coin."
    elif t is None:
        status = "inconclusive"
        decided = "Inconclusive: the t-statistic could not be computed (zero dispersion)."
    elif t >= 2 and support_ok:
        status = "confirmed"
        decided = "Confirm: pooled mean excess after top-quintile positions has t >= 2 and the supporting check holds."
    elif t <= -2:
        status = "rejected"
        decided = "Reject: pooled mean excess after top-quintile positions has t <= -2."
    else:
        status = "inconclusive"
        decided = ("Inconclusive: t is between -2 and 2." if t < 2
                   else "Inconclusive: t >= 2 but the supporting check fails, so the confirm rule is not met.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
            "threshold": thr_text,
        },
        "supporting_check": {
            "name": "coins (of 3) with top-quintile minus neutral excess > 0, need >= 2",
            "value": n_pos,
            "passed": bool(support_ok),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The top quintile is defined per coin as forecasts at or above the 80th percentile of that coin's "
                    "non-zero forecasts pooled over its windows, the hold baseline is the mean 5-bar return on the same "
                    "window's non-overlapping grid, and the '2 of 3 coins' rule is applied literally as at least 2 "
                    "positive coins among those present."),
    }
