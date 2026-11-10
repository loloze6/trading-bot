import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    MIN_CASES = 15

    coins = [c for c in bars if "BTC" in str(c).upper()]
    if not coins:
        coins = list(bars.keys())

    all_rets, short_rets, short_fc = [], [], []
    for coin in coins:
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] < 0:
                    short_rets.append(r)
                    short_fc.append(fc[t])

    all_rets = np.array(all_rets, dtype=float)
    short_rets = np.array(short_rets, dtype=float)
    short_fc = np.array(short_fc, dtype=float)
    n_short = int(len(short_rets))

    reading = ("Sampled bars at offsets 0, 20, 40, ... within each window (return to t+20 inside the window), "
               "used all sampled bars as the unconditional set and sampled bars with forecast < 0 as short cases; "
               "t-stat is the one-sample t of short-bar returns against the unconditional mean "
               "(difference / (std of short returns / sqrt(n))); differences are in percentage points; "
               "largest-tertile shorts are the short cases with forecast at or below the 1/3 quantile of their forecasts.")

    main_name = "mean 20-bar fwd return on short bars minus mean over all bars (pp), sampled every 20 bars"
    main_thr = "confirm at or below -2 pp with t-stat <= -2; reject at 0 or above"

    diff = None
    tstat = None
    hit_diff = None
    top_mean = None
    if n_short > 0 and len(all_rets) > 0:
        uncond_mean = float(np.mean(all_rets))
        diff = (float(np.mean(short_rets)) - uncond_mean) * 100.0
        if n_short > 1:
            sd = float(np.std(short_rets, ddof=1))
            if sd > 0:
                tstat = (float(np.mean(short_rets)) - uncond_mean) / (sd / np.sqrt(n_short))
        hit_short = float(np.mean(short_rets < 0))
        hit_all = float(np.mean(all_rets < 0))
        hit_diff = (hit_short - hit_all) * 100.0
        q = np.quantile(short_fc, 1.0 / 3.0)
        top = short_rets[short_fc <= q]
        if len(top) > 0:
            top_mean = float(np.mean(top))

    hit_passed = None if hit_diff is None else bool(hit_diff >= 10.0)
    supporting = {
        "name": "hit rate short bars minus unconditional negative share (pp)",
        "value": None if hit_diff is None else float(hit_diff),
        "passed": hit_passed,
    }

    if n_short < MIN_CASES or diff is None:
        status = "inconclusive"
        decided = (f"Fewer than {MIN_CASES} non-overlapping short cases pooled across windows "
                   f"({n_short}), so the run is inconclusive whatever the numbers show.")
    else:
        reasons = []
        if diff >= 0:
            reasons.append("the difference is 0 or positive")
        if hit_diff <= 0:
            reasons.append("the short-bar hit rate is not above the unconditional share")
        if top_mean is not None and top_mean > 0:
            reasons.append("mean forward return after the largest-tertile shorts is positive")
        if reasons:
            status = "rejected"
            decided = "Reject: " + "; ".join(reasons) + "."
        elif diff <= -2.0 and tstat is not None and tstat <= -2.0 and hit_diff >= 10.0:
            status = "confirmed"
            decided = ("Confirm: difference at most -2 pp with t-stat at or below -2, and the short-bar hit rate "
                       "exceeds the unconditional share by at least 10 points.")
        else:
            status = "inconclusive"
            decided = "The result lies between the confirm and reject lines, so it is inconclusive."

    return {
        "status": status,
        "main_measure": {
            "name": main_name,
            "value": None if diff is None else float(diff),
            "threshold": main_thr,
        },
        "supporting_check": supporting,
        "cases": n_short,
        "decided_by": decided,
        "reading": reading,
        "details": {
            "t_stat": None if tstat is None else float(tstat),
            "n_all_sampled": int(len(all_rets)),
            "largest_tertile_short_mean_return": top_mean,
        },
    }
