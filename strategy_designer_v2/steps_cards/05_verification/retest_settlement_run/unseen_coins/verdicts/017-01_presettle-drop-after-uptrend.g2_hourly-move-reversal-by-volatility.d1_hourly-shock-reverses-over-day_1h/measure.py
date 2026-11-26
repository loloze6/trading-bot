import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    RAW = "debug_info.components.hour_move.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            ret1 = close / close.shift(1) - 1.0
            vol = ret1.rolling(24, min_periods=24).std()
            recomputed = ret1 / vol
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # situation: a non-zero last-hour move scaled by 24h vol; expected side: against the move
            ok = active & raw.notna() & (raw != 0) & (np.sign(fc) == -np.sign(raw))
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of slope of 24-bar excess forward return on forecast (grid bars, pooled)"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive; min 500 grid cases with non-zero forecast"
    reading = ("The situation is taken as every bar with a non-zero volatility-scaled hourly return (the plan sets no size cut-off, "
               "the forecast being graded), the expected side as opposite to that return; the regression is OLS with intercept on all grid bars "
               "with valid values, the drift is each coin's mean grid 24-bar return over all its windows, and the plan's minimum of 500 "
               "non-zero-forecast grid cases is treated as a minimum count (not observable if unmet).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars have a forecast opposite in sign to the volatility-scaled "
                           "hourly return, so the config does not bet against the move as the Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, fc[t]))
    d = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    if len(d):
        drift = d.groupby("coin")["ret"].mean()
        d["excess"] = d["ret"] - d["coin"].map(drift)
        d = d.dropna(subset=["excess", "fc"])
    n_grid = int(len(d))
    n_nonzero = int((d["fc"] != 0).sum()) if n_grid else 0
    counts = {"grid cases": n_grid, "grid cases with a non-zero forecast": n_nonzero}

    if n_nonzero < 500:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Only {n_nonzero} grid cases with a non-zero forecast, fewer than the plan's minimum of 500.",
            "reading": reading,
        }

    x = d["fc"].values.astype(float)
    y = d["excess"].values.astype(float)
    if np.var(x) == 0:
        slope, t = 0.0, 0.0
    else:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t = float(res.slope / res.stderr) if res.stderr > 0 else 0.0

    if slope > 0 and t >= 2:
        status = "confirmed"
        decided = f"The slope is positive with t = {t:.2f} >= 2 (confirm rule)."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = f"The slope is negative with t = {t:.2f} <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = f"The slope's t = {t:.2f} lies strictly between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": t,
                         "statistic": {"name": "OLS slope t", "value": t},
                         "threshold": threshold},
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
