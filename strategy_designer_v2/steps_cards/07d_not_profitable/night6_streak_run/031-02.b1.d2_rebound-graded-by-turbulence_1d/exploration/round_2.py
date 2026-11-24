def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]
            b["r1"]=c.pct_change()
            sd60=b["r1"].rolling(60,min_periods=30).std()
            b["vr"]=b["r1"].rolling(10).std()/sd60
            b["fallz"]=np.maximum(0,-b["r1"])/sd60
            for h in [2,4,6]:
                b["fwd%d"%h]=c.shift(-h)/c-1
            b["coin"]=coin;b["w"]=w;b["pos"]=np.arange(len(b))
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            v=b["postRebalance_total_value"]
            b["bret"]=v/v.shift(1)-1
            b["alloc"]=b["postRebalance_current_allocation"]
            b["prev_vr"]=b["vr"].shift(1)
            b["prev_fc"]=b["forecast"].shift(1)
            b["prev_alloc"]=b["alloc"].shift(1)
            rows.append(b)
    B=pd.concat(rows,ignore_index=True)
    out={}
    def summ(g,col):
        d=g.groupby("day")["ex"].sum()
        return pd.Series({"n":len(g),"days":len(d),"mean_ex":g["ex"].mean(),"mean_tot":g[col].mean(),"t_day":d.mean()/(d.std()/np.sqrt(len(d))) if len(d)>2 else np.nan})
    q=B["vr"].dropna().quantile([1/3,2/3]).values
    B["vrq"]=pd.cut(B["vr"],[-np.inf,q[0],q[1],np.inf],labels=["lo","mid","hi"])
    for h in [2,4,6]:
        G=B[(B.pos%h==0)].dropna(subset=["fwd%d"%h,"vr"]).copy()
        drift=G.groupby("coin")["fwd%d"%h].mean()
        G["ex"]=G["fwd%d"%h]-G["coin"].map(drift)
        G["sig"]=G["forecast"]>0
        out["h%d sig x vr"%h]=G.groupby(["sig","vrq"]).apply(lambda g:summ(g,"fwd%d"%h))
    G=B[(B.pos%2==0)].dropna(subset=["fwd2","vr"]).copy()
    drift=G.groupby("coin")["fwd2"].mean()
    G["ex"]=G["fwd2"]-G["coin"].map(drift)
    S=G[G.forecast>0].copy()
    S["fq"]=pd.qcut(S["fallz"],3,labels=["small","mid","big"])
    out["h2 signal: fall x vr"]=S.groupby(["fq","vrq"])["ex"].agg(["count","mean"]).unstack()
    out["alloc share held with fc==0"]=pd.Series({"share_pos_days_fc0":((B.alloc.abs()>0)&(B.forecast<=0)).sum()/(B.alloc.abs()>0).sum(),"mean_alloc_fc0":B.loc[B.forecast<=0,"alloc"].mean(),"mean_alloc_fcpos":B.loc[B.forecast>0,"alloc"].mean()})
    B["gain"]=B["alloc"]*(B.groupby(["coin","w"])["close"].shift(-1)/B["close"]-1)
    out["gain by fc>0 x vr"]=B.dropna(subset=["vrq"]).groupby([B.forecast>0,"vrq"])["gain"].agg(["count","mean","sum"])
    def chain(df,col):
        d=df.groupby(["w","day"])[col].mean().reset_index()
        d["wn"]=d["w"].str[1:].astype(int); d=d.sort_values(["wn","day"])
        r=d[col].fillna(0).values
        eq=np.cumprod(1+r); dd=eq/np.maximum.accumulate(eq)-1
        return pd.Series({"yr":eq[-1]**(365/len(r))-1,"mdd":dd.min(),"calmar":(eq[-1]**(365/len(r))-1)/-dd.min(),"sharpe":r.mean()/r.std()*np.sqrt(365)})
    out["book"]=chain(B,"bret")
    B["g_novrlo"]=np.where(B["prev_vr"]<q[0],0.0,B["bret"])
    out["book out when prev vr lo"]=chain(B,"g_novrlo")
    B["g_novrhi"]=np.where(B["prev_vr"]>q[1],0.0,B["bret"])
    out["book out when prev vr hi"]=chain(B,"g_novrhi")
    B["g_onlysig"]=np.where(B["prev_fc"]>0,B["bret"],np.where(B.groupby(["coin","w"])["forecast"].shift(2)>0,B["bret"],0.0))
    out["book only 2 days after signal"]=chain(B,"g_onlysig")
    return out
