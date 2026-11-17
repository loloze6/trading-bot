def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    fr = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            pos = b["postRebalance_current_allocation"].values
            fc = b["forecast"].values
            # distance from 364-bar high recomputed in-window (approx from recorded component)
            dist = b["debug_info.components.closeness.last_history_value"].values
            # 30-day past return and 60-day vol (in window)
            ret1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            for t in range(0, n-30, 30):
                past30 = c[t]/c[t-30]-1 if t>=30 else np.nan
                fr.append(dict(coin=coin, w=w, fc=fc[t], pos=pos[t], dist=dist[t],
                               fwd=c[t+30]/c[t]-1, past30=past30))
            nxt = np.r_[c[1:]/c[:-1]-1, np.nan]
            for t in range(n-1):
                rows.append(dict(coin=coin, w=w, pos=pos[t], fc=fc[t], dist=dist[t], nxt=nxt[t],
                                 gain=pos[t]*nxt[t]))
    F = pd.DataFrame(fr); R = pd.DataFrame(rows)
    for coin in F.coin.unique():
        m = F.coin==coin
        F.loc[m,"ex"] = F.loc[m,"fwd"]-F.loc[m,"fwd"].mean()
    F["fq"] = pd.qcut(F.fc, 5, labels=False, duplicates="drop")
    out["fwd30 by forecast quintile"] = F.groupby("fq").agg(n=("ex","size"), fc=("fc","mean"), pos=("pos","mean"), ex=("ex","mean"), fwd=("fwd","mean"))
    F["dq"] = pd.qcut(F.dist, 5, labels=False, duplicates="drop")
    out["fwd30 by raw distance quintile"] = F.groupby("dq").agg(n=("ex","size"), dist=("dist","mean"), ex=("ex","mean"), pos=("pos","mean"))
    sl = stats.linregress(F.fc.dropna(), F.loc[F.fc.notna(),"ex"])
    out["slope t, n"] = f"{sl.slope:.5f} t={sl.slope/sl.stderr:.2f} n={F.fc.notna().sum()}"
    # book daily
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=coin; dd["w"]=w
            D.append(dd)
    D = pd.concat(D)
    g = D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    out["book vs hold daily"] = pd.DataFrame({"mean":g[["book_return","coin_return"]].mean(),
        "sd":g[["book_return","coin_return"]].std(),
        "sharpe":g[["book_return","coin_return"]].mean()/g[["book_return","coin_return"]].std()*np.sqrt(365)})
    out["by window"] = g.groupby("w").agg(book=("book_return","sum"), hold=("coin_return","sum"), n=("book_return","size"))
    # position stats
    out["position dist"] = R.pos.describe()
    out["share short / long / flat"] = f"short {(R.pos<-0.01).mean():.3f} long {(R.pos>0.01).mean():.3f}"
    R["pq"] = pd.qcut(R.pos.rank(method="first"), 5, labels=False)
    out["daily gain by pos quintile"] = R.groupby("pq").agg(pos=("pos","mean"), nxt=("nxt","mean"), gain=("gain","mean"), n=("gain","size"))
    # by coin
    out["by coin"] = R.groupby("coin").agg(pos=("pos","mean"), gain=("gain","mean"), nxt=("nxt","mean"))
    return out
