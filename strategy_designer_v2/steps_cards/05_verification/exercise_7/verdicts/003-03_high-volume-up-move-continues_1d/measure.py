import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    UP_COL = "debug_info.components.up_move.last_history_value"
    POS_COL = "postRebalance_current_allocation"

    # ---------- 1. Situation check ----------
    n_active_checked = 0
    n_agree = 0
    pooled_rows = []
    all_next_rets = []

    for coin in sorted(bars.keys()):
        for win in sorted(bars[coin].keys()):
            df = bars[coin][win].copy().reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")

            # Use the component's raw one-day move, or the close-to-close change if it is missing.
            if UP_COL in df.columns:
                move = pd.to_numeric(df[UP_COL], errors="coerce")
                move = move.where(move.notna(), close.pct_change())
            else:
                move = close.pct_change()

            # The 20-day mean volume includes the current bar.
            vol_mean = vol.rolling(20, min_periods=20).mean()
            situation = (move > 0) & (vol >= vol_mean)
            evaluable = move.notna() & vol_mean.notna() & vol.notna()

            active = fc.notna() & (fc != 0)
            chk = active & evaluable
            n_active_checked += int(chk.sum())
            n_agree += int((chk & situation & (fc > 0)).sum())

            # Next-bar return, computed inside this window only.
            nxt = close.shift(-1) / close - 1.0
            all_next_rets.append(nxt.dropna().values)

            pos = pd.to_numeric(df[POS_COL], errors="coerce") if POS_COL in df.columns else pd.Series(np.nan, index=df.index)
            sel = (fc > 0) & nxt.notna() & pos.notna()
            for i in df.index[sel]:
                pooled_rows.append((float(nxt[i]), float(pos[i])))

    agreement = (n_agree / n_active_checked) if n_active_checked > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("The situation is the up_move raw value > 0 (close-to-close change if missing) with volume >= the "
               "rolling 20-bar mean volume including the current bar, and active bars lacking 20 bars of volume "
               "history are left out of the agreement; the benchmark is the pooled mean of all next-bar returns "
               "over the 6 windows; the t of the position-weighted mean is the ordinary t of "
               "position*excess/mean(position); the thirds are the pooled active bars ranked by "
               "postRebalance_current_allocation (n//3 each); the supporting check is top minus bottom with "
               "Welch t.")

    threshold_txt = "position-weighted mean next-bar excess return > 0 with t >= 2 to confirm; <= 0 to reject"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "position-weighted mean next-bar excess return", "value": None,
                             "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active_checked)},
            "decided_by": ("Fewer than 90% of active bars are long bars with a one-day rise on volume at or above "
                           "the 20-day mean, so the config does not trade the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    allr = np.concatenate(all_next_rets) if all_next_rets else np.array([])
    mu = float(np.mean(allr)) if allr.size else np.nan

    n_active = len(pooled_rows)
    r = np.array([x[0] for x in pooled_rows], dtype=float)
    w = np.array([x[1] for x in pooled_rows], dtype=float)
    ex = r - mu

    main_val, t_main = None, None
    if n_active > 1 and np.sum(w) > 0:
        main_val = float(np.sum(w * ex) / np.sum(w))
        z = w * ex / np.mean(w)
        sd = np.std(z, ddof=1)
        t_main = float(np.mean(z) / (sd / np.sqrt(len(z)))) if sd > 0 else None

    # Supporting check: top third minus bottom third of positions.
    diff, t_sup = None, None
    k = n_active // 3
    if k >= 2:
        order = np.argsort(w, kind="mergesort")
        bot = r[order[:k]]
        top = r[order[-k:]]
        diff = float(np.mean(top) - np.mean(bot))
        tt = stats.ttest_ind(top, bot, equal_var=False)
        t_sup = float(tt.statistic) if np.isfinite(tt.statistic) else None

    sup_passed = None if diff is None else bool(diff > 0)

    if n_active < 60:
        status = "inconclusive"
        decided = f"Only {n_active} active bars, fewer than the 60 required, so the test is inconclusive."
    elif main_val is None:
        status = "inconclusive"
        decided = "The position-weighted main measure cannot be computed, so the test is inconclusive."
    elif main_val <= 0:
        status = "rejected"
        decided = "The position-weighted mean next-bar excess return is <= 0, which meets the reject rule."
    elif diff is not None and diff < 0 and t_sup is not None and t_sup <= -2:
        status = "rejected"
        decided = ("The top third of positions has a lower next-bar return than the bottom third with "
                   "t <= -2, which meets the reject rule.")
    elif t_main is not None and t_main >= 2 and diff is not None and diff > 0:
        status = "confirmed"
        decided = ("The pooled position-weighted mean next-bar excess return is > 0 with t >= 2, and the "
                   "top-minus-bottom-third return is positive, which meets the confirm rule.")
    elif diff is not None and diff < 0:
        status = "inconclusive"
        decided = ("The main measure is positive but the supporting check has the opposite sign, which meets "
                   "the inconclusive rule.")
    else:
        status = "inconclusive"
        decided = ("The excess return is positive but t < 2 (or the supporting check is undetermined), "
                   "which meets the inconclusive rule.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "position-weighted mean next-bar excess return",
            "value": main_val,
            "statistic": None if t_main is None else {"name": "t of the weighted mean", "value": t_main},
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "next-bar return, top third minus bottom third of positions",
            "value": diff,
            "passed": sup_passed,
        },
        "counts": {"active bars": int(n_active)},
        "decided_by": decided,
        "reading": reading,
    }
