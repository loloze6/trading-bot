import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    RAW = "debug_info.components.absorb.last_history_value"
    PPV = "debug_info.components.absorb.post_pipeline_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            high = df["high"].astype(float)
            low = df["low"].astype(float)
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)
            prior_mean = vol.shift(1).rolling(20, min_periods=20).mean()
            rng = (high - low).replace(0, np.nan)
            raw_px = (high - close) / rng * vol / prior_mean.replace(0, np.nan)
            if RAW in df.columns:
                raw = df[RAW].astype(float).where(df[RAW].notna(), raw_px)
            else:
                raw = raw_px
            fc = df["forecast"].astype(float)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # situation: the close below the high, weighted by the volume multiple (raw > 0), on the long side
            agree = active & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The situation for this graded, long-only idea is taken as every bar where the raw close-near-low "
               "times volume-multiple value is positive (recomputed from prices where unrecorded); the coin's mean "
               "2-day return is taken over its grid cells in all windows; the forecast for the regression and the "
               "ranking is post_pipeline_value; the top fifth is the floor(n/5) highest cells (stable sort); and "
               "the plan's minimum counts, when not reached, give 'not observable' per the workflow.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the close sits "
                           "below the high on a volume multiple (positive raw absorption value), as the Fidelity's "
                           "situation and long outcome require."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            ppv = df[PPV].astype(float).values if PPV in df.columns else np.full(len(df), np.nan)
            n = len(df)
            for t in range(0, n - H, H):
                r = close[t + H] / close[t] - 1.0
                rows.append((coin, w, ppv[t], r))
    cells = pd.DataFrame(rows, columns=["coin", "window", "fc", "ret"])
    cells = cells[np.isfinite(cells["ret"])]
    coin_mean = cells.groupby("coin")["ret"].mean()
    cells["excess"] = cells["ret"] - cells["coin"].map(coin_mean)
    cells = cells[np.isfinite(cells["fc"]) & np.isfinite(cells["excess"])].reset_index(drop=True)

    n_cells = int(len(cells))
    n_top = int(n_cells // 5)

    slope = None
    t_stat = None
    if n_cells >= 3 and np.std(cells["fc"].values) > 0:
        lr = stats.linregress(cells["fc"].values, cells["excess"].values)
        slope = float(lr.slope)
        t_stat = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    top_mean = None
    if n_top > 0:
        order = np.argsort(-cells["fc"].values, kind="mergesort")
        top_mean = float(cells["excess"].values[order[:n_top]].mean())
    top_pass = None if top_mean is None else bool(top_mean > 0)

    counts = {"grid cells pooled": n_cells, "top fifth cells": n_top}

    main = {
        "name": "OLS slope of excess 2-day return on forecast, pooled",
        "value": slope,
        "statistic": {"name": "OLS slope t", "value": t_stat} if t_stat is not None else None,
        "threshold": "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2",
    }
    support = {"name": "top-fifth mean excess 2-day return > 0", "value": top_mean, "passed": top_pass}

    if n_cells < 1000 or n_top < 200:
        status = "not observable"
        decided = (f"The plan's minimum counts are not reached: {n_cells} grid cells (need 1000) and "
                   f"{n_top} in the top fifth (need 200).")
    elif t_stat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t_stat >= 2:
        if top_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the top-fifth mean excess return is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the top fifth fails the check (mean excess not above 0)."
    elif slope < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
