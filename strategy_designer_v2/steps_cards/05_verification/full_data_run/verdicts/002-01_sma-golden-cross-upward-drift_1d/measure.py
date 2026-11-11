import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    RAW = "debug_info.components.sma_cross.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: the 50-day SMA is above the 200-day SMA (raw spread > 0); outcome "rise" means long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & (raw > 0) & (f > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "forecast-weighted mean 10-bar forward return minus mean 10-bar forward return of all bars of the same coin and window"
    main_thr = "excess > 0 with t >= 2 confirms (with positive hit-rate difference); excess < 0 with t <= -2 rejects; otherwise or fewer than 30 positive-forecast blocks inconclusive"
    sup_name = "hit rate of positive-forecast bars minus hit rate of all bars (10-bar forward return > 0)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars where the 50-day SMA is above the 200-day SMA, as the plan's situation requires.",
            "reading": "none",
        }

    # ---------- 2. Criterion on non-overlapping 10-bar grid ----------
    pos_x, pos_w = [], []          # excess returns and forecast weights of positive-forecast blocks
    pos_hits = []                  # forward return > 0 for positive-forecast blocks
    all_hits = []                  # forward return > 0 for all blocks
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            idx = np.arange(0, n - H, H)
            if len(idx) == 0:
                continue
            fwd = close[idx + H] / close[idx] - 1.0
            fc = f[idx]
            ok = np.isfinite(fwd)
            if ok.sum() == 0:
                continue
            hold_mean = float(np.mean(fwd[ok]))
            all_hits.extend((fwd[ok] > 0).astype(float).tolist())
            sel = ok & np.isfinite(fc) & (fc > 0)
            if sel.any():
                pos_x.extend((fwd[sel] - hold_mean).tolist())
                pos_w.extend(fc[sel].tolist())
                pos_hits.extend((fwd[sel] > 0).astype(float).tolist())

    x = np.asarray(pos_x, dtype=float)
    wt = np.asarray(pos_w, dtype=float)
    n_blocks = int(len(x))

    excess = None
    tstat = None
    if n_blocks > 0 and wt.sum() > 0:
        excess = float(np.sum(wt * x) / np.sum(wt))
        if n_blocks > 1:
            se = np.sqrt(np.sum(wt ** 2 * (x - excess) ** 2) * n_blocks / (n_blocks - 1)) / np.sum(wt)
            if se > 0 and np.isfinite(se):
                tstat = float(excess / se)

    hit_diff = None
    if len(pos_hits) > 0 and len(all_hits) > 0:
        hit_diff = float(np.mean(pos_hits) - np.mean(all_hits))
    sup_passed = None if hit_diff is None else bool(hit_diff > 0)

    if n_blocks < 30:
        status = "inconclusive"
        decided = "Fewer than 30 non-overlapping 10-bar blocks with a positive forecast, pooled across coins and windows, so the result is inconclusive."
    elif excess is None or tstat is None:
        status = "inconclusive"
        decided = "The t-statistic of the excess could not be computed, so the result is inconclusive."
    elif excess > 0 and tstat >= 2 and sup_passed:
        status = "confirmed"
        decided = "The excess over holding is positive with t >= 2 across the non-overlapping blocks and the hit-rate difference is positive."
    elif excess < 0 and tstat <= -2:
        status = "rejected"
        decided = "The excess over holding is negative with t <= -2: moves after up-crosses underperform holding."
    elif excess > 0 and tstat >= 2:
        status = "inconclusive"
        decided = "The excess is positive with t >= 2 but the supporting hit-rate difference is not positive, so the confirm rule is not met and the reject rule does not apply."
    else:
        status = "inconclusive"
        decided = "The t-statistic of the excess lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": excess,
            "statistic": None if tstat is None else {"name": "t of the forecast-weighted mean excess across non-overlapping blocks", "value": tstat},
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": hit_diff, "passed": sup_passed},
        "counts": {"non-overlapping 10-bar blocks with a positive forecast": n_blocks,
                   "non-overlapping 10-bar blocks, all bars": int(len(all_hits))},
        "decided_by": decided,
        "reading": "Blocks are the bars at positions 0, 10, 20, ... of each window with a full 10-bar forward return inside it; each positive-forecast block's return is taken minus the mean over all grid blocks of its own coin and window, then forecast-weighted and pooled, with t = weighted mean / weighted standard error; the hit-rate shares use the same grid pooled across coins and windows.",
    }
