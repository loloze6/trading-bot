import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    RAW = "debug_info.components.mom_over_vol.last_history_value"
    MOM = 28

    def tstat(x):
        x = np.asarray(x, dtype=float)
        x = x[np.isfinite(x)]
        n = len(x)
        if n < 2:
            return None
        sd = np.std(x, ddof=1)
        if not np.isfinite(sd) or sd == 0:
            return None
        return float(np.mean(x) / (sd / np.sqrt(n)))

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            # situation: sign of the 28-bar return; from the raw component when recorded,
            # else from the prices inside the window
            price_ret = close / close.shift(MOM) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            side = np.sign(raw)
            side = side.where(raw.notna(), np.sign(price_ret))
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & side.notna() & (side != 0) & (np.sign(fc) == side)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90

    main_name = "mean of forecast/10 x (20-bar forward return minus coin's normal 20-bar drift), non-overlapping grid, coins pooled"
    threshold = "confirm: mean > 0 with t >= 2.0 and timing gain > 0; reject: mean < 0 with t <= -2.0; at least 300 grid cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars have a forecast whose sign matches the sign of the 28-bar return (long after a rise, short after a fall), as the plan's Fidelity requires.",
            "reading": "The situation side is the sign of the recorded raw component (28-bar return over 30-bar volatility), falling back to the 28-bar price return inside the window when the raw value is missing.",
        }

    # ---------- 2. main measure ----------
    grid = {}  # coin -> list of (forecast, fwd)
    daily_rets = {}  # coin -> list of daily returns
    for coin, wins in bars.items():
        g = []
        dr = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H < n and np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] != 0:
                    g.append((fc[i], close[i + H] / close[i] - 1.0))
            if n > 1:
                r = close[1:] / close[:-1] - 1.0
                dr.extend([x for x in r if np.isfinite(x)])
        grid[coin] = g
        daily_rets[coin] = dr

    products = []
    for coin, g in grid.items():
        fwds = [f for _, f in g if np.isfinite(f)]
        if not fwds:
            continue
        drift = float(np.mean(fwds))
        for fcv, f in g:
            if np.isfinite(fcv) and np.isfinite(f):
                products.append(fcv / 10.0 * (f - drift))
    n_cases = len(products)
    main_mean = float(np.mean(products)) if n_cases > 0 else None
    t_main = tstat(products)

    # ---------- 3. supporting check: timing gain ----------
    mu = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in daily_rets.items()}
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) < 2:
                continue
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            day = ts.dt.floor("D")
            val = pd.to_numeric(df["postRebalance_total_value"], errors="coerce")
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            d = pd.DataFrame({"day": day, "val": val, "alloc": alloc})
            d = d.groupby("day", sort=True).last()  # last bar of each day
            d["book"] = d["val"] / d["val"].shift(1) - 1.0
            d["mkt"] = d["alloc"].shift(1) * mu.get(coin, np.nan)
            d = d.dropna(subset=["book", "mkt"])
            d = d[np.isfinite(d["book"]) & np.isfinite(d["mkt"])]
            for dayv, r in d.iterrows():
                rows.append((dayv, coin, r["book"], r["mkt"]))
    timing = None
    if rows:
        dd = pd.DataFrame(rows, columns=["day", "coin", "book", "mkt"])
        byday = dd.groupby("day")[["book", "mkt"]].mean()
        timing = float(byday["book"].mean() - byday["mkt"].mean())
    timing_pass = None if timing is None else bool(timing > 0)

    # ---------- 4. decision ----------
    if n_cases < 300:
        status = "not observable"
        decided = f"Only {n_cases} pooled grid cases, below the plan's minimum of 300."
    elif main_mean is None or t_main is None:
        status = "inconclusive"
        decided = "The t of the main mean could not be computed, so neither the confirm nor the reject rule is met."
    elif main_mean > 0 and t_main >= 2.0:
        if timing_pass:
            status = "confirmed"
            decided = "The main mean is positive with t >= 2.0 and the timing gain is above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2.0 but the timing gain is 0 or less, which the plan calls inconclusive."
    elif main_mean < 0 and t_main <= -2.0:
        status = "rejected"
        decided = "The main mean is negative with t <= -2.0."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2.0 and 2.0 (or its sign disagrees with the mean), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": main_mean,
            "statistic": None if t_main is None else {"name": "t of the mean", "value": t_main},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "book timing gain (mean daily book return minus gain from market's own rise)",
            "value": timing,
            "passed": timing_pass,
        },
        "counts": {"grid cases pooled": int(n_cases)},
        "decided_by": decided,
        "reading": "Every grid bar with a 20-bar forward return inside its window counts as a case, including flat (forecast 0) bars, and the coin's normal 20-bar drift is the mean of its grid forward returns over all windows; the plan's 'fewer than 300 grid cases' is treated as a minimum count, so it gives 'not observable'.",
    }
