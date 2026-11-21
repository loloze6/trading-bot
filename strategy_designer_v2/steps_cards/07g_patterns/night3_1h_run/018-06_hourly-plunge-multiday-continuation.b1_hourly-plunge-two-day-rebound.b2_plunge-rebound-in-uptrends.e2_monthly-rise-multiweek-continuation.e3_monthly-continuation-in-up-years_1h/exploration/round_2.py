def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []; big = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            c = b["close"].astype(float).values; n = len(c)
            if n < 1000: continue
            ts = pd.to_datetime(b["timestamp"]); reg = b["regime"].values
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            vol = pd.Series(r1).rolling(168, min_periods=100).std().values
            z = r1/np.r_[np.nan, vol[:-1]]
            for i in range(0, n-168, 168):
                rows.append({"coin":coin,"w":w,"yr":ts.iloc[i].year,"reg":reg[i],"f168":c[i+168]/c[i]-1,
                    "dd": c[i]/np.max(c[max(0,i-720):i+1])-1 if i>=720 else np.nan,
                    "dd14": c[i]/np.max(c[max(0,i-336):i+1])-1 if i>=336 else np.nan,
                    "r30": c[i]/c[i-720]-1 if i>=720 else np.nan})
            last=-200
            for i in np.where(z>3)[0]:
                if i-last<168 or i+168>=n: continue
                last=i
                big.append({"coin":coin,"z":z[i],"reg":reg[i],"yr":ts.iloc[i].year,"f168":c[i+168]/c[i]-1})
    g = pd.DataFrame(rows)
    dr = g.groupby("coin")["f168"].mean()
    g["un"] = g["f168"]-g["coin"].map(dr)
    def summ(df,key):
        a=df.groupby(key,observed=True)["un"].agg(["mean","std","count"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"])); return a.round(4)
    out={}
    gt = g[g.reg=="trending"].dropna(subset=["dd"]).copy()
    gt["q"]=gt.groupby("coin")["dd"].transform(lambda x: pd.qcut(x,5,labels=False,duplicates="drop"))
    out["trend top dd quintile by coin"]=summ(gt[gt.q==4],"coin")
    out["trend top dd quintile by year"]=summ(gt[gt.q==4],"yr")
    gt["d10"]=gt.groupby("coin")["dd"].transform(lambda x: pd.qcut(x.rank(method="first"),10,labels=False))
    out["trend dd decile"]=summ(gt,"d10")
    ga = g.dropna(subset=["dd"]).copy()
    ga["d10"]=ga.groupby("coin")["dd"].transform(lambda x: pd.qcut(x.rank(method="first"),10,labels=False))
    out["all dd decile"]=summ(ga,"d10")
    g14 = g[g.reg=="trending"].dropna(subset=["dd14"]).copy()
    g14["q"]=g14.groupby("coin")["dd14"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    out["trend 14d dd quintile"]=summ(g14,"q")
    # nearness within top quintile controlling r30
    gt2=gt.dropna(subset=["r30"]).copy()
    gt2["q30"]=gt2.groupby("coin")["r30"].transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    gt2["near"]=(gt2.q>=3)
    out["trend near x r30 tercile"]=summ(gt2,["q30","near"])
    B=pd.DataFrame(big); B["un"]=B["f168"]-B["coin"].map(dr)
    B["zq"]=pd.qcut(B["z"].rank(method="first"),4,labels=False)
    out["after z>3 up hour by z quartile"]=summ(B,"zq")
    out["after z>3 up hour by regime"]=summ(B,"reg")
    out["after z>3 up hour by year"]=summ(B,"yr")
    return out
