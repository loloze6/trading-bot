import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    RAW = "debug_info.components.mom60.last_history_value"

    def _sorted(df):
        df = df.copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        return df.sort_values("timestamp").reset_index(drop=True)

    data = {c: {w: _sorted(df) for w, df in wins.items() if df is not None and len(df) > 0}
            for c, wins in bars.items()}

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for c, wins in data.items():
        for w, df in wins.items():
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # where the raw value is missing, recompute the 60-bar return inside the window
            recomputed = close / close.shift(60) - 1.0
            raw = raw.where(raw.notna(), recomputed)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (np.sign(fc) == np.sign(raw)) & (raw != 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of the 20-bar forward return (minus the coin's mean 20-bar return) on the forecast"
    threshold = "confirm: slope > 0 with t >= 2 and timing part > 0; reject: slope < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a nonzero forecast have the forecast's sign equal to the sign of the coin's 60-day return, which the plan's situation and side require.",
            "reading": "The expected side is long when the raw 60-day return (last_history_value, recomputed from closes where missing) is positive and short when negative.",
        }

    # ---------- 2. main measure ----------
    rows = []
    for c, wins in data.items():
        crow = []
        for w, df in wins.items():
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for p in range(0, n, H):
                if p + H < n:
                    r = close[p + H] / close[p] - 1.0
                    if np.isfinite(r):
                        crow.append((c, fc[p], r))
        if crow:
            mean_r = np.mean([x[2] for x in crow])
            for (cc, f, r) in crow:
                rows.append((cc, f, r - mean_r))
    grid = pd.DataFrame(rows, columns=["coin", "forecast", "xret"])
    grid = grid.dropna()
    n_cases = int(len(grid))
    n_nonzero = int((grid["forecast"] != 0).sum()) if n_cases else 0

    slope = None
    tstat = None
    if n_cases >= 3 and grid["forecast"].var() > 0:
        x = grid["forecast"].values.astype(float)
        y = grid["xret"].values.astype(float)
        xm = x - x.mean()
        b = float(np.sum(xm * (y - y.mean())) / np.sum(xm ** 2))
        a = y.mean() - b * x.mean()
        resid = y - a - b * x
        s2 = np.sum(resid ** 2) / (len(y) - 2)
        se = np.sqrt(s2 / np.sum(xm ** 2))
        slope = b
        tstat = float(b / se) if se > 0 else None

    # ---------- supporting check: timing part ----------
    coin_mean_daily = {}
    for c, wins in data.items():
        rs = []
        for w, df in wins.items():
            cl = df["close"].astype(float)
            rs.append((cl / cl.shift(1) - 1.0).dropna())
        allr = pd.concat(rs) if rs else pd.Series(dtype=float)
        coin_mean_daily[c] = float(allr.mean()) if len(allr) else np.nan

    recs = []
    for c, wins in data.items():
        md = coin_mean_daily[c]
        for w, df in wins.items():
            d = df.copy()
            d["day"] = d["timestamp"].dt.floor("D")
            d = d.groupby("day").last()
            v = pd.to_numeric(d["postRebalance_total_value"], errors="coerce")
            alloc = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce")
            br = v / v.shift(1) - 1.0
            mk = alloc.shift(1) * md
            tmp = pd.DataFrame({"day": d.index, "coin": c, "book": br.values, "mkt": mk.values}).iloc[1:]
            recs.append(tmp)
    timing = None
    if recs:
        allrec = pd.concat(recs).dropna(subset=["book", "mkt"])
        if len(allrec):
            daily = allrec.groupby("day")[["book", "mkt"]].mean()
            timing = float(daily["book"].mean() - daily["mkt"].mean())
    timing_pass = None if timing is None else bool(timing > 0)

    counts = {"non-overlapping grid cases with a nonzero forecast": n_nonzero,
              "non-overlapping grid cases": n_cases}

    reading = ("The regression uses all non-overlapping 20-bar grid cases (positions 0, 20, ... of each window) with an intercept, "
               "the coin's mean 20-bar return is the mean over those grid cases of all its windows, and the timing part is the book's mean "
               "daily return (postRebalance_total_value, mean across coins per day) minus the previous bar's allocation times the coin's "
               "all-window mean daily return, averaged the same way.")

    if n_nonzero < 300:
        status = "not observable"
        decided = f"Only {n_nonzero} non-overlapping grid cases with a nonzero forecast, fewer than the 300 the plan requires."
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed."
    elif slope > 0 and tstat >= 2 and timing_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the timing part of the book's mean daily return is above 0."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    elif slope > 0 and tstat >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the timing check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": None if slope is None else float(slope),
                         "statistic": None if tstat is None else {"name": "OLS t of the slope", "value": float(tstat)},
                         "threshold": threshold},
        "supporting_check": {"name": "timing part of the book's mean daily return (book minus market gain) > 0",
                             "value": timing, "passed": timing_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
