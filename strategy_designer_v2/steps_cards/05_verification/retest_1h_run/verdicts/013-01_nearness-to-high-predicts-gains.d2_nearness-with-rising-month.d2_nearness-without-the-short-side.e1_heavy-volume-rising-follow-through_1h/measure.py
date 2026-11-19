import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    RV = "debug_info.components.relvol.last_history_value"

    active_total = 0
    active_agree = 0
    grid_frames = []

    for coin, windows in bars.items():
        coin_grid = []
        for w, df in windows.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            vol = d["volume"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce")

            # --- situation: 720-bar return > 0 and 24/480 volume ratio above 1 (centred > 0), long side
            ret720 = close / close.shift(720) - 1.0
            regime_trend = d["regime"].astype(str) == "trending"
            # where the 720-bar history lies before the window (warm-up not recorded), use the detector's decision
            trend = pd.Series(np.where(ret720.notna(), ret720 > 0, regime_trend), index=d.index).astype(bool)

            if RV in d.columns:
                rv = pd.to_numeric(d[RV], errors="coerce")
            else:
                rv = pd.Series(np.nan, index=d.index)
            rv_re = vol.rolling(24).mean() / vol.rolling(480).mean() - 1.0
            rv = rv.where(rv.notna(), rv_re)

            situ = trend & (rv > 0)
            act = fc.notna() & (fc != 0)
            active_total += int(act.sum())
            active_agree += int((act & situ & (fc > 0)).sum())

            # --- non-overlapping 72-bar grid from the window's first row
            n = len(d)
            pos = np.arange(0, n, H)
            pos = pos[pos + H < n]
            if len(pos) == 0:
                continue
            fwd = close.values[pos + H] / close.values[pos] - 1.0
            g = pd.DataFrame({
                "coin": coin,
                "fwd": fwd,
                "forecast": fc.values[pos],
                "trending": regime_trend.values[pos],
            })
            coin_grid.append(g)
        if coin_grid:
            cg = pd.concat(coin_grid, ignore_index=True)
            cg = cg[np.isfinite(cg["fwd"])]
            cg["excess"] = cg["fwd"] - cg["fwd"].mean()
            grid_frames.append(cg)

    agreement = (active_agree / active_total) if active_total > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("Trending-regime grid bars are those whose recorded regime is 'trending' at grid positions 0, 72, 144, ... "
               "of each window with a full 72-bar forward return inside the window, the coin's mean 72-bar return is the "
               "mean over all its grid bars of all windows, the top third of positive forecasts is the ceil(n/3) largest "
               "positive grid forecasts pooled over coins, and the situation check uses the 720-bar return from prices "
               "(the recorded regime where the window lacks 720 bars of history) with the recorded relvol raw value.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(active_total)},
            "decided_by": ("Fewer than 90% of non-zero forecasts fall on bars with a positive 720-bar return and a 24/480 "
                           "volume ratio above 1 with a long forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    if grid_frames:
        G = pd.concat(grid_frames, ignore_index=True)
    else:
        G = pd.DataFrame(columns=["coin", "fwd", "forecast", "trending", "excess"])
    T = G[G["trending"].astype(bool)].dropna(subset=["excess", "forecast"])
    n_cases = int(len(T))
    n_pos = int((T["forecast"] > 0).sum())

    # main measure: OLS slope of excess return on forecast
    slope = None
    tstat = None
    if n_cases >= 3 and T["forecast"].nunique() > 1:
        lr = stats.linregress(T["forecast"].values.astype(float), T["excess"].values.astype(float))
        slope = float(lr.slope)
        if lr.stderr and lr.stderr > 0:
            tstat = float(lr.slope / lr.stderr)

    # supporting check
    sup_val = None
    sup_pass = None
    posf = T[T["forecast"] > 0].sort_values("forecast", ascending=False, kind="mergesort")
    zero = T[T["forecast"] == 0]
    if len(posf) > 0 and len(zero) > 0:
        k = int(np.ceil(len(posf) / 3.0))
        top = posf.iloc[:k]
        sup_val = float(top["excess"].mean() - zero["excess"].mean())
        sup_pass = bool(sup_val > 0)

    counts = {
        "pooled trending-regime grid cases": n_cases,
        "grid cases with a positive forecast": n_pos,
        "grid cases with forecast 0": int(len(zero)),
    }

    if n_cases < 100 or n_pos < 30:
        status = "not observable"
        decided_by = ("The plan's minimum of 100 pooled trending-regime grid cases with at least 30 positive-forecast "
                      "cases is not reached.")
    elif tstat is None:
        status = "inconclusive"
        decided_by = "The slope's t cannot be computed, so neither the confirm nor the reject rule is met."
    elif tstat >= 2 and sup_pass:
        status = "confirmed"
        decided_by = "The slope's t is 2 or more and the supporting check passes."
    elif tstat <= -2:
        status = "rejected"
        decided_by = "The slope's t is -2 or less."
    elif tstat >= 2:
        status = "inconclusive"
        decided_by = "The slope's t is 2 or more but the supporting check fails."
    else:
        status = "inconclusive"
        decided_by = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": {
            "name": "pooled OLS slope of excess 72-bar return on forecast, trending grid bars",
            "value": slope,
            "statistic": None if tstat is None else {"name": "OLS slope t", "value": tstat},
            "threshold": "confirm if t >= 2 with the supporting check passing; reject if t <= -2",
        },
        "supporting_check": {
            "name": "mean excess return, top third of positive forecasts minus forecast 0",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
