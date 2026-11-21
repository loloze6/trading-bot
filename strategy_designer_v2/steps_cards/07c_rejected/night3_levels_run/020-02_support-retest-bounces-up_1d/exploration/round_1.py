def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    rows = []
    allbars = []
    drift = {}
    for coin, wins in bars.items():
        # drift per horizon: non-overlapping grid over all windows
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            rs = np.array(rs)
            drift[(coin, h)] = (rs.mean(), rs.std())
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            lo = df["low"].values
            n = len(c)
            f = df["forecast"].fillna(0).values
            raw = df.get("debug_info.components.support_touches.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            fall5 = np.full(n, np.nan)
            fall5[5:] = c[5:] / c[:-5] - 1
            ret20 = np.full(n, np.nan)
            ret20[20:] = c[20:] / c[:-20] - 1
            # swing lows inside window (side 2), confirmed 2 bars later
            sw = [(j, lo[j]) for j in range(2, n - 2)
                  if lo[j] < lo[j-1] and lo[j] < lo[j-2] and lo[j] < lo[j+1] and lo[j] < lo[j+2]]
            for t in range(n):
                fw = {}
                for h in H:
                    fw[h] = c[t + h] / c[t] - 1 if t + h < n else np.nan
                lows = [v for (j, v) in sw if j + 2 <= t and j >= t - 90]
                near_above = sum(1 for v in lows if 0 <= c[t] / v - 1 <= 0.015)
                near_below = sum(1 for v in lows if 0 < 1 - c[t] / v <= 0.03)
                minlow = min(lows) if lows else np.nan
                rec = dict(coin=coin, w=w, wi=int(w[1:]), t=t, f=f[t], raw=raw[t],
                           fall5=fall5[t], ret20=ret20[t], na=near_above, nb=near_below,
                           brk=(c[t] < minlow) if lows else False,
                           year=pd.Timestamp(df["timestamp"].iloc[t]).year)
                for h in H:
                    rec[f"x{h}"] = fw[h] - drift[(coin, h)][0]
                    rec[f"r{h}"] = fw[h]
                allbars.append(rec)
    A = pd.DataFrame(allbars)
    A["cell5"] = A["t"] // 5
    # cases: forecast >=2, first per 5-grid cell
    cases = A[A.f >= 2].sort_values(["coin", "w", "t"]).groupby(["coin", "w", "cell5"]).head(1)
    def tm(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean%": 100*s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out = {}
    out["cases by horizon"] = pd.DataFrame({h: tm(cases[f"x{h}"]) for h in H}).T
    out["cases by coin x5"] = cases.groupby("coin")["x5"].apply(tm).unstack()
    out["cases by year x5"] = cases.groupby("year")["x5"].apply(tm).unstack()
    cases["fq"] = pd.qcut(cases.f.rank(method="first"), 4, labels=False)
    out["cases by forecast quartile x5"] = cases.groupby("fq")["x5"].apply(tm).unstack()
    cases["tr"] = np.sign(cases.ret20)
    out["cases by 20d trend sign x5"] = cases.groupby("tr")["x5"].apply(tm).unstack()
    # grid-sampled all bars, 5-day
    G = A[A.t % 5 == 0].copy()
    G["fell"] = G.fall5 < 0
    G["raw_pos"] = G.raw > 0
    out["grid fell x raw>0 x5"] = G.groupby(["fell", "raw_pos"])["x5"].apply(tm).unstack()
    G["fallq"] = pd.qcut(G.fall5.rank(method="first"), 5, labels=False)
    out["grid by 5d return quintile x5"] = G.groupby("fallq")["x5"].apply(tm).unstack()
    out["grid broke below all 90d swing lows x5"] = G.groupby("brk")["x5"].apply(tm).unstack()
    out["grid nb count (just below lows) x5"] = G.groupby(G.nb.clip(upper=3))["x5"].apply(tm).unstack()
    out["grid na count (just above lows), fell x5"] = G[G.fell].groupby(G.na.clip(upper=3))["x5"].apply(tm).unstack()
    out["grid brk by horizon"] = pd.DataFrame({h: tm(A[(A.t % h == 0) & A.brk][f"x{h}"]) for h in H}).T
    return out
