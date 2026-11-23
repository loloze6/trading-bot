import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.excess_vol_power.last_history_value"
    H = 5
    MIN_CELLS = 300

    # ---------- 1. Situation check ----------
    # Fidelity: graded situation (past power above or below its 365-day mean, times the signal's z).
    # The outcome is that the power turns lower, so each bar bets against the excess power.
    # The expected forecast sign is therefore minus the sign of the raw component value.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            expected = -np.sign(raw)
            ok = active & raw.notna() & (raw != 0) & (np.sign(f) == expected)
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of forecast/10 x (5-day return minus coin's mean 5-day return), non-overlapping 5-bar cells, pooled"
    threshold = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 300 non-zero cells"
    reading = ("The mean and t are taken over the non-zero-forecast cells only, which are the cells the plan's minimum counts. "
               "Each coin's mean 5-day return is the mean over all its valid grid cells in all windows. "
               "Cells whose 5-day return would leave the window are dropped.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast have a forecast sign opposite to the "
                           "excess-power component's raw sign. The plan says each bar bets against the excess power."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    cells = []  # (coin, forecast, ret5)
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "close" not in df.columns or "forecast" not in df.columns:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = c[i], c[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                cells.append((coin, f[i], c1 / c0 - 1.0))

    cdf = pd.DataFrame(cells, columns=["coin", "forecast", "ret"])
    if len(cdf):
        coin_mean = cdf.groupby("coin")["ret"].mean()
        cdf["excess"] = cdf["ret"] - cdf["coin"].map(coin_mean)
        nz = cdf[cdf["forecast"].notna() & (cdf["forecast"] != 0)].copy()
    else:
        nz = pd.DataFrame(columns=["coin", "forecast", "ret", "excess"])

    n_nz = int(len(nz))
    mean_val = None
    t_val = None
    if n_nz >= 2:
        x = (nz["forecast"].astype(float) / 10.0 * nz["excess"].astype(float)).to_numpy()
        mean_val = float(np.mean(x))
        sd = float(np.std(x, ddof=1))
        if sd > 0:
            t_val = float(mean_val / (sd / np.sqrt(n_nz)))
        else:
            t_val = 0.0
    elif n_nz == 1:
        x = (nz["forecast"].astype(float) / 10.0 * nz["excess"].astype(float)).to_numpy()
        mean_val = float(x[0])

    counts = {"non-zero cells": n_nz, "cells": int(len(cdf))}

    if n_nz < MIN_CELLS:
        status = "not observable"
        decided_by = f"Only {n_nz} non-zero cells, fewer than the plan's minimum of 300."
    elif t_val is not None and mean_val > 0 and t_val >= 2:
        status = "confirmed"
        decided_by = "The mean is positive with t >= 2 over at least 300 non-zero cells, which meets the confirm rule."
    elif t_val is not None and mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided_by = "The mean is negative with t <= -2 over at least 300 non-zero cells, which meets the reject rule."
    else:
        status = "inconclusive"
        decided_by = "t lies between -2 and 2 with at least 300 non-zero cells, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": ({"name": "t of the mean", "value": t_val} if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
