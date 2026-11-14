import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.drop.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df[FC], errors="coerce") if FC in df else pd.Series(np.nan, index=df.index)
            close = pd.to_numeric(df["close"], errors="coerce")
            ret1 = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), ret1)
            else:
                raw = ret1
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw < 0) & (fc > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    threshold_txt = ("confirm if hit-rate excess > 0 with z >= 2, reject if excess < 0 with z <= -2, "
                     "over at least 100 qualifying bars; otherwise inconclusive")
    main_name = "share of positive next-bar returns on bars with forecast >= 16 minus all-bar share, pooled over coins"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"qualifying bars": None},
            "decided_by": ("The plan's situation is a long position after a daily drop (negative one-day return), "
                           "but fewer than 90% of the active forecast bars are long bars after a drop."),
            "reading": "Situation taken as any bar whose one-day return is negative with a positive forecast, since the plan makes the drop threshold graded.",
        }

    # ---------- 2. Criterion ----------
    q_rets = []
    all_rets = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df[FC], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            ok = nxt.notna() & np.isfinite(nxt)
            all_rets.append(nxt[ok].values)
            q = ok & fc.notna() & (fc >= 16)
            q_rets.append(nxt[q].values)
    q_rets = np.concatenate(q_rets) if q_rets else np.array([])
    all_rets = np.concatenate(all_rets) if all_rets else np.array([])

    n_q = int(len(q_rets))
    n_all = int(len(all_rets))
    counts = {"qualifying bars": n_q}

    p_q = float(np.mean(q_rets > 0)) if n_q > 0 else None
    p_all = float(np.mean(all_rets > 0)) if n_all > 0 else None
    excess = (p_q - p_all) if (p_q is not None and p_all is not None) else None

    z = None
    if n_q > 0 and n_all > 0:
        x1 = np.sum(q_rets > 0)
        x2 = np.sum(all_rets > 0)
        pp = (x1 + x2) / (n_q + n_all)
        se = np.sqrt(pp * (1 - pp) * (1.0 / n_q + 1.0 / n_all))
        z = float((p_q - p_all) / se) if se > 0 else 0.0

    sup_val, sup_t = None, None
    if n_q >= 2 and n_all >= 2:
        sup_val = float(np.mean(q_rets) - np.mean(all_rets))
        t = stats.ttest_ind(q_rets, all_rets, equal_var=False).statistic
        sup_t = float(t) if np.isfinite(t) else None
    elif n_q >= 1 and n_all >= 1:
        sup_val = float(np.mean(q_rets) - np.mean(all_rets))

    if n_q < 100:
        status = "not observable"
        decided = f"The plan's minimum of 100 qualifying bars (forecast >= 16) is not reached ({n_q})."
    elif excess is not None and z is not None and excess > 0 and z >= 2:
        status = "confirmed"
        decided = "Confirm rule met: the hit-rate excess is positive with z >= 2 over at least 100 qualifying bars."
    elif excess is not None and z is not None and excess < 0 and z <= -2:
        status = "rejected"
        decided = "Reject rule met: the hit-rate excess is negative with z <= -2 over at least 100 qualifying bars."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule met: z is strictly between -2 and 2 with at least 100 qualifying bars."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": excess,
            "statistic": {"name": "two-proportion z (pooled variance)", "value": z} if z is not None else None,
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "mean next-bar return on qualifying bars minus mean of all bars (Welch t)",
            "value": sup_val,
            "t_statistic": sup_t,
            "passed": None,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Qualifying bars and the baseline (all bars with a next close in the same window) are each pooled over all coins "
                    "and windows, a positive return is strictly > 0, the baseline includes the qualifying bars, the supporting check "
                    "has no threshold so its passed is null, and the plan's '<100 bars' case is reported as not observable per the instructions."),
    }
