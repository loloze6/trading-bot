import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.rise28.last_history_value"

    # ---------- 1. situation check: a 28-day rise (raw > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # recompute the 28-day percent change from prices where not recorded
            recomputed = (close / close.shift(28) - 1.0) * 100.0
            raw = raw.where(raw.notna(), recomputed)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "Mean 5-day excess return, top fifth of positive forecasts minus all other grid bars"
    threshold = "Welch t >= 2 confirms (with supporting check); Welch t <= -2 rejects"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars after a "
                           "28-day rise with a long forecast, as the plan's situation and side require."
                           if n_active > 0 else "No bar has a non-zero forecast."),
            "reading": "The situation is a positive raw 28-day change (last_history_value, recomputed "
                       "from closes where missing) and the expected side is long.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    continue
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0):
                    continue
                if not np.isfinite(fc[t]):
                    continue
                rows.append((coin, w, fc[t], c1 / c0 - 1.0))

    if len(rows) == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold},
            "supporting_check": None,
            "counts": {"top-fifth grid cases": 0},
            "decided_by": "No grid case with a 5-day return exists, below the minimum of 30 top-fifth cases.",
            "reading": "none",
        }

    g = pd.DataFrame(rows, columns=["coin", "window", "forecast", "ret"])
    g["excess"] = g["ret"] - g.groupby("coin")["ret"].transform("mean")

    pos = g[g["forecast"] > 0]
    if len(pos) > 0:
        cut = float(np.quantile(pos["forecast"].values, 0.8))
        top_mask = (g["forecast"] > 0) & (g["forecast"] >= cut)
    else:
        cut = None
        top_mask = pd.Series(False, index=g.index)

    top = g.loc[top_mask, "excess"].values
    other = g.loc[~top_mask, "excess"].values
    rest_pos = g.loc[(g["forecast"] > 0) & ~top_mask, "excess"].values

    counts = {
        "top-fifth grid cases": int(len(top)),
        "other grid cases": int(len(other)),
        "remaining positive-forecast grid cases": int(len(rest_pos)),
        "positive-forecast grid cases": int(len(pos)),
    }

    reading = ("The top fifth is the positive-forecast grid bars whose forecast is at or above the 80th "
               "percentile of positive grid forecasts (ties at the cut kept in the top group), the coin's "
               "mean 5-day return is taken over its non-overlapping grid in all windows, and the plan's "
               "minimum of 30 top-fifth cases gives 'not observable' when unmet.")

    diff = float(np.mean(top) - np.mean(other)) if len(top) > 0 and len(other) > 0 else None
    t_val = None
    if len(top) >= 2 and len(other) >= 2:
        t_val = float(stats.ttest_ind(top, other, equal_var=False).statistic)
        if not np.isfinite(t_val):
            t_val = None

    sup_val = None
    sup_pass = None
    if len(top) > 0 and len(rest_pos) > 0:
        sup_val = float(np.mean(top) - np.mean(rest_pos))
        sup_pass = bool(sup_val > 0)

    main = {"name": main_name, "value": diff,
            "statistic": {"name": "Welch t", "value": t_val} if t_val is not None else None,
            "threshold": threshold}
    support = {"name": "Top-fifth mean excess minus remaining positive-forecast mean excess",
               "value": sup_val, "passed": sup_pass}

    if len(top) < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": main,
            "supporting_check": support,
            "counts": counts,
            "decided_by": f"Only {len(top)} top-fifth grid cases, below the plan's minimum of 30.",
            "reading": reading,
        }

    if t_val is None:
        status = "inconclusive"
        decided = "The Welch t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "Welch t >= 2 (top fifth minus the rest) and the supporting check passes."
    elif t_val <= -2:
        status = "rejected"
        decided = "Welch t <= -2 (top fifth minus the rest)."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "Welch t >= 2 but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "Welch t is between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
