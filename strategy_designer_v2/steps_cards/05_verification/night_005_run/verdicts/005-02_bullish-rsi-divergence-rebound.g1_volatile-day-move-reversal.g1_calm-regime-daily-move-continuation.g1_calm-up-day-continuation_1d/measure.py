import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.calm_up.last_history_value"

    # The idea's coins: BTC and ETH
    coins = [c for c in bars.keys() if str(c).upper().startswith("BTC") or str(c).upper().startswith("ETH")]
    coins = sorted(coins)

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin in coins:
        for w, df in bars[coin].items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            close = pd.to_numeric(d["close"], errors="coerce")
            day_ret = close / close.shift(1) - 1.0  # inside the window only
            active = fc.notna() & (fc != 0)
            # Situation: graded calm up day -> raw product > 0 (an up day with rank < 1);
            # where the day's return is computable inside the window it must also be an up day.
            up_ok = day_ret.isna() | (day_ret > 0)
            situ = raw.notna() & (raw > 0) & up_ok
            agree = active & situ & (fc > 0)  # expected side: long
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    main_name = "mean 5-bar forward return, forecast >= 2 minus all other grid bars"
    threshold = "confirm: difference > 0 with Welch t >= 2 and >= 30 cases with forecast >= 2; reject: difference < 0 with Welch t <= -2"
    reading_base = ("Situation taken as bars where the raw component is positive (and the day's in-window close-to-close return is up when computable), side long; "
                    "grid is positions 0,5,10,... of each BTC and ETH window with grid bars lacking a 5-bar forward return in the window dropped, "
                    "'all other grid bars' means grid bars with forecast < 2, and the slope is undefined (not positive) with fewer than 2 positive-forecast cases.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of the plan's situation "
                           "(a graded calm up day, long only)" if n_active > 0 else
                           "No bar has a non-zero forecast, so the config never takes the plan's situation."),
            "reading": reading_base,
        }

    # ---------- 2. Criterion ----------
    fcs = []
    rets = []
    for coin in coins:
        for w, df in bars[coin].items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            n = len(d)
            for i in range(0, n, H):
                j = i + H
                if j >= n:
                    continue
                c0, c1, f = close[i], close[j], fc[i]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 == 0:
                    continue
                fcs.append(float(f))
                rets.append(float(c1 / c0 - 1.0))

    fcs = np.array(fcs, dtype=float)
    rets = np.array(rets, dtype=float)
    hi = fcs >= 2
    r_hi = rets[hi]
    r_lo = rets[~hi]
    n_hi = int(hi.sum())
    n_lo = int((~hi).sum())
    pos = fcs > 0
    n_pos = int(pos.sum())

    diff = None
    t = None
    if n_hi >= 1 and n_lo >= 1:
        diff = float(np.mean(r_hi) - np.mean(r_lo))
    if n_hi >= 2 and n_lo >= 2:
        tt = stats.ttest_ind(r_hi, r_lo, equal_var=False)
        t = float(tt.statistic) if np.isfinite(tt.statistic) else None

    slope = None
    if n_pos >= 2 and np.ptp(fcs[pos]) > 0:
        lr = stats.linregress(fcs[pos], rets[pos])
        slope = float(lr.slope) if np.isfinite(lr.slope) else None
    slope_pass = bool(slope is not None and slope > 0)

    counts = {
        "cases with forecast >= 2": n_hi,
        "other grid bars": n_lo,
        "grid bars with forecast > 0": n_pos,
    }

    if n_hi < 30:
        status = "not observable"
        decided = f"Fewer than 30 cases with forecast >= 2 ({n_hi}), the plan's minimum count, so the data could not show the idea."
    elif t is None or diff is None:
        status = "inconclusive"
        decided = "Welch t could not be computed (too few other grid bars or zero variance), which meets neither the confirm nor the reject rule."
    elif diff > 0 and t >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "The difference is positive with Welch t >= 2 from at least 30 cases with forecast >= 2, and the supporting slope is positive."
        else:
            status = "inconclusive"
            decided = "Welch t >= 2 while the supporting slope among forecast > 0 grid bars is not positive."
    elif diff < 0 and t <= -2:
        status = "rejected"
        decided = "The difference is negative with Welch t <= -2 from at least 30 cases with forecast >= 2."
    else:
        status = "inconclusive"
        decided = "Welch t is between -2 and 2 (or its sign disagrees with the difference), meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": diff,
            "statistic": {"name": "Welch t", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "OLS slope of 5-bar forward return on forecast, grid bars with forecast > 0",
            "value": slope,
            "passed": slope_pass if slope is not None else (False if n_pos >= 0 else None),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
