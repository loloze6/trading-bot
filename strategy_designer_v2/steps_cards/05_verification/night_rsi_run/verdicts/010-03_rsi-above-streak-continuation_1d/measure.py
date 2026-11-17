import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 14
    RAW = "debug_info.components.rsi_age.last_history_value"

    # ---------- 1. Situation check: RSI(14) run above 50 (raw age > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars where the 14-day RSI "
                           "run above 50 is under way (raw age > 0) with a long forecast"
                           if n_active > 0 else "No bar has a non-zero forecast, so the config never takes the plan's situation"),
            "reading": "Situation taken as the recorded raw RsiMidlineAgeComponent value above 0 (RSI(14) above 50 for n days), expected side long; bars with a missing raw value count as outside the situation.",
        }

    # ---------- 2. Main measure: pooled regression of excess 14-bar return on forecast ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            for p in range(0, len(df) - H, H):
                c0, c1 = close[p], close[p + H]
                if np.isnan(c0) or np.isnan(c1) or c0 == 0 or np.isnan(fc[p]):
                    continue
                rows.append((coin, fc[p], c1 / c0 - 1.0))
    grid = pd.DataFrame(rows, columns=["coin", "forecast", "ret"])
    n_cases = int(len(grid))
    n_pos = int((grid["forecast"] > 0).sum()) if n_cases else 0

    slope = None
    t_slope = None
    if n_cases >= 3:
        grid["excess"] = grid["ret"] - grid.groupby("coin")["ret"].transform("mean")
        x = grid["forecast"].to_numpy(float)
        y = grid["excess"].to_numpy(float)
        if np.std(x) > 0:
            lr = stats.linregress(x, y)
            slope = float(lr.slope)
            t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- 3. Supporting check: timing part of book's mean daily return, before costs ----------
    # coin mean daily return over all windows
    coin_mean = {}
    per_coin = {}
    for coin, wins in bars.items():
        frames = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            pos = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            f = pd.DataFrame({
                "window": w,
                "timestamp": pd.to_datetime(df["timestamp"]).dt.floor("D"),
                "pos": pos,
                "ret_next": nxt,
            }).iloc[:-1]
            frames.append(f)
        if frames:
            cf = pd.concat(frames, ignore_index=True)
            coin_mean[coin] = float(cf["ret_next"].dropna().mean())
            per_coin[coin] = cf
    day_rows = []
    for coin, cf in per_coin.items():
        cf = cf.dropna(subset=["pos", "ret_next"]).copy()
        cf["gain"] = cf["pos"] * cf["ret_next"]
        cf["mkt"] = cf["pos"] * coin_mean[coin]
        # last bar of each day (daily bars: one per day)
        cf = cf.groupby(["window", "timestamp"], as_index=False).agg(gain=("gain", "sum"), mkt=("mkt", "last"))
        cf["coin"] = coin
        day_rows.append(cf)
    timing = None
    check_passed = None
    if day_rows:
        d = pd.concat(day_rows, ignore_index=True)
        book = d.groupby(["window", "timestamp"]).agg(gain=("gain", "mean"), mkt=("mkt", "mean"))
        if len(book):
            timing = float(book["gain"].mean() - book["mkt"].mean())
            check_passed = bool(timing > 0)

    # ---------- 4. Decision ----------
    counts = {"grid cases in total": n_cases, "cases with a forecast above 0": n_pos}
    if n_cases < 300:
        status = "not observable"
        decided = f"Only {n_cases} grid cases in total, fewer than the plan's minimum of 300."
    elif n_pos < 100:
        status = "not observable"
        decided = f"Only {n_pos} grid cases with a forecast above 0, fewer than the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither confirm nor reject is met."
    elif t_slope >= 2 and check_passed:
        status = "confirmed"
        decided = f"The slope's t is {t_slope:.2f} (>= 2) over {n_cases} cases and the timing part of the book's mean daily return is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = f"The slope's t is {t_slope:.2f} (<= -2) over {n_cases} cases: longer stretches above 50 are followed by lower excess 14-day returns."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = f"The slope's t is {t_slope:.2f} (>= 2) but the timing part of the book's mean daily return is not above 0."
    else:
        status = "inconclusive"
        decided = f"The slope's t is {t_slope:.2f}, between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "t of the pooled slope of excess 14-bar forward return on forecast",
            "value": t_slope,
            "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": "confirm if t >= 2 (with the check passing), reject if t <= -2",
        },
        "supporting_check": {
            "name": "timing part of the book's mean daily return before costs > 0",
            "value": timing,
            "passed": check_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Grid bars at positions 0, 14, 28, ... of each window with a full 14-bar forward return inside it; "
                    "each coin's mean 14-bar return is the mean over its grid cases across all windows; the slope is "
                    "one pooled OLS of excess return on forecast with the OLS standard error; the book before costs is "
                    "the daily mean over coins of position after the trade x next-bar return, and its market part uses "
                    "each coin's mean daily return over all windows."),
    }
