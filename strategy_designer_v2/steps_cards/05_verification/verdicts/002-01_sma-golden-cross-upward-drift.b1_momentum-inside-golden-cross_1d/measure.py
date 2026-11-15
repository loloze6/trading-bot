import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    MOM = "debug_info.components.mom.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation: SMA50 above SMA200, which is the detector's rule, read from the `regime` column.
    # Side: momentum (a rise gives a long, a fall gives a short), so the forecast sign must equal the sign of the raw 20-bar change.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            fallback = close / close.shift(H) - 1
            if MOM in df.columns:
                mom = pd.to_numeric(df[MOM], errors="coerce")
                mom = mom.where(mom.notna(), fallback)
            else:
                mom = fallback
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            trending = df["regime"].astype(str) == "trending"
            side_ok = np.sign(fc) == np.sign(mom)
            n_agree += int((active & trending & side_ok & mom.notna()).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a nonzero forecast are trending-regime "
                          "(SMA50>SMA200) bars whose forecast sign equals the sign of the 20-bar price change.",
            "reading": "Situation taken from the regime column; side taken from the sign of the raw 20-bar momentum.",
        }

    # ---------- 2. Main measure: grid regression ----------
    grid_rows = []
    coin_grid_rets = {}
    coin_daily_rets = {}
    for coin, wins in bars.items():
        g_all = []
        d_all = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                r = close[i + H] / close[i] - 1
                if not np.isfinite(r):
                    continue
                g_all.append(r)
                grid_rows.append((coin, r, fc[i], reg[i] == "trending"))
            d = close[1:] / close[:-1] - 1
            d_all.extend([x for x in d if np.isfinite(x)])
        coin_grid_rets[coin] = float(np.mean(g_all)) if g_all else np.nan
        coin_daily_rets[coin] = float(np.mean(d_all)) if d_all else np.nan

    xs, ys = [], []
    for coin, r, f, tr in grid_rows:
        if tr and np.isfinite(f) and np.isfinite(coin_grid_rets[coin]):
            xs.append(f)
            ys.append(r - coin_grid_rets[coin])
    xs = np.array(xs, dtype=float)
    ys = np.array(ys, dtype=float)
    n_cases = int(len(xs))
    slope, t_slope = None, None
    if n_cases >= 3 and np.std(xs) > 0:
        res = stats.linregress(xs, ys)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    # ---------- 3. Supporting check: timing part ----------
    recs = []
    for coin, wins in bars.items():
        mu = coin_daily_rets[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            pos = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            r = close.shift(-1) / close - 1
            tr = df["regime"].astype(str) == "trending"
            day = pd.to_datetime(df["timestamp"]).dt.normalize()
            sub = pd.DataFrame({"w": w, "day": day, "gain": pos * r, "mkt": pos * mu})
            sub = sub[tr & sub["gain"].notna() & sub["mkt"].notna()]
            recs.append(sub)
    timing = None
    book_mean = None
    mkt_mean = None
    if recs:
        allr = pd.concat(recs, ignore_index=True)
        if len(allr):
            daily = allr.groupby(["w", "day"])[["gain", "mkt"]].mean()
            book_mean = float(daily["gain"].mean())
            mkt_mean = float(daily["mkt"].mean())
            timing = book_mean - mkt_mean
    timing_pass = None if timing is None else bool(timing > 0)

    # ---------- 4. Decision ----------
    if n_cases < 50:
        status = "not observable"
        decided = f"Only {n_cases} trending-regime grid cases, fewer than the 50 the plan requires."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope t could not be computed on the grid cases."
    elif t_slope >= 2:
        if timing_pass:
            status = "confirmed"
            decided = "Slope t is 2 or more on at least 50 grid cases and the timing part is positive."
        else:
            status = "inconclusive"
            decided = "Slope t is 2 or more but the timing part is 0 or less (or not measurable)."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Slope t is -2 or less on at least 50 grid cases."
    else:
        status = "inconclusive"
        decided = "Slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "OLS slope of next-20-bar excess return on forecast, trending grid bars",
            "value": slope,
            "statistic": {"name": "t of OLS slope", "value": t_slope} if t_slope is not None else None,
            "threshold": "t >= 2 confirms (with positive timing), t <= -2 rejects, on at least 50 grid cases",
        },
        "supporting_check": {
            "name": "trending-regime book mean daily return minus market-rise gain (timing), before costs",
            "value": timing,
            "passed": timing_pass,
        },
        "counts": {"trending-regime grid cases": n_cases},
        "decided_by": decided,
        "reading": "Trending bars are those with regime=='trending'; the coin's mean 20-bar return is the mean over all "
                   "its non-overlapping grid returns in all windows; the regression is pooled OLS with an intercept; "
                   "the timing part uses held position x (next daily return minus the coin's all-window mean daily "
                   "return) on trending-regime bars, averaged across coins per (window, day) and then over days.",
    }
