import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    MIN_CASES = 100
    RET_COL = "debug_info.components.ret30_size.last_history_value"

    def _num(s):
        return pd.to_numeric(s, errors="coerce")

    # ---------- 1. Situation check: ret30 > 0 (gate), side long ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = _num(df["close"])
            fc = _num(df["forecast"]).fillna(0.0)
            # Raw 30-day price change: recorded value where present, else recomputed inside the window
            ret_rec = _num(df[RET_COL]) if RET_COL in df.columns else pd.Series(np.nan, index=df.index)
            ret_px = close / close.shift(30) - 1.0
            ret30 = ret_rec.where(ret_rec.notna(), ret_px)
            active = fc != 0
            situation = ret30 > 0
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    reading = ("The situation is read as the gate 'PriceEvolution(30) > 0' with a long side, since 'near the high' has no "
               "cut-off and is the graded part of the comparison; the coin's mean 7-bar return is taken over all its "
               "non-overlapping grid bars in all windows; the regression is pooled OLS with intercept across coins and "
               "windows; the before-cost book is the held allocation times the next bar's return per coin, averaged "
               "across coins per day.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "slope of 7-bar excess return on forecast", "value": None,
                             "statistic": None, "threshold": "slope > 0 with t >= 2 to confirm; slope < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"non-overlapping in-regime cases": 0, "active bars": n_active},
            "decided_by": (f"Only {agreement:.1%} of active bars are long bars with a positive 30-day return, "
                           "below the 90% needed for the config to match the plan's situation and side."),
            "reading": reading,
        }

    # ---------- 2. Main measure ----------
    grid_rows = []           # all grid bars with a valid forward return
    daily_rows = []          # per coin per bar: day, alloc, next-bar return
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = _num(df["close"]).values
            fc = _num(df["forecast"]).values
            reg = df["regime"].astype(str).values
            n = len(df)
            for i in range(0, n, H):
                if i + H < n and np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0:
                    grid_rows.append({"coin": coin, "fwd": close[i + H] / close[i] - 1.0,
                                      "forecast": fc[i], "trending": reg[i] == "trending"})
            alloc = _num(df["postRebalance_current_allocation"]).values
            ts = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D").values
            for i in range(n - 1):
                if np.isfinite(close[i]) and np.isfinite(close[i + 1]) and close[i] > 0:
                    daily_rows.append({"coin": coin, "day": ts[i], "alloc": alloc[i],
                                       "r": close[i + 1] / close[i] - 1.0})

    g = pd.DataFrame(grid_rows, columns=["coin", "fwd", "forecast", "trending"])
    if len(g):
        coin_mean7 = g.groupby("coin")["fwd"].mean()
        g["excess"] = g["fwd"] - g["coin"].map(coin_mean7)
        cases = g[g["trending"] & g["forecast"].notna() & g["excess"].notna()]
    else:
        cases = g
    n_cases = int(len(cases))

    slope = None
    tval = None
    if n_cases >= 3 and cases["forecast"].nunique() > 1:
        res = stats.linregress(cases["forecast"].astype(float).values, cases["excess"].astype(float).values)
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    # ---------- 3. Supporting check: timing gain ----------
    timing = None
    total_gain = None
    market_gain = None
    d = pd.DataFrame(daily_rows, columns=["coin", "day", "alloc", "r"])
    if len(d):
        coin_mean1 = d.groupby("coin")["r"].mean()
        d = d[d["alloc"].notna()].copy()
        if len(d):
            d["gross"] = d["alloc"] * d["r"]
            d["mkt"] = d["alloc"] * d["coin"].map(coin_mean1)
            per_day = d.groupby("day")[["gross", "mkt"]].mean()
            total_gain = float(per_day["gross"].mean())
            market_gain = float(per_day["mkt"].mean())
            timing = total_gain - market_gain
    timing_passed = None if timing is None else bool(timing > 0)

    # ---------- 4. Decision ----------
    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = f"Only {n_cases} non-overlapping in-regime cases, fewer than the 100 the plan requires."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if timing_passed:
            status = "confirmed"
            decided_by = "The slope is above 0 with t >= 2 and the timing gain is positive."
        else:
            status = "inconclusive"
            decided_by = "The slope is above 0 with t >= 2 but the timing gain is 0 or less."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided_by = "The slope is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided_by = "The slope's t lies between -2 and 2 (or its sign disagrees with the confirm/reject rules)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "slope of 7-bar excess return on forecast, in-regime grid cases",
            "value": slope,
            "statistic": None if tval is None else {"name": "OLS slope t", "value": tval},
            "threshold": "slope > 0 with t >= 2 to confirm; slope < 0 with t <= -2 to reject",
        },
        "supporting_check": {
            "name": "timing part of the book's mean daily return before costs",
            "value": timing,
            "passed": timing_passed,
        },
        "counts": {"non-overlapping in-regime cases": n_cases, "active bars": n_active},
        "decided_by": decided_by,
        "reading": reading,
    }
