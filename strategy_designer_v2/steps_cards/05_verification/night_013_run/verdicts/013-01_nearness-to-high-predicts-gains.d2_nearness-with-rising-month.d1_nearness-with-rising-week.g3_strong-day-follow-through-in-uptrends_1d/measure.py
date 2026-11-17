import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    MIN_CASES = 100
    RAW_COL = "debug_info.components.zday.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))

            # Situation: 30-bar return > 0. Recompute it from prices inside the window.
            # On the first 30 bars there is no price history, so fall back to the detector's decision.
            ret30 = close / close.shift(30) - 1.0
            situation = pd.Series(np.where(ret30.notna(), ret30 > 0, regime == "trending"),
                                  index=d.index).astype(bool)

            # Expected side: the sign of the raw volatility-scaled 1-bar return.
            # Use the recorded raw value; where it is missing, use the 1-bar return from prices.
            if RAW_COL in d.columns:
                raw = pd.to_numeric(d[RAW_COL], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            ret1 = close / close.shift(1) - 1.0
            raw = raw.where(raw.notna(), ret1)
            exp_sign = np.sign(raw)

            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & situation & (np.sign(fc) == exp_sign) & exp_sign.notna()
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "OLS slope of 7-bar excess forward return on forecast, trending grid bars"
    threshold = "slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects; at least 100 grid cases"
    reading = ("The coin's mean 7-bar return is taken over all non-overlapping grid bars of all its windows, "
               "whatever their regime. 'Trending' grid bars are read from the recorded regime column. "
               "In the situation check, the 30-bar return is recomputed from prices, falling back to the "
               "recorded regime on the first 30 bars of a window. The expected side there is the sign of "
               "the raw zday value, or of the 1-bar return where zday is not recorded.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"trending grid cases": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are bars with a positive 30-bar return and a "
                           "forecast whose sign matches the volatility-scaled 1-bar return "
                           f"(agreement {agreement:.3f})."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            regime = d["regime"].astype(str).values
            n = len(d)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                coin_rows.append((c1 / c0 - 1.0, fc[t], regime[t] == "trending"))
        if coin_rows:
            fr = np.array([r[0] for r in coin_rows], dtype=float)
            coin_mean = float(np.mean(fr))
            for r in coin_rows:
                if r[2] and np.isfinite(r[1]):
                    rows.append((r[0] - coin_mean, float(r[1])))

    n_cases = len(rows)
    counts = {"trending grid cases": int(n_cases)}

    slope, tstat = None, None
    if n_cases >= 3:
        y = np.array([r[0] for r in rows])
        x = np.array([r[1] for r in rows])
        if np.std(x) > 0:
            lr = stats.linregress(x, y)
            slope = float(lr.slope)
            tstat = float(lr.slope / lr.stderr) if lr.stderr > 0 else (np.inf if lr.slope > 0 else -np.inf)

    main = {"name": main_name, "value": slope,
            "statistic": None if tstat is None else {"name": "OLS slope t", "value": tstat},
            "threshold": threshold}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} trending grid cases, below the plan's minimum of 100."
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope could not be estimated (the forecast has no variation), so neither rule is met."
    elif slope > 0 and tstat >= 2:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 on at least 100 grid cases (the confirm rule)."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 on at least 100 grid cases (the reject rule)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (the inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
