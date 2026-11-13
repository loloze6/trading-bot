import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.drop.last_history_value"
    THRESH = 16.0
    MIN_N = 100

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    qual_rets = []
    all_rets = []

    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys(), key=lambda s: int(str(s).lstrip("w")) if str(s).lstrip("w").isdigit() else str(s)):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").astype(float).reset_index(drop=True)
            fc = pd.to_numeric(df[FC], errors="coerce").astype(float).reset_index(drop=True)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").astype(float).reset_index(drop=True)
            else:
                raw = pd.Series(np.nan, index=close.index)
            # fallback to the price's own one-day return where the raw value is missing
            own_ret = close / close.shift(1) - 1.0
            raw = raw.where(raw.notna(), own_ret)

            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            situation = raw < 0  # a drop day (only drops count)
            agree = active & situation & (fc > 0)  # long side expected
            n_agree += int(agree.sum())

            # next-bar close-to-close return inside the window
            nxt = close.shift(-1) / close - 1.0
            valid = nxt.notna()
            all_rets.append(nxt[valid].values)
            q = valid & fc.notna() & (fc >= THRESH)
            qual_rets.append(nxt[q].values)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "hit rate of next-bar return on bars with forecast >= 16 minus pooled all-bar hit rate"
    thr_txt = "confirm if excess > 0 with z >= 2, reject if excess < 0 with z <= -2, over at least 100 qualifying bars"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_txt},
            "supporting_check": None,
            "counts": {"qualifying bars": None, "active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a nonzero forecast are drop days with a long forecast, so the config does not hold the plan's situation (drops) on its side (long).",
            "reading": "The situation is read as a drop day (negative one-day return, the sign of the component's raw value) with a positive (long) forecast.",
        }

    qr = np.concatenate(qual_rets) if qual_rets else np.array([])
    ar = np.concatenate(all_rets) if all_rets else np.array([])
    n1 = int(len(qr))
    n2 = int(len(ar))

    value = None
    z = None
    sup_val = None
    sup_t = None
    if n1 > 0 and n2 > 0:
        p1 = float(np.mean(qr > 0))
        p2 = float(np.mean(ar > 0))
        value = p1 - p2
        pp = (np.sum(qr > 0) + np.sum(ar > 0)) / (n1 + n2)
        se = np.sqrt(pp * (1 - pp) * (1.0 / n1 + 1.0 / n2))
        z = float(value / se) if se > 0 else None
        sup_val = float(np.mean(qr) - np.mean(ar))
        if n1 > 1 and n2 > 1:
            t_res = stats.ttest_ind(qr, ar, equal_var=False)
            sup_t = float(t_res.statistic) if np.isfinite(t_res.statistic) else None

    if n1 < MIN_N:
        status = "not observable"
        decided = f"Only {n1} qualifying bars (forecast >= 16), fewer than the plan's minimum of 100."
    elif z is not None and value > 0 and z >= 2:
        status = "confirmed"
        decided = "The hit-rate excess is positive with z >= 2 over at least 100 qualifying bars (confirm rule)."
    elif z is not None and value < 0 and z <= -2:
        status = "rejected"
        decided = "The hit-rate excess is negative with z <= -2 over at least 100 qualifying bars (reject rule)."
    else:
        status = "inconclusive"
        decided = "The z of the hit-rate excess lies strictly between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": None if value is None else float(value),
            "statistic": None if z is None else {"name": "two-proportion z (pooled)", "value": float(z)},
            "threshold": thr_txt,
        },
        "supporting_check": {
            "name": "mean next-bar return on qualifying bars minus pooled all-bar mean daily return (Welch t = %s)" % (
                "nan" if sup_t is None else "%.3f" % sup_t),
            "value": sup_val,
            "passed": None if sup_val is None else bool(sup_val > 0),
        },
        "counts": {"qualifying bars": n1, "all bars": n2},
        "decided_by": decided,
        "reading": "The baseline hit rate and mean are pooled over every bar with a next-bar return in all windows of all coins, the qualifying bars are pooled over all coins, the two-proportion z uses the pooled-proportion standard error, the supporting difference uses Welch's t and counts as passed when positive (the plan gives it no threshold), and the situation check counts a drop day (negative raw one-day value) with a positive forecast.",
    }
