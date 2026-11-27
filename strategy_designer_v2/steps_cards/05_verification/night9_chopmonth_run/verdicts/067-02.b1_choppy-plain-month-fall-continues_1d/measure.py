import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    FC = "forecast"
    RAW30 = "debug_info.components.fall30.last_history_value"

    def _ts(df):
        return pd.to_datetime(df["timestamp"], utc=True, errors="coerce")

    # ---------------- 1. situation check ----------------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0).astype(float)
            # 60-day return in percent, recomputed from the prices inside the window
            r60 = (close / close.shift(60) - 1.0) * 100.0
            choppy_px = (r60 >= -10.0) & (r60 <= 10.0)
            if "regime" in d.columns:
                choppy_reg = d["regime"].astype(str) == "mean_reversion"
            else:
                choppy_reg = pd.Series(False, index=d.index)
            choppy = np.where(r60.notna(), choppy_px, choppy_reg)
            # 30-day return: recorded raw value where present, else recomputed from prices
            r30_px = close / close.shift(30) - 1.0
            if RAW30 in d.columns:
                raw30 = pd.to_numeric(d[RAW30], errors="coerce")
                r30 = raw30.where(raw30.notna(), r30_px)
            else:
                r30 = r30_px
            fall = (r30 < 0).fillna(False).values
            situ = np.asarray(choppy, dtype=bool) & fall
            active = (fc != 0).values
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0).values).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "mean of -(forecast/10) x (7-bar return minus normal 7-bar drift), non-overlapping grid, forecast < 0"
    threshold = "confirm: mean > 0 with day-clustered t >= 2 on >= 30 case-days and check passing; reject: mean < 0 with t <= -2 on >= 30 case-days"
    reading = ("Choppy is recomputed as the 60-day close return in percent within [-10, +10] inside each window, falling back to the "
               "recorded regime 'mean_reversion' on bars without 60 prior bars in the window; the 30-day fall uses the recorded raw fall30 "
               "value (prices where missing); the coin's normal drift is the mean of all its non-overlapping 7-bar grid returns over all windows; "
               "the t clusters cases by UTC day (deviations summed per day, D/(D-1) correction); the deeper half is |forecast| above the median, "
               "the shallower half at or below it, compared on the unweighted short-direction excess move.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "case-days": 0},
            "decided_by": ("Fewer than 90 % of the active bars are choppy-regime bars (60-day return within -10 % to +10 %) with a "
                           "30-day fall and a short forecast, so the config does not do what the plan's situation says."
                           if n_active > 0 else "The record has no active bar, so the plan's situation cannot be matched."),
            "reading": reading,
        }

    # ---------------- 2. criterion ----------------
    rows = []
    for coin, wins in bars.items():
        grid_all = []
        coin_cells = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").astype(float).values
            fc = pd.to_numeric(d[FC], errors="coerce").astype(float).values
            ts = _ts(d)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_all.append(r)
                f = fc[i]
                if np.isfinite(f) and f < 0 and pd.notna(ts.iloc[i]):
                    coin_cells.append((r, f, ts.iloc[i].floor("D")))
        if len(grid_all) == 0:
            continue
        drift = float(np.mean(grid_all))
        for r, f, day in coin_cells:
            ex_short = -(r - drift)
            rows.append({"value": -(f / 10.0) * (r - drift), "ex_short": ex_short,
                         "absf": abs(f), "day": day})

    cells = pd.DataFrame(rows, columns=["value", "ex_short", "absf", "day"])
    n_cells = int(len(cells))
    n_days = int(cells["day"].nunique()) if n_cells else 0

    mean_v = None
    t_v = None
    if n_cells > 0:
        mean_v = float(cells["value"].mean())
        dev = cells["value"] - mean_v
        S = dev.groupby(cells["day"]).sum().values
        D = len(S)
        if D > 1:
            var_mean = (D / (D - 1.0)) * float(np.sum(S ** 2)) / (n_cells ** 2)
            if var_mean > 0:
                t_v = float(mean_v / np.sqrt(var_mean))

    sup_val = None
    sup_pass = None
    if n_cells > 0:
        med = float(cells["absf"].median())
        deep = cells.loc[cells["absf"] > med, "ex_short"]
        shallow = cells.loc[cells["absf"] <= med, "ex_short"]
        if len(deep) > 0 and len(shallow) > 0:
            sup_val = float(deep.mean() - shallow.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"case-days": n_days, "cells": n_cells}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} case-days with a short forecast on the 7-bar grid, fewer than the plan's minimum of 30."
    elif t_v is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_v > 0 and t_v >= 2 and sup_pass:
        status = "confirmed"
        decided = "Main mean above 0 with t >= 2 on at least 30 case-days, and the deeper-fall half beats the shallower half."
    elif mean_v < 0 and t_v <= -2:
        status = "rejected"
        decided = "Main mean below 0 with t <= -2 on at least 30 case-days."
    elif mean_v > 0 and t_v >= 2:
        status = "inconclusive"
        decided = "A confirming t (>= 2) with the supporting check failing (deeper-fall half not above the shallower half)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 on at least 30 case-days, meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_v,
                         "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t_v}
                                       if t_v is not None else None),
                         "threshold": threshold},
        "supporting_check": {"name": "deeper-fall half minus shallower half, mean short-direction excess move",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
