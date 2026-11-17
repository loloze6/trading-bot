import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 30
    MIN_CASES = 300
    C_COL = "debug_info.components.closeness.last_history_value"
    O_COL = "debug_info.components.offset.last_history_value"

    # ---------- 1. Situation check ----------
    # Graded rule on every bar: long when the standardised distance (closeness) is above its usual
    # depth, short when below; the centre is the config's standardised constant (offset component).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            if C_COL in df.columns and O_COL in df.columns:
                c = pd.to_numeric(df[C_COL], errors="coerce")
                o = pd.to_numeric(df[O_COL], errors="coerce")
                expected = np.sign(c + o)
                ok = active & c.notna() & o.notna() & (expected != 0) & (np.sign(f) == expected)
                n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = agreement >= 0.9

    main_name = "pooled slope of demeaned 30-bar forward return on forecast"
    threshold = "t >= 2 confirms (with timing gain > 0); t <= -2 rejects; otherwise inconclusive; at least 300 cases"
    reading = ("Expected side taken as sign(closeness + offset) from the recorded standardised values; samples at window "
               "positions 0,30,60,90 kept only when t+30 lies in the window; coin mean 30-bar return taken over the same "
               "non-overlapping samples of all its windows; OLS slope with intercept; timing gain computed before costs as "
               "position after bar t's trade x next-bar coin return, averaged across coins per day then over days.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars have a forecast sign equal to the sign of the standardised "
                           "distance relative to its usual depth (closeness + offset), as the Fidelity's graded "
                           "closer-than-usual long / farther short rule requires."),
            "reading": reading,
        }

    # ---------- 2. Main measure ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for p in (0, 30, 60, 90):
                if p + H < n:
                    r = close[p + H] / close[p] - 1.0
                    if np.isfinite(r) and np.isfinite(fc[p]):
                        rows.append((coin, fc[p], r))
    samp = pd.DataFrame(rows, columns=["coin", "f", "r"])
    n_cases = int(len(samp))

    slope = None
    t_val = None
    if n_cases >= 3:
        samp["rd"] = samp["r"] - samp.groupby("coin")["r"].transform("mean")
        x = samp["f"].to_numpy(dtype=float)
        y = samp["rd"].to_numpy(dtype=float)
        if np.var(x) > 0:
            res = stats.linregress(x, y)
            slope = float(res.slope)
            t_val = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    # ---------- 3. Supporting check: timing gain ----------
    drows = []
    for coin, wins in bars.items():
        coin_parts = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            pos = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            ts = pd.to_datetime(df["timestamp"], utc=True)
            ret_next = close.shift(-1) / close - 1.0
            part = pd.DataFrame({
                "day": ts.dt.floor("D").to_numpy(),
                "pos": pos.to_numpy(),
                "ret": ret_next.to_numpy(),
            }).iloc[:-1]
            coin_parts.append(part)
        if not coin_parts:
            continue
        cp = pd.concat(coin_parts, ignore_index=True).dropna(subset=["pos", "ret"])
        if len(cp) == 0:
            continue
        mu = cp["ret"].mean()
        cp["book"] = cp["pos"] * cp["ret"]
        cp["mkt"] = cp["pos"] * mu
        cp["coin"] = coin
        drows.append(cp)

    timing = None
    if drows:
        allp = pd.concat(drows, ignore_index=True)
        daily = allp.groupby("day")[["book", "mkt"]].mean()
        if len(daily) > 0:
            timing = float(daily["book"].mean() - daily["mkt"].mean())
    check_passed = (timing is not None) and (timing > 0)

    # ---------- 4. Decision ----------
    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping 30-bar cases, below the plan's minimum of 300."
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and check_passed:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the timing gain is above zero."
    elif t_val <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: closer to the high is followed by lower returns than usual."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the timing gain is zero or below, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_val} if t_val is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "book timing gain before costs (mean daily)",
            "value": timing,
            "passed": bool(check_passed) if timing is not None else None,
        },
        "counts": {"non-overlapping 30-bar cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
