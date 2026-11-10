import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    POS = "postRebalance_current_allocation"
    MIN_ACTIVE = 60

    rows = []  # (excess, raw_next_ret, position)
    for coin, windows in bars.items():
        for wname, df in windows.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0  # inside this window only
            base_vals = nxt.dropna()
            if len(base_vals) == 0:
                continue
            base = float(base_vals.mean())  # coin's mean daily return over all bars of this window
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            pos = pd.to_numeric(d[POS], errors="coerce")
            mask = (fc > 0) & nxt.notna() & pos.notna()
            for i in np.where(mask.values)[0]:
                r = float(nxt.iloc[i])
                rows.append((r - base, r, float(pos.iloc[i])))

    n_active = len(rows)
    counts = {"active bars": int(n_active)}

    main_val = None
    main_t = None
    if n_active > 0:
        ex = np.array([r[0] for r in rows])
        w = np.array([r[2] for r in rows])
        sw = w.sum()
        if sw > 0:
            m = float((w * ex).sum() / sw)
            main_val = m
            if n_active > 1:
                se = np.sqrt((w ** 2 * (ex - m) ** 2).sum()) / sw * np.sqrt(n_active / (n_active - 1))
                if se > 0 and np.isfinite(se):
                    main_t = float(m / se)

    supp_val = None
    supp_t = None
    if n_active >= 3:
        order = sorted(range(n_active), key=lambda i: (rows[i][2], i))
        k = n_active // 3
        bottom = np.array([rows[i][1] for i in order[:k]])
        top = np.array([rows[i][1] for i in order[-k:]])
        if k >= 1:
            supp_val = float(top.mean() - bottom.mean())
            if k >= 2:
                tt = stats.ttest_ind(top, bottom, equal_var=False)
                if np.isfinite(tt.statistic):
                    supp_t = float(tt.statistic)

    supp_passed = None if supp_val is None else bool(supp_val > 0)

    if n_active < MIN_ACTIVE:
        status = "inconclusive"
        decided = f"Only {n_active} active bars, fewer than the 60 needed, so the test is inconclusive."
    elif main_val is None:
        status = "inconclusive"
        decided = "The position-weighted main measure could not be computed (no positive position weight), so the test is inconclusive."
    elif main_val <= 0:
        status = "rejected"
        decided = "The position-weighted mean next-bar excess return is <= 0, which meets the reject rule."
    elif supp_val is not None and supp_val < 0 and supp_t is not None and supp_t <= -2:
        status = "rejected"
        decided = "The top third of positions has a lower next-bar return than the bottom third with t <= -2, which meets the reject rule."
    elif main_t is not None and main_t >= 2 and supp_val is not None and supp_val > 0:
        status = "confirmed"
        decided = "Pooled over the windows, the position-weighted mean next-bar excess return is above 0 with t >= 2 and the top-minus-bottom-third check has the same sign, which meets the confirm rule."
    elif main_t is None or main_t < 2:
        status = "inconclusive"
        decided = "The excess return is positive but its t is below 2, which meets the inconclusive rule."
    else:
        status = "inconclusive"
        decided = "The main measure is positive with t >= 2 but the supporting check does not have the same sign, which meets the inconclusive rule."

    return {
        "status": status,
        "main_measure": {
            "name": "position-weighted mean next-bar excess return on active bars",
            "value": main_val,
            "statistic": None if main_t is None else {"name": "t of the weighted mean", "value": main_t},
            "threshold": "above 0 with t >= 2 to confirm; <= 0 rejects",
        },
        "supporting_check": {
            "name": "top-third minus bottom-third positions, mean next-bar return",
            "value": supp_val,
            "passed": supp_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": (
            "Position is postRebalance_current_allocation; excess is each active bar's next-bar return minus the mean "
            "next-bar return of all bars in its own window; the t of the weighted mean uses the weighted standard error "
            "sqrt(sum w^2 (x-m)^2)/sum w times sqrt(n/(n-1)); the thirds are the n//3 largest and n//3 smallest positions "
            "among pooled active bars (ties broken by order), compared on unweighted raw next-bar returns with Welch t."
        ),
    }
