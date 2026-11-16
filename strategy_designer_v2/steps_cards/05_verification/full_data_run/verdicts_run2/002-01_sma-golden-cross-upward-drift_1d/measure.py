import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.sma_cross.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: 50-day SMA above 200-day SMA (raw spread > 0); expected side: long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            d = df[["forecast", RAW]].dropna()
            fc = d["forecast"].astype(float).values
            raw = d[RAW].astype(float).values
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & (raw > 0) & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "OLS slope of excess forward 10-bar return on forecast (non-overlapping, pooled)"
    threshold = ("confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; "
                 "otherwise inconclusive; inconclusive if fewer than 100 non-overlapping blocks with forecast > 0")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation (50-day SMA above 200-day SMA, long side) holds on fewer than 90% "
                           "of the bars where the forecast is non-zero, so the config does not trade the plan's situation."),
            "reading": "Situation taken as raw SMA spread > 0 with forecast > 0 (long).",
        }

    # ---------- 2. Criterion ----------
    # Per coin: all forward 10-bar returns (all bars, all windows) for holding mean and positive share.
    xs, ys = [], []
    sup_terms = []
    n_blocks_pos = 0
    n_blocks = 0

    for coin, wins in bars.items():
        coin_rets = []
        per_window = []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = d["forecast"].astype(float).values
            n = len(d)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            per_window.append((fwd, fc))
            ok = np.isfinite(fwd)
            coin_rets.append(fwd[ok])
        if not coin_rets:
            continue
        all_r = np.concatenate(coin_rets) if coin_rets else np.array([])
        if all_r.size == 0:
            continue
        hold_mean = float(np.mean(all_r))
        share_pos_all = float(np.mean(all_r > 0))

        for fwd, fc in per_window:
            n = len(fwd)
            # supporting: all bars with forecast > 0
            ok = np.isfinite(fwd) & np.isfinite(fc)
            m = ok & (fc > 0)
            if m.any():
                sup_terms.append((fwd[m] > 0).astype(float) - share_pos_all)
            # main: non-overlapping grid 0, H, 2H, ...
            idx = np.arange(0, n, H)
            for i in idx:
                if np.isfinite(fwd[i]) and np.isfinite(fc[i]):
                    xs.append(fc[i])
                    ys.append(fwd[i] - hold_mean)
                    n_blocks += 1
                    if fc[i] > 0:
                        n_blocks_pos += 1

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)

    slope = None
    tstat = None
    if x.size >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        tstat = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    if sup_terms:
        sup_val = float(np.mean(np.concatenate(sup_terms)))
        sup_passed = bool(sup_val > 0)
    else:
        sup_val = None
        sup_passed = None

    if n_blocks_pos < 100:
        status = "inconclusive"
        decided = "Fewer than 100 non-overlapping blocks with forecast > 0, so the result is inconclusive."
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope or its t could not be estimated, so the result is inconclusive."
    elif slope > 0 and tstat >= 2:
        status = "confirmed"
        decided = "The slope is positive with t >= 2, counting each non-overlapping block once: confirmed."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: rejected (gains fall as the position grows)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tstat is None else {"name": "OLS t of slope", "value": tstat},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "share of positive fwd 10-bar returns on forecast>0 bars minus coin's share over all bars",
            "value": sup_val,
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping blocks with forecast > 0": int(n_blocks_pos),
            "non-overlapping blocks": int(n_blocks),
        },
        "decided_by": decided,
        "reading": ("The coin's holding mean and positive share use all overlapping 10-bar returns of all its windows, "
                    "the regression is OLS with intercept on grid bars 0,10,20,... of each window, and the supporting "
                    "check pools all forecast>0 bars, each compared with its own coin's share."),
    }
