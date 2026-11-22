import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.range_pos.last_history_value"
    PERIOD = 30

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # recompute from closes where the raw value is not recorded
            hi = close.rolling(PERIOD, min_periods=PERIOD).max()
            lo = close.rolling(PERIOD, min_periods=PERIOD).min()
            rng = hi - lo
            mid = (hi + lo) / 2.0
            pos = np.where(rng > 0, (close - mid) / (rng / 2.0), 0.0)
            pos = pd.Series(pos, index=df.index).where(rng.notna())
            raw = raw.fillna(pos)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # situation: close away from the range middle; side: long above, short below
            agree = active & raw.notna() & (raw != 0) & (np.sign(fc) == np.sign(raw))
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of active bars have a forecast whose sign matches the side of the close "
                           "relative to the middle of its 30-day closing range (long above, short below)."),
            "reading": "Situation bars are those with a nonzero raw range position; the expected side is its sign.",
        }

    # ---------- 2. Main measure: pooled regression of demeaned 10-bar forward return on forecast ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n, H):
                if t + H < n:
                    r = close[t + H] / close[t] - 1.0
                    rows.append((coin, fc[t], r))
    samp = pd.DataFrame(rows, columns=["coin", "fc", "r"]).dropna()
    if len(samp) > 0:
        samp["r_dm"] = samp["r"] - samp.groupby("coin")["r"].transform("mean")
    n_cases = int(len(samp))

    slope = None
    tval = None
    if n_cases >= 3 and samp["fc"].std() > 0:
        res = stats.linregress(samp["fc"].values, samp["r_dm"].values)
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr > 0 else None

    # ---------- 3. Supporting check: timing part of the book's mean daily return ----------
    per = []
    for coin, wins in bars.items():
        cr = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            cr.append((c / c.shift(1) - 1.0).iloc[1:])
        cr = pd.concat(cr) if cr else pd.Series(dtype=float)
        mu = float(cr.mean()) if len(cr.dropna()) else np.nan
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            d = pd.DataFrame({
                "day": ts.dt.floor("D"),
                "v": pd.to_numeric(df["postRebalance_total_value"], errors="coerce"),
                "a": pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce"),
            })
            d = d.groupby("day").last()
            br = d["v"] / d["v"].shift(1) - 1.0
            mg = d["a"].shift(1) * mu
            x = pd.DataFrame({"day": d.index, "coin": coin, "w": w,
                              "br": br.values, "mg": mg.values}).iloc[1:]
            per.append(x)
    timing = None
    book_mean = None
    if per:
        allx = pd.concat(per).dropna(subset=["br", "mg"])
        if len(allx):
            daily = allx.groupby("day")[["br", "mg"]].mean()
            book_mean = float(daily["br"].mean())
            timing = float(daily["br"].mean() - daily["mg"].mean())
    timing_pass = None if timing is None else bool(timing > 0)

    # ---------- 4. Decision ----------
    counts = {"non-overlapping cases": n_cases}
    if n_cases < 300:
        status = "not observable"
        decided_by = f"Only {n_cases} non-overlapping cases, fewer than the plan's minimum of 300."
    elif tval is None:
        status = "inconclusive"
        decided_by = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and timing_pass:
        status = "confirmed"
        decided_by = "The slope t is 2 or more and the timing part is positive."
    elif tval <= -2:
        status = "rejected"
        decided_by = "The slope t is -2 or less: moves away from the range middle reverse."
    elif tval >= 2:
        status = "inconclusive"
        decided_by = "The slope t is 2 or more but the timing part is 0 or less."
    else:
        status = "inconclusive"
        decided_by = "The slope t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "OLS slope of coin-demeaned 10-bar forward return on forecast, pooled",
            "value": slope,
            "statistic": None if tval is None else {"name": "OLS slope t", "value": tval},
            "threshold": "confirm if t >= 2 (with positive timing part); reject if t <= -2",
        },
        "supporting_check": {
            "name": "book mean daily return minus gain from market rise (timing part)",
            "value": timing,
            "passed": timing_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("All grid bars (0, 10, 20, ... with a full 10-bar return inside the window) enter the regression "
                    "including zero forecasts, the coin mean 10-bar return is taken on those same grid samples over all "
                    "windows, each coin's book is its own value series with the position held into a day taken from the "
                    "previous bar's post-rebalance allocation, and the plan's 'fewer than 300 cases' is reported as "
                    "'not observable' per the workflow."),
    }
