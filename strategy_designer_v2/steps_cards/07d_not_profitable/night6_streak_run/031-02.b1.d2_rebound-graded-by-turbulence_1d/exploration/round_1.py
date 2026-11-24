def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]
            b["r1"]=c.pct_change()
            b["ret20"]=c/c.shift(20)-1
            b["ret5"]=c/c.shift(5)-1
            b["ma50"]=c/c.rolling(50,min_periods=30).mean()-1
            b["vr"]=b["r1"].rolling(10).std()/b["r1"].rolling(40,min_periods=30).std()
            b["fwd2"]=c.shift(-2)/c-1
            b["gain"]=b["postRebalance_current_allocation"]*(c.shift(-1)/c-1)
            b["coin"]=coin;b["w"]=w;b["pos"]=np.arange(len(b))
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            v=b["postRebalance_total_value"]
            b["bret"]=v/v.shift(1)-1
            rows.append(b)
    B=pd.concat(rows,ignore_index=True)
    out={}
    G=B[(B.pos%2==0)].dropna(subset=["fwd2"]).copy()
    drift=G.groupby("coin")["fwd2"].mean()
    G["ex"]=G["fwd2"]-G["coin"].map(drift)
    G["sig"]=G["forecast"]>0
    def summ(g):
        d=g.groupby("day")["ex"].sum()
        return pd.Series({"n":len(g),"days":len(d),"mean_ex":g["ex"].mean(),"mean_tot":g["fwd2"].mean(),"t_day":d.mean()/(d.std()/np.sqrt(len(d))) if len(d)>2 else np.nan})
    for cond in ["ret20","ret5","ma50"]:
        G2=G.dropna(subset=[cond]).copy()
        G2["st"]=np.where(G2[cond]>0,"up","down")
        out["grid by sig x "+cond]=G2.groupby(["sig","st"]).apply(summ)
    G3=G.dropna(subset=["vr"]).copy()
    G3["vrq"]=pd.qcut(G3["vr"],3,labels=["lo","mid","hi"])
    out["grid by sig x vr"]=G3.groupby(["sig","vrq"]).apply(summ)
    def chain(df,col):
        d=df.groupby(["w","day"])[col].mean().reset_index()
        d["wn"]=d["w"].str[1:].astype(int); d=d.sort_values(["wn","day"])
        r=d[col].fillna(0).values
        eq=np.cumprod(1+r); dd=eq/np.maximum.accumulate(eq)-1
        yr=eq[-1]**(365/len(r))-1
        return d.assign(eq=eq,dd=dd),yr,dd.min(),r.mean()/r.std()*np.sqrt(365)
    d,yr,mdd,sh=chain(B,"bret")
    out["book"]=pd.Series({"yr":yr,"mdd":mdd,"calmar":yr/-mdd,"sharpe":sh})
    i=d["dd"].values.argmin(); eq=d["eq"].values; pk=np.argmax(eq[:i+1])
    seg=d.iloc[pk:i+1]
    out["deepest fall"]=pd.Series({"days":len(seg),"depth":d["dd"].iloc[i],"windows":",".join(seg["w"].unique())})
    keys=set(zip(seg["w"],seg["day"]))
    Bs=B[[(a,b_) in keys for a,b_ in zip(B["w"],B["day"])]]
    out["in deepest fall"]=pd.Series({"mean_alloc":Bs["postRebalance_current_allocation"].mean(),"coin_r1":Bs["r1"].mean(),"share_ret20_neg":(Bs["ret20"]<0).mean(),"share_ma50_neg":(Bs["ma50"]<0).mean(),"share_fc_pos":(Bs["forecast"]>0).mean(),"gain_sum":Bs["gain"].sum()})
    out["dd by year"]=d.groupby(d["day"].dt.year)["dd"].min()
    for cond in ["ret20","ma50","ret5"]:
        B["prev"]=B.groupby(["coin","w"])[cond].shift(1)
        B["g"]=np.where(B["prev"]<0,0.0,B["bret"])
        _,y2,m2,s2=chain(B,"g")
        B["g2"]=np.where(B["prev"]>0,0.0,B["bret"])
        _,y3,m3,s3=chain(B,"g2")
        out["gate "+cond]=pd.Series({"yr_outdown":y2,"mdd_outdown":m2,"cal_outdown":y2/-m2,"sh_outdown":s2,"yr_outup":y3,"mdd_outup":m3,"cal_outup":y3/-m3,"sh_outup":s3})
    return out
