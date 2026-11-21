import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    MIN_POS = 100
    MIN_TOTAL = 860

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            regime = df["regime"].astype(str)
            in_sit = regime == "trending"  # detector's decision for close >= SMA(200)
            n_active += int(active.sum())
            n_agree += int((active & in_sit & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The situation 'close at or above SMA(200)' is read from the recorded regime == 'trending', "
               "because the detector's ma200 component is not recorded and windows are too short to recompute a 200-bar SMA, "
               "with the expected side long (forecast > 0) and the range position and rise only grading the size; "
               "the coin's mean 20-bar return is the mean of its non-overlapping grid returns over all windows, "
               "the slope t is the OLS slope t (with intercept) of the pooled grid cases, "
               "'about 860 cases' is taken as at least 860 grid cases, and the book's daily returns are "
               "postRebalance_total_value bar-to-bar within each window, averaged across coins per day.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars in the 'trending' regime "
                           "(close at or above SMA(200)), so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. Main measure ----------
    grid_rows = []  # (coin, forecast, fwd)
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(close)
            for i in range(0, n, H):
                j = i + H
                if j >= n:
                    break
                c0, c1, f = close[i], close[j], fc[i]
                if not (np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f)) or c0 == 0:
                    continue
                grid_rows.append((coin, f, c1 / c0 - 1.0))
    g = pd.DataFrame(grid_rows, columns=["coin", "forecast", "fwd"])

    n_total = int(len(g))
    n_pos = int((g["forecast"] > 0).sum()) if n_total else 0

    slope = None
    tstat = None
    if n_total >= 3:
        g["coin_mean"] = g.groupby("coin")["fwd"].transform("mean")
        g["y"] = g["fwd"] - g["coin_mean"]
        x = g["forecast"].to_numpy(dtype=float)
        y = g["y"].to_numpy(dtype=float)
        if np.std(x) > 0:
            lr = stats.linregress(x, y)
            slope = float(lr.slope)
            tstat = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- 3. Supporting check: timing gain ----------
    recs = []
    for coin, wins in bars.items():
        # coin's mean daily return over all windows
        rets_all = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = pd.to_numeric(df["close"], errors="coerce")
            rets_all.append((c / c.shift(1) - 1.0).iloc[1:])
        if not rets_all:
            continue
        mu = float(pd.concat(rets_all).dropna().mean())
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            d = df.copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            d["day"] = d["ts"].dt.floor("D")
            d = d.sort_values("ts")
            d = d.groupby("day", as_index=False).last()
            v = pd.to_numeric(d["postRebalance_total_value"], errors="coerce")
            a = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce")
            br = (v / v.shift(1) - 1.0)
            mk = a.shift(1) * mu
            sub = pd.DataFrame({"day": d["day"], "book": br, "mkt": mk}).iloc[1:].dropna()
            sub["coin"] = coin
            recs.append(sub)
    timing = None
    if recs:
        r = pd.concat(recs, ignore_index=True)
        if len(r):
            daily = r.groupby("day")[["book", "mkt"]].mean()
            timing = float(daily["book"].mean() - daily["mkt"].mean())
    timing_pass = None if timing is None else bool(timing > 0)

    counts = {"grid cases with forecast above 0": n_pos, "grid cases in total": n_total}

    main = {
        "name": "t of slope of de-meaned forward 20-bar return on forecast, pooled",
        "value": tstat,
        "statistic": {"name": "OLS slope t", "value": tstat} if tstat is not None else None,
        "threshold": "confirm if t >= 2 (with positive timing gain); reject if t <= -2",
    }
    main["slope"] = slope
    supporting = {"name": "book timing gain (mean daily return minus market-rise gain)",
                  "value": timing, "passed": timing_pass}

    # ---------- 4. Decision ----------
    if n_pos < MIN_POS or n_total < MIN_TOTAL:
        status = "not observable"
        decided_by = (f"Minimum counts not reached: {n_pos} grid cases with forecast above 0 (need {MIN_POS}) "
                      f"and {n_total} cases in total (need about {MIN_TOTAL}).")
    elif tstat is None:
        status = "inconclusive"
        decided_by = "The slope t could not be computed (no variation in the forecast), so neither rule is met."
    elif tstat >= 2 and timing_pass:
        status = "confirmed"
        decided_by = "Confirm rule met: the slope t is 2 or more and the timing gain is positive."
    elif tstat <= -2:
        status = "rejected"
        decided_by = "Reject rule met: the slope t is -2 or less."
    elif tstat >= 2:
        status = "inconclusive"
        decided_by = "The slope t is 2 or more but the timing gain is 0 or less (or missing), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided_by = "The slope t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
