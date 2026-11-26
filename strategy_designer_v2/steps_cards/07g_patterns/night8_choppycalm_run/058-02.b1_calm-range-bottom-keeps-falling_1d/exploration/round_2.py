def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float); h = df["high"].astype(float); l = df["low"].astype(float); o=df["open"].astype(float)
            hi = h.rolling(20).max(); lo = l.rolling(20).min()
            pos = 2*(c-lo)/(hi-lo) - 1
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            tr60 = c/c.shift(60)-1
            vol30 = r1.rolling(30).std()
            vrel = vol30/ r1.rolling(90).std()
            ts = pd.to_datetime(df["timestamp"])
            d = pd.DataFrame({"coin":coin,"w":w,"i":np.arange(len(df)),"pos":pos,"r1":r1,
                "z1": r1/vol20.shift(1),"fwd1":c.shift(-1)/c-1,"fwd2":c.shift(-2)/c-1,"fwd5":c.shift(-5)/c-1,
                "tr60":tr60,"vrel":vrel,"inprof":(df["regime"]=="unknown").values,"year":ts.dt.year.values,
                "clv":(c-l)/(h-l),"wd":ts.dt.weekday.values})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    for hz in [1,2,5]:
        dr = A[A.i%hz==0].groupby("coin")[f"fwd{hz}"].mean()
        A[f"ex{hz}"] = A[f"fwd{hz}"]-A.coin.map(dr)
    def summ(g, col):
        x = g[col].dropna()
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    A["trend"] = np.where(A.tr60>0.10,"rising",np.where(A.tr60<-0.10,"falling",np.where(A.tr60.notna(),"choppy","na")))
    A["agit"] = np.where(A.vrel>1,"agit",np.where(A.vrel.notna(),"calm","na"))
    A["zq"] = pd.cut(A.z1,[-99,-2,-1,1,2,99])
    out = {}
    B = A[A.z1< -1.5]
    out["drop z<-1.5 ex1 by trend"] = B.groupby("trend").apply(lambda g: summ(g,"ex1"))
    out["drop z<-1.5 ex1 by inprof"] = B.groupby("inprof").apply(lambda g: summ(g,"ex1"))
    out["drop z<-1.5 ex1 by year"] = B.groupby("year").apply(lambda g: summ(g,"ex1"))
    out["drop z<-1.5 ex1 by coin"] = B.groupby("coin").apply(lambda g: summ(g,"ex1"))
    out["drop z<-1.5 ex2 grid2"] = summ(B[B.i%2==0],"ex2")
    # grade
    out["z bins ex1 by trend"] = A.groupby(["trend","zq"]).apply(lambda g: summ(g,"ex1"))
    G = A[A.i%5==0]
    T = G[G.pos>0.6]
    out["top pos ex5 by trend"] = T.groupby("trend").apply(lambda g: summ(g,"ex5"))
    out["top pos ex5 by agit"] = T.groupby("agit").apply(lambda g: summ(g,"ex5"))
    Bt = G[G.pos<-0.6]
    out["bottom pos ex5 by trend"] = Bt.groupby("trend").apply(lambda g: summ(g,"ex5"))
    # up days: rise followed by fall in falling markets (short side)
    U = A[A.z1>1.5]
    out["rise z>1.5 ex1 by trend"] = U.groupby("trend").apply(lambda g: summ(g,"ex1"))
    out["rise z>1.5 ex5 grid by trend"] = G[G.z1>1.5].groupby("trend").apply(lambda g: summ(g,"ex5"))
    out["weekday ex1 by year (wed)"] = A[A.wd==2].groupby("year").apply(lambda g: summ(g,"ex1"))
    out["trend share"] = A.trend.value_counts(normalize=True)
    return out
