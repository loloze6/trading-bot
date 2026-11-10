import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    ALLOC = "postRebalance_current_allocation"
    rows = []  # (excess, raw_next_ret, position, window, timestamp)

    for coin in sorted(bars.keys()):
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0  # next-bar return inside this window only
            # coin's mean daily return over all bars of this window
            m = nxt.dropna().mean() if nxt.notna().any() else np.nan
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            pos = pd.to_numeric(df[ALLOC], errors="coerce")
            ts = df["timestamp"]
            for i in range(len(df)):
                if pd.isna(fc.iloc[i]) or pd.isna(nxt.iloc[i]) or pd.isna(pos.iloc[i]) or pd.isna(m):
                    continue
                if fc.iloc[i] > 0:
                    rows.append((float(nxt.iloc[i] - m), float(nxt.iloc[i]), float(pos.iloc[i]),
                                 f"{coin}:{window}", ts.iloc[i]))

    n = len(rows)
    main_value = None
    main_t = None
    if n > 0:
        x = np.array([r[0] for r in rows], dtype=float)
        w = np.array([r[2] for r in rows], dtype=float)
        sw = w.sum()
        if sw != 0:
            mu = float(np.sum(w * x) / sw)
            main_value = mu
            if n > 1:
                se = float(np.sqrt(np.sum((w ** 2) * (x - mu) ** 2)) / abs(sw))
                se *= np.sqrt(n / (n - 1.0))
                if se > 0:
                    main_t = mu / se

    # Supporting check: top third vs bottom third of positions on active bars
    sup_diff = None
    sup_t = None
    k = n // 3
    if k >= 2:
        order = sorted(range(n), key=lambda i: (rows[i][2], str(rows[i][4]), rows[i][3]))
        bottom = np.array([rows[i][1] for i in order[:k]], dtype=float)
        top = np.array([rows[i][1] for i in order[-k:]], dtype=float)
        sup_diff = float(top.mean() - bottom.mean())
        tt = stats.ttest_ind(top, bottom, equal_var=False)
        if np.isfinite(tt.statistic):
            sup_t = float(tt.statistic)
    sup_passed = None if sup_diff is None else bool(sup_diff > 0)

    if n < 60:
        status = "inconclusive"
        decided = f"Only {n} active bars, fewer than the 60 required, so the test is inconclusive."
    elif main_value is None:
        status = "inconclusive"
        decided = "The position-weighted mean could not be computed (zero total position), so the test is inconclusive."
    elif main_value <= 0:
        status = "rejected"
        decided = "The position-weighted mean next-bar excess return is <= 0, which meets the reject rule."
    elif sup_diff is not None and sup_diff < 0 and sup_t is not None and sup_t <= -2:
        status = "rejected"
        decided = "The top third of positions has a lower next-bar return than the bottom third with t <= -2, which meets the reject rule."
    elif main_t is not None and main_t >= 2 and sup_passed is True:
        status = "confirmed"
        decided = "The pooled position-weighted mean next-bar excess return is above 0 with t >= 2 and the top-minus-bottom-third difference has the same sign, which meets the confirm rule."
    elif sup_passed is False:
        status = "inconclusive"
        decided = "The main measure is positive but the supporting check has the opposite sign, which meets the inconclusive rule."
    else:
        status = "inconclusive"
        decided = "The excess return is positive but t < 2 (or the supporting check could not be computed), which meets the inconclusive rule."

    return {
        "status": status,
        "main_measure": {
            "name": "position-weighted mean next-bar excess return on active bars",
            "value": main_value,
            "threshold": "above 0 with t >= 2 to confirm; <= 0 rejects",
            "t_stat": main_t,
        },
        "supporting_check": {
            "name": "top-third minus bottom-third positions mean next-bar return",
            "value": sup_diff,
            "passed": sup_passed,
            "t_stat": sup_t,
        },
        "cases": int(n),
        "decided_by": decided,
        "reading": (
            "Active bars are forecast > 0 with the position taken as postRebalance_current_allocation; excess is the next-bar return minus that window's mean next-bar return over all its bars; "
            "the weighted mean's t uses a heteroskedasticity-robust weighted standard error pooled over all windows; "
            "thirds are n//3 active bars ranked by position, compared on raw next-bar return with a Welch t-test; and the 60-bar minimum is checked before the other rules."
        ),
    }
