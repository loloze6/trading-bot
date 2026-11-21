import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    RAW = "debug_info.components.mom7d.last_history_value"

    def raw_from_prices(df):
        c = df["close"].astype(float)
        r1 = c.pct_change()
        ret42 = c / c.shift(42) - 1.0
        vol = r1.rolling(20).std()
        return ret42 / (vol * np.sqrt(42))

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = df["forecast"].astype(float)
            if RAW in df.columns:
                raw = df[RAW].astype(float)
                fallback = raw_from_prices(df)
                raw = raw.where(raw.notna(), fallback)
            else:
                raw = raw_from_prices(df)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            # Situation: the volatility-scaled 7-day return (ungated); expected side: long after a rise, short after a fall
            agree = active & raw.notna() & (np.sign(f) == np.sign(raw)) & (raw != 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t-statistic of the pooled slope of 72-bar drift-adjusted forward return on the forecast"
    threshold = "confirm t >= 2 with per-coin check passing; reject t <= -2; otherwise inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars have a forecast whose sign matches the sign of the volatility-scaled 42-bar return the Fidelity says the idea follows (long after a rise, short after a fall).",
            "reading": "Situation taken as every bar with a non-zero raw scaled return, expected side its sign; raw recomputed from prices where not recorded.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            c = df["close"].astype(float).to_numpy()
            f = df["forecast"].astype(float).to_numpy()
            for i in range(0, len(df) - H, H):
                fwd = c[i + H] / c[i] - 1.0
                coin_rows.append((coin, fwd, f[i]))
        if not coin_rows:
            continue
        cdf = pd.DataFrame(coin_rows, columns=["coin", "fwd", "fc"])
        cdf = cdf[np.isfinite(cdf["fwd"])]
        drift = cdf["fwd"].mean()  # coin's mean 72-bar return over all its windows
        cdf["ex"] = cdf["fwd"] - drift
        rows.append(cdf)

    if rows:
        data = pd.concat(rows, ignore_index=True)
        data = data[np.isfinite(data["ex"]) & np.isfinite(data["fc"])]
    else:
        data = pd.DataFrame(columns=["coin", "fwd", "fc", "ex"])

    n_grid = int(len(data))
    n_nonzero = int((data["fc"] != 0).sum()) if n_grid else 0

    def slope_t(x, y):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        if len(x) < 3 or np.std(x) == 0:
            return None, None
        lr = stats.linregress(x, y)
        t = lr.slope / lr.stderr if lr.stderr and lr.stderr > 0 else None
        return float(lr.slope), (float(t) if t is not None else None)

    slope, t = slope_t(data["fc"], data["ex"]) if n_grid else (None, None)

    per_coin = {}
    for coin, g in data.groupby("coin"):
        s, _ = slope_t(g["fc"], g["ex"])
        per_coin[coin] = s
    n_pos = int(sum(1 for s in per_coin.values() if s is not None and s > 0))
    check_pass = bool(n_pos >= 4)

    counts = {
        "grid cases with a non-zero forecast": n_nonzero,
        "grid cases": n_grid,
        "coins with a positive slope": n_pos,
        "coins": int(len(per_coin)),
    }
    reading = ("Regression is OLS with intercept on all grid cases (forecast at the grid bar, zero forecasts included) "
               "with drift = the coin's mean non-overlapping 72-bar grid return over all its windows; the per-coin check "
               "counts coins with a positive slope against the fixed requirement of 4; grid cells without a full 72-bar "
               "forward return in the window are dropped.")

    supp = {"name": "coins with a positive per-coin slope (need >= 4 of 6)", "value": n_pos, "passed": check_pass}
    mm = {"name": main_name, "value": t,
          "statistic": ({"name": "OLS slope t", "value": t} if t is not None else None),
          "threshold": threshold}

    if n_nonzero < 300:
        status = "not observable"
        decided = f"Only {n_nonzero} grid cases with a non-zero forecast, below the plan's minimum of 300."
    elif t is None:
        status = "inconclusive"
        decided = "The pooled slope's t-statistic could not be computed, so no confirm or reject rule is met."
    elif t >= 2 and check_pass:
        status = "confirmed"
        decided = "Pooled slope t >= 2 and the slope is positive for at least 4 of the 6 coins."
    elif t <= -2:
        status = "rejected"
        decided = "Pooled slope t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "Pooled slope t >= 2 but the per-coin check fails (fewer than 4 coins with a positive slope)."
    else:
        status = "inconclusive"
        decided = "Pooled slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": mm,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
