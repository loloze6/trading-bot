import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RET7 = "debug_info.components.ret7.last_history_value"
    H = 7

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].astype(float)
            ret30 = close / close.shift(30) - 1.0
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            if RET7 in d.columns:
                r7 = pd.to_numeric(d[RET7], errors="coerce")
            else:
                r7 = pd.Series(np.nan, index=d.index)
            r7_prices = close / close.shift(7) - 1.0
            r7 = r7.fillna(r7_prices)
            active = fc.notna() & (fc != 0) & ret30.notna() & r7.notna()
            if active.sum() == 0:
                continue
            situ = ret30 < 0
            side_ok = np.sign(fc) == -np.sign(r7)
            n_active += int(active.sum())
            n_agree += int((active & situ & side_ok).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "OLS slope of demeaned 7-bar forward return on forecast, mean_reversion grid bars"
    main_thr = "t >= 2 confirms (with timing gain > 0); t <= -2 rejects; otherwise inconclusive; at least 100 grid cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": "Fewer than 90% of active bars (with computable 30-bar return) have a negative 30-bar return "
                          "and a forecast sign opposite to the 7-bar return, as the plan's Fidelity requires.",
            "reading": "The 30-bar return is recomputed from closes inside each window, so the first 30 bars of each "
                       "window are left out of the check; the expected side is short on a positive 7-bar return and long on a negative one.",
        }

    # ---------- 2. Main measure ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid_rets = []
        cand = []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            reg = d["regime"].astype(str).values
            n = len(d)
            for p in range(0, n, H):
                if p + H >= n:
                    continue
                fr = close[p + H] / close[p] - 1.0
                if not np.isfinite(fr):
                    continue
                grid_rets.append(fr)
                if reg[p] == "mean_reversion" and np.isfinite(fc[p]):
                    cand.append((fc[p], fr))
        if not grid_rets:
            continue
        mu = float(np.mean(grid_rets))
        for f, fr in cand:
            xs.append(float(f))
            ys.append(fr - mu)
    xs = np.asarray(xs)
    ys = np.asarray(ys)
    n_cases = int(len(xs))

    slope = None
    tstat = None
    if n_cases >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        tstat = float(lr.slope / lr.stderr) if lr.stderr > 0 else (float(np.sign(lr.slope) * np.inf) if lr.slope != 0 else 0.0)

    # ---------- 3. Supporting check: timing gain ----------
    rows = []
    for coin, wins in bars.items():
        all_r = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            all_r.append((c / c.shift(1) - 1.0).dropna())
        mu_d = float(pd.concat(all_r).mean()) if all_r else np.nan
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            day = ts.dt.floor("D")
            v = pd.to_numeric(d["postRebalance_total_value"], errors="coerce")
            a = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce")
            tmp = pd.DataFrame({"day": day, "v": v, "a": a})
            last = tmp.groupby("day", sort=True).last()
            br = last["v"] / last["v"].shift(1) - 1.0
            mk = last["a"].shift(1) * mu_d
            out = pd.DataFrame({"day": last.index, "book": br.values, "mkt": mk.values, "coin": coin})
            rows.append(out.iloc[1:])
    timing = None
    if rows:
        allr = pd.concat(rows, ignore_index=True).dropna(subset=["book", "mkt"])
        if len(allr):
            daily = allr.groupby("day")[["book", "mkt"]].mean()
            timing = float(daily["book"].mean() - daily["mkt"].mean())
    sup_pass = (timing is not None) and (timing > 0)

    counts = {"independent grid cases in mean_reversion": n_cases}
    reading = ("The 30-bar return for the situation check is recomputed from closes inside each window (first 30 bars "
               "left out); the coin mean subtracted is the mean 7-bar forward return over all its windows' grid bars; "
               "the slope t is the OLS slope over its standard error; the timing gain uses each coin's book value after "
               "rebalance, daily returns averaged across coins per day, minus the held allocation times the coin's mean daily return.")

    stat = {"name": "OLS slope t", "value": tstat} if tstat is not None else None
    main = {"name": main_name, "value": slope, "statistic": stat, "threshold": main_thr}
    sup = {"name": "book mean daily timing gain > 0", "value": timing, "passed": bool(sup_pass) if timing is not None else None}

    if n_cases < 100 or tstat is None:
        status = "not observable"
        decided = f"Only {n_cases} independent mean_reversion grid cases, below the plan's minimum of 100."
    elif tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope has t >= 2 and the book's mean daily timing gain is above 0."
    elif tstat <= -2:
        status = "rejected"
        decided = "The slope has t <= -2: larger bounces in falling months come before higher excess returns."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "The slope has t >= 2 but the timing gain is not above 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
