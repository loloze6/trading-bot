import numpy as np
import pandas as pd


def measure(bars):
    H = 24
    BAND = 2.0
    MIN_CASES = 100
    FALL_COL = "debug_info.components.fall.last_history_value"

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
            # volatility regime: 24h std of hourly returns vs its 720-bar mean, recomputed inside the window
            r1 = close / close.shift(1) - 1.0
            vol = r1.rolling(24, min_periods=24).std()
            ratio = vol / vol.rolling(720, min_periods=720).mean()
            reg_ok = (df["regime"].astype(str) == "mean_reversion") if "regime" in df.columns \
                else pd.Series(False, index=df.index)
            vol_ok = pd.Series(np.where(ratio.notna(), ratio >= 1.0, reg_ok), index=df.index).astype(bool)
            # falling hour: raw component value (vol-scaled 1h return) below 0; price return where not recorded
            if FALL_COL in df.columns:
                raw = pd.to_numeric(df[FALL_COL], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            fall_ok = pd.Series(np.where(raw.notna(), raw < 0, r1 < 0), index=df.index).astype(bool)
            situ = vol_ok & fall_ok
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean 24-bar excess return over coin's mean 24-bar return, per bet case"
    thr = "confirm: mean > 0 with t >= 2 (and larger-forecast half beats smaller); reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"independent cases": 0},
            "decided_by": "Fewer than 90% of bars with a nonzero forecast are long bars on a falling hour "
                          "with 24h volatility at or above its 720-bar average, as the Fidelity's situation requires.",
            "reading": "Volatility ratio recomputed from closes inside each window (the detector's regime where "
                       "history is too short); falling hour from the recorded raw component, else the price return.",
        }

    # ---------- 2. criterion ----------
    exc = []
    fcs = []
    for coin, wins in bars.items():
        # coin's mean 24-bar return over all windows (non-overlapping grid)
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            n = len(df)
            for p in range(0, n - H, H):
                a, b = close[p], close[p + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1.0)
            # bets: rise of the long forecast by >= BAND from its lowest level since the last bet
            low = 0.0
            taken_cells = set()
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    low = f
                    cell = t // H
                    if cell in taken_cells:
                        continue
                    taken_cells.add(cell)
                    if t + H < n:
                        a, b = close[t], close[t + H]
                        if np.isfinite(a) and np.isfinite(b) and a > 0:
                            coin_cases.append((b / a - 1.0, f))
                else:
                    low = min(low, f)
        if len(grid_rets) == 0:
            continue
        mu = float(np.mean(grid_rets))
        for r, f in coin_cases:
            exc.append(r - mu)
            fcs.append(f)

    exc = np.asarray(exc, dtype=float)
    fcs = np.asarray(fcs, dtype=float)
    n_cases = int(len(exc))

    mean_exc = float(np.mean(exc)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(exc, ddof=1))
        t_stat = float(mean_exc / (sd / np.sqrt(n_cases))) if sd > 0 else None

    diff = None
    sup_pass = None
    if n_cases > 0:
        med = float(np.median(fcs))
        hi = exc[fcs > med]
        lo = exc[fcs <= med]
        if len(hi) > 0 and len(lo) > 0:
            diff = float(np.mean(hi) - np.mean(lo))
            sup_pass = bool(diff > 0)
        else:
            sup_pass = False

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} independent cases, fewer than the plan's minimum of 100 pooled over coins and windows."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (no dispersion in excess returns)."
    elif mean_exc > 0 and t_stat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean excess return is positive with t >= 2 and the larger-forecast half beats the smaller half."
        else:
            status = "inconclusive"
            decided = "Mean excess return is positive with t >= 2 but the larger-forecast half does not beat the smaller half."
    elif mean_exc < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean excess return is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_exc,
            "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean excess of above-median-forecast half minus at-or-below-median half",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": {"independent cases": n_cases},
        "decided_by": decided,
        "reading": "Cases are long-side forecast rises of at least 2 points from the lowest long level since the last "
                   "bet (reset to 0 on flat), the first such bet in each 24-row grid cell of a window with a full 24 "
                   "bars ahead; the coin mean is over non-overlapping 24-bar grid returns of all its windows; the "
                   "median split puts forecasts strictly above the median in the larger half; the plan's 'fewer than "
                   "100 cases' is reported as not observable as the workflow requires.",
    }
