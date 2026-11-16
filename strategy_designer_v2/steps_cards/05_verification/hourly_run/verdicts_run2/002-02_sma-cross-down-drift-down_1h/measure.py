import numpy as np
import pandas as pd


def measure(bars):
    H = 24
    RAW = "debug_info.components.sma_cross_down.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: SMA50 below SMA200, i.e. the raw spread (SMA50 - SMA200) / SMA200 < 0.
    # Expected side: short (forecast < 0).
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            sub = df[["forecast", RAW]].dropna()
            active = sub["forecast"] != 0
            n_active += int(active.sum())
            agree = active & (sub[RAW] < 0) & (sub["forecast"] < 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    threshold_txt = "t-stat >= 2 confirms, <= -2 rejects, strictly between is inconclusive; fewer than 100 active blocks is inconclusive"
    main_name = "t-stat of mean of (forecast/10 x block forward 24-bar excess return over window mean 24-bar return)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars where SMA50 is below SMA200 "
                           "with a short forecast: the config's forecast (spread standardised against its own past and "
                           "clipped at 0) does not trade only the plan's situation 'short SMA below long SMA' on the short side."
                           if n_active > 0 else
                           "The record has no active bars, so the config never trades the plan's situation."),
            "reading": "The situation is taken as last_history_value (raw SMA50-SMA200 spread) < 0 and the expected side as forecast < 0.",
        }

    # ---------- 2. Criterion ----------
    products = []
    active_excess = []
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            if n <= H:
                continue
            fwd = np.full(n, np.nan)
            fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            win_mean = np.nanmean(fwd) if np.isfinite(fwd).any() else np.nan
            if not np.isfinite(win_mean):
                continue
            for p in range(0, n - H, H):
                r = fwd[p]
                f = fc[p]
                if not (np.isfinite(r) and np.isfinite(f)):
                    continue
                ex = r - win_mean
                products.append((f / 10.0) * ex)
                if f < 0:
                    active_excess.append(ex)

    products = np.asarray(products, dtype=float)
    active_excess = np.asarray(active_excess, dtype=float)
    n_blocks = int(len(products))
    n_active_blocks = int(len(active_excess))

    mean_prod = float(products.mean()) if n_blocks > 0 else None
    t_stat = None
    if n_blocks > 1:
        sd = products.std(ddof=1)
        if sd > 0:
            t_stat = float(products.mean() / (sd / np.sqrt(n_blocks)))

    share_neg = float((active_excess < 0).mean()) if n_active_blocks > 0 else None
    sup_passed = None if share_neg is None else bool(share_neg > 0.5)

    if n_active_blocks < 100:
        status = "inconclusive"
        decided = "Inconclusive: fewer than 100 non-overlapping active blocks (forecast < 0) across the windows."
    elif t_stat is None:
        status = "inconclusive"
        decided = "Inconclusive: the main-measure t-stat could not be computed."
    elif t_stat >= 2:
        status = "confirmed"
        decided = "Confirm: the main-measure t-stat is >= 2 with at least 100 active blocks."
    elif t_stat <= -2:
        status = "rejected"
        decided = "Reject: the main-measure t-stat is <= -2 with at least 100 active blocks."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the main-measure t-stat is strictly between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_prod,
            "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "share of active blocks with negative 24-bar excess return vs 50%",
            "value": share_neg,
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping active blocks (forecast < 0)": n_active_blocks,
            "non-overlapping blocks": n_blocks,
        },
        "decided_by": decided,
        "reading": ("Blocks start at positions 0, 24, 48, ... of each window with a full 24-bar forward return inside it, "
                    "all blocks (including forecast 0) enter the products, the window's mean 24-bar return is the mean "
                    "of the forward 24-bar returns from every bar of that window, and the supporting check passes when "
                    "the negative share exceeds 50%."),
    }
