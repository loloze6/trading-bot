import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 84
    BAND = 2.0
    RAW = "debug_info.components.panic.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            # prior 30-day return: 180-bar return ending 6 bars ago, inside this window only
            prior = np.full(n, np.nan)
            for t in range(186, n):
                prior[t] = close[t - 6] / close[t - 186] - 1.0
            # panic drop: prior 24h high minus close (recorded raw value); recompute if missing
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(n, np.nan)
            high = df["high"].astype(float).values
            for t in range(n):
                if np.isnan(raw[t]) and t >= 6:
                    raw[t] = high[t - 6:t].max() - close[t]
            for t in range(n):
                if not np.isfinite(fc[t]) or fc[t] == 0:
                    continue
                if np.isnan(prior[t]) or np.isnan(raw[t]):
                    n_active_uncomputable += 1
                    continue
                n_active += 1
                if prior[t] < 0 and raw[t] > 0 and fc[t] > 0:
                    n_agree += 1

    reading = ("Situation = 180-bar close return ending 6 bars ago below 0 (recomputed from prices inside each window, "
               "active bars in a window's first 186 bars left out of the agreement as not computable) and close below "
               "the prior 24h high (raw component > 0), side long; a case is the first long bet (forecast rise >= 2 from "
               "its lowest positive level since the last bet, reset at flat) in each 84-bar grid cell from each window's "
               "first row; the coin's mean 84-bar return uses the same non-overlapping grid over all its windows; terciles "
               "are the n//3 highest and n//3 lowest forecasts at entry after a stable sort.")

    main_name = "mean excess 84-bar return of bets over the coin's mean 84-bar return"
    thr = "confirm: mean > 0 with t >= 2 over >= 30 cases and top-minus-bottom third > 0; reject: mean < 0 with t <= -2 over >= 30 cases"

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": 0, "active_bars": 0},
            "decided_by": "No active bar with a computable situation: the record shows no bet, fewer than the 30 cases required.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active_bars": int(n_active)},
            "decided_by": ("Only {:.1%} of active bars are long bars with a negative prior 30-day return and a close "
                           "below the prior 24h high, under the 90 % required.".format(agreement)),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin mean 84-bar return over all windows (non-overlapping grid)
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    excess = []
    entry_fc = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(c)
            low = 0.0
            seen_cells = set()
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    low = f
                    cell = t // H
                    if cell in seen_cells:
                        continue
                    seen_cells.add(cell)
                    if t + H < n and np.isfinite(c[t + H]) and c[t] > 0 and np.isfinite(coin_mean[coin]):
                        r = c[t + H] / c[t] - 1.0
                        excess.append(r - coin_mean[coin])
                        entry_fc.append(f)
                else:
                    low = min(low, f)

    excess = np.array(excess, dtype=float)
    entry_fc = np.array(entry_fc, dtype=float)
    n_cases = int(len(excess))

    mean_ex = float(np.mean(excess)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(excess, ddof=1))
        t_stat = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None

    diff = None
    k = n_cases // 3
    if k >= 1:
        order = np.argsort(entry_fc, kind="stable")
        bottom = excess[order[:k]]
        top = excess[order[-k:]]
        diff = float(np.mean(top) - np.mean(bottom))
    sup_pass = None if diff is None else bool(diff > 0)

    counts = {"cases": n_cases, "active_bars": int(n_active), "top_third_cases": int(k), "bottom_third_cases": int(k)}

    if n_cases < 30:
        status = "not observable"
        decided = "Fewer than 30 cases ({}), the plan's minimum.".format(n_cases)
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t-statistic cannot be computed (zero dispersion), so neither rule is met."
    elif mean_ex > 0 and t_stat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean excess return above 0 with t >= 2 over at least 30 cases and top-minus-bottom third above 0."
        else:
            status = "inconclusive"
            decided = "Mean excess above 0 with t >= 2, but the top-minus-bottom third difference is at or below 0."
    elif mean_ex < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean excess return below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2: no verdict."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
            "threshold": thr,
        },
        "supporting_check": {"name": "top-third minus bottom-third excess return by entry forecast",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
