import numpy as np, pandas as pd

def tstat(x):
    x=pd.Series(x).dropna()
    return pd.Series({"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan,"n":len(x)})

def explore(data):
    rows=[]; trades=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"]
            r=cl.pct_change().shift(-1)
            a=b["postRebalance_current_allocation"].fillna(0)
            held=a.abs()>1e-9
            # run length of held
            grp=(held!=held.shift()).cumsum()
            age=held.groupby(grp).cumcount()+1
            r20=cl.pct_change(20); r60=cl.pct_change(60)
            vol=cl.pct_change().rolling(20).std()
            f5=cl.shift(-5)/cl-1
            idx=np.arange(len(b))
            yr=pd.to_datetime(b["timestamp"]).dt.year
            ext=cl/cl.rolling(20).max()
            rows.append(pd.DataFrame({"coin":c,"w":w,"yr":yr,"r":r,"held":held,"age":age.where(held),
                "fc":b["forecast"],"r20":r20,"r60":r60,"vol":vol,"f5":f5,"i":idx,"ext":ext}))
        for w,t in data["trades"][c].items():
            t=t.copy(); t["coin"]=c; t["w"]=w; trades.append(t)
    D=pd.concat(rows,ignore_index=True)
    D["cm"]=D.groupby("coin")["r"].transform("mean")
    D["ex"]=D["r"]-D["cm"]
    D["cm5"]=D.groupby("coin")["f5"].transform("mean")
    D["ex5"]=D["f5"]-D["cm5"]
    H=D[D.held & D.r.notna()].copy()
    out={}
    H["ageb"]=pd.cut(H["age"],[0,3,10,20,40,1000])
    out["held_ex_by_age"]=H.groupby("ageb")["ex"].apply(tstat).unstack().round(4)
    H["fcq"]=H.groupby("coin")["fc"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["held_ex_by_fc_tercile"]=H.groupby("fcq")["ex"].apply(tstat).unstack().round(4)
    D["volq"]=D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    H["volq"]=D.loc[H.index,"volq"]
    out["held_ex_by_vol"]=H.groupby("volq")["ex"].apply(tstat).unstack().round(4)
    H["extb"]=pd.cut(H["ext"],[0,0.85,0.95,0.99,1.01])
    out["held_ex_by_dist_from_20hi"]=H.groupby("extb")["ex"].apply(tstat).unstack().round(4)
    out["held_ex_by_coin"]=H.groupby("coin")["ex"].apply(tstat).unstack().round(4)
    out["held_ex_by_year"]=H.groupby("yr")["ex"].apply(tstat).unstack().round(4)
    # non-overlapping 5-bar
    N=D[(D.i%5==0)&D.held&D.f5.notna()]
    out["held_ex5_nonoverlap"]=tstat(N["ex5"]).round(4)
    F=D[(D.i%5==0)&(~D.held)&D.f5.notna()]
    out["flat_ex5_nonoverlap"]=tstat(F["ex5"]).round(4)
    # flat but r20>0 and r60<=0 etc
    T=pd.concat(trades)
    p=T["net_profit_loss_percent"]
    out["trades_minus_top"]=pd.Series({"sum_all":p.sum(),"minus_top10":p.sort_values().iloc[:-10].sum(),
        "minus_top25":p.sort_values().iloc[:-25].sum(),"minus_top50":p.sort_values().iloc[:-50].sum()}).round(1)
    top=T.sort_values("net_profit_loss_percent",ascending=False).head(25)
    out["top25_by_coin"]=top.groupby("coin")["net_profit_loss_percent"].agg(["count","sum"]).round(1)
    T["durb"]=pd.cut(T["duration_minutes"]/1440,[0,2,5,10,20,40,1000])
    out["trades_by_duration"]=T.groupby("durb")["net_profit_loss_percent"].agg(["count","sum","mean","median"]).round(2)
    return out
