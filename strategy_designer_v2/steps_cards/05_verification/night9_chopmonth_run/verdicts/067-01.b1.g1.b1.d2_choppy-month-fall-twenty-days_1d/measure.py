import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    BAND = 2.0
    LARGE = -10.0
    FALL_COL = "debug_info.components.fall30.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(df)
            # 60-day return in percent, from the prices where 60 earlier bars exist in the window
            trend60 = np.full(n, np.nan)
            if n > 60:
                trend60[60:] = (close[60:] / close[:-60] - 1.0) * 100.0
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * n)
            choppy_reg = reg == "mean_reversion"
            choppy = np.where(np.isnan(trend60), choppy_reg,
                              (trend60 >= -10.0) & (trend60 <= 10.0))
            if FALL_COL in df.columns:
                fall_raw = pd.to_numeric(df[FALL_COL], errors="coerce").values
            else:
                fall_raw = np.full(n, np.nan)
            # fall over 30 days: recorded raw value, else recomputed from prices
            fall_px = np.full(n, np.nan)
            if n > 30:
                fall_px[30:] = (close[30:] / close[:-30] - 1.0) * 100.0
            fall = np.where(np.isnan(fall_raw), fall_px, fall_raw)
            is_fall = np.where(np.isnan(fall), False, fall < 0)
            active = fc != 0
            ok = active & choppy & is_fall & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.90)
    reading_check = ("the choppy regime is the 60-day close-to-close return in percent within [-10, +10] recomputed "
                     "from the prices, using the recorded regime label on bars without 60 earlier bars in the window; "
                     "the fall is the recorded fall30 raw value below 0")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean unusual move per short case over 20 bars", "value": None,
                             "statistic": None, "threshold": "t >= 2 (confirm), t <= -2 (reject)"},
            "supporting_check": None,
            "counts": {"active bars": n_active, "agreeing bars": n_agree},
            "decided_by": ("fewer than 90 % of the active bars are choppy bars (60-day return within +-10 %) after a "
                           "30-day fall with a short forecast, as the Fidelity states"),
            "reading": reading_check,
        }

    # ---------- 2. criterion ----------
    # normal drift per coin: mean 20-bar return on the non-overlapping grid of all its windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = df["close"].astype(float).values
            n = len(close)
            for p in range(0, n - H, H):
                if np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] > 0:
                    rets.append(close[p + H] / close[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (day, unusual, forecast)
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            # short bets: the forecast's size on the short side rises by >= band from its lowest since the last bet
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                m = max(-fc[i], 0.0)
                if m == 0.0:
                    ref = 0.0
                    continue
                if m - ref >= BAND - 1e-12:
                    bet[i] = True
                    ref = m
                else:
                    ref = min(ref, m)
            # once per 20-bar grid cell: the first bet in the cell
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                i = start + int(idx[0])
                if i + H >= n:
                    continue
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                r = close[i + H] / close[i] - 1.0
                u = -(r - drift[coin])
                cases.append((ts.iloc[i].floor("D"), u, fc[i]))

    n_cases = len(cases)
    days = sorted(set(c[0] for c in cases))
    n_days = len(days)

    mean_u = None
    t = None
    if n_cases > 0:
        u = np.array([c[1] for c in cases])
        mean_u = float(u.mean())
        dev = pd.Series(u - u.mean(), index=[c[0] for c in cases]).groupby(level=0).sum()
        se = np.sqrt(float((dev.values ** 2).sum())) / n_cases
        t = float(mean_u / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    n_large = n_small = 0
    if n_cases > 0:
        u = np.array([c[1] for c in cases])
        f = np.array([c[2] for c in cases])
        large = f <= LARGE
        n_large = int(large.sum())
        n_small = int((~large).sum())
        if n_large > 0 and n_small > 0:
            sup_val = float(u[large].mean() - u[~large].mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n_days < 30:
        status = "not observable"
        decided = f"fewer than 30 independent case-days ({n_days}), the plan's minimum"
    elif t is not None and mean_u > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "the mean unusual move is positive with a t of 2 or more, and large minus small cases is above 0"
        else:
            status = "inconclusive"
            decided = "a t of 2 or more with the supporting check failing is inconclusive"
    elif t is not None and mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "the mean unusual move is negative with a t of -2 or less"
    else:
        status = "inconclusive"
        decided = "the t lies between -2 and 2, which the plan calls inconclusive"

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {"name": "mean unusual move per short case over 20 bars (short-signed, minus coin drift)",
                         "value": mean_u,
                         "statistic": {"name": "t of the mean, same-day cases pooled", "value": t} if t is not None else None,
                         "threshold": "positive with t >= 2 to confirm; negative with t <= -2 to reject"},
        "supporting_check": {"name": "mean unusual move of cases with forecast <= -10 minus that of forecast > -10",
                             "value": sup_val, "passed": sup_pass},
        "counts": {"independent case-days": n_days, "cases": n_cases,
                   "large cases": n_large, "smaller cases": n_small},
        "decided_by": decided,
        "reading": (reading_check + "; a case is the first short bet (forecast size up >= 2 from its lowest since the "
                    "last bet) in each 20-bar grid cell of a window, its return taken from its own close, cases "
                    "without 20 later bars in the window dropped, and a supporting check with an empty group counts "
                    "as failed"),
    }
