def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    col = "debug_info.components.failed_bo.last_history_value"
    drift = {}
    rows = []
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs))
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            ts = pd.to_datetime(df["timestamp"]).dt.year.values
            raw = df[col].values if col in df else np.full(n, np.nan)
            fc = df["forecast"].values
            for t in range(24, n):
                # recompute failed breakout
                j = None
                for k in (1, 2, 3):
                    jj = t - k
                    if jj - 20 < 0: continue
                    ph = c[jj-20:jj].max()
                    if c[jj] > ph:
                        j = jj; hi = ph; break
                if j is None or not (c[t] < hi): continue
                # first failing bar only
                prev_fail = False
                if t - 1 > j:
                    prev_fail = c[t-1] < hi
                if prev_fail: continue
                pre = c[j-1] / c[j-21] - 1 if j - 21 >= 0 else np.nan
                tr60 = c[t] / c[t-60] - 1 if t - 60 >= 0 else np.nan
                depth = hi / c[t] - 1
                bo_size = c[j] / hi - 1
                r = {"coin": coin, "w": w, "t": t, "year": ts[t], "pre": pre, "tr60": tr60,
                     "depth": depth, "bo": bo_size, "lag": t - j, "fc": fc[t]}
                for h in H:
                    if t + h < n:
                        m, s = drift[(coin, h)]
                        r[f"u{h}"] = -((c[t+h] / c[t] - 1) - m)
                        r[f"tot{h}"] = -(c[t+h] / c[t] - 1)
                    else:
                        r[f"u{h}"] = np.nan; r[f"tot{h}"] = np.nan
                rows.append(r)
    E = pd.DataFrame(rows)
    # non-overlap per horizon 5 grid
    E["cell5"] = E["t"] // 5
    E5 = E.drop_duplicates(["coin", "w", "cell5"])
    def tt(x):
        x = pd.Series(x).dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    hz = {}
    for h in H:
        Eh = E.assign(cell=E["t"] // h).drop_duplicates(["coin", "w", "cell"])
        hz[f"h{h}"] = tt(Eh[f"u{h}"])
        hz[f"h{h}_tot"] = tt(Eh[f"tot{h}"])
    out["by_horizon_unusual_short"] = pd.DataFrame(hz).T
    out["by_coin_u5"] = E5.groupby("coin")["u5"].apply(tt).unstack()
    out["by_year_u5"] = E5.groupby("year")["u5"].apply(tt).unstack()
    E5 = E5.copy()
    E5["pre_q"] = pd.qcut(E5["pre"], 5, labels=False)
    E5["depth_q"] = pd.qcut(E5["depth"], 4, labels=False, duplicates="drop")
    E5["bo_q"] = pd.qcut(E5["bo"], 4, labels=False, duplicates="drop")
    E5["tr60_sign"] = np.sign(E5["tr60"])
    out["by_pre_q_u5"] = E5.groupby("pre_q")["u5"].apply(tt).unstack()
    out["by_pre_q_u10"] = E5.groupby("pre_q")["u10"].apply(tt).unstack()
    out["by_depth_q_u5"] = E5.groupby("depth_q")["u5"].apply(tt).unstack()
    out["by_bo_q_u5"] = E5.groupby("bo_q")["u5"].apply(tt).unstack()
    out["by_tr60_u5"] = E5.groupby("tr60_sign")["u5"].apply(tt).unstack()
    out["by_tr60_u10"] = E5.groupby("tr60_sign")["u10"].apply(tt).unstack()
    out["by_lag_u5"] = E5.groupby("lag")["u5"].apply(tt).unstack()
    out["n_events_total"] = len(E)
    return out
