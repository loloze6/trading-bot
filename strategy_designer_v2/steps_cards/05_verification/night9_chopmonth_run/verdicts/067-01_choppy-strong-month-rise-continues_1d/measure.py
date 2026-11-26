import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    RAW = "debug_info.components.month_rise.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            # The raw 30-bar return. Use the recorded value; where it is missing,
            # recompute it from the prices inside the window.
            recomputed = (close / close.shift(30) - 1.0) * 100.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            # Choppy market: the config's veto labels markets with a 60-bar move
            # beyond +-10 % as "chop", which is the non-choppy regime.
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            choppy = regime != "chop"
            active = fc.notna() & (fc != 0)
            situation = (raw > 0) & choppy & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situation).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "OLS slope of 7-bar forward excess return on forecast, cells with forecast > 0"
    threshold = "t >= 2 with mean excess > 0 confirms; t <= -2 rejects; at least 100 cells"
    sup_name = "mean 7-bar forward excess return on the same cells > 0"

    if not passed:
        if agreement is None:
            decided = "No bar has a non-zero forecast, so the plan's long-only situation cannot be checked."
        else:
            decided = ("Fewer than 90 % of the bars with a non-zero forecast are long bars with a positive "
                       "raw 30-day return in a choppy market, as the plan's Fidelity requires.")
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cells": 0},
            "decided_by": decided,
            "reading": ("The situation is a positive raw 30-day return, taken from last_history_value and "
                        "recomputed from closes where it is missing, with a regime other than the config's "
                        "trend veto label 'chop' and a forecast above 0."),
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, fc[i]))

    cells = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    if len(cells):
        coin_mean = cells.groupby("coin")["ret"].mean()
        cells["excess"] = cells["ret"] - cells["coin"].map(coin_mean)
        sel = cells[cells["fc"].notna() & (cells["fc"] > 0)].dropna(subset=["excess"])
    else:
        sel = cells
    n_cells = int(len(sel))

    slope = None
    t_val = None
    mean_ex = None
    if n_cells >= 3 and sel["fc"].nunique() > 1:
        lr = stats.linregress(sel["fc"].to_numpy(float), sel["excess"].to_numpy(float))
        slope = float(lr.slope)
        t_val = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    if n_cells > 0:
        mean_ex = float(sel["excess"].mean())
    sup_pass = None if mean_ex is None else bool(mean_ex > 0)

    if n_cells < 100:
        status = "not observable"
        decided = f"Fewer than 100 cells with a forecast above 0 ({n_cells}), the plan's minimum count."
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t cannot be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess return is above 0, on at least 100 cells."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the mean excess return is at or below 0."
    elif t_val <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less, on at least 100 cells."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2, on at least 100 cells."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t_val is None else {"name": "OLS slope t", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": mean_ex, "passed": sup_pass},
        "counts": {"cells": n_cells},
        "decided_by": decided,
        "reading": ("Cells are pooled over all coins and windows. The slope is a one-variable OLS with an "
                    "intercept of the excess return (a fraction) on the forecast. Each coin's mean 7-bar return "
                    "is the mean over its non-overlapping grid cells of all windows. The situation counts a "
                    "regime other than the config's trend veto label 'chop' as choppy."),
    }
