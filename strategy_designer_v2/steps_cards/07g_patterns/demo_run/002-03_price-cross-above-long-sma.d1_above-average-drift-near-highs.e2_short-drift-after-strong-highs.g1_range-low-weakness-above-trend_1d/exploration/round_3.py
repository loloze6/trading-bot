def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            lo=c.rolling(20).min(); hi=c.rolling(20).max()
            rp=(c-lo)/(hi-lo)
            p20=c/c.shift(20)-1
            vol=c.pct_change().rolling(20).std()
            f5=c.shift(-5)/c-1
            ts=pd.to_datetime(b["timestamp"])
            idx=np.arange(0,len(b),5)
            rows.append(pd.DataFrame({"coin":coin,"w":w,"p20":p20.iloc[idx].values,"rp":rp.iloc[idx].values,
                "f5":f5.iloc[idx].values,"vol":vol.iloc[idx].values,"reg":b["regime"].iloc[idx].values,
                "fc":b["forecast"].iloc[idx].values,"pos":b["postRebalance_current_allocation"].iloc[idx].values,
                "year":ts.dt.year.iloc[idx].values}))
    G=pd.concat(rows).dropna(subset=["f5"])
    G["ex"]=G["f5"]-G.groupby("coin")["f5"].transform("mean")
    G["vn"]=G["p20"]/(G["vol"]*np.sqrt(20))
    out={}
    res=[]
    for reg in ["trending","unknown"]:
        S=G[G.reg==reg].dropna(subset=["vn","rp"])
        for x in ["vn","rp"]:
            r,p=stats.spearmanr(S[x],S["ex"]); res.append(("ALL",reg,x,round(r,3),len(S),round(p,5)))
        for coin,s in S.groupby("coin"):
            r,p=stats.spearmanr(s["vn"],s["ex"]); res.append((coin,reg,"vn",round(r,3),len(s),round(p,4)))
    out["spearman ex5"]=pd.DataFrame(res,columns=["coin","reg","x","rho","n","p"])
    def summ(df,key):
        a=df.groupby(key)["ex"].agg(["mean","count","std"])
        a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"])); return a.drop(columns="std").round(4)
    G["half"]=np.where(G["year"]<=2021,"2018-21","2022-25")
    S=G.dropna(subset=["vn"]).copy()
    S["vq"]=S.groupby(["coin","reg"])["vn"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["vn quintile by reg x half"]=summ(S,["reg","half","vq"])
    A=G[G.reg=="trending"].copy()
    A["fb"]=pd.cut(A["fc"],[-21,-10,-0.001,0.001])
    A["posret"]=A["pos"]*A["f5"]
    out["trend fc bucket"]=pd.DataFrame({"posret":A.groupby("fb")["posret"].mean(),"ex":A.groupby("fb")["ex"].mean(),
        "pos":A.groupby("fb")["pos"].mean(),"n":A.groupby("fb")["ex"].count()}).round(4)
    return out
