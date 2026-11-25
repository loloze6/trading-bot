def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; h=b["high"]; l=b["low"]
            r1=c/c.shift(1)-1
            rng=(h-l)/c
            f=pd.DataFrame({
                "coin":coin,"win":w,"ts":pd.to_datetime(b["timestamp"]),
                "fwd3":c.shift(-3)/c-1,
                "ret3":c/c.shift(3)-1,"ret7":c/c.shift(7)-1,
                "vol14":r1.rolling(14).std(),
                "vol7":r1.rolling(7).std(),
                "rng14":rng.rolling(14).mean(),
                "vol14_60":r1.rolling(14).std()/r1.shift(14).rolling(46).std(),
                "rawrr":b.get("debug_info.components.range_calm.last_history_value"),
                "rising":(b["regime"]=="unknown").astype(int),
            })
            f=f.iloc[::3]
            rows.append(f)
    d=pd.concat(rows,ignore_index=True).dropna(subset=["fwd3"])
    d["ex"]=d["fwd3"]-d.groupby("coin")["fwd3"].transform("mean")
    d["vol14r"]=d.groupby("coin")["vol14"].rank(pct=True)
    d["rng14r"]=d.groupby("coin")["rng14"].rank(pct=True)
    d["day"]=d["ts"].dt.floor("D")
    d["half"]=np.where(d["win"].str[1:].astype(int)<=12,"w7-w12","w13-w18")
    out={}
    def q(col,sub,name,n=5,grp=None):
        s=sub.dropna(subset=[col]).copy()
        s["q"]=pd.qcut(s[col].rank(method="first"),n,labels=False)
        g=s.groupby("q")["ex"].agg(["count","mean","std"])
        g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
        top=s[s.q==n-1]["ex"];bot=s[s.q==0]["ex"]
        g.loc["top-bot","mean"]=top.mean()-bot.mean()
        g.loc["top-bot","t"]=stats.ttest_ind(top,bot,equal_var=False).statistic
        # rank correlation and day-clustered t of slope sign
        s["z"]=(s[col].rank(pct=True)-0.5)
        s["p"]=s["z"]*s["ex"]
        pd_=s.groupby("day")["p"].sum()
        g.loc["daycl","t"]=pd_.mean()/(pd_.std()/np.sqrt(len(pd_)))
        g.loc["daycl","count"]=len(pd_)
        g.loc["spearman","mean"]=stats.spearmanr(s[col],s["ex"]).correlation
        out[name]=g.round(4)
        if grp:
            s["third"]=pd.qcut(s[col].rank(method="first"),3,labels=["lo","mid","hi"])
            gg=s.groupby([grp,"third"],observed=True)["ex"].agg(["count","mean"])
            out[name+"_by_"+grp]=gg.round(4)
    R=d[d.rising==1]; N=d[d.rising==0]
    for col in ["vol14","vol14r","vol7","rng14","rng14r","vol14_60","rawrr"]:
        q(col,R,col+"_rising")
    q("vol14r",R,"vol14r_rising",grp="half")
    q("vol14r",R,"vol14r_rising_c",grp="coin")
    q("ret3",R,"ret3_rising",grp="half")
    q("ret7",d,"ret7_all",grp="half")
    q("vol14",N,"vol14_notrising")
    return out
