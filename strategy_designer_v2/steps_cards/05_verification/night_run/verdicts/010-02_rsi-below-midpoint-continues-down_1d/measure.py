import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    MIN_CASES = 300
    RAW = "debug_info.components.rsi_below_share.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: the situation is the share of the last 14 days with RSI(14) below 50, graded.
    # A larger share means a larger fall (short). So a share above half should give a short
    # forecast, and a share below half a long one.
    raw_all = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if RAW in df.columns:
                raw_all.append(pd.to_numeric(df[RAW], errors="coerce"))
    raw_cat = pd.concat(raw_all) if raw_all else pd.Series(dtype=float)
    # The plan describes the raw value as share - 0.5. If no raw value is negative,
    # the raw value is read as the plain share, in 0..1.
    offset = 0.5 if (raw_cat.dropna() < 0).any() else 0.0

    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            share = raw + offset
            active = fc.notna() & (fc != 0)
            agree = active & (((share > 0.5) & (fc < 0)) | ((share < 0.5) & (fc > 0)))
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of the slope of the 7-bar forward excess return on the forecast (pooled, non-overlapping)"
    threshold = "confirm if t >= 2 with timing gain > 0; reject if t <= -2; at least 300 non-overlapping cases"
    reading = ("The raw value is read as share-0.5 when any raw value is negative, else as the plain share, "
               "with the situation's midpoint at a share of 0.5. Bars with a missing raw value count as disagreeing. "
               "The coin's mean 7-bar return is taken over its non-overlapping samples in all its windows. "
               "The minimum of 300 cases applies to the coins present in the record. "
               "The timing gain is measured before costs, from the position held times the next bar's close-to-close "
               "return minus the position times the coin's mean daily return, averaged over coins each day.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": (f"Only {agreement:.1%} of active bars are short when the RSI-below-50 share exceeds half "
                           "or long when it is below half, under the 90% required by the plan's Fidelity."),
            "reading": reading,
        }

    # ---------- 2. Main measure ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, fc[i]))
    samp = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    if len(samp):
        samp["excess"] = samp["ret"] - samp.groupby("coin")["ret"].transform("mean")
        samp = samp.dropna(subset=["excess", "fc"])
    n_cases = int(len(samp))

    slope = None
    t_slope = None
    if n_cases >= 3 and samp["fc"].std() > 0:
        x = samp["fc"].to_numpy(float)
        y = samp["excess"].to_numpy(float)
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr > 0 else None

    # ---------- 3. Supporting check: timing gain before costs ----------
    recs = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce")
            allr.append(close / close.shift(1) - 1.0)
        mu = float(pd.concat(allr).dropna().mean()) if allr else np.nan
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce")
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            r = close / close.shift(1) - 1.0
            pos = alloc.shift(1)
            d = pd.DataFrame({
                "ts": pd.to_datetime(df["timestamp"]).values,
                "book": (pos * r).values,
                "mkt": (pos * mu).values,
            }).dropna()
            recs.append(d)
    timing = None
    if recs:
        allrec = pd.concat(recs)
        if len(allrec):
            daily = allrec.groupby("ts")[["book", "mkt"]].mean()
            timing = float(daily["book"].mean() - daily["mkt"].mean())
    timing_pass = None if timing is None else bool(timing > 0)

    counts = {"non-overlapping cases pooled": n_cases}

    # ---------- 4. Decision ----------
    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases, below the plan's minimum of 300."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither rule is met."
    elif t_slope >= 2 and timing_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the timing gain is positive, which meets the confirm rule."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less, which meets the reject rule."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the timing gain is 0 or below, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and +2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": t_slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "book mean daily timing gain before costs > 0",
            "value": timing,
            "passed": timing_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
