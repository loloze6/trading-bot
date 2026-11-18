import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.fall_1d.last_history_value"
    MIN_CASES = 300

    # ---------- per-coin mean daily return over all windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) >= 2:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if allr.size else np.nan

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            ret_price = np.full(len(c), np.nan)
            if len(c) >= 2:
                ret_price[1:] = c[1:] / c[:-1] - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
                raw = np.where(np.isfinite(raw), raw, ret_price)
            else:
                raw = ret_price
            active = np.isfinite(f) & (f != 0)
            n_active += int(active.sum())
            situ = np.isfinite(raw) & (raw < 0)
            n_agree += int((active & situ & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of next-day excess return on forecast (forecast > 0 bars, pooled)"
    thr = "confirm: slope > 0 with t >= 2 and timing gain > 0; reject: slope < 0 with t <= -2; at least 300 bars with forecast > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"bars with forecast > 0": None, "active bars": n_active},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars after a negative 1-day return, as the plan's situation (a 1-day fall, expecting a rise) requires.",
            "reading": "The situation is a negative recorded 1-bar return (recomputed from closes where missing), and the expected side is long.",
        }

    # ---------- main measure ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        mu = coin_mean[coin]
        for w, df in wins.items():
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) < 2:
                continue
            fwd = np.full(len(c), np.nan)
            fwd[:-1] = c[1:] / c[:-1] - 1.0
            ex = fwd - mu
            m = np.isfinite(f) & (f > 0) & np.isfinite(ex)
            xs.append(f[m])
            ys.append(ex[m])
    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    n_cases = int(x.size)

    slope = None
    tstat = None
    if n_cases >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        tstat = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- supporting check: timing gain ----------
    book_rows, mkt_rows = [], []
    for coin, wins in bars.items():
        mu = coin_mean[coin]
        for w, df in wins.items():
            v = pd.to_numeric(df["postRebalance_total_value"], errors="coerce").to_numpy(dtype=float)
            a = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            day = ts.dt.floor("D").to_numpy()
            if len(v) < 2:
                continue
            # last bar of each day
            tmp = pd.DataFrame({"day": day, "v": v, "a": a}).groupby("day", sort=True).last()
            vv = tmp["v"].to_numpy(dtype=float)
            aa = tmp["a"].to_numpy(dtype=float)
            dd = tmp.index.to_numpy()
            if len(vv) < 2:
                continue
            br = vv[1:] / vv[:-1] - 1.0
            mg = aa[:-1] * mu
            for d, b, g in zip(dd[1:], br, mg):
                if np.isfinite(b) and np.isfinite(g):
                    book_rows.append((d, coin, b))
                    mkt_rows.append((d, coin, g))
    timing = None
    if book_rows:
        bdf = pd.DataFrame(book_rows, columns=["day", "coin", "r"]).groupby("day")["r"].mean()
        mdf = pd.DataFrame(mkt_rows, columns=["day", "coin", "r"]).groupby("day")["r"].mean()
        timing = float(bdf.mean() - mdf.mean())
    sup_pass = None if timing is None else bool(timing > 0)

    counts = {"bars with forecast > 0": n_cases}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} bars with forecast > 0, fewer than the plan's minimum of 300."
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope's t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the timing gain is above 0 (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the timing gain is not above 0, which the plan calls inconclusive."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tstat is None else {"name": "OLS slope t", "value": tstat},
            "threshold": thr,
        },
        "supporting_check": {
            "name": "timing gain (book mean daily return minus market-rise gain)",
            "value": timing,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "The slope is an ordinary least-squares fit with intercept of every forecast > 0 bar's next-day excess return (coin mean over all its within-window daily returns) on its forecast, its t being slope over the fit's standard error, and the plan's 'fewer than 300 is inconclusive' is reported as 'not observable' per the workflow's minimum-count rule.",
    }
