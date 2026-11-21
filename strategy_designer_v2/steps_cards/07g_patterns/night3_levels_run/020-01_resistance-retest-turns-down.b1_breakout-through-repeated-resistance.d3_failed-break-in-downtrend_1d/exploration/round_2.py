def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    out = {}
    grid = []; brk = []; dayrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            if n < 40: continue
            ts = pd.to_datetime(b["timestamp"])
            yr = ts.iloc[0].year
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            fwd = np.full(n, np.nan); fwd[:n-H] = c[H:]/c[:n-H]-1
            fwd20 = np.full(n, np.nan); fwd20[:n-20] = c[20:]/c[:n-20]-1
            p20 = np.full(n, np.nan); p20[20:] = c[20:]/c[:-20]-1
            p10 = np.full(n, np.nan); p10[10:] = c[10:]/c[:-10]-1
            vol20 = pd.Series(r1).rolling(20).std().values
            sh = np.zeros(n, bool)
            for i in range(2, n-2):
                if c[i] > max(c[i-2], c[i-1], c[i+1], c[i+2]): sh[i] = True
            brkflag = np.zeros(n); dist = np.full(n, np.nan)
            for t in range(3, n):
                lv = np.array([c[i] for i in range(max(0, t-90), t-2) if sh[i]])
                if not len(lv): continue
                crossed = lv[(c[t-1] <= lv) & (c[t] > lv)]
                if len(crossed):
                    brkflag[t] = 1; dist[t] = c[t]/crossed.max()-1
            for t in range(0, n, H):
                grid.append(dict(coin=coin, w=w, yr=yr, fwd=fwd[t], p20=p20[t], p10=p10[t], vol=vol20[t]))
            for t in range(0, n, 20):
                pass
            for g0 in range(0, n, H):
                for t in range(g0, min(g0+H, n)):
                    if brkflag[t]:
                        brk.append(dict(coin=coin, w=w, yr=yr, fwd=fwd[t], fwd20=fwd20[t], p20=p20[t],
                                        vol=vol20[t], dist=dist[t]))
                        break
    G = pd.DataFrame(grid).dropna(subset=["fwd"])
    drift = G.groupby("coin")["fwd"].mean(); sd = G.groupby("coin")["fwd"].std()
    G["u"] = G["fwd"] - G["coin"].map(drift)
    G["z"] = G["u"]/G["coin"].map(sd)
    G["p10z"] = G["p10"]/(G["vol"]*np.sqrt(10))
    G["p20z"] = G["p20"]/(G["vol"]*np.sqrt(20))
    def reg(df, x, y="z"):
        d = df.dropna(subset=[x, y])
        r = stats.linregress(d[x], d[y])
        return pd.Series({"n": len(d), "slope": r.slope, "t": r.slope/r.stderr, "corr": r.rvalue})
    out["grid_reg"] = pd.DataFrame({"p10z": reg(G, "p10z"), "p20z": reg(G, "p20z")}).T
    out["grid_p10z_by_coin"] = G.groupby("coin").apply(lambda d: reg(d, "p10z"))
    out["grid_p10z_by_year"] = G.groupby("yr").apply(lambda d: reg(d, "p10z"))
    B = pd.DataFrame(brk).dropna(subset=["fwd", "p20", "vol"])
    B["u"] = B["fwd"] - B["coin"].map(drift)
    B["z"] = B["u"]/B["coin"].map(sd)
    B["p20z"] = B["p20"]/(B["vol"]*np.sqrt(20))
    B["distz"] = B["dist"]/B["vol"]
    out["brk_reg"] = pd.DataFrame({"p20z": reg(B, "p20z"), "distz": reg(B, "distz")}).T
    Bu = B[B["p20"] > 0]
    out["brk_up_reg"] = pd.DataFrame({"p20z": reg(Bu, "p20z"), "distz": reg(Bu, "distz")}).T
    out["brk_up_by_coin"] = Bu.groupby("coin")["u"].agg(["size", "mean"])
    out["brk_up_by_year"] = Bu.groupby("yr")["u"].agg(["size", "mean"])
    # compare breaks in uptrend vs non-break grid bars of same uptrend
    Gu = G[G["p20"] > 0]
    out["up_break_vs_up_grid"] = pd.Series({"brk_up_mean": Bu["u"].mean(), "grid_up_mean": Gu["u"].mean(),
        "welch_t": stats.ttest_ind(Bu["u"], Gu["u"], equal_var=False).statistic, "n_b": len(Bu), "n_g": len(Gu)})
    B20 = B.dropna(subset=["fwd20"])
    d20 = G.groupby("coin")["fwd"].mean()*2
    B20u = B20[B20["p20"] > 0]
    x = B20u["fwd20"] - B20u["coin"].map(d20)
    out["brk_up_20d"] = pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x)))})
    # book: daily returns by window sign pattern
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): T.append(t.assign(coin=coin))
    if T:
        T = pd.concat(T)
        out["trades"] = T.groupby("side")["net_profit_loss_percent"].agg(["size", "mean", "median"])
    return out
