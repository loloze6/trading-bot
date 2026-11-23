import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    FC = "forecast"
    POS = "postRebalance_current_allocation"
    VAL = "postRebalance_total_value"

    def prep(df):
        d = df.copy()
        if "timestamp" in d.columns:
            d = d.sort_values("timestamp").reset_index(drop=True)
        else:
            d = d.reset_index(drop=True)
        return d

    # ---------- 1. Situation check: a down day (close < prior close), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = prep(df)
            close = d["close"].astype(float)
            prev = close.shift(1)
            fc = pd.to_numeric(d[FC], errors="coerce")
            known = prev.notna() & close.notna() & fc.notna()
            active = known & (fc != 0)
            down = close < prev
            n_active += int(active.sum())
            n_agree += int((active & down & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("The situation is checked from prices as close below the previous close inside the same window, "
               "with the first bar of each window left out of the check since its prior close is not recorded; "
               "the coin's mean 3-bar return is taken on the same non-overlapping grid of all bars of all its windows; "
               "the timing gain is read on daily book returns (postRebalance_total_value, inside windows, mean over coins per day) "
               "minus the position held into the day times the coin's mean daily return over all windows, averaged the same way; "
               "a count under the plan's 200 cases is reported as not observable, as the workflow requires.")

    main_name = "t of slope of 3-bar excess return on forecast, down-day grid bars"
    threshold = "confirm if t >= 2 (with timing gain > 0); reject if t <= -2; else inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "down-day grid cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are down days (close below the prior close) "
                           "with a positive (long) forecast, so the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    # ---------- 2. Main measure ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # coin mean 3-bar return over all windows, non-overlapping grid
        all_r = []
        rows = []
        for w, df in wins.items():
            d = prep(df)
            close = d["close"].astype(float).values
            fc = pd.to_numeric(d[FC], errors="coerce").values
            reg = d["regime"].astype(str).values
            n = len(d)
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    all_r.append(r)
                    if reg[i] == "mean_reversion" and np.isfinite(fc[i]):
                        rows.append((fc[i], r))
        if len(all_r) == 0:
            continue
        mu = float(np.mean(all_r))
        for f, r in rows:
            xs.append(float(f))
            ys.append(r - mu)

    n_cases = len(xs)
    slope = None
    t_val = None
    if n_cases >= 3:
        xa = np.array(xs)
        ya = np.array(ys)
        if np.std(xa) > 0:
            lr = stats.linregress(xa, ya)
            slope = float(lr.slope)
            t_val = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- 3. Supporting check: timing gain ----------
    recs = []
    for coin, wins in bars.items():
        rets = []
        frames = []
        for w, df in wins.items():
            d = prep(df)
            close = d["close"].astype(float)
            rets.append((close / close.shift(1) - 1.0).dropna())
            frames.append(d)
        allr = pd.concat(rets) if rets else pd.Series(dtype=float)
        if len(allr) == 0:
            continue
        mu_d = float(allr.mean())
        for d in frames:
            ts = pd.to_datetime(d["timestamp"], utc=True)
            day = ts.dt.floor("D")
            v = pd.to_numeric(d[VAL], errors="coerce")
            pos = pd.to_numeric(d[POS], errors="coerce")
            tmp = pd.DataFrame({"day": day, "v": v, "pos": pos})
            daily = tmp.groupby("day").agg(v=("v", "last"), pos=("pos", "last"))
            book = daily["v"] / daily["v"].shift(1) - 1.0
            mkt = daily["pos"].shift(1) * mu_d
            out = pd.DataFrame({"book": book, "mkt": mkt}).dropna()
            out["coin"] = coin
            recs.append(out)
    timing = None
    if recs:
        allrec = pd.concat(recs).reset_index().rename(columns={"index": "day"})
        if "day" not in allrec.columns:
            allrec = allrec.rename(columns={allrec.columns[0]: "day"})
        per_day = allrec.groupby("day")[["book", "mkt"]].mean()
        if len(per_day) > 0:
            timing = float(per_day["book"].mean() - per_day["mkt"].mean())
    sup_passed = None if timing is None else bool(timing > 0)

    # ---------- 4. Decision ----------
    if n_cases < 200:
        status = "not observable"
        decided = f"Only {n_cases} down-day grid cases across all coins and windows, fewer than the plan's minimum of 200."
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and sup_passed:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the timing gain is above 0 (the plan's confirm rule)."
    elif t_val <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less (the plan's reject rule)."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the timing gain is at or below 0 (the plan's inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2 (the plan's inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t_val is None else {"name": "OLS slope t", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "book timing gain (mean daily return minus position x coin mean daily return)",
            "value": timing,
            "passed": sup_passed,
        },
        "counts": {"down-day grid cases": n_cases, "active bars": n_active},
        "decided_by": decided,
        "reading": reading,
    }
