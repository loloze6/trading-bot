def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    # 1. per-window: which coins drive the fall; contribution of each coin to book in worst windows
    dd = []
    for c in days:
        for w, d in days[c].items():
            dd.append(d.assign(coin=c, win=w))
    D = pd.concat(dd)
    ncoin = D.groupby(["win","day"])["coin"].transform("count")
    D["contrib"] = D["book_return"]/ncoin
    out["coin contribution in w14,w7,w9,w12 (sum of daily contrib)"] = D[D.win.isin(["w14","w7","w9","w12"])].pivot_table(index="coin", columns="win", values="contrib", aggfunc="sum")
    # 2. per trade features: entry scaled rise raw, entry allocation, realised vol, regime at exit, prior 30d return, prior 7d
    rows = []
    for c in trades:
        for w, t in trades[c].items():
            if not len(t): continue
            b = bars[c][w].reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"]; r1 = cl.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            sr = cl.pct_change(7)/(vol30*np.sqrt(7))
            r30 = cl.pct_change(30); r3 = cl.pct_change(3)
            # in-profile run length before entry
            for _, tr in t.iterrows():
                et = pd.to_datetime(tr["entry_time"]); xt = pd.to_datetime(tr["exit_time"])
                ie = ts.searchsorted(et, side="right")-1; ix = ts.searchsorted(xt, side="right")-1
                if ie < 0: continue
                ix = min(max(ix,ie),len(b)-1)
                alloc = b["postRebalance_current_allocation"].iloc[ie]
                rows.append(dict(coin=c, win=w, net=tr["net_profit_loss_percent"], fc=tr["entry_forecast"],
                    sr=sr.iloc[ie], r30=r30.iloc[ie], r3=r3.iloc[ie], vol=vol30.iloc[ie], alloc=alloc,
                    exit_reg=b["regime"].iloc[ix], exit_fc=b["forecast"].iloc[ix],
                    dur=tr["duration_minutes"]/1440,
                    pnl_book=tr["net_profit_loss_percent"]*abs(alloc)))
    T = pd.DataFrame(rows)
    def s(d):
        return pd.Series(dict(n=len(d), mean_net=d.net.mean(), med=d.net.median(), hit=(d.net>0).mean(),
                              book_pnl=d.pnl_book.sum(), alloc=d.alloc.abs().mean()))
    out["trades by exit regime"] = T.groupby("exit_reg").apply(s)
    out["trades by exit forecast zero"] = T.groupby(T.exit_fc<=0).apply(s)
    out["trades by raw sr"] = T.groupby(pd.cut(T.sr,[-np.inf,0,0.5,1,1.5,2,np.inf])).apply(s)
    out["trades by prior 3d return"] = T.groupby(pd.cut(T.r3,[-np.inf,0,0.03,0.07,0.15,np.inf])).apply(s)
    out["trades by alloc"] = T.groupby(pd.cut(T.alloc.abs(),[0,0.5,1,1.5,2.1])).apply(s)
    out["worst 15 trades (aggregated)"] = T.nsmallest(15,"pnl_book")[["net","fc","sr","r3","r30","alloc","dur","exit_reg"]].describe().loc[["mean","min","max"]]
    out["trades by win"] = T.groupby("win").apply(s)
    # 3. forward returns in profile by raw sr, horizons 14 and 28, grid-based; and same out of profile
    g = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True); cl = b["close"].values; n=len(b)
            r1 = pd.Series(cl).pct_change(); vol30 = r1.rolling(30,min_periods=20).std()
            sr = pd.Series(cl).pct_change(7)/(vol30*np.sqrt(7))
            for H in (7,14,28):
                for i in range(0,n-H,H):
                    g.append(dict(coin=c,H=H,fwd=cl[i+H]/cl[i]-1,sr=sr.iloc[i],inp=b["regime"].iloc[i]=="unknown",fc=b["forecast"].iloc[i]))
    g = pd.DataFrame(g)
    g["ex"] = g.fwd - g.groupby(["coin","H"]).fwd.transform("mean")
    g["srq"] = pd.cut(g.sr,[-np.inf,0,0.5,1,np.inf])
    def s2(d): return pd.Series(dict(n=len(d), mean_ex=d.ex.mean(), t=d.ex.mean()/(d.ex.std()/np.sqrt(len(d))) if len(d)>2 else np.nan))
    out["ex by H, profile, raw sr"] = g.groupby(["H","inp","srq"]).apply(s2)
    out["ex by H, profile, fc>=15"] = g[g.inp].groupby(["H", g.fc>=15]).apply(s2)
    return out
