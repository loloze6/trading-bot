import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    MIN_BLOCKS = 15
    MIN_CROSSES = 8

    def find_raw_col(df):
        preferred = "debug_info.components.ma_dist.last_history_value"
        if preferred in df.columns:
            return preferred
        cands = [c for c in df.columns
                 if c.startswith("debug_info.components.") and c.endswith(".last_history_value")]
        return cands[0] if cands else None

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    raw_col_used = None
    for coin, wins in bars.items():
        for w, df in wins.items():
            col = find_raw_col(df)
            if col is None:
                continue
            raw_col_used = col
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[col], errors="coerce")
            ok = f.notna() & raw.notna()
            active = ok & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & (raw > 0) & (f > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    threshold_txt = "difference > 0 with Welch t >= 2 across non-overlapping 20-bar blocks"
    main_name = "mean 20-bar fwd return in position minus all bars (non-overlapping)"
    reading = ("Close above SMA200 taken as the raw component value > 0 (column "
               f"{raw_col_used}); the all-bars group is every grid bar (positions 0,20,40,... per window) "
               "and Welch's t compares it with the in-position grid bars; up-crosses are bars with forecast > 0 "
               "whose previous bar in the same window had forecast 0, counted only when their 20-bar forward "
               "return exists, and the unconditional share of positive returns uses all bars with a 20-bar "
               "forward return.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars with the close "
                           "above its SMA200 as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    in_rets, all_rets = [], []
    cross_rets = []
    uncond_rets = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:n - H] = close[H:] / close[:n - H] - 1.0
            # non-overlapping grid
            for i in range(0, n, H):
                r = fwd[i]
                if not np.isfinite(r):
                    continue
                all_rets.append(r)
                if np.isfinite(f[i]) and f[i] > 0:
                    in_rets.append(r)
            # unconditional share (all bars with a valid forward return)
            uncond_rets.extend([r for r in fwd if np.isfinite(r)])
            # up-crosses
            for i in range(1, n):
                if np.isfinite(f[i - 1]) and np.isfinite(f[i]) and f[i - 1] == 0 and f[i] > 0:
                    if np.isfinite(fwd[i]):
                        cross_rets.append(fwd[i])

    in_rets = np.array(in_rets)
    all_rets = np.array(all_rets)
    cross_rets = np.array(cross_rets)
    uncond_rets = np.array(uncond_rets)

    n_blocks = int(len(in_rets))
    n_cross = int(len(cross_rets))

    diff = None
    t_val = None
    if len(in_rets) >= 2 and len(all_rets) >= 2:
        diff = float(in_rets.mean() - all_rets.mean())
        t = stats.ttest_ind(in_rets, all_rets, equal_var=False).statistic
        t_val = float(t) if np.isfinite(t) else None
    elif len(in_rets) >= 1 and len(all_rets) >= 1:
        diff = float(in_rets.mean() - all_rets.mean())

    share_cross = float((cross_rets > 0).mean()) if n_cross > 0 else None
    share_uncond = float((uncond_rets > 0).mean()) if len(uncond_rets) > 0 else None
    mean_cross = float(cross_rets.mean()) if n_cross > 0 else None
    sup_value = (share_cross - share_uncond) if (share_cross is not None and share_uncond is not None) else None
    sup_passed = (bool(sup_value > 0) if sup_value is not None else None)

    if n_blocks < MIN_BLOCKS or n_cross < MIN_CROSSES:
        status = "inconclusive"
        decided = (f"Fewer than {MIN_BLOCKS} non-overlapping in-position blocks or fewer than {MIN_CROSSES} "
                   "up-crosses, so the test neither confirms nor rejects.")
    elif diff is None:
        status = "inconclusive"
        decided = "The difference could not be computed, so the test neither confirms nor rejects."
    elif diff <= 0 or (mean_cross is not None and mean_cross < 0):
        status = "rejected"
        if diff <= 0:
            decided = "The in-position minus all-bars difference is <= 0, which the plan rejects."
        else:
            decided = "The 20-bar forward returns after up-crosses are on average negative (reversal), which the plan rejects."
    elif t_val is not None and t_val >= 2 and sup_passed:
        status = "confirmed"
        decided = ("The difference is above 0 with t >= 2 and the share of up-crosses followed by a positive "
                   "20-bar return exceeds the unconditional share, which the plan confirms.")
    else:
        status = "inconclusive"
        if t_val is None or t_val < 2:
            decided = "The difference is positive but t < 2, which the plan calls inconclusive."
        else:
            decided = ("The main measure is positive with t >= 2 but the supporting check fails, so they disagree "
                       "and the plan calls it inconclusive.")

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name,
                         "value": diff,
                         "statistic": ({"name": "Welch t", "value": t_val} if t_val is not None else None),
                         "threshold": threshold_txt},
        "supporting_check": {"name": "share of positive 20-bar returns after up-crosses minus unconditional share",
                             "value": sup_value,
                             "passed": sup_passed},
        "counts": {"non-overlapping in-position blocks": n_blocks,
                   "up-crosses": n_cross},
        "decided_by": decided,
        "reading": reading,
    }
