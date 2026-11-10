import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    POS = "postRebalance_current_allocation"
    MIN_ACTIVE = 60

    all_rets = []
    act_ret = []
    act_pos = []

    for coin in bars:
        for window in bars[coin]:
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0  # inside this window only
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            pos = pd.to_numeric(df[POS], errors="coerce")

            # horizon 1 bar: grid 0,1,2,... = every bar, no overlap
            ok_all = nxt.notna() & np.isfinite(nxt)
            all_rets.extend(nxt[ok_all].tolist())

            ok_act = ok_all & fc.notna() & (fc > 0) & pos.notna()
            act_ret.extend(nxt[ok_act].tolist())
            act_pos.extend(pos[ok_act].tolist())

    all_rets = np.asarray(all_rets, float)
    r = np.asarray(act_ret, float)
    w = np.asarray(act_pos, float)
    n_active = int(len(r))

    baseline = float(np.mean(all_rets)) if len(all_rets) else np.nan
    excess = r - baseline

    # Position-weighted mean excess return; t as ordinary t of the mean of w_i*x_i/mean(w)
    main_val, main_t = None, None
    if n_active >= 2 and np.sum(w) != 0 and np.isfinite(baseline):
        main_val = float(np.sum(w * excess) / np.sum(w))
        z = w * excess / np.mean(w)
        sd = np.std(z, ddof=1)
        if sd > 0:
            main_t = float(np.mean(z) / (sd / np.sqrt(n_active)))

    # Supporting check: top third minus bottom third of positions, next-bar return, Welch t
    supp_diff, supp_t, n_third = None, None, n_active // 3
    if n_third >= 2:
        order = np.argsort(w, kind="mergesort")
        bottom = r[order[:n_third]]
        top = r[order[-n_third:]]
        supp_diff = float(np.mean(top) - np.mean(bottom))
        tt = stats.ttest_ind(top, bottom, equal_var=False)
        if np.isfinite(tt.statistic):
            supp_t = float(tt.statistic)

    supp_passed = None if supp_diff is None else bool(supp_diff > 0)

    if n_active < MIN_ACTIVE:
        status = "inconclusive"
        decided = f"Only {n_active} active bars, fewer than the 60 needed, so the test is inconclusive."
    elif main_val is None:
        status = "inconclusive"
        decided = "The position-weighted mean excess return could not be computed (zero total position), so the test is inconclusive."
    elif main_val <= 0:
        status = "rejected"
        decided = "The position-weighted mean next-bar excess return is <= 0, which meets the reject rule."
    elif supp_t is not None and supp_diff is not None and supp_diff < 0 and supp_t <= -2:
        status = "rejected"
        decided = "The top third of positions has a lower next-bar return than the bottom third with t <= -2, which meets the reject rule."
    elif main_t is not None and main_t >= 2 and supp_diff is not None and supp_diff > 0:
        status = "confirmed"
        decided = "The pooled position-weighted mean excess return is above 0 with t >= 2 and the top-minus-bottom-third check is positive, which meets the confirm rule."
    elif supp_diff is not None and supp_diff <= 0:
        status = "inconclusive"
        decided = "The main measure is positive but the supporting check has the opposite sign, which meets the inconclusive rule."
    else:
        status = "inconclusive"
        decided = "The excess return is positive but its t is below 2 (or not computable), which meets the inconclusive rule."

    return {
        "status": status,
        "main_measure": {
            "name": "position-weighted mean next-bar excess return over coin mean daily return",
            "value": main_val,
            "statistic": None if main_t is None else {"name": "t of the weighted mean", "value": main_t},
            "threshold": "above 0 with t >= 2 to confirm; <= 0 rejects",
        },
        "supporting_check": {
            "name": "next-bar return, top third minus bottom third of positions on active bars (Welch t)",
            "value": supp_diff,
            "passed": supp_passed,
        },
        "counts": {
            "active bars": n_active,
            "all bars": int(len(all_rets)),
            "bars per third": int(n_third),
            "supporting Welch t": supp_t if supp_t is not None else float("nan"),
        },
        "decided_by": decided,
        "reading": (
            "Active bars are forecast > 0 pooled over all windows, weighted by postRebalance_current_allocation "
            "(zero-position active bars get zero weight); the benchmark is the mean next-bar return over all bars "
            "of all windows pooled; the weighted-mean t is the ordinary t of w_i*x_i/mean(w); thirds are the lowest "
            "and highest floor(n/3) positions."
        ),
    }
