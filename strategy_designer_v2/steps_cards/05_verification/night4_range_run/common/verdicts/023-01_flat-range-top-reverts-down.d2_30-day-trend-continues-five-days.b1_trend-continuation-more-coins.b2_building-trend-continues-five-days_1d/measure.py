import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.hump_ret.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(df), np.nan)
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            # situation: graded hump R*s*(1-s) non-zero; side: sign of the 30-day return = sign of raw
            situ = np.isfinite(raw) & (raw != 0)
            agree = active & situ & (np.sign(fc) == np.sign(raw))
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of drift-excess 5-bar return on forecast, non-overlapping grid, pooled"
    thr = "slope t >= 2 (confirm, with timing gain > 0) or <= -2 (reject), on >= 300 grid cases with non-zero forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are bars where the hump-weighted 30-day return is non-zero with the forecast on the side of the 30-day move.",
            "reading": "The situation is taken as a non-zero raw value R*s*(1-s), and the expected side as the sign of the 30-day return, which is the raw value's sign.",
        }

    # ---------- 2. main measure ----------
    rows = []  # coin, ret, forecast
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            for t in range(0, len(df) - H, H):
                r = c[t + H] / c[t] - 1.0
                rows.append((coin, r, fc[t]))
    g = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    g = g[np.isfinite(g["ret"])]
    drift = g.groupby("coin")["ret"].mean()
    g["exc"] = g["ret"] - g["coin"].map(drift)
    g = g[np.isfinite(g["exc"]) & np.isfinite(g["fc"])]
    n_grid = int(len(g))
    n_nonzero = int((g["fc"] != 0).sum())

    slope = None
    tval = None
    if n_grid >= 3 and g["fc"].var() > 0:
        x = g["fc"].to_numpy(dtype=float)
        y = g["exc"].to_numpy(dtype=float)
        res = stats.linregress(x, y)
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    # ---------- 3. supporting check: timing gain ----------
    drows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            a = pd.to_numeric(df[ALLOC], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D").to_numpy()
            r = c[1:] / c[:-1] - 1.0
            for i in range(len(r)):
                drows.append((coin, ts[i + 1], a[i], r[i]))
    d = pd.DataFrame(drows, columns=["coin", "day", "pos", "ret"])
    d = d[np.isfinite(d["ret"])]
    cmean = d.groupby("coin")["ret"].mean()
    d = d[np.isfinite(d["pos"])].copy()
    d["gain"] = d["pos"] * d["ret"]
    d["mkt"] = d["pos"] * d["coin"].map(cmean)
    timing = None
    if len(d) > 0:
        daily = d.groupby("day")[["gain", "mkt"]].mean()
        timing = float(daily["gain"].mean() - daily["mkt"].mean())
    sup_pass = None if timing is None else bool(timing > 0)

    # ---------- 4. decision ----------
    if n_nonzero < 300:
        status = "not observable"
        decided = f"Only {n_nonzero} grid cases with a non-zero forecast, below the plan's minimum of 300."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more on at least 300 grid cases with a non-zero forecast, and the timing gain is above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less on at least 300 grid cases with a non-zero forecast."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the timing gain is 0 or below."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tval is None else {"name": "OLS slope t", "value": tval},
            "threshold": thr,
        },
        "supporting_check": {
            "name": "timing gain (mean daily gain before costs minus market-rise gain)",
            "value": timing,
            "passed": sup_pass,
        },
        "counts": {
            "grid cases with a non-zero forecast": n_nonzero,
            "grid cases": n_grid,
        },
        "decided_by": decided,
        "reading": "The regression uses every grid case of each window (bars 0, 5, 10, ... from its first row), including those with a zero forecast, with an intercept, and the drift is each coin's mean of those grid returns over all its windows; the timing gain uses the position held after each bar times the next bar's coin return, with the market part being that position times the coin's mean daily return over all its windows, both averaged over coins each day and then over days.",
    }
