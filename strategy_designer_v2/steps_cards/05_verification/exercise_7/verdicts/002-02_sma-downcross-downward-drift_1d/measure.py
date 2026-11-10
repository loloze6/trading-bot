import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    COMP = "debug_info.components.sma_cross_down.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation (adapted): SMA50 below SMA200, i.e. raw spread (SMA50-SMA200)/SMA200 < 0; expected side: short.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if COMP not in df.columns or "forecast" not in df.columns:
                continue
            sub = df[["forecast", COMP]].dropna()
            active = sub["forecast"] != 0
            n_active += int(active.sum())
            ok = active & (sub[COMP] < 0) & (sub["forecast"] < 0)
            n_agree += int(ok.sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.90
    else:
        agreement = None
        passed = True

    main_name = "mean 10-bar forward return on short bars minus mean over all bars (non-overlapping blocks)"
    threshold = "difference <= -1.0% per 10 bars with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active_bars": int(n_active), "active_bars_in_situation_on_short_side": int(n_agree)},
            "decided_by": "Fewer than 90% of active (non-zero forecast) bars are short bars with SMA50 below SMA200 "
                          "(raw spread < 0), so the config does not trade the plan's situation on its side.",
            "reading": "Situation taken as last_history_value (SMA50-SMA200)/SMA200 < 0 with forecast < 0 on every bar with a non-zero forecast.",
        }

    # ---------- 2. Criterion ----------
    all_rets = []
    short_rets = []
    n_crosses = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].to_numpy(dtype=float)
            fc = df["forecast"].to_numpy(dtype=float)
            n = len(df)
            for p in range(0, n, H):
                if p + H >= n:
                    break
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if np.isfinite(fc[p]) and fc[p] < 0:
                    short_rets.append(r)
            # distinct downward crosses: spread goes from >= 0 to < 0 between consecutive rows of a window
            if COMP in df.columns:
                s = df[COMP].to_numpy(dtype=float)
                for i in range(1, n):
                    if np.isfinite(s[i - 1]) and np.isfinite(s[i]) and s[i - 1] >= 0 and s[i] < 0:
                        n_crosses += 1

    all_rets = np.array(all_rets, dtype=float)
    short_rets = np.array(short_rets, dtype=float)
    n_short = len(short_rets)
    n_all = len(all_rets)

    diff = None
    tval = None
    share_diff_pts = None
    if n_short > 0 and n_all > 0:
        diff = float(short_rets.mean() - all_rets.mean())
        share_short = float((short_rets < 0).mean())
        share_all = float((all_rets < 0).mean())
        share_diff_pts = (share_short - share_all) * 100.0
    if n_short >= 2 and n_all >= 2:
        t = stats.ttest_ind(short_rets, all_rets, equal_var=False).statistic
        tval = float(t) if np.isfinite(t) else None

    sup_passed = None if share_diff_pts is None else bool(share_diff_pts >= 10.0)

    if n_short < 12 or n_crosses < 2 or diff is None:
        status = "inconclusive"
        decided = (f"Inconclusive: {n_short} non-overlapping 10-bar short blocks (minimum 12) and "
                   f"{n_crosses} distinct downward crosses (minimum 2).")
    elif diff <= -0.01 and tval is not None and tval <= -2 and share_diff_pts >= 10.0:
        status = "confirmed"
        decided = "Confirmed: difference <= -1.0% per 10 bars, t <= -2, and falling share on short bars exceeds the unconditional share by >= 10 points."
    elif diff >= 0 or share_diff_pts <= 0:
        status = "rejected"
        decided = "Rejected: the difference is 0 or above, or the falling share on short bars is not above the unconditional share."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the difference lies between -1.0% and 0, or |t| < 2, or the falling-share excess is below 10 points without a reject condition."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": None if diff is None else diff * 100.0,
            "statistic": None if tval is None else {"name": "Welch t (short blocks vs all blocks)", "value": tval},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "falling share on short blocks minus falling share on all blocks (points)",
            "value": share_diff_pts,
            "passed": sup_passed,
        },
        "counts": {
            "non_overlapping_10bar_short_blocks": int(n_short),
            "non_overlapping_10bar_all_blocks": int(n_all),
            "distinct_downward_crosses": int(n_crosses),
        },
        "decided_by": decided,
        "reading": ("Short bars are grid bars (positions 0,10,20,... of each window) with forecast < 0, compared with all grid bars "
                    "via Welch t, value in percent per 10 bars; a downward cross is a bar whose raw spread is < 0 after a bar with "
                    "spread >= 0 in the same window; minimum counts are checked first, then confirm, then reject."),
    }
