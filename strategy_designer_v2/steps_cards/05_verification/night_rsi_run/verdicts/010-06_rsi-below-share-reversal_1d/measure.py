import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 14
    RAW = "debug_info.components.rsi_below_share.last_history_value"
    ALLOC = "postRebalance_current_allocation"
    VAL = "postRebalance_total_value"

    # ---------- 1. Situation check ----------
    # Fidelity: situation = share of last 30 days with RSI(14) < 50; a larger share (above half) is
    # expected to give a higher return -> long when share > 0.5, short when share < 0.5.
    # Raw value = share - 0.5, so the expected side is the raw value's sign.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                ok = active & raw.notna() & (raw != 0) & (np.sign(raw) == np.sign(fc))
                n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of coin-demeaned forward 14-bar return on forecast (pooled, non-overlapping grid, non-zero forecast)"
    threshold = "confirm: slope > 0 with t >= 2 and timing gain > 0; reject: slope < 0 with t <= -2; at least 100 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"non-overlapping cases with a non-zero forecast": None, "active bars": n_active},
            "decided_by": ("The forecast's sign does not follow the sign of the share of the last 30 days with RSI(14) "
                           "below 50 minus one half (long when the share is above half) on at least 90% of active bars "
                           f"(agreement {agreement:.3f})."),
            "reading": "Expected side taken as the sign of the raw value (share below 50 minus 0.5); bars with a missing or zero raw value count as not in the situation.",
        }

    # ---------- 2. Main measure ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid_rows = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            for i in range(0, len(df) - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    grid_rows.append((r, fc[i]))
        if not grid_rows:
            continue
        rets = np.array([g[0] for g in grid_rows])
        fcs = np.array([g[1] for g in grid_rows])
        mu = float(np.mean(rets))  # coin's mean 14-bar return over all windows (grid)
        m = np.isfinite(fcs) & (fcs != 0)
        xs.extend(fcs[m].tolist())
        ys.extend((rets[m] - mu).tolist())

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n = int(len(x))
    slope, tstat = None, None
    if n >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        tstat = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    # ---------- 3. Supporting check: timing gain ----------
    frames = []
    for coin, wins in bars.items():
        cr = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = pd.to_numeric(df["close"], errors="coerce")
            cr.append((c / c.shift(1) - 1.0).iloc[1:])
        if not cr:
            continue
        mu_d = float(pd.concat(cr).dropna().mean())
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            d = pd.DataFrame({
                "ts": pd.to_datetime(df["timestamp"], utc=True),
                "v": pd.to_numeric(df[VAL], errors="coerce"),
                "a": pd.to_numeric(df[ALLOC], errors="coerce"),
            })
            d["day"] = d["ts"].dt.floor("D")
            d = d.groupby("day", sort=True).last().reset_index()
            if len(d) < 2:
                continue
            br = d["v"] / d["v"].shift(1) - 1.0
            mk = d["a"].shift(1) * mu_d
            out = pd.DataFrame({"day": d["day"], "book": br, "mkt": mk}).iloc[1:].dropna()
            frames.append(out)
    timing = None
    if frames:
        allf = pd.concat(frames)
        daily = allf.groupby("day")[["book", "mkt"]].mean()
        if len(daily) > 0:
            timing = float(daily["book"].mean() - daily["mkt"].mean())
    timing_pass = None if timing is None else bool(timing > 0)

    # ---------- 4. Decision ----------
    if n < 100:
        status = "not observable"
        decided = f"Only {n} non-overlapping cases with a non-zero forecast, below the plan's minimum of 100."
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope's t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tstat >= 2:
        if timing_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the timing gain is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the timing gain is not above 0."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tstat is None else {"name": "OLS slope t", "value": tstat},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "book timing gain before costs (mean daily book return minus position x coin mean daily return)",
            "value": timing,
            "passed": timing_pass,
        },
        "counts": {"non-overlapping cases with a non-zero forecast": n, "active bars": n_active},
        "decided_by": decided,
        "reading": ("The coin's mean 14-bar return is the mean over all its non-overlapping grid returns in all windows "
                    "(any forecast), the regression is OLS with an intercept on the raw forecast, and the book's daily "
                    "return is the change of postRebalance_total_value per coin averaged across coins per day, with the "
                    "market part as the previous day's position times the coin's mean daily close return."),
    }
