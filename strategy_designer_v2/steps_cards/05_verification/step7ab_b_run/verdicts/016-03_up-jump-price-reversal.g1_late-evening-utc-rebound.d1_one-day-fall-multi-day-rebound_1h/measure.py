import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    RAW = "debug_info.components.fall_24h.last_history_value"

    # ---------- 1. Situation check: 24h fall (raw < 0), expected side long ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            recomputed = close / close.shift(24) - 1.0
            if RAW in df.columns:
                raw = df[RAW].astype(float).where(df[RAW].notna(), recomputed)
            else:
                raw = recomputed
            fc = df["forecast"].astype(float)
            active = fc.notna() & (fc != 0) & raw.notna()
            n_active += int(active.sum())
            n_agree += int((active & (raw < 0) & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    situation_check = {"agreement": agreement, "passed": passed}

    main_name = "OLS slope of 72-bar excess return (vs coin mean 72-bar return) on forecast, grid 0,72,144,..."
    threshold = "confirm: slope > 0 with t >= 2 and timing check > 0; reject: slope < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active-forecast bars are 24-hour-fall bars with a long forecast, "
                          "so the config does not trade the plan's situation on its side.",
            "reading": "The situation is a negative raw 24-bar percent change (recomputed from closes where not recorded), the side is long; bars with neither value are left out.",
        }

    # ---------- 2. Main measure ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            for t in range(0, n - H, H):
                r = close[t + H] / close[t] - 1.0
                if np.isfinite(r) and np.isfinite(fc[t]):
                    rows.append((coin, w, fc[t], r))
    g = pd.DataFrame(rows, columns=["coin", "window", "forecast", "ret"])
    n_total = int(len(g))
    n_pos = int((g["forecast"] > 0).sum()) if n_total else 0

    slope = None
    tstat = None
    if n_total >= 3 and g["forecast"].nunique() > 1:
        g["excess"] = g["ret"] - g.groupby("coin")["ret"].transform("mean")
        res = stats.linregress(g["forecast"].values, g["excess"].values)
        slope = float(res.slope)
        tstat = float(res.slope / res.stderr) if res.stderr > 0 else None

    # ---------- 3. Supporting check: timing part of the book's mean daily return ----------
    coin_daily = []
    for coin, wins in bars.items():
        per_w = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True).copy()
            df["ts"] = pd.to_datetime(df["timestamp"], utc=True)
            df["day"] = df["ts"].dt.floor("D")
            # position held during each bar's interval ending at this bar's close
            df["pos_held"] = df["postRebalance_current_allocation"].astype(float).shift(1)
            last = df.groupby("day").tail(1).set_index("day")
            d = pd.DataFrame(index=last.index)
            d["book_ret"] = last["postRebalance_total_value"].astype(float).pct_change()
            d["coin_ret"] = last["close"].astype(float).pct_change()
            # bars after the previous day's last bar up to this day's last bar = the day's bars
            d["pos"] = df.groupby("day")["pos_held"].mean()
            d = d.iloc[1:]
            d["window"] = w
            per_w.append(d)
        if not per_w:
            continue
        cd = pd.concat(per_w)
        mu = cd["coin_ret"].mean()
        cd["market_gain"] = cd["pos"] * mu
        cd["coin"] = coin
        coin_daily.append(cd.reset_index())
    timing = None
    if coin_daily:
        alld = pd.concat(coin_daily).dropna(subset=["book_ret", "market_gain"])
        daily = alld.groupby(["window", "day"])[["book_ret", "market_gain"]].mean()
        if len(daily):
            timing = float((daily["book_ret"] - daily["market_gain"]).mean())
    sup_pass = None if timing is None else bool(timing > 0)

    # ---------- 4. Decision ----------
    counts = {"grid cases with forecast > 0": n_pos, "grid cases in total": n_total}
    if n_pos < 200:
        status = "not observable"
        decided = f"Only {n_pos} grid cases with forecast > 0, fewer than the plan's minimum of 200."
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope or its t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the timing part of the book's daily return is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the timing check fails, which the plan calls inconclusive."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t-statistic lies between -2 and 2."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tstat is None else {"name": "OLS slope t", "value": tstat},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "book mean daily return minus market-rise gain (timing)",
            "value": timing,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "The slope comes from OLS with an intercept, pooled over all grid bars that have a full 72-bar forward return in their window; the coin's mean 72-bar return is the mean of its grid returns over all windows; the position behind each day's market gain is the mean of the positions held over that day's bars; and the plan's 'fewer than 200 cases' rule is reported as not observable, as the instructions require.",
    }
