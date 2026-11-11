import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    RAW = "debug_info.components.sma_cross.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: situation is "SMA50 above SMA200" (raw spread > 0); the outcome is a rise, so the side is long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce")
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "excess mean 20-bar forward return when forecast > 0",
                "value": None,
                "statistic": None,
                "threshold": "excess > 0 with t >= 2 confirms; excess < 0 with t <= -2 rejects",
            },
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars where SMA50 is above "
                           "SMA200 (raw spread > 0), so the config does not trade the plan's situation."
                           if n_active > 0 else
                           "The record has no bars with a non-zero forecast, so the plan's situation is never traded."),
            "reading": "Situation taken as raw SMA50-minus-SMA200 spread > 0 with a long (positive) forecast.",
        }

    # ---------- 2. Criterion ----------
    cond_rets = []
    all_rets = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            c_list = []
            a_list = []
            for i in range(0, n - H, H):
                c0 = close[i]
                c1 = close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                a_list.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    c_list.append(r)
            # "same coin-windows": only coin-windows holding at least one forecast > 0 block
            if len(c_list) > 0:
                cond_rets.extend(c_list)
                all_rets.extend(a_list)

    cond = np.asarray(cond_rets, dtype=float)
    allr = np.asarray(all_rets, dtype=float)
    n_cond = int(len(cond))
    n_all = int(len(allr))

    excess = None
    t_val = None
    if n_cond >= 2 and n_all >= 2:
        excess = float(cond.mean() - allr.mean())
        t_res = stats.ttest_ind(cond, allr, equal_var=False)
        t_val = float(t_res.statistic) if np.isfinite(t_res.statistic) else None
    elif n_cond >= 1 and n_all >= 1:
        excess = float(cond.mean() - allr.mean())

    hit_c = float((cond > 0).mean()) if n_cond > 0 else None
    hit_a = float((allr > 0).mean()) if n_all > 0 else None
    hit_diff = (hit_c - hit_a) if (hit_c is not None and hit_a is not None) else None
    sup_passed = None if hit_diff is None else bool(hit_diff > 0)

    if n_cond < 30:
        status = "inconclusive"
        decided_by = "Fewer than 30 non-overlapping 20-bar blocks with forecast > 0, so the result is inconclusive."
    elif t_val is None or excess is None:
        status = "inconclusive"
        decided_by = "The t-statistic could not be computed, so no confirm or reject rule is met."
    elif excess > 0 and t_val >= 2:
        status = "confirmed"
        decided_by = "The excess return is above 0 with t >= 2 over non-overlapping blocks, so the idea is confirmed."
    elif excess < 0 and t_val <= -2:
        status = "rejected"
        decided_by = "The excess return is below 0 with t <= -2, so moves during up-cross spans underperform and the idea is rejected."
    else:
        status = "inconclusive"
        decided_by = "The t-statistic lies between -2 and 2, so the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean 20-bar forward return when forecast > 0 minus mean of all blocks in same coin-windows",
            "value": excess,
            "statistic": None if t_val is None else {"name": "Welch t", "value": t_val},
            "threshold": "excess > 0 with t >= 2 confirms; excess < 0 with t <= -2 rejects; otherwise inconclusive",
        },
        "supporting_check": {
            "name": "hit rate of 20-bar returns when forecast > 0 minus unconditional hit rate",
            "value": hit_diff,
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping 20-bar blocks with forecast > 0": n_cond,
            "non-overlapping 20-bar blocks in the same coin-windows": n_all,
        },
        "decided_by": decided_by,
        "reading": ("Blocks start at positions 0, 20, 40, ... of each window with a full 20-bar return inside it; "
                    "'the same coin-windows' is read as the coin-windows holding at least one forecast > 0 block, "
                    "and the excess is tested with Welch's t between the forecast > 0 blocks and all blocks of those windows."),
    }
