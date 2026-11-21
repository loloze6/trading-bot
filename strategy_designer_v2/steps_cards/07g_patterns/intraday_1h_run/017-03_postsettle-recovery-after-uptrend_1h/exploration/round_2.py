def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            d = df[["timestamp","close"]].copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d["hour"] = d["ts"].dt.hour; d["year"]=d["ts"].dt.year
            d["r1"] = d["close"].shift(-1)/d["close"]-1
            d["r24"] = d["close"].shift(-24)/d["close"]-1
            d["past1"] = d["close"]/d["close"].shift(1)-1
            d["past24"] = d["close"]/d["close"].shift(24)-1
            d["rise72"] = d["close"]/d["close"].shift(72)-1
            d["vol720"] = d["past1"].rolling(720).std()
            d["i"]=np.arange(len(d)); d["coin"]=c; d["w"]=w
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["x1"] = A["r1"]-A["coin"].map(A.groupby("coin")["r1"].mean())
    def tt(g): return pd.DataFrame({"bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    out={}
    # 1h reversal: standardized past1 z by vol, slope per coin and per year
    A["z1"] = A["past1"]/A["vol720"]
    res=[]
    for key,grp in list(A.groupby("coin"))+list(A.groupby("year")):
        g=grp.dropna(subset=["z1","x1"])
        x=g["z1"].clip(-6,6); y=g["x1"]
        b=np.cov(x,y)[0,1]/x.var(); e=y-y.mean()-b*(x-x.mean())
        se=np.sqrt((e**2).sum()/(len(g)-2)/((x-x.mean())**2).sum())
        res.append((str(key),b*1e4,b/se,len(g)))
    out["rev1h_slope_bp_per_z"]=pd.DataFrame(res,columns=["grp","bp_per_z","t","n"]).set_index("grp")
    # 1h reversal by vol720 tercile
    A["vt"]=A.groupby("coin")["vol720"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    A["zq"]=pd.cut(A["z1"],[-99,-2,-1,1,2,99],labels=False)
    out["x1_by_voltercile_zbin"]=(A.groupby(["vt","zq"])["x1"].mean()*1e4).unstack()
    # 24h reversal on grid, per coin and year, slope on z24
    G=A[A["i"]%24==0].copy()
    G["x24"]=G["r24"]-G["coin"].map(G.groupby("coin")["r24"].mean())
    G["z24"]=(G["past24"]/(G["vol720"]*np.sqrt(24))).clip(-5,5)
    res=[]
    for key,grp in [("all",G)]+list(G.groupby("coin"))+list(G.groupby("year")):
        g=grp.dropna(subset=["z24","x24"]); x=g["z24"]; y=g["x24"]
        b=np.cov(x,y)[0,1]/x.var(); e=y-y.mean()-b*(x-x.mean())
        se=np.sqrt((e**2).sum()/(len(g)-2)/((x-x.mean())**2).sum())
        res.append((str(key),b*1e4,b/se,len(g)))
    out["rev24h_slope_bp_per_z"]=pd.DataFrame(res,columns=["grp","bp_per_z","t","n"]).set_index("grp")
    # hour 20-21 effect by coin and year
    H=A[A["hour"].isin([20,21])]
    out["h2021_by_coin"]=tt(H.groupby("coin")["x1"]); out["h2021_by_year"]=tt(H.groupby("year")["x1"])
    H=A[A["hour"]==13]
    out["h13_by_coin"]=tt(H.groupby("coin")["x1"])
    # trend-signed at 15-16 by coin
    A["tx1"]=A["x1"]*np.sign(A["rise72"])
    H=A[A["hour"].isin([15,16])]
    out["trend_h1516_by_coin"]=tt(H.groupby("coin")["tx1"]); out["trend_h1516_by_year"]=tt(H.groupby("year")["tx1"])
    return out
