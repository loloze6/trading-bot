import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    SIG_RAW = "debug_info.components.signal_rise.last_history_value"
    H = 7
    MIN_CASES = 100

    def scaled_rise_from_prices(close):
        # 7-day return ending 7 bars ago, over (30-day daily std ending 7 bars ago x sqrt 7)
        r1 = close.pct_change()
        ret7 = close / close.shift(7) - 1.0
        vol = r1.rolling(30).std()
        return (ret7 / (vol * np.sqrt(7))).shift(7)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            if SIG_RAW in df.columns:
                sig = pd.to_numeric(df[SIG_RAW], errors="coerce")
            else:
                sig = pd.Series(np.nan, index=df.index)
            sig = sig.where(sig.notna(), scaled_rise_from_prices(close))
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            active = fc != 0
            # situation: lagged scaled weekly rise > 0, inside the choppy calm profile
            # (profile vetoes are the detector's decision: regime not 'chop'/'unknown', i.e. 'trending'),
            # expected side long (outcome: a rise)
            situ = (sig > 0) & (regime == "trending")
            agree = active & situ & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars where the lagged "
                          "7-day vol-scaled rise is above 0 in the choppy calm (trending, unvetoed) regime, "
                          "as the plan's Fidelity requires.",
            "reading": "The situation is the recorded signal_rise raw value (recomputed from prices if missing) above 0 "
                       "on a bar whose detector regime is 'trending' (profile vetoes not triggered), with a long forecast.",
        }

    # ---------- 2. criterion ----------
    # coin mean 7-bar return over all windows (non-overlapping grid of every window)
    xs, ys = [], []
    for coin, wins in bars.items():
        all_fwd = []
        per_win = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            grid = np.arange(0, n, H)
            for i in grid:
                if i + H < n:
                    c0, c1 = close[i], close[i + H]
                    if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                        fwd = c1 / c0 - 1.0
                        all_fwd.append(fwd)
                        per_win.append((fc[i], fwd))
        if len(all_fwd) == 0:
            continue
        coin_mean = float(np.mean(all_fwd))
        for f, fwd in per_win:
            if np.isfinite(f) and f > 0:
                xs.append(float(f))
                ys.append(fwd - coin_mean)

    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    n_cases = int(len(xs))

    slope = None
    t_slope = None
    if n_cases >= 3 and np.std(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            t_slope = float(lr.slope / lr.stderr)
    mean_excess = float(np.mean(ys)) if n_cases > 0 else None
    support_pass = (mean_excess > 0) if mean_excess is not None else None

    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = f"Only {n_cases} independent grid cases with forecast above 0, fewer than the plan's minimum of 100."
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed (no spread in the forecast), so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and support_pass:
        status = "confirmed"
        decided_by = "Slope t is 2 or more and the mean excess 7-bar return is above 0, on at least 100 independent grid cases."
    elif t_slope >= 2:
        status = "inconclusive"
        decided_by = "Slope t is 2 or more but the mean excess 7-bar return is at or below 0 (a confirming slope with a failed supporting check)."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "Slope t is -2 or less, on at least 100 independent grid cases."
    else:
        status = "inconclusive"
        decided_by = "Slope t lies between -2 and 2, on at least 100 independent grid cases."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": "pooled OLS slope of excess 7-bar forward return on forecast (grid cases, forecast > 0)",
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": "confirm if t >= 2 (with mean excess > 0), reject if t <= -2, on at least 100 independent grid cases",
        },
        "supporting_check": {
            "name": "mean excess 7-bar forward return over the same grid cases > 0",
            "value": mean_excess,
            "passed": None if support_pass is None else bool(support_pass),
        },
        "counts": {"independent grid cases": n_cases},
        "decided_by": decided_by,
        "reading": "Grid bars are positions 0, 7, 14, ... of each window with a full 7-bar forward return inside the window, "
                   "the coin's mean 7-bar return is the mean over all such grid bars of all its windows, and the profile part "
                   "of the situation is read from the detector's 'regime' column since its components are not recorded.",
    }
