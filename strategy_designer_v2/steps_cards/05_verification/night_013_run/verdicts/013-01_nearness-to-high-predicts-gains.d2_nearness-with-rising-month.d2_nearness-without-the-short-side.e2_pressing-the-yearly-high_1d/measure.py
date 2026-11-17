import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    DCOL = "debug_info.components.dist_high.last_history_value"
    OCOL = "debug_info.components.offset.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            d = pd.to_numeric(df[DCOL], errors="coerce") if DCOL in df.columns else pd.Series(np.nan, index=df.index)
            o = pd.to_numeric(df[OCOL], errors="coerce") if OCOL in df.columns else pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            # closeness relative to the coin's usual distance: standardised distance plus the centring offset
            score = d + o
            valid = active & score.notna()
            near = score > 0
            agree = valid & (((f > 0) & near) | ((f < 0) & (~near)))
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    reading = ("Situation check: an active bar agrees when the forecast sign matches closeness relative to the coin's usual "
               "distance (recorded standardised dist_high plus the recorded offset, positive = nearer than usual, which the "
               "Fidelity says is the long side of a graded, centred forecast); quintiles use the 60th/80th percentiles of the "
               "forecast pooled over all grid bars with a valid 7-bar return (top = forecast >= 80th percentile, fourth = "
               "60th <= forecast < 80th); holding is each coin's mean 7-bar grid return over all its windows; fewer than 100 "
               "top-quintile cases gives 'not observable'.")

    main_name = "mean 7-bar forward return of top forecast quintile minus coin holding"
    main_thr = "confirm if t >= 2 (with supporting check), reject if t <= -2, else inconclusive; at least 100 top-quintile cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars have a forecast whose sign matches the plan's situation "
                           "(long when the close is nearer its 52-week high than usual)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            for t in range(0, len(df) - H, H):
                r = c[t + H] / c[t] - 1.0 if (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] != 0) else np.nan
                rows.append((coin, w, f[t], r))
    g = pd.DataFrame(rows, columns=["coin", "window", "forecast", "ret"])
    g = g.dropna(subset=["ret"])
    hold = g.groupby("coin")["ret"].mean()
    g["excess"] = g["ret"] - g["coin"].map(hold)
    gq = g.dropna(subset=["forecast"])

    if len(gq) == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": "top minus fourth quintile 7-bar return, Welch t > 0", "value": None, "passed": None},
            "counts": {"independent top-quintile cases": 0},
            "decided_by": "Fewer than 100 independent top-quintile cases (none).",
            "reading": reading,
        }

    q60 = float(np.percentile(gq["forecast"], 60))
    q80 = float(np.percentile(gq["forecast"], 80))
    top = gq[gq["forecast"] >= q80]
    q4 = gq[(gq["forecast"] >= q60) & (gq["forecast"] < q80)]
    n_top = int(len(top))
    n_q4 = int(len(q4))

    ex = top["excess"].to_numpy()
    mean_ex = float(np.mean(ex)) if n_top > 0 else None
    if n_top > 1 and np.std(ex, ddof=1) > 0:
        t_main = float(np.mean(ex) / (np.std(ex, ddof=1) / np.sqrt(n_top)))
    else:
        t_main = None

    if n_top > 1 and n_q4 > 1:
        tw = stats.ttest_ind(top["ret"].to_numpy(), q4["ret"].to_numpy(), equal_var=False).statistic
        t_sup = float(tw) if np.isfinite(tw) else None
    else:
        t_sup = None
    sup_pass = (t_sup > 0) if t_sup is not None else None

    counts = {"independent top-quintile cases": n_top, "fourth-quintile cases": n_q4,
              "grid cases": int(len(gq))}

    if n_top < 100:
        status = "not observable"
        decided = f"Only {n_top} independent top-quintile cases, fewer than the 100 the plan requires."
    elif t_main is None:
        status = "inconclusive"
        decided = "The t of the top-quintile excess return could not be computed."
    elif t_main >= 2 and sup_pass:
        status = "confirmed"
        decided = "Top-quintile mean excess return over holding has t >= 2 and the top quintile beats the fourth (Welch t > 0)."
    elif t_main <= -2:
        status = "rejected"
        decided = "Top-quintile mean excess return over holding has t <= -2."
    elif t_main >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check (top minus fourth quintile Welch t > 0) fails."
    else:
        status = "inconclusive"
        decided = "The top-quintile excess return t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_ex,
                         "statistic": ({"name": "t of the mean", "value": t_main} if t_main is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": "top minus fourth quintile 7-bar return, Welch t > 0",
                             "value": t_sup, "passed": (bool(sup_pass) if sup_pass is not None else None)},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
