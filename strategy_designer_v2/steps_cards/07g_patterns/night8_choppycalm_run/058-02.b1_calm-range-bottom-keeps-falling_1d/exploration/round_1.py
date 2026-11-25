def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float); h = df["high"].astype(float); l = df["low"].astype(float)
            hi = h.rolling(20).max(); lo = l.rolling(20).min()
            pos = 2*(c-lo)/(hi-lo) - 1
            r1 = c.pct_change()
            prev5 = c/c.shift(5)-1
            vol20 = r1.rolling(20).std()
            fwd5 = c.shift(-5)/c - 1
            fwd1 = c.shift(-1)/c - 1
            ts = pd.to_datetime(df["timestamp"])
            d = pd.DataFrame({"coin":coin,"w":w,"i":np.arange(len(df)),"pos":pos,"r1":r1,"prev5":prev5,
                              "vol20":vol20,"fwd5":fwd5,"fwd1":fwd1,"inprof":(df["regime"]=="unknown").values,
                              "wd":ts.dt.weekday.values,"year":ts.dt.year.values,
                              "z1": r1/vol20.shift(1), "fc":df["forecast"].values,
                              "alloc":df["postRebalance_current_allocation"].values})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    drift5 = A[A.i%5==0].groupby("coin")["fwd5"].mean()
    drift1 = A.groupby("coin")["fwd1"].mean()
    A["ex5"] = A["fwd5"] - A["coin"].map(drift5)
    A["ex1"] = A["fwd1"] - A["coin"].map(drift1)
    G = A[(A.i%5==0)].dropna(subset=["ex5","pos"])
    def summ(g, col="ex5"):
        x = g[col].dropna()
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    G["posq"] = pd.cut(G["pos"], [-1.01,-0.6,-0.2,0.2,0.6,1.01])
    out = {}
    out["pos bins, in profile"] = G[G.inprof].groupby("posq").apply(summ)
    out["pos bins, out profile"] = G[~G.inprof].groupby("posq").apply(summ)
    out["in-profile share"] = float(A.inprof.mean())
    # large daily move z next day / 5 days, all bars non-overlap for 5d
    G["zq"] = pd.cut(G["z1"], [-99,-2,-1,1,2,99])
    out["z1 bins ex5 all"] = G.groupby("zq").apply(summ)
    A1 = A.dropna(subset=["ex1","z1"]).copy()
    A1["zq"] = pd.cut(A1["z1"], [-99,-2,-1,1,2,99])
    out["z1 bins ex1 all"] = A1.groupby("zq").apply(lambda g: summ(g,"ex1"))
    G["p5q"] = pd.qcut(G["prev5"], 5)
    out["prev5 quintile ex5"] = G.groupby("p5q").apply(summ)
    out["weekday ex1"] = A1.groupby("wd").apply(lambda g: summ(g,"ex1"))
    G["vq"] = G.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["vol tercile ex5"] = G.groupby("vq").apply(summ)
    out["vol tercile x pos<-0.6 ex5"] = G[G.pos<-0.6].groupby("vq").apply(summ)
    out["vol tercile x pos>0.6 ex5"] = G[G.pos>0.6].groupby("vq").apply(summ)
    out["pos<-0.6 by year"] = G[G.pos<-0.6].groupby("year").apply(summ)
    out["pos>0.6 by year"] = G[G.pos>0.6].groupby("year").apply(summ)
    # book
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w,t in ws.items()], ignore_index=True)
    out["trades"] = pd.Series({"n":len(tr),"mean net%":tr["net_profit_loss_percent"].mean(),
                               "win share":(tr["net_profit_loss_percent"]>0).mean()})
    out["trades by coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["count","mean"])
    return out
