import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RET_P = 28
    RAW = "debug_info.components.hp_mom.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: position takes the sign of the 28-day return (proximity weight is always > 0),
    # so the expected side is long when the 28-day return > 0, short when < 0.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # fallback: 28-day return from prices inside the window where raw is missing
            r28 = close / close.shift(RET_P) - 1.0
            side_src = raw.where(raw.notna(), r28)
            active = fc.notna() & (fc != 0)
            for i in np.where(active.values)[0]:
                n_active += 1
                s = side_src.iloc[i]
                if pd.notna(s) and s != 0 and np.sign(s) == np.sign(fc.iloc[i]):
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of 10-bar excess return on forecast"
    threshold = "slope t >= +2 with >= 200 cases and timing gain > 0 confirms; slope t <= -2 with >= 200 cases rejects"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": 0, "active_bars": int(n_active)},
            "decided_by": "fewer than 90% of active bars have a forecast sign equal to the sign of the 28-day return "
                          "(the raw component value), as the plan's Fidelity requires",
            "reading": "the expected side is the sign of the raw component value (28-day return times a positive "
                       "proximity weight), with the price-based 28-day return used where the raw value is missing",
        }

    # ---------- 2. Main measure ----------
    rows = []  # (coin, fwd, forecast)
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            n = len(d)
            for p in range(0, n, H):
                if p + H < n:
                    c0, c1 = close[p], close[p + H]
                    if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                        rows.append((coin, c1 / c0 - 1.0, fc[p]))
    cases = pd.DataFrame(rows, columns=["coin", "fwd", "fc"])
    if len(cases):
        drift = cases.groupby("coin")["fwd"].mean()
        cases["excess"] = cases["fwd"] - cases["coin"].map(drift)
        cases = cases.dropna(subset=["excess", "fc"])
    n_cases = int(len(cases))

    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(cases["fc"].values) > 0:
        lr = stats.linregress(cases["fc"].values.astype(float), cases["excess"].values.astype(float))
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- 3. Supporting check: timing gain ----------
    # mean daily return per coin over all windows
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            rets.append((c.shift(-1) / c - 1.0).iloc[:-1])
        allr = pd.concat(rets) if rets else pd.Series(dtype=float)
        coin_mean[coin] = float(allr.dropna().mean()) if allr.notna().any() else np.nan

    gain_parts = []
    mkt_parts = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            day = ts.dt.floor("D")
            c = pd.to_numeric(d["close"], errors="coerce")
            pos = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce")
            r = c.shift(-1) / c - 1.0
            g = (pos * r).iloc[:-1]
            m = (pos * coin_mean[coin]).iloc[:-1]
            dd = day.iloc[:-1]
            tmp = pd.DataFrame({"day": dd.values, "g": g.values, "m": m.values}).dropna()
            # daily: sum within a day (1d bars: one bar per day)
            tmp = tmp.groupby("day")[["g", "m"]].sum().reset_index()
            tmp["coin"] = coin
            gain_parts.append(tmp)
    timing = None
    if gain_parts:
        allg = pd.concat(gain_parts, ignore_index=True)
        book = allg.groupby("day")[["g", "m"]].mean()
        if len(book):
            timing = float(book["g"].mean() - book["m"].mean())
    timing_pass = None if timing is None else bool(timing > 0)

    # ---------- 4. Decision ----------
    counts = {"cases": n_cases}
    if n_cases < 200:
        status = "not observable"
        decided = f"only {n_cases} non-overlapping cases, below the plan's minimum of 200"
    elif t_slope is None:
        status = "inconclusive"
        decided = "the slope's t could not be computed with enough cases"
    elif t_slope >= 2:
        if timing_pass:
            status = "confirmed"
            decided = "slope t is +2 or more with at least 200 cases and the timing gain is above zero"
        else:
            status = "inconclusive"
            decided = "slope t is +2 or more but the timing gain is zero or below"
    elif t_slope <= -2:
        status = "rejected"
        decided = "slope t is -2 or less with at least 200 cases"
    else:
        status = "inconclusive"
        decided = "slope t lies between -2 and +2"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "timing gain (book mean daily return before costs minus market-rise gain)",
            "value": timing,
            "passed": timing_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "all grid cases are kept, including those with a zero forecast, in a pooled OLS with intercept on "
                   "the coin's drift-removed 10-bar return; the book's return before costs is the held position times "
                   "the next bar's coin return, averaged over coins per day.",
    }
