def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r=c.pct_change()
            sd=r.rolling(20).std().shift(1)
            z=r/sd
            vr=v/v.shift(1).rolling(20).median()
            r5=c/c.shift(5)-1
            ts=pd.to_datetime(b["timestamp"])
            n=len(b)
            for H in (1,3):
                fwd=c.shift(-H)/c-1
                idx=np.arange(0,n,H)
                rows.append(pd.DataFrame({"coin":coin,"w":w,"H":H,"fwd":fwd.iloc[idx].values,"z":z.iloc[idx].values,
                  "vr":vr.iloc[idx].values,"r5":r5.iloc[idx].values,"yr":ts.iloc[idx].dt.year.values,
                  "wnum":int(w[1:])}))
    D=pd.concat(rows).dropna(subset=["fwd","vr","z"])
    D["ex"]=D["fwd"]-D.groupby(["coin","H"])["fwd"].transform("mean")
    D["lvr"]=np.log(D["vr"])
    out={}
    def reg(g,x):
        g=g.dropna(subset=[x,"ex"])
        if len(g)<10: return pd.Series({"n":len(g),"slope":np.nan,"t":np.nan})
        s=stats.linregress(g[x],g["ex"])
        return pd.Series({"n":len(g),"slope":s.slope,"t":s.slope/s.stderr})
    out["logvr_reg_all"]=D.groupby("H").apply(lambda g:reg(g,"lvr"))
    out["logvr_reg_coin_H1"]=D[D.H==1].groupby("coin").apply(lambda g:reg(g,"lvr"))
    out["logvr_reg_coin_H3"]=D[D.H==3].groupby("coin").apply(lambda g:reg(g,"lvr"))
    D["half"]=np.where(D.wnum<=12,"w1-12","w13-24")
    out["logvr_reg_half"]=D.groupby(["H","half"]).apply(lambda g:reg(g,"lvr"))
    D["sign"]=np.where(D.z<0,"down","up")
    out["logvr_reg_bysign"]=D.groupby(["H","sign"]).apply(lambda g:reg(g,"lvr"))
    D["vrq"]=pd.qcut(D["vr"],5,labels=False)
    out["vrq_by_sign_H1_mean"]=D[D.H==1].groupby(["vrq","sign"])["ex"].agg(["count","mean"]).unstack()
    out["r5_reg"]=D.groupby(["H","half"]).apply(lambda g:reg(g,"r5"))
    out["r5_reg_coin_H3"]=D[D.H==3].groupby("coin").apply(lambda g:reg(g,"r5"))
    # book around biggest days
    bk=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.reset_index(drop=True)
            bk.append(pd.DataFrame({"br":d["book_return"],"cr":d["coin_return"],"cr_next":d["coin_return"].shift(-1)}))
    B=pd.concat(bk).dropna()
    act=B[B.br!=0]
    out["book_active_days"]=pd.Series({"n_active":len(act),"mean_br":act.br.mean(),"t":act.br.mean()/(act.br.std()/np.sqrt(len(act))),"share_days_active":len(act)/len(B)})
    return out
