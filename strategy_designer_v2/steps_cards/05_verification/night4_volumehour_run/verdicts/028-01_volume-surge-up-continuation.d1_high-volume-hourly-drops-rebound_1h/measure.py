import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.vol_fall.last_history_value"

    def wkey(w):
        s = "".join(ch for ch in str(w) if ch.isdigit())
        return (int(s) if s else 0, str(w))

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys(), key=wkey):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            price_ret = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # Situation: the hour fell (graded product negative); fall back to the price return where raw is missing
            fall = np.where(raw.notna(), raw < 0, price_ret < 0)
            fall = pd.Series(fall, index=df.index).astype(bool)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & fall & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean excess 24-bar return after bets, both coins"
    threshold = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2"
    sup_name = "OLS slope of excess 24-bar return on signal-bar forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars on an hour whose "
                           "volume-weighted scaled return is negative (a fall), as the plan's situation requires."),
            "reading": "The situation is read as a negative raw component value (an hourly fall), on the long side.",
        }

    # ---------- 2. criterion ----------
    case_ex = []
    case_fc = []
    per_coin = {}
    for coin in sorted(bars.keys()):
        # drift: mean 24-bar return on the non-overlapping grid, all windows pooled
        grid_rets = []
        coin_cases = []
        for w in sorted(bars[coin].keys(), key=wkey):
            df = bars[coin][w].reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            # bets: rise of the long forecast >= band from its lowest level since the last bet
            trough = 0.0
            taken_cells = set()
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f <= 0:
                    trough = 0.0
                    continue
                if f - trough >= BAND:
                    trough = f
                    cell = t // H
                    if cell in taken_cells:
                        continue
                    taken_cells.add(cell)
                    if t + H < n:
                        r = close[t + H] / close[t] - 1.0
                        if np.isfinite(r):
                            coin_cases.append((r, f))
                else:
                    trough = min(trough, f)
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan
        per_coin[coin] = len(coin_cases)
        if np.isfinite(drift):
            for r, f in coin_cases:
                case_ex.append(r - drift)
                case_fc.append(f)

    case_ex = np.asarray(case_ex, dtype=float)
    case_fc = np.asarray(case_fc, dtype=float)
    n_cases = int(len(case_ex))

    mean_ex = float(np.mean(case_ex)) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        sd = float(np.std(case_ex, ddof=1))
        t_val = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None
    slope = None
    if n_cases > 1 and np.var(case_fc) > 0:
        slope = float(np.polyfit(case_fc, case_ex, 1)[0])
    slope_pass = None if slope is None else bool(slope > 0)

    counts = {"cases over both coins": n_cases}
    for c, k in per_coin.items():
        counts["cases " + str(c)] = int(k)

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases over both coins, below the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean excess return could not be computed, so neither rule is met."
    elif mean_ex > 0 and t_val >= 2 and slope_pass:
        status = "confirmed"
        decided = "Mean excess return is positive with t >= 2 and the slope is above 0 (confirm rule)."
    elif mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean excess return is negative with t <= -2 (reject rule)."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the slope is at or below 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_ex,
                         "statistic": None if t_val is None else {"name": "t of the mean", "value": t_val},
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": slope, "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("A bet is the first bar in each 24-bar grid cell (from each window's first row) where the "
                    "positive forecast rises at least 2 points above its lowest level since the last bet (reset to 0 "
                    "when flat), the drift is each coin's own pooled grid mean, cases of both coins are pooled for the "
                    "mean, t and slope, and the plan's count below 30 is reported as not observable."),
    }
