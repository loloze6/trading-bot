import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    MIN_CASES = 30
    T_THR = 2.0
    RAW = "debug_info.components.vol30_vs_year.last_history_value"

    # ---------- 1. Situation check ----------
    n_active_checked = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            reg = d["regime"].astype(str)
            raw = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else pd.Series(np.nan, index=d.index)
            # 30-bar price evolution, inside the window only
            ret30 = close / close.shift(30) - 1.0
            active = fc != 0
            for i in np.where(active.values)[0]:
                r30 = ret30.iloc[i]
                if not np.isfinite(r30):
                    continue  # 30-day return not computable inside this window
                n_active_checked += 1
                in_situation = (r30 < 0) and (reg.iloc[i] == "mean_reversion")
                rv = raw.iloc[i]
                side_ok = bool(np.isfinite(rv) and rv != 0 and np.sign(rv) == np.sign(fc.iloc[i]))
                if in_situation and side_ok:
                    n_agree += 1

    agreement = (n_agree / n_active_checked) if n_active_checked > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading_check = ("The situation is checked on active bars whose 30-bar return can be computed inside their window "
                     "(30-bar return < 0 from closes, with the falling-calm profile taken from the recorded regime "
                     "'mean_reversion' since its components are not recorded), and the expected side is the sign of the raw "
                     "log volume ratio (heavier than the 365-bar mean = long)")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean 5-bar forward return, heavy minus quiet volume",
                             "value": None, "statistic": None,
                             "threshold": "difference > 0 with Welch t >= 2 confirms; < 0 with t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active_checked), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90 % of active bars are in the plan's situation (30-day fall, falling calm) with the "
                           "forecast's sign equal to the sign of the log volume ratio against its year mean."),
            "reading": reading_check + ".",
        }

    # ---------- 2. Criterion ----------
    heavy, quiet = [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            reg = d["regime"].astype(str).values
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                f = fc[i]
                if not np.isfinite(f) or f == 0 or reg[i] != "mean_reversion":
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                if f > 0:
                    heavy.append(r)
                else:
                    quiet.append(r)

    n_h, n_q = len(heavy), len(quiet)
    counts = {"heavy-volume cases (forecast > 0)": int(n_h), "quiet-volume cases (forecast < 0)": int(n_q)}

    diff = None
    t = None
    if n_h >= 2 and n_q >= 2:
        diff = float(np.mean(heavy) - np.mean(quiet))
        tt = stats.ttest_ind(np.array(heavy), np.array(quiet), equal_var=False)
        t = float(tt.statistic) if np.isfinite(tt.statistic) else None

    if n_h < MIN_CASES or n_q < MIN_CASES:
        status = "not observable"
        decided = "Fewer than 30 cases in at least one group (heavy or quiet), the plan's minimum count."
    elif t is None or diff is None:
        status = "inconclusive"
        decided = "Welch t could not be computed; no confirm or reject rule is met."
    elif diff > 0 and t >= T_THR:
        status = "confirmed"
        decided = "The heavy-minus-quiet difference is positive with Welch t >= 2 (confirm rule)."
    elif diff < 0 and t <= -T_THR:
        status = "rejected"
        decided = "The heavy-minus-quiet difference is negative with Welch t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "Welch t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean 5-bar forward return, heavy minus quiet volume",
                         "value": diff,
                         "statistic": ({"name": "Welch t", "value": t} if t is not None else None),
                         "threshold": "difference > 0 with Welch t >= 2 confirms; < 0 with t <= -2 rejects; at least 30 cases per group"},
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": (reading_check + "; cases are the bars at positions 0, 5, 10, ... of each window with regime "
                    "'mean_reversion', a non-zero forecast and a close 5 bars later in the same window, and the plan's "
                    "'fewer than 30 cases in either group' is applied as the minimum count giving 'not observable'."),
    }
