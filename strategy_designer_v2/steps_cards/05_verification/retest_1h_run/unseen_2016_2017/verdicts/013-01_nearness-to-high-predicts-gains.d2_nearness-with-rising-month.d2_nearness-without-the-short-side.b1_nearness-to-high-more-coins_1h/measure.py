import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 168
    RET_P = 720
    MIN_POS = 300

    hpm_col = "debug_info.components.hpm.last_history_value"

    # ---------- 1. Situation check: active only while 720-bar return > 0, long only ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            # 720-bar return from the window's own prices (never across windows)
            ret30 = np.full(n, np.nan)
            if n > RET_P:
                ret30[RET_P:] = close[RET_P:] / close[:-RET_P] - 1.0
            # where the window's prices do not reach 720 bars back, use the raw HPM value
            # (720-bar return x positive proximity factor: same sign as the 720-bar return)
            if hpm_col in df.columns:
                hpm_raw = pd.to_numeric(df[hpm_col], errors="coerce").to_numpy(dtype=float)
            else:
                hpm_raw = np.full(n, np.nan)
            in_state = np.full(n, np.nan)
            ok_price = ~np.isnan(ret30)
            in_state[ok_price] = (ret30[ok_price] > 0).astype(float)
            ok_hpm = (~ok_price) & ~np.isnan(hpm_raw)
            in_state[ok_hpm] = (hpm_raw[ok_hpm] > 0).astype(float)

            active = (~np.isnan(fc)) & (fc != 0)
            judged = active & ~np.isnan(in_state)
            n_active += int(judged.sum())
            n_agree += int((judged & (in_state == 1.0) & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "pooled OLS slope t of excess 168-bar forward return on forecast (non-overlapping grid)"
    threshold = "confirm if t >= 2 and supporting check passes; reject if t <= -2; else inconclusive; needs >= 300 grid cases with forecast > 0"
    reading = ("The 720-bar return is recomputed from each window's closes and, on bars without 720 bars of history "
               "in the window, its sign is taken from the raw HPM value; the coin's benchmark is the mean of all its "
               "non-overlapping 168-bar grid returns over all its windows; the slope's t is the ordinary OLS t with an "
               "intercept; the plan's 'fewer than 300 cases' rule is reported as not observable per the workflow.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are long bars with a positive 720-bar return, "
                           "so the config does not trade only inside the plan's state on the long side."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for t in range(0, n - H, H):
                if t + H >= n:
                    break
                r = close[t + H] / close[t] - 1.0
                rows.append((coin, fc[t], r))
    grid = pd.DataFrame(rows, columns=["coin", "forecast", "fwd"])
    grid = grid.replace([np.inf, -np.inf], np.nan)
    grid = grid.dropna(subset=["fwd"])
    coin_mean = grid.groupby("coin")["fwd"].mean()
    grid["excess"] = grid["fwd"] - grid["coin"].map(coin_mean)
    g = grid.dropna(subset=["forecast", "excess"])

    n_grid = int(len(g))
    pos = g[g["forecast"] > 0]
    n_pos = int(len(pos))

    slope = None
    t_slope = None
    if n_grid >= 3 and g["forecast"].nunique() > 1:
        lr = stats.linregress(g["forecast"].to_numpy(float), g["excess"].to_numpy(float))
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    sup_val = float(pos["excess"].mean()) if n_pos > 0 else None
    sup_pass = (sup_val > 0) if sup_val is not None else None

    counts = {
        "non-overlapping grid cases with forecast > 0": n_pos,
        "non-overlapping grid cases (all)": n_grid,
    }

    if n_pos < MIN_POS:
        status = "not observable"
        decided = f"Only {n_pos} non-overlapping grid cases with forecast > 0, below the plan's minimum of 300."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither rule is met."
    elif t_slope >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is >= 2 and the mean excess return on forecast > 0 grid bars is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is <= -2."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is >= 2 but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 168-bar forward return on grid bars with forecast > 0 above 0",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
