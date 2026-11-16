import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    MIN_CASES = 30

    # ---------- 1. Situation check: golden cross (SMA50 > SMA200) -> regime 'trending', side long ----------
    # The detector's SMA spread is not recorded and windows (~120 bars, warm-up removed) are too short
    # to recompute a 200-day SMA, so the situation is read from the `regime` column.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            if "regime" in df.columns:
                reg = df["regime"].astype(str).str.strip().str.lower()
                in_sit = reg == "trending"
            else:
                in_sit = pd.Series(False, index=df.index)
            n_active += int(active.sum())
            n_agree += int((active & in_sit & (f > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    threshold_txt = ("mean excess > 0 with t >= 2 (and top-half minus bottom-half > 0) to confirm; "
                     "mean excess < 0 with t <= -2 to reject; at least 30 cases")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean 20-bar forward excess return over coin mean, active grid bars",
                             "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active grid cases": 0, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars in the 'trending' "
                           "regime (50-day SMA above 200-day SMA), so the config does not trade the plan's situation."
                           if n_active > 0 else
                           "No bar has a non-zero forecast, so the plan's situation cannot be matched."),
            "reading": "The golden-cross situation is checked on the regime column ('trending') with a positive forecast.",
        }

    # ---------- 2. Criterion ----------
    case_rows = []  # (coin, forward return, forecast)
    coin_grid_returns = {}
    for coin, wins in bars.items():
        rets_all = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = (pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
                 if "forecast" in df.columns else np.full(len(df), np.nan))
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                rets_all.append(r)
                if np.isfinite(f[t]) and f[t] > 0:
                    case_rows.append((coin, r, float(f[t])))
        coin_grid_returns[coin] = rets_all

    coin_mean = {c: (float(np.mean(v)) if len(v) > 0 else np.nan) for c, v in coin_grid_returns.items()}

    excess = []
    fc = []
    for coin, r, fv in case_rows:
        m = coin_mean.get(coin, np.nan)
        if np.isfinite(m):
            excess.append(r - m)
            fc.append(fv)
    excess = np.asarray(excess, dtype=float)
    fc = np.asarray(fc, dtype=float)
    n_cases = int(len(excess))

    mean_ex = float(np.mean(excess)) if n_cases > 0 else None
    t_stat = None
    if n_cases >= 2:
        sd = float(np.std(excess, ddof=1))
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n_cases)))

    diff = None
    check_passed = None
    n_top = n_bot = 0
    if n_cases >= 2:
        med = float(np.median(fc))
        top = excess[fc > med]
        bot = excess[fc <= med]
        n_top, n_bot = int(len(top)), int(len(bot))
        if n_top > 0 and n_bot > 0:
            diff = float(np.mean(top) - np.mean(bot))
            check_passed = bool(diff > 0)
        else:
            check_passed = False

    counts = {"active grid cases": n_cases, "top half cases": n_top, "bottom half cases": n_bot}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} active grid cases, below the plan's minimum of 30."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean cannot be computed (zero dispersion), so neither confirm nor reject is met."
    elif mean_ex > 0 and t_stat >= 2 and check_passed:
        status = "confirmed"
        decided = "Mean excess above 0 with t >= 2, top half beats bottom half, with at least 30 cases."
    elif mean_ex < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean excess below 0 with t <= -2, with at least 30 cases."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the top half does not beat the bottom half, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies strictly between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean 20-bar forward excess return over coin mean, active grid bars",
                         "value": mean_ex,
                         "statistic": ({"name": "t of the mean", "value": t_stat} if t_stat is not None else None),
                         "threshold": threshold_txt},
        "supporting_check": {"name": "mean excess top half minus bottom half by forecast (median split)",
                             "value": diff, "passed": check_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Situation read from regime == 'trending' with forecast > 0; grid at positions 0, 20, 40, ... of "
                    "each window with only bars having a full 20-bar forward return inside the window; the coin's mean "
                    "20-bar return is the mean over all its grid bars in all windows; the median split puts forecasts "
                    "above the median in the top half and those at or below it in the bottom half."),
    }
