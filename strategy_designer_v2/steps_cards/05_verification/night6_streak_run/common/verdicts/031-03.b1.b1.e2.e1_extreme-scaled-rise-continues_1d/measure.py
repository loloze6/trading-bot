import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    THR = 0.9487
    RAW = "debug_info.components.rise.last_history_value"

    def prep(df):
        df = df.copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df = df.sort_values("timestamp").reset_index(drop=True)
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df["forecast"] = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
        return df

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df0 in wins.items():
            if df0 is None or len(df0) == 0:
                continue
            df = prep(df0)
            close = df["close"]
            r1 = close.pct_change()
            vol = r1.rolling(60, min_periods=60).std()
            vsr_re = (close / close.shift(10) - 1.0) / (vol * np.sqrt(10.0))
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), vsr_re)
            else:
                raw = vsr_re
            f = df["forecast"].values
            active = f != 0
            n_active += int(active.sum())
            ok = active & (f > 0) & (raw.values >= THR - 1e-9)
            n_agree += int(np.nansum(ok))
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    threshold_words = ("confirm: mean > 0 with t >= 2 and supporting check passes; "
                       "reject: mean < 0 with t <= -2; at least 30 distinct case days")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean unusual 10-bar move per long case", "value": None,
                             "statistic": None, "threshold": threshold_words},
            "supporting_check": None,
            "counts": {"distinct case days": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the raw "
                           "10-day volatility-scaled return is at least 0.9487, so the config does not do what "
                           "the Fidelity's situation and side state."),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    cases = []  # (unusual, forecast, day)
    for coin, wins in bars.items():
        dfs = []
        grid_rets = []
        for w, df0 in wins.items():
            if df0 is None or len(df0) == 0:
                continue
            df = prep(df0)
            dfs.append(df)
            c = df["close"].values
            for p in range(0, len(df), H):
                if p + H < len(df) and np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for df in dfs:
            f = df["forecast"].values
            c = df["close"].values
            n = len(df)
            # long bets
            bet = np.zeros(n, dtype=bool)
            low = 0.0
            prev = 0.0
            for i in range(n):
                fi = f[i]
                if fi > 0:
                    if prev <= 0:
                        low = 0.0
                    if fi - low >= BAND - 1e-12:
                        bet[i] = True
                        low = fi
                    else:
                        low = min(low, fi)
                else:
                    low = 0.0
                prev = fi
            # one case per grid cell: first bet in the cell
            for g in range(0, n, H):
                idx = np.where(bet[g:min(g + H, n)])[0]
                if len(idx) == 0:
                    continue
                t = g + int(idx[0])
                if t + H >= n or not np.isfinite(c[t]) or not np.isfinite(c[t + H]) or c[t] == 0:
                    continue
                ret = c[t + H] / c[t] - 1.0
                cases.append((ret - drift, float(f[t]), df["timestamp"].iloc[t].normalize()))

    n_cases = len(cases)
    days = pd.Series([x[2] for x in cases]) if cases else pd.Series(dtype=object)
    n_days = int(days.nunique()) if n_cases else 0

    mean_u = None
    tval = None
    sup_val = None
    sup_pass = None
    if n_cases > 0:
        u = np.array([x[0] for x in cases])
        fc = np.array([x[1] for x in cases])
        mean_u = float(u.mean())
        dev = pd.Series(u - mean_u).groupby(days.values).sum().values
        K = len(dev)
        if K > 1:
            se = np.sqrt(np.sum(dev ** 2) * K / (K - 1)) / n_cases
            tval = float(mean_u / se) if se > 0 else None
        k3 = n_cases // 3
        if k3 >= 1:
            order = np.argsort(fc, kind="mergesort")
            bottom = u[order[:k3]]
            top = u[order[-k3:]]
            sup_val = float(top.mean() - bottom.mean())
            sup_pass = bool(sup_val > 0)

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, fewer than the plan's minimum of 30."
    elif tval is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2 and the top-minus-bottom-third check above 0."
    elif mean_u > 0 and tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check failed, which the plan calls inconclusive."
    elif mean_u < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": "mean unusual 10-bar move per long case",
            "value": mean_u,
            "statistic": None if tval is None else {"name": "t of the mean, cases pooled by day", "value": tval},
            "threshold": threshold_words,
        },
        "supporting_check": {"name": "mean unusual move, top third by forecast minus bottom third",
                             "value": sup_val, "passed": sup_pass},
        "counts": {"distinct case days": n_days, "cases": n_cases},
        "decided_by": decided,
        "reading": ("A case is the first long bet (forecast rise of at least 2 points from its lowest long level "
                    "since the last bet) in each 10-bar grid cell of a window, its return taken from that bar's close "
                    "10 bars ahead within the window, the drift is the mean of the coin's grid 10-bar returns over all "
                    "its windows, and the thirds are floor(n/3) cases at each end of the forecast ranking."),
    }
