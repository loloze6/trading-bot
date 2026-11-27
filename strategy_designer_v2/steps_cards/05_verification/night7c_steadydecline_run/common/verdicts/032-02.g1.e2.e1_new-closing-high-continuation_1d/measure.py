import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    PROX = "debug_info.components.prox.last_history_value"
    H = 10
    LOOK = 28

    # ---------- 1. Situation check ----------
    # Situation (Fidelity): close above its close of 28 days ago (28-day return > 0), graded by proximity to the
    # 28-day closing high; outcome "a larger rise" -> long side (forecast > 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            ret28 = np.full(len(df), np.nan)
            if len(df) > LOOK:
                ret28[LOOK:] = close[LOOK:] / close[:-LOOK] - 1.0
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            prox = df[PROX].astype(float).values if PROX in df.columns else np.full(len(df), np.nan)
            for i in range(len(df)):
                if not np.isfinite(fc[i]) or fc[i] == 0:
                    continue
                n_active += 1
                if np.isfinite(ret28[i]):
                    in_sit = ret28[i] > 0
                else:
                    # no 28 bars of in-window history: use the detector's recorded decision of ret28 > 0
                    in_sit = regime[i] == "trending"
                # graded by proximity: a recorded proximity in (0, 1]
                graded = np.isfinite(prox[i]) and 0 < prox[i] <= 1 + 1e-9
                if in_sit and graded and fc[i] > 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "mean excess 10-bar return, new-high (prox=1) minus other in-regime grid cases"
    threshold = "Welch t >= 2 (with correlation > 0) confirms; Welch t <= -2 rejects; at least 30 grid cases per group"
    reading = ("In-regime grid cases are grid bars (positions 0,10,20,... of each window) with a recorded prox value; "
               "new-high means prox equal to 1 within 1e-9; the coin's mean 10-bar return is taken over the same "
               "non-overlapping grid of all its windows; for bars with fewer than 28 in-window bars of history the "
               "situation check uses the recorded regime ('trending').")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars inside the 28-day "
                           "return > 0 regime graded by proximity to the 28-day closing high."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        all_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            prox = df[PROX].astype(float).values if PROX in df.columns else np.full(len(df), np.nan)
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    break
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                r = close[i + H] / close[i] - 1.0
                all_rets.append(r)
                if np.isfinite(prox[i]):
                    coin_cases.append((prox[i], r))
        if not all_rets:
            continue
        mu = float(np.mean(all_rets))
        for p, r in coin_cases:
            rows.append((p, r - mu))

    if rows:
        arr = np.array(rows, dtype=float)
        prox_v, ex = arr[:, 0], arr[:, 1]
    else:
        prox_v, ex = np.array([]), np.array([])
    is_new = np.abs(prox_v - 1.0) <= 1e-9
    g_new = ex[is_new]
    g_oth = ex[~is_new]
    counts = {"new-high grid cases": int(len(g_new)), "other in-regime grid cases": int(len(g_oth)),
              "all in-regime grid cases": int(len(ex))}

    diff = None
    t = None
    if len(g_new) >= 2 and len(g_oth) >= 2:
        diff = float(np.mean(g_new) - np.mean(g_oth))
        tt = stats.ttest_ind(g_new, g_oth, equal_var=False)
        t = float(tt.statistic) if np.isfinite(tt.statistic) else None

    corr = None
    if len(ex) >= 3 and np.std(prox_v) > 0 and np.std(ex) > 0:
        corr = float(np.corrcoef(prox_v, ex)[0, 1])
    corr_pass = None if corr is None else bool(corr > 0)

    if len(g_new) < 30 or len(g_oth) < 30:
        status = "not observable"
        decided = (f"The plan's minimum of 30 grid cases in each group is not reached "
                   f"(new-high {len(g_new)}, other {len(g_oth)}).")
    elif t is None:
        status = "inconclusive"
        decided = "The Welch t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and corr_pass:
        status = "confirmed"
        decided = "Welch t >= 2 and the correlation of prox with the excess return is above 0 (confirm rule)."
    elif t <= -2:
        status = "rejected"
        decided = "Welch t <= -2 (reject rule)."
    elif t >= 2:
        status = "inconclusive"
        decided = "Welch t >= 2 but the correlation is at or below 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "Welch t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": diff,
                         "statistic": None if t is None else {"name": "Welch t", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": "correlation of prox with excess 10-bar return across in-regime grid cases",
                             "value": corr, "passed": corr_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
