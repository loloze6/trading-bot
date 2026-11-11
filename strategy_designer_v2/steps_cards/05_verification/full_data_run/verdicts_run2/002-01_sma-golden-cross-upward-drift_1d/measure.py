import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    RAW = "debug_info.components.sma_cross.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce")
            ok = f.notna() & raw.notna()
            active = ok & (f != 0)
            n_active += int(active.sum())
            # situation: 50-day SMA above 200-day SMA (positive spread); expected side: long
            n_agree += int((active & (raw > 0) & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "forecast-weighted mean 10-bar forward return minus holding",
                "value": None,
                "statistic": None,
                "threshold": "t >= 2 to confirm, t <= -2 to reject",
            },
            "supporting_check": None,
            "counts": {"non-overlapping 10-bar blocks with a positive forecast": 0,
                       "active bars": int(n_active)},
            "decided_by": ("The plan's situation (long while the 50-day SMA is above the 200-day SMA) "
                           "does not cover at least 90% of the bars where the forecast is non-zero, "
                           "on the long side."),
            "reading": "Situation taken as raw SMA spread > 0 with a positive forecast; active bars are forecast != 0.",
        }

    # ---------- 2. Criterion ----------
    ex_vals, wts = [], []
    pos_hits, pos_n = 0, 0
    all_hits, all_n = 0, 0

    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(d)
            if n <= H:
                continue
            fwd = np.full(n, np.nan)
            fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            grid = np.arange(0, n, H)
            g_fwd = fwd[grid]
            g_f = f[grid]
            valid_all = np.isfinite(g_fwd)
            if valid_all.sum() == 0:
                continue
            hold_mean = float(np.mean(g_fwd[valid_all]))
            all_hits += int((g_fwd[valid_all] > 0).sum())
            all_n += int(valid_all.sum())

            sel = valid_all & np.isfinite(g_f) & (g_f > 0)
            if sel.sum() == 0:
                continue
            ex_vals.extend(list(g_fwd[sel] - hold_mean))
            wts.extend(list(g_f[sel]))
            pos_hits += int((g_fwd[sel] > 0).sum())
            pos_n += int(sel.sum())

    ex_vals = np.asarray(ex_vals, dtype=float)
    wts = np.asarray(wts, dtype=float)
    n_blocks = int(len(ex_vals))

    excess = None
    tstat = None
    if n_blocks >= 1 and wts.sum() > 0:
        W = wts.sum()
        excess = float(np.sum(wts * ex_vals) / W)
        if n_blocks >= 2:
            se = float(np.sqrt(np.sum((wts ** 2) * (ex_vals - excess) ** 2)) / W)
            se *= np.sqrt(n_blocks / (n_blocks - 1))
            if se > 0:
                tstat = float(excess / se)

    hit_diff = None
    if pos_n > 0 and all_n > 0:
        hit_diff = float(pos_hits / pos_n - all_hits / all_n)

    if n_blocks < 30 or excess is None or tstat is None:
        status = "inconclusive"
        decided = ("Fewer than 30 non-overlapping 10-bar blocks with a positive forecast "
                   "(or no computable t), which the plan calls inconclusive.")
    elif excess > 0 and tstat >= 2 and hit_diff is not None and hit_diff > 0:
        status = "confirmed"
        decided = "The excess is positive with t >= 2 and the hit-rate difference is positive: confirm."
    elif excess < 0 and tstat <= -2:
        status = "rejected"
        decided = "The excess is negative with t <= -2: reject."
    else:
        status = "inconclusive"
        if tstat >= 2:
            decided = ("t >= 2 but the supporting hit-rate difference is not positive, "
                       "so the confirm rule is not met and the result is inconclusive.")
        else:
            decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "forecast-weighted mean 10-bar forward return minus holding",
            "value": excess,
            "statistic": None if tstat is None else {"name": "t of the forecast-weighted mean excess", "value": tstat},
            "threshold": "excess > 0 with t >= 2 to confirm; excess < 0 with t <= -2 to reject",
        },
        "supporting_check": {
            "name": "hit rate of positive-forecast blocks minus hit rate of all blocks",
            "value": hit_diff,
            "passed": None if hit_diff is None else bool(hit_diff > 0),
        },
        "counts": {"non-overlapping 10-bar blocks with a positive forecast": n_blocks,
                   "non-overlapping 10-bar blocks, all": int(all_n)},
        "decided_by": decided,
        "reading": ("Blocks are bars at positions 0,10,20,... of each window for both groups, the holding mean "
                    "and the all-bar hit rate use that same grid per coin and window, and the t is the "
                    "forecast-weighted mean of per-block excesses over its weighted (sandwich) standard error "
                    "across the pooled positive-forecast blocks."),
    }
