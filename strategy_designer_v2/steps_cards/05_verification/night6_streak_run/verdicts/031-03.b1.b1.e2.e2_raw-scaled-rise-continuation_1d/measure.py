import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    THRESH = 2.0
    RAW = "debug_info.components.vsr_long.last_history_value"

    def recompute_vsr(close):
        r = close.pct_change()
        vol = r.rolling(60, min_periods=60).std()
        ret10 = close / close.shift(10) - 1.0
        return ret10 / (vol * np.sqrt(10.0))

    def find_bets(fc):
        # A bet: a rise of the forecast on its side of at least BAND from its lowest level
        # on that side since its last bet (from 0 after a flat or a change of side).
        bets = np.zeros(len(fc), dtype=bool)
        side, low = 0, 0.0
        for i, f in enumerate(fc):
            if not np.isfinite(f) or f == 0:
                side, low = 0, 0.0
                continue
            s = 1 if f > 0 else -1
            a = abs(f)
            if s != side:
                side, low = s, 0.0
            if a - low >= BAND:
                bets[i] = True
                low = a
            else:
                low = min(low, a)
        return bets

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            rec = recompute_vsr(close)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                vsr = raw.where(raw.notna(), rec)
            else:
                vsr = rec
            active = fc != 0
            n_active += int(active.sum())
            ok = active & (vsr >= THRESH) & (fc > 0)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 5-day move per case, long direction"
    thr_words = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 30 distinct case days"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_words},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars where the volatility-scaled "
                           "10-day return is at least 2 with a long forecast, so the config does not do what the "
                           "plan's Fidelity states." if n_active > 0 else
                           "The record has no bar with a non-zero forecast, so the plan's long extreme-rise situation is never traded."),
            "reading": "The situation is read as the raw vsr (recorded last_history_value, recomputed from prices where missing) >= 2 with a positive forecast.",
        }

    # ---------- criterion ----------
    vals = []
    days = []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 5-bar returns over all windows of the coin
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(close)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            bets = find_bets(fc)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for c0 in range(0, n, H):
                idx = [i for i in range(c0, min(c0 + H, n)) if bets[i] and fc[i] > 0]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                coin_cases.append((r, ts.iloc[i].strftime("%Y-%m-%d")))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for r, d in coin_cases:
            vals.append(r - drift)
            days.append(d)

    vals = np.array(vals, dtype=float)
    n_cases = int(len(vals))
    n_days = int(len(set(days)))
    mean = float(vals.mean()) if n_cases > 0 else None

    t = None
    if n_cases > 0 and n_days >= 2:
        dev = pd.Series(vals - mean).groupby(pd.Series(days)).sum().values
        D = len(dev)
        var = (D / (D - 1.0)) * np.sum(dev ** 2) / (n_cases ** 2)
        se = np.sqrt(var)
        t = float(mean / se) if se > 0 else None

    counts = {"distinct case days": n_days, "cases": n_cases}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, below the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed (zero standard error)."
    elif mean > 0 and t >= 2:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 over at least 30 distinct case days (confirm rule)."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2 over at least 30 distinct case days (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t} if t is not None else None),
            "threshold": thr_words,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": ("A case is the first long bet (forecast rise >= 2 points from its lowest level since the last bet) in each "
                    "5-bar grid cell from each window's first row, its 5-bar return inside the window minus the coin's mean "
                    "non-overlapping 5-bar return over all its windows, with the t's standard error clustered by the signal "
                    "bar's UTC date (deviations summed per day, D/(D-1) correction), and fewer than 30 days reported as not observable."),
    }
