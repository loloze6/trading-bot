import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.weekend_ret.last_history_value"
    H = 2
    MIN_CASES = 100

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    per_coin = {}
    for coin, wins in bars.items():
        per_coin[coin] = {}
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            # Raw Sunday-bar return: recorded component value, else recomputed from prices inside the window
            ret1 = close / close.shift(1) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").where(lambda s: s.notna(), ret1)
            else:
                raw = ret1
            is_sunday = (ts.dt.dayofweek == 6).values
            rise = (raw > 0).values
            active = (fc != 0).values
            agree = active & is_sunday & rise & (fc < 0).values
            n_active += int(active.sum())
            n_agree += int(agree.sum())
            per_coin[coin][w] = (ts, close, fc, is_sunday)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean per-case gain (forecast/10) x (2-bar return - m) on Sunday bars with forecast < 0"
    threshold = "confirm: mean gain > 0 with t >= 2 and supporting check passes; reject: mean gain < 0 with t <= -2"
    sup_name = "excess 2-bar return of large-|forecast| half minus small-|forecast| half (< 0 passes)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases pooled": None},
            "decided_by": ("No active bars in the record." if agreement is None else
                           f"Only {agreement:.1%} of active bars are Sunday-stamped bars after a weekend rise with a short "
                           "forecast, below the 90% the plan's situation requires."),
            "reading": "Situation taken as: bar stamped Sunday (UTC), Sunday-bar return > 0, forecast < 0.",
        }

    # ---------- 2. Criterion ----------
    gains, excess, absf = [], [], []
    for coin, wins in per_coin.items():
        # m: coin's mean 2-bar return over all windows, from non-overlapping grid
        grid = []
        for w, (ts, close, fc, sun) in wins.items():
            c = close.values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    grid.append(c[i + H] / c[i] - 1.0)
        if len(grid) == 0:
            continue
        m = float(np.mean(grid))
        for w, (ts, close, fc, sun) in wins.items():
            c = close.values
            f = fc.values
            n = len(c)
            for t in range(n):
                if sun[t] and f[t] < 0 and t + H < n:
                    if np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] != 0:
                        r = c[t + H] / c[t] - 1.0
                        ex = r - m
                        gains.append((f[t] / 10.0) * ex)
                        excess.append(ex)
                        absf.append(abs(f[t]))

    gains = np.array(gains, dtype=float)
    excess = np.array(excess, dtype=float)
    absf = np.array(absf, dtype=float)
    n_cases = int(len(gains))

    mean_gain = float(np.mean(gains)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(gains, ddof=1))
        t_stat = float(mean_gain / (sd / np.sqrt(n_cases))) if sd > 0 else None

    diff = None
    sup_pass = None
    n_large = n_small = 0
    if n_cases > 0:
        med = float(np.median(absf))
        large = absf > med
        small = ~large
        n_large, n_small = int(large.sum()), int(small.sum())
        if n_large > 0 and n_small > 0:
            diff = float(np.mean(excess[large]) - np.mean(excess[small]))
            sup_pass = bool(diff < 0)

    reading = ("Cases are Sunday-stamped (UTC) bars with forecast < 0 that have close[t+2] in the same window; "
               "m per coin from the 0,2,4,... grid of each window pooled over all windows; the median split puts "
               "|forecast| above the median in the large half and the rest in the small half; the plan's "
               "'fewer than 100 cases' minimum is reported as not observable.")

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases pooled, fewer than the plan's minimum of 100."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean gain could not be computed (zero dispersion)."
    elif mean_gain > 0 and t_stat >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "Mean gain above 0 with t >= 2 and the large-minus-small excess return below 0."
    elif mean_gain < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean gain below 0 with t <= -2: weekend rises continue into Monday-Tuesday."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name,
                         "value": mean_gain,
                         "statistic": None if t_stat is None else {"name": "ordinary t of the mean", "value": t_stat},
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": {"cases pooled": n_cases, "large-forecast half": n_large, "small-forecast half": n_small},
        "decided_by": decided,
        "reading": reading,
    }
