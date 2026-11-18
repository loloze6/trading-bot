import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    MIN_CASES = 30
    REGIME = "mean_reversion"

    def prep(df):
        df = df.copy()
        if "timestamp" in df.columns:
            df = df.sort_values("timestamp")
        df = df.reset_index(drop=True)
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df["forecast"] = pd.to_numeric(df["forecast"], errors="coerce")
        return df

    def fwd_ret(close):
        c = close.to_numpy(dtype=float)
        r = np.full(len(c), np.nan)
        if len(c) > H:
            r[:-H] = c[H:] / c[:-H] - 1.0
        return r

    def non_overlap(positions):
        kept, last = [], None
        for p in positions:
            if last is None or p > last + H:
                kept.append(p)
                last = p
        return kept

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df0 in wins.items():
            df = prep(df0)
            prepared[coin][w] = df
            close = df["close"]
            prior_min = close.shift(1).rolling(30, min_periods=30).min()
            sit = (close < prior_min).to_numpy()
            computable = prior_min.notna().to_numpy() & close.notna().to_numpy()
            reg = (df["regime"].astype(str) == REGIME).to_numpy() if "regime" in df.columns \
                else np.zeros(len(df), dtype=bool)
            situation = np.where(computable, sit, reg)
            fc = df["forecast"].to_numpy(dtype=float)
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.90
    else:
        agreement = None
        passed = True

    reading = ("The new-30-day-low situation is recomputed per window as close below the minimum of the prior 30 "
               "closes, falling back to the recorded regime ('mean_reversion') on a window's first 30 bars where "
               "that cannot be computed; the coin's mean 10-bar return is taken on the non-overlapping grid "
               "(positions 0, 10, 20, ... of each window) over all its windows; cases without a close 10 bars ahead "
               "in the same window are left out before the non-overlap rule; 'regime bars' are bars with regime "
               "'mean_reversion'; the plan's 'fewer than 30 independent cases' minimum is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "ordinary t of mean of forecast-scaled demeaned 10-bar return",
                             "value": None, "statistic": None,
                             "threshold": "mean > 0 with t >= 2 (confirm), mean < 0 with t <= -2 (reject), over >= 30 independent cases"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long on a new 30-day-low bar "
                           "(close below the lowest of the prior 30 closes), as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- coin mean 10-bar return (all windows, non-overlapping grid) ----------
    coin_mean = {}
    for coin, wins in prepared.items():
        vals = []
        for w, df in wins.items():
            r = fwd_ret(df["close"])
            grid = np.arange(0, len(df), H)
            g = r[grid] if len(grid) else np.array([])
            vals.extend([v for v in g if np.isfinite(v)])
        coin_mean[coin] = float(np.mean(vals)) if vals else np.nan

    # ---------- main measure and supporting check ----------
    xs = []
    div_rets = []
    zero_rets = []
    for coin, wins in prepared.items():
        cm = coin_mean[coin]
        for w, df in wins.items():
            r = fwd_ret(df["close"])
            fc = df["forecast"].to_numpy(dtype=float)
            ok = np.isfinite(r) & np.isfinite(fc)
            reg = (df["regime"].astype(str) == REGIME).to_numpy()

            pos_case = [i for i in range(len(df)) if ok[i] and fc[i] > 0]
            for i in non_overlap(pos_case):
                if np.isfinite(cm):
                    xs.append((fc[i] / 10.0) * (r[i] - cm))

            div_pos = [i for i in range(len(df)) if ok[i] and reg[i] and fc[i] > 0]
            for i in non_overlap(div_pos):
                div_rets.append(r[i])
            zero_pos = [i for i in range(len(df)) if ok[i] and reg[i] and fc[i] == 0]
            for i in non_overlap(zero_pos):
                zero_rets.append(r[i])

    n = len(xs)
    xs = np.asarray(xs, dtype=float)
    mean_x = float(xs.mean()) if n > 0 else None
    t_x = None
    if n > 1:
        sd = xs.std(ddof=1)
        if sd > 0:
            t_x = float(mean_x / (sd / np.sqrt(n)))

    if len(div_rets) > 0 and len(zero_rets) > 0:
        diff = float(np.mean(div_rets) - np.mean(zero_rets))
        sup_passed = bool(diff > 0)
    else:
        diff = None
        sup_passed = None

    counts = {
        "independent cases": int(n),
        "divergence cases (regime, forecast > 0)": int(len(div_rets)),
        "new-low cases with forecast 0": int(len(zero_rets)),
    }

    if n < MIN_CASES:
        status = "not observable"
        decided_by = f"Only {n} independent cases across all coins and windows, below the plan's minimum of 30."
    elif t_x is not None and mean_x > 0 and t_x >= 2:
        if sup_passed:
            status = "confirmed"
            decided_by = "Mean of x > 0 with t >= 2 over at least 30 independent cases, and the supporting difference is > 0."
        else:
            status = "inconclusive"
            decided_by = "A confirming t (>= 2) but the supporting difference is not > 0 (or not measurable), which the plan calls inconclusive."
    elif t_x is not None and mean_x < 0 and t_x <= -2:
        status = "rejected"
        decided_by = "Mean of x < 0 with t <= -2 over at least 30 independent cases."
    else:
        status = "inconclusive"
        decided_by = "t lies between -2 and 2 (or is undefined), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": "mean of x = (forecast/10) x (10-bar return - coin mean 10-bar return)",
            "value": mean_x,
            "statistic": {"name": "ordinary t of the mean", "value": t_x} if t_x is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 over >= 30 independent cases; reject: mean < 0 with t <= -2 over >= 30",
        },
        "supporting_check": {
            "name": "mean 10-bar return of divergence cases minus new-low cases with forecast 0",
            "value": diff,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
