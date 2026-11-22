def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r1=c/c.shift(1)-1
            mabs=r1.abs().rolling(720,min_periods=240).mean().shift(1)
            vr=v/v.rolling(720,min_periods=240).mean().shift(1)
            z=r1/mabs
            r24=c/c.shift(24)-1
            vol24=r1.rolling(24).std()
            vol24r=vol24/(r1.rolling(720,min_periods=240).std().shift(1))
            f6=c.shift(-6)/c-1
            f1=c.shift(-1)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"z":z,"vr":vr,"r24":r24,"vol24r":vol24r,"f6":f6,"f1":f1,
                            "hour":ts.dt.hour,"wd":ts.dt.weekday,"pos":np.arange(len(b)),
                            "fc":b["forecast"],"alloc":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    drift6=D[D.pos%6==0].groupby("coin")["f6"].mean()
    G=D[(D.pos%6==0)].dropna(subset=["z","vr","f6"]).copy()
    G["ex"]=G["f6"]-G["coin"].map(drift6)
    G["sgn"]=np.sign(G["z"])
    G["exs"]=G["ex"]*G["sgn"]
    G["zb"]=pd.cut(G["z"].abs(),[0,1,2,3,5,100])
    G["vb"]=pd.cut(G["vr"],[0,0.5,1.5,3,100])
    def agg(g,col):
        x=g[col]; n=len(x)
        return pd.Series({"n":n,"mean_bp":x.mean()*1e4,"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    out["cont6_by_absz_volbucket"]=G.groupby(["vb","zb"],observed=True).apply(lambda g:agg(g,"exs")).round(2)
    out["cont6_by_absz_dir"]=G.groupby([G["sgn"],"zb"],observed=True).apply(lambda g:agg(g,"exs")).round(2)
    # 24h momentum
    G["mb"]=pd.qcut(G["r24"]/ (G["vol24r"].clip(lower=0.1)),5,labels=False,duplicates="drop") if False else pd.qcut(G["r24"],5,labels=False)
    out["f6ex_by_r24_quintile"]=G.groupby(["coin","mb"]).apply(lambda g:agg(g,"ex")).round(2)
    G["vlb"]=pd.qcut(G["vol24r"],4,labels=False)
    out["f6ex_by_vol24ratio_q_signed_cont"]=G.groupby("vlb").apply(lambda g:agg(g,"exs")).round(2)
    H=D.dropna(subset=["f1"]).copy()
    H["ex1"]=H["f1"]-H["coin"].map(D.groupby("coin")["f1"].mean())
    out["f1ex_by_hour"]=H.groupby("hour").apply(lambda g:agg(g,"ex1")).round(2)
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["wd"]=pd.to_datetime(x["day"]).dt.weekday; dd.append(x)
    DD=pd.concat(dd).dropna(subset=["book_return","coin_return"])
    out["day_by_weekday"]=DD.groupby("wd").agg(n=("coin_return","size"),coin_bp=("coin_return",lambda s:s.mean()*1e4),book_bp=("book_return",lambda s:s.mean()*1e4)).round(2)
    out["corr_book_coin_daily"]=float(DD["book_return"].corr(DD["coin_return"]))
    T=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items(): T.append(t)
    T=pd.concat(T)
    out["trades"]=pd.Series({"n":len(T),"gross_mean_pct":T["profit_loss_percent"].mean(),"net_mean_pct":T["net_profit_loss_percent"].mean(),"mean_dur_h":T["duration_minutes"].mean()/60,"share_short":(T["side"]=="SHORT").mean()}).round(4)
    out["short_alloc_mean_when_active"]=float(D.loc[D.alloc<0,"alloc"].mean())
    return out
