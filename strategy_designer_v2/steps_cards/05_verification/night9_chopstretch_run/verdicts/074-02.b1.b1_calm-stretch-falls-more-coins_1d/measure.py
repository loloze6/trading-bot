import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    RAW = "debug_info.components.stretch.last_history_value"

    def raw_from_prices(df):
        c = df["close"].astype(float)
        sma = c.rolling(20, min_periods=20).mean()
        sd = c.pct_change().rolling(20, min_periods=20).std()
        return ((c - sma) / sma) / sd

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            raw = raw.where(raw.notna(), raw_from_prices(df))
            calm = df["regime"].astype(str) == "unknown"
            active = fc != 0
            situ = calm & (raw < 0) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the active bars are short bars with the close below its SMA20 in the calm profile (regime 'unknown'), as the Fidelity's situation and side require.",
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, ret, absfc)
    for coin, wins in bars.items():
        # normal drift: non-overlapping 5-bar returns over all windows of the coin
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            n = len(df)
            for i in range(0, n - H, H):
                if np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0:
                    grid_rets.append(close[i + H] / close[i] - 1.0)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            days = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D")
            # bets on the short side
            low = 0.0
            prev_side = 0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                m = -fc[i] if fc[i] < 0 else 0.0
                side = -1 if fc[i] < 0 else (1 if fc[i] > 0 else 0)
                if side != -1:
                    low = 0.0
                    prev_side = side
                    continue
                if prev_side != -1:
                    low = 0.0
                prev_side = -1
                if m - low >= BAND:
                    bet[i] = True
                    low = m
                else:
                    low = min(low, m)
            # one case per grid cell: first bet in the cell
            for start in range(0, n, H):
                idx = [j for j in range(start, min(start + H, n)) if bet[j]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    continue
                coin_cases.append((coin, days.iloc[t], close[t + H] / close[t] - 1.0, abs(fc[t])))
        if coin_cases:
            drift = float(np.mean(grid_rets)) if grid_rets else np.nan
            for (c, d, r, a) in coin_cases:
                if np.isfinite(drift):
                    cases.append((c, d, -(r - drift), a))

    N = len(cases)
    cdf = pd.DataFrame(cases, columns=["coin", "day", "u", "absfc"]) if N else pd.DataFrame(columns=["coin", "day", "u", "absfc"])
    n_days = int(cdf["day"].nunique()) if N else 0

    mean_u = float(cdf["u"].mean()) if N else None
    t_stat = None
    if N and n_days >= 2:
        g = cdf.groupby("day")["u"].agg(["sum", "count"])
        resid = g["sum"] - g["count"] * mean_u
        var = (n_days / (n_days - 1)) * float((resid ** 2).sum())
        se = np.sqrt(var) / N
        if se > 0:
            t_stat = float(mean_u / se)

    sup_val = None
    sup_pass = None
    if N:
        med = float(cdf["absfc"].median())
        deep = cdf.loc[cdf["absfc"] > med, "u"]
        shallow = cdf.loc[cdf["absfc"] <= med, "u"]
        if len(deep) and len(shallow):
            sup_val = float(deep.mean() - shallow.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n_days < 30:
        status = "not observable"
        decided = f"Fewer than 30 distinct days with cases ({n_days}): the plan's minimum count is not reached."
    elif t_stat is not None and mean_u > 0 and t_stat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move in the short direction above 0 with t >= 2, and the deeper half's mean exceeds the shallower half's."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting check (deeper half minus shallower half > 0) fails, which the plan calls inconclusive."
    elif t_stat is not None and mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean unusual move in the short direction below 0 with t <= -2: deep calm stretches rebound."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": "mean unusual 5-bar move per case, short direction",
            "value": mean_u,
            "statistic": None if t_stat is None else {"name": "t of the mean, cases of one day summed", "value": t_stat},
            "threshold": "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "deeper half minus shallower half mean unusual move (split at median |forecast|)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": int(N), "distinct days with cases": n_days, "active bars": int(n_active)},
        "decided_by": decided,
        "reading": "The calm profile is read as regime 'unknown' (no chop veto); a case is the first short bet (rise of short forecast size by >= 2 from its low since the last bet) in each 5-bar grid cell from the window's first row; the normal drift is the coin's mean 5-bar return on that grid over all its windows; the day-clustered t uses per-day summed deviations with a G/(G-1) correction; the deeper half is |forecast| strictly above the median, the shallower half at or below it; the plan's '<30 distinct days' rule is treated as the minimum count giving 'not observable'.",
    }
