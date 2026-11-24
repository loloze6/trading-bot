import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 30
    SIT = "mean_reversion"
    T_CONF = 2.0
    MIN_HALF = 20

    # ---------- 1. Situation check ----------
    # The detector's component r90 needs a 365-day window behind a 90-day return, which the
    # recorded windows (~120 bars, no warm-up) cannot rebuild. So the situation is read from the
    # detector's recorded decision, `regime == mean_reversion`. Expected side: long (outcome: rebound).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            reg = df["regime"].astype(str)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & (reg == SIT) & (f > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {
                "name": "Welch t of demeaned 30-day forward return, upper minus lower half of forecast",
                "value": None,
                "statistic": None,
                "threshold": "t >= +2 confirms (with supporting check), t <= -2 rejects",
            },
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on the long side": int(n_agree)},
            "decided_by": (
                "Fewer than 90 % of the bars with a non-zero forecast are mean_reversion-regime bars with a long "
                "forecast, while the plan's Fidelity expects a rebound (long) inside the deep-fall situation."
                if n_active > 0 else
                "The record has no bar with a non-zero forecast, so the plan's situation and side cannot be matched."
            ),
            "reading": (
                "The situation is read from the recorded `regime` column because r90's 365-day scale cannot be "
                "rebuilt inside the recorded windows, and the expected side is long because the outcome is a rebound."
            ),
        }

    # ---------- 2. Criterion ----------
    # Coin drift: mean 30-bar return over all windows on the non-overlapping grid (positions 0, 30, 60, ...).
    drift = {}
    cases = []  # (coin, forecast, fwd return)
    for coin, wins in bars.items():
        all_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            reg = df["regime"].astype(str).to_numpy()
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if reg[i] == SIT and np.isfinite(fc[i]):
                    coin_cases.append((fc[i], r))
        if all_rets:
            drift[coin] = float(np.mean(all_rets))
            for fv, r in coin_cases:
                cases.append((coin, fv, r - drift[coin]))

    n_cases = len(cases)
    if n_cases > 0:
        fvals = np.array([c[1] for c in cases], dtype=float)
        excess = np.array([c[2] for c in cases], dtype=float)
        med = float(np.median(fvals))
        upper_mask = fvals > med
        lower_mask = ~upper_mask
    else:
        fvals = np.array([]); excess = np.array([]); med = float("nan")
        upper_mask = np.array([], dtype=bool); lower_mask = np.array([], dtype=bool)

    up = excess[upper_mask]
    lo = excess[lower_mask]
    n_up, n_lo = int(len(up)), int(len(lo))

    diff = float(np.mean(up) - np.mean(lo)) if (n_up > 0 and n_lo > 0) else None
    t = None
    if n_up >= 2 and n_lo >= 2:
        tt = stats.ttest_ind(up, lo, equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None

    pos = excess[fvals > 0] if n_cases > 0 else np.array([])
    n_pos = int(len(pos))
    sup_val = float(np.mean(pos)) if n_pos > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    counts = {
        "situation cases": n_cases,
        "upper half cases": n_up,
        "lower half cases": n_lo,
        "situation cases with forecast above 0": n_pos,
    }

    if n_up < MIN_HALF or n_lo < MIN_HALF:
        status = "not observable"
        decided_by = (f"The minimum of 20 cases in each half (40 situation cases) is not reached: "
                      f"{n_up} upper and {n_lo} lower of {n_cases} cases.")
    elif t is None:
        status = "inconclusive"
        decided_by = "The Welch t could not be computed (no variance in the halves), so neither rule is met."
    elif t >= T_CONF and sup_pass:
        status = "confirmed"
        decided_by = "Main-measure t >= +2 and the supporting check passes (cases with a positive forecast beat the coin's drift)."
    elif t >= T_CONF:
        status = "inconclusive"
        decided_by = "Main-measure t >= +2 but the supporting check fails, which the plan calls inconclusive."
    elif t <= -T_CONF:
        status = "rejected"
        decided_by = "Main-measure t <= -2: the upper-forecast half rebounds less than the lower half."
    else:
        status = "inconclusive"
        decided_by = "Main-measure t lies between -2 and +2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "Upper minus lower forecast half, 30-day forward return minus coin drift",
            "value": diff,
            "statistic": ({"name": "Welch t", "value": t} if t is not None else None),
            "threshold": "t >= +2 with the supporting check confirms; t <= -2 rejects; at least 20 cases per half",
        },
        "supporting_check": {
            "name": "Mean demeaned 30-day return of situation cases with forecast > 0 above 0",
            "value": sup_val,
            "passed": (bool(sup_pass) if sup_pass is not None else None),
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": (
            "The situation is the recorded regime 'mean_reversion' (r90 cannot be rebuilt from in-window bars), "
            "the expected side is long, cases are grid bars 0, 30, 60, ... of each window with a full 30-bar "
            "forward return inside it, the coin's drift is the mean of its grid 30-bar returns over all its "
            "windows, the cases of all coins are pooled, and the upper half is forecast strictly above the "
            "median with the lower half at or below it."
        ),
    }
