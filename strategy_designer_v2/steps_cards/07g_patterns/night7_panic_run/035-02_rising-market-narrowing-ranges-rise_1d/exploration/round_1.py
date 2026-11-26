def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; h=b["high"]; l=b["low"]; o=b["open"]
            r1=c/c.shift(1)-1
            rng=(h-l)/c
            f=pd.DataFrame({
                "coin":coin,"win":w,
                "fwd3":c.shift(-3)/c-1,
                "ret1":r1,"ret3":c/c.shift(3)-1,"ret7":c/c.shift(7)-1,"ret14":c/c.shift(14)-1,
                "rr":rng.rolling(14).mean()/rng.shift(14).rolling(28).mean(),
                "rng1":rng/rng.shift(1).rolling(14).mean(),
                "clv":(c-l)/(h-l).replace(0,np.nan),
                "vol14":r1.rolling(14).std(),
                "fc":b["forecast"],
                "rising":(b["regime"]=="unknown").astype(int),
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "year":pd.to_datetime(b["timestamp"]).dt.year,
                "alloc":b["postRebalance_current_allocation"],
            })
            f=f.iloc[::3]
            rows.append(f)
    d=pd.concat(rows,ignore_index=True)
    d=d.dropna(subset=["fwd3"])
    d["ex"]=d["fwd3"]-d.groupby("coin")["fwd3"].transform("mean")
    d["vol14r"]=d.groupby("coin")["vol14"].rank(pct=True)
    out={}
    def q(col,sub,name,n=5):
        s=sub.dropna(subset=[col]).copy()
        s["q"]=pd.qcut(s[col].rank(method="first"),n,labels=False)
        g=s.groupby("q")["ex"].agg(["count","mean","std"])
        g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
        top=s[s.q==n-1]["ex"];bot=s[s.q==0]["ex"]
        g.loc["top-bot","mean"]=top.mean()-bot.mean()
        g.loc["top-bot","t"]=stats.ttest_ind(top,bot,equal_var=False).statistic
        out[name]=g.round(4)
    for col in ["ret1","ret3","ret7","ret14","rr","rng1","clv","vol14r"]:
        q(col,d,col+"_all")
    for col in ["ret3","ret7","rr","vol14r"]:
        q(col,d[d.rising==1],col+"_rising")
        q(col,d[d.rising==0],col+"_notrising")
    q("fc",d[d.rising==1],"fc_rising")
    g=d.groupby(["rising"])["ex"].agg(["count","mean","std"]);g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["by_rising"]=g.round(4)
    g=d.groupby(["win"])["ex"].agg(["count","mean"]);out["by_win"]=g.round(4)
    g=d.groupby(["coin","rising"])["ex"].agg(["count","mean"]);out["coin_rising"]=g.round(4)
    # book daily
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            x=x.copy();x["coin"]=coin;x["win"]=w;dd.append(x)
    D=pd.concat(dd)
    D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    g=D.groupby("wd")[["book_return","coin_return"]].agg(["mean","count"]);out["days_wd"]=g.round(5)
    return out
