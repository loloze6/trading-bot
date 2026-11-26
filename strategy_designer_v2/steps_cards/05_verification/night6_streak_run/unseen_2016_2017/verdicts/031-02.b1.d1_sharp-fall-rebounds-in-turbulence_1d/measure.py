import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    FALL_COL = "debug_info.components.fall.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: turbulence (std of the last 10 daily returns over std of the last 60 > 1)
    # and the latest day is a fall (raw fall component < 0). Expected side: long (forecast > 0).
    n_active = 0
    n_agree = 0
    n_fallback = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            ret = close.pct_change()
            sd10 = ret.rolling(10, min_periods=10).std()
            sd60 = ret.rolling(60, min_periods=60).std()
            ratio = sd10 / sd60
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            if FALL_COL in df.columns:
                raw = pd.to_numeric(df[FALL_COL], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            for i in range(len(df)):
                if fc.iloc[i] == 0:
                    continue
                n_active += 1
                r = ratio.iloc[i]
                if np.isfinite(r):
                    turb = r > 1.0
                else:
                    # not enough in-window history to recompute: use the detector's recorded decision
                    turb = regime.iloc[i] == "mean_reversion"
                    n_fallback += 1
                rv = raw.iloc[i]
                if np.isfinite(rv):
                    fall = rv < 0
                else:
                    pr = ret.iloc[i]
                    fall = bool(np.isfinite(pr) and pr < 0)
                if turb and fall and fc.iloc[i] > 0:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation = 10-day over 60-day return std (ddof 1, last 60 including the last 10) above 1, "
               "recomputed from in-window closes, falling back to the recorded regime on bars without 60 in-window "
               "returns, and raw fall component below 0, on the long side; drift = the coin's mean 2-bar return on "
               "the non-overlapping grid of all its windows; slope t from a pooled OLS with intercept of excess "
               "return on forecast; the plan's 30-case minimum is applied as 'not observable' per the workflow.")

    if n_active == 0 or not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("No active bars, so the forecast never takes the plan's position." if n_active == 0 else
                           "Fewer than 90% of active bars are bars of turbulence with a daily fall carrying a long "
                           "forecast, as the Fidelity's situation and rise outcome require."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    drift = {}
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    break
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                all_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    rows.append((coin, float(fc[i]), float(r)))
        drift[coin] = float(np.mean(all_rets)) if all_rets else np.nan

    x = []
    y = []
    for coin, f, r in rows:
        d = drift.get(coin, np.nan)
        if np.isfinite(d):
            x.append(f)
            y.append(r - d)
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    n = int(len(x))

    slope = None
    tval = None
    if n >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        if lr.stderr is not None and lr.stderr > 0:
            tval = float(lr.slope / lr.stderr)
    mean_exc = float(np.mean(y)) if n > 0 else None
    sup_pass = (mean_exc > 0) if mean_exc is not None else None

    main = {
        "name": "pooled OLS slope of 2-bar excess return on forecast (grid bars with forecast > 0)",
        "value": slope,
        "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
        "threshold": "confirm if slope t >= 2 with mean excess > 0; reject if slope t <= -2; otherwise inconclusive",
    }
    support = {"name": "mean excess 2-bar return on the same bars", "value": mean_exc, "passed": sup_pass}
    counts = {"independent grid cases with a positive forecast": n}

    if n < 30:
        status = "not observable"
        decided = f"Only {n} independent grid cases with a positive forecast, fewer than the 30 the plan requires."
    elif tval is None or not np.isfinite(tval):
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and mean_exc > 0:
        status = "confirmed"
        decided = "The slope t is 2 or more and the mean excess return is above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope t is -2 or less."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope t is 2 or more but the mean excess return is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
