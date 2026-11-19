import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.fade.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    # ---------- Prepare per-window frames ----------
    frames = []
    for coin, wins in bars.items():
        for win, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            if "timestamp" in d.columns:
                d = d.sort_values("timestamp", kind="mergesort")
            d = d.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            d["_coin"] = coin
            d["_win"] = win
            d["_ret_prev"] = close / close.shift(1) - 1.0   # last hour's move (within window)
            d["_ret_next"] = close.shift(-1) / close - 1.0  # next hour's move (within window)
            frames.append(d)

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean timing gain per bar vs holding", "value": None,
                             "statistic": None, "threshold": "t >= 2 to confirm, t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"bars with a non-zero position": 0},
            "decided_by": "No bars in the record.",
            "reading": "none",
        }

    # ---------- Situation check ----------
    # Situation: the last hour's move (scaled by vol), kept on every bar; side: fade (opposite sign of the move).
    agree_num = 0
    active_total = 0
    for d in frames:
        fc = pd.to_numeric(d["forecast"], errors="coerce")
        if RAW in d.columns:
            raw = pd.to_numeric(d[RAW], errors="coerce")
        else:
            raw = pd.Series(np.nan, index=d.index)
        # Where the raw value is not recorded, recompute its sign from prices (sign of the 1-bar return).
        raw_sign = np.sign(raw)
        raw_sign = raw_sign.where(raw.notna(), np.sign(d["_ret_prev"]))
        active = fc.notna() & (fc != 0)
        active_total += int(active.sum())
        ok = active & raw_sign.notna() & (raw_sign != 0) & (np.sign(fc) == -raw_sign)
        agree_num += int(ok.sum())

    agreement = float(agree_num / active_total) if active_total > 0 else 0.0
    passed = agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": active_total},
            "decided_by": ("Fewer than 90% of active bars have a forecast opposite in sign to the last hour's "
                           "volatility-scaled move, so the config does not fade the move as the Fidelity states."),
            "reading": "none",
        }

    # ---------- Main measure ----------
    allf = pd.concat(frames, ignore_index=True)
    # Coin's mean hourly return over all its windows (within-window 1-bar returns pooled).
    mu = allf.groupby("_coin")["_ret_next"].mean()
    allf["_mu"] = allf["_coin"].map(mu)
    allf["_alloc"] = pd.to_numeric(allf[ALLOC], errors="coerce")
    allf["_fc"] = pd.to_numeric(allf["forecast"], errors="coerce")
    allf["_gain"] = allf["_alloc"] * (allf["_ret_next"] - allf["_mu"])

    valid = allf[allf["_gain"].notna()].copy()
    n = int(len(valid))
    n_nonzero = int(((valid["_alloc"] != 0) & valid["_alloc"].notna()).sum())

    g = valid["_gain"].to_numpy(dtype=float)
    mean_gain = float(np.mean(g)) if n > 0 else None
    if n > 1:
        sd = float(np.std(g, ddof=1))
        t_stat = float(mean_gain / (sd / np.sqrt(n))) if sd > 0 else 0.0
    else:
        t_stat = None

    # ---------- Supporting check ----------
    diff = None
    sup_passed = None
    vq = valid[valid["_fc"].notna()].copy()
    if len(vq) >= 5:
        r = vq["_fc"].abs().rank(method="first")
        vq["_q"] = pd.qcut(r, 5, labels=False)
        top = vq.loc[vq["_q"] == 4, "_gain"].mean()
        bot = vq.loc[vq["_q"] == 0, "_gain"].mean()
        diff = float(top - bot)
        sup_passed = bool(diff > 0)

    counts = {
        "bars with a non-zero position across all coins and windows": n_nonzero,
        "bars in the main measure": n,
    }

    # ---------- Decision ----------
    if n_nonzero < 10000:
        status = "not observable"
        decided_by = "Fewer than the plan's minimum of 10,000 bars with a non-zero position across all coins and windows."
    elif t_stat is None:
        status = "inconclusive"
        decided_by = "The t of the mean timing gain could not be computed."
    elif mean_gain > 0 and t_stat >= 2 and sup_passed:
        status = "confirmed"
        decided_by = "Mean timing gain positive with t >= 2 and top-minus-bottom quintile difference above 0."
    elif mean_gain < 0 and t_stat <= -2:
        status = "rejected"
        decided_by = "Mean timing gain negative with t <= -2."
    elif t_stat >= 2:
        status = "inconclusive"
        decided_by = "t >= 2 but the top-minus-bottom quintile difference is not above 0."
    else:
        status = "inconclusive"
        decided_by = "t of the mean timing gain lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean per-bar timing gain of the position vs holding the coin, 1 bar",
            "value": mean_gain,
            "statistic": {"name": "ordinary t of the mean", "value": t_stat} if t_stat is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 (and supporting check passes); reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "mean timing gain, top minus bottom quintile of abs(forecast)",
            "value": diff,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("Quintiles of abs(forecast) are cut on the pooled bars of the main measure by rank "
                    "(ties broken by row order); the coin's mean hourly return is the mean of all its within-window "
                    "1-bar returns; the 10,000-bar minimum counts bars with a non-zero postRebalance_current_allocation "
                    "and a next-bar return inside the window, and is treated as 'not observable' when unmet."),
    }
