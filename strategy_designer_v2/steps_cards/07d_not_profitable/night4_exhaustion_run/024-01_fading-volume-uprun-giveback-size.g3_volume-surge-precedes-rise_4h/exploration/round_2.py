def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    # drift per coin
    drift = {}
    for c in coins:
        v = []
        for w, b in bars[c].items():
            cl = b.close.values; idx = np.arange(0, len(cl) - 18, 18)
            v += list(cl[idx + 18] / cl[idx] - 1)
        drift[c] = np.mean(v)
    cs = []; held = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b.close.values; op = b.open.values; f = b.forecast.fillna(0).values
            n = len(b)
            fwd = np.full(n, np.nan); fwd[:n - 18] = cl[18:] / cl[:n - 18] - 1
            r180 = np.full(n, np.nan); r180[180:] = cl[180:] / cl[:-180] - 1
            r42 = np.full(n, np.nan); r42[42:] = cl[42:] / cl[:-42] - 1
            lr = pd.Series(cl).pct_change()
            sd = lr.rolling(180, min_periods=60).std().values
            sdl = lr.rolling(1080, min_periods=180).std().values
            r1 = (cl / op - 1) / sd
            # bar-level position gain by trend state
            alloc = b.postRebalance_current_allocation.fillna(0).values
            nxt = np.full(n, np.nan); nxt[:-1] = cl[1:] / cl[:-1] - 1
            held.append(pd.DataFrame(dict(coin=c, w=w, g=alloc * nxt, a=alloc,
                                          tr30=r180 / (sd * np.sqrt(180)), volr=sd / sdl)))
            grid = np.arange(n) // 18
            seen = set(); low = 0.0
            for i in range(1, n):
                if f[i] <= 0: low = 0.0; continue
                if f[i] - low >= 2 and grid[i] not in seen:
                    seen.add(grid[i])
                    cs.append(dict(coin=c, w=int(w[1:]), fwd=fwd[i], r1=r1[i],
                                   tr30=r180[i] / (sd[i] * np.sqrt(180)) if sd[i] > 0 else np.nan,
                                   tr7=r42[i] / (sd[i] * np.sqrt(42)) if sd[i] > 0 else np.nan,
                                   volr=sd[i] / sdl[i] if sdl[i] > 0 else np.nan))
                    low = f[i]
                low = min(low, f[i])
    C = pd.DataFrame(cs).dropna(subset=["fwd"])
    C["ex"] = C.fwd - C.coin.map(drift)
    def grp(df, col, k=5):
        g = df.dropna(subset=[col]).copy()
        g["q"] = pd.qcut(g[col], k, labels=False, duplicates="drop")
        r = g.groupby("q").agg(n=("ex", "size"), x=(col, "mean"), ex=("ex", "mean"), sd=("ex", "std"), fwd=("fwd", "mean"))
        r["t"] = r.ex / (r.sd / np.sqrt(r.n)); r["p10_fwd"] = g.groupby("q").fwd.quantile(0.1)
        return r.drop(columns="sd").round(4)
    out["cases by trailing 30d trend z"] = grp(C, "tr30")
    out["cases by trailing 7d trend z"] = grp(C, "tr7")
    out["cases by vol ratio 30d/180d"] = grp(C, "volr")
    C["absr1"] = C.r1.abs()
    out["cases by |surge bar body| z"] = grp(C, "absr1")
    C["signed_body_x_trend"] = np.sign(C.r1) * np.sign(C.tr30)
    out["body sign vs trend sign"] = C.dropna(subset=["tr30"]).groupby(["signed_body_x_trend"]).ex.agg(["size", "mean", "std"]).round(4)
    out["bad windows 2,14,16 by trend z quintile"] = grp(C[C.w.isin([2, 14, 16])], "tr30", 3)
    H = pd.concat(held).dropna(subset=["g", "tr30"])
    H["q"] = pd.qcut(H.tr30, 5, labels=False)
    out["bar gain of position by 30d trend z"] = H.groupby("q").agg(mean_alloc=("a", "mean"), mean_gain=("g", "mean"), sum_gain=("g", "sum"), worst=("g", "min")).round(5)
    return out
