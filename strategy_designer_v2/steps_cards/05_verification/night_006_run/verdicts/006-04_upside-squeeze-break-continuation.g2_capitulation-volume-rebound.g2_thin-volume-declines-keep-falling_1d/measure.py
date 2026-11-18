import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RAW = "debug_info.components.volratio.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            ret5 = close / close.shift(5) - 1.0
            # situation: 5-bar return < 0; on the first 5 bars of a window it cannot be
            # recomputed from the record, so the detector's own decision (regime) stands in
            sit = ret5 < 0
            no_ret = ret5.isna()
            sit = sit.where(~no_ret, df["regime"].astype(str) == "mean_reversion")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            # expected side: graded on the volume ratio, short when thin (log ratio < 0), long when heavy
            exp_sign = np.sign(raw)
            active = fc != 0
            ok = active & sit & (np.sign(fc) == exp_sign) & raw.notna()
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of slope of excess 3-bar forward return on forecast, mean_reversion grid bars"
    threshold = "confirm if t >= 2 with supporting check passed; reject if t <= -2; else inconclusive; at least 100 grid cases"
    reading = ("Expected side read as the graded relation (short when the 5/30 log volume ratio is below 0, long when above), "
               "situation recomputed as close/close[-5]-1 < 0 with the recorded regime used on each window's first 5 bars; "
               "the coin's mean 3-bar return is taken over its non-overlapping grid bars of all windows, and the regression is pooled over coins.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"grid cases in the regime": None},
            "decided_by": ("Fewer than 90% of active bars are bars with a negative 5-bar return whose forecast sign "
                           "follows the volume ratio's sign (short on thin volume), as the Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                coin_rows.append({
                    "coin": coin,
                    "ret": r,
                    "regime": str(df["regime"].iloc[i]),
                    "forecast": pd.to_numeric(df["forecast"].iloc[i], errors="coerce"),
                })
        if not coin_rows:
            continue
        cdf = pd.DataFrame(coin_rows)
        cdf = cdf[np.isfinite(cdf["ret"])]
        mu = cdf["ret"].mean()
        cdf["excess"] = cdf["ret"] - mu
        rows.append(cdf)

    if rows:
        g = pd.concat(rows, ignore_index=True)
        g = g[(g["regime"] == "mean_reversion") & g["forecast"].notna() & np.isfinite(g["excess"])]
    else:
        g = pd.DataFrame(columns=["excess", "forecast"])
    n_cases = int(len(g))

    slope = None
    t = None
    if n_cases >= 3 and g["forecast"].astype(float).nunique() > 1:
        lr = stats.linregress(g["forecast"].astype(float).values, g["excess"].astype(float).values)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    neg = g[g["forecast"].astype(float) < 0] if n_cases > 0 else g
    n_neg = int(len(neg))
    sup_val = float(neg["excess"].mean()) if n_neg > 0 else None
    sup_pass = (sup_val < 0) if sup_val is not None else None

    counts = {"grid cases in the regime": n_cases, "grid cases with forecast < 0": n_neg}

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} grid cases in the regime, fewer than the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The slope's t is >= 2 and the mean excess 3-bar return on forecast < 0 grid bars is below 0."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is <= -2."
    elif t >= 2:
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
            "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 3-bar return on grid bars with forecast < 0 below 0",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
