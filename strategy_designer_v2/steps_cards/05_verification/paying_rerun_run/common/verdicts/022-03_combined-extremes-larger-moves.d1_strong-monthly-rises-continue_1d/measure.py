import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.rise28.last_history_value"

    # ---------- 1. Situation check: 28-bar rise (raw value > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # where the raw value is missing, recompute the 28-bar return from prices inside the window
            close = pd.to_numeric(df["close"], errors="coerce")
            recomputed = (close / close.shift(28) - 1.0) * 100.0
            raw = raw.where(raw.notna(), recomputed)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of drift-adjusted 5-bar return on forecast at cell's first bar"
    threshold = "confirm: slope t >= 2 with supporting check passing; reject: slope t <= -2"
    reading = ("Situation bars are those whose raw 28-bar return (recomputed from closes where not recorded) is above 0 "
               "with a positive forecast; cells are bars at positions 0,5,10,... of each window having a close 5 bars later "
               "in the same window, the slope's t is the ordinary OLS t, and the plan's minimum counts are read as "
               "'not observable' when unmet.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"grid cells": 0, "grid cells with forecast > 0": 0},
            "decided_by": ("Fewer than 90% of the active bars are bars with a positive 28-bar rise and a long forecast, "
                           "as the plan's Fidelity requires (agreement %.3f)." % agreement),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, w, c1 / c0 - 1.0, fc[t]))

    cells = pd.DataFrame(rows, columns=["coin", "window", "ret", "fc"])
    if len(cells) > 0:
        drift = cells.groupby("coin")["ret"].mean()
        cells["adj"] = cells["ret"] - cells["coin"].map(drift)
    else:
        cells["adj"] = []
    cells = cells.dropna(subset=["adj", "fc"])

    n_cells = int(len(cells))
    pos = cells[cells["fc"] > 0]
    n_pos = int(len(pos))
    counts = {"grid cells": n_cells, "grid cells with forecast > 0": n_pos}

    # Slope
    slope = None
    t_slope = None
    if n_cells >= 3 and np.nanstd(cells["fc"].values) > 0:
        res = stats.linregress(cells["fc"].values.astype(float), cells["adj"].values.astype(float))
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    # Supporting check
    sup_val = float(pos["adj"].mean()) if n_pos > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    main = {
        "name": main_name,
        "value": slope,
        "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
        "threshold": threshold,
    }
    supporting = {
        "name": "mean drift-adjusted 5-bar return over cells with forecast > 0 above 0",
        "value": sup_val,
        "passed": sup_pass,
    }

    if n_cells < 300 or n_pos < 100:
        status = "not observable"
        decided_by = ("Minimum counts not reached: %d grid cells (need 300) and %d with forecast > 0 (need 100)."
                      % (n_cells, n_pos))
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided_by = "The slope's t is 2 or more and the supporting check passes (confirm rule)."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "The slope's t is -2 or less (reject rule)."
    elif t_slope >= 2:
        status = "inconclusive"
        decided_by = "The slope's t is 2 or more but the supporting check fails (inconclusive rule)."
    else:
        status = "inconclusive"
        decided_by = "The slope's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
