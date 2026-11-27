def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            r1=c.pct_change()
            rng=(h-l).replace(0,np.nan)
            loc=(c-l)/rng
            vol20=r1.rolling(20).std()
            r5s=(c/c.shift(5)-1)/(vol20*np.sqrt(5))
            r1s=r1/vol20
            r20=c/c.shift(20)-1
            vrank=vol20.rolling(60,min_periods=30).rank(pct=True)
            fwd3=c.shift(-3)/c-1
            fwd1=c.shift(-1)/c-1
            wd=pd.to_datetime(b["timestamp"]).dt.dayofweek
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"loc":loc,"r5s":r5s,"r1s":r1s,"r20":r20,
                            "vrank":vrank,"fwd3":fwd3,"fwd1":fwd1,"wd":wd,"inpos":b["postRebalance_current_allocation"].abs()>1e-6,
                            "rngrel":(rng/c)/( (rng/c).rolling(20).mean())})
            rows.append(d)
    D=pd.concat(rows)
    G=D[D.pos%3==0].dropna(subset=["fwd3"]).copy()
    drift=G.groupby("coin")["fwd3"].mean()
    G["ex"]=G["fwd3"]-G["coin"].map(drift)
    sd=G.groupby("coin")["fwd3"].std(); G["exs"]=G["ex"]/G["coin"].map(sd)
    def tab(key):
        g=G.dropna(subset=[key]).groupby(key)["exs"]
        return pd.DataFrame({"n":g.size(),"mean_exs":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    for k,q in [("loc",5),("r5s",5),("r1s",5),("r20",5),("vrank",4),("rngrel",4)]:
        G[k+"_q"]=pd.qcut(G[k],q,labels=False,duplicates="drop")
    out={}
    for k in ["loc_q","r5s_q","r1s_q","r20_q","vrank_q","rngrel_q","wd"]:
        out[k]=tab(k)
    g=G.dropna(subset=["loc_q","r5s_q"]).groupby(["r5s_q","loc_q"])["exs"]
    out["r5s_x_loc"]=pd.DataFrame({"n":g.size(),"m":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    g=G.dropna(subset=["r20_q","r5s_q"]).groupby(["r20_q","r5s_q"])["exs"]
    out["r20_x_r5s"]=pd.DataFrame({"n":g.size(),"m":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    out["corr_spearman"]=pd.Series({k:stats.spearmanr(G[k],G["exs"],nan_policy="omit")[0] for k in ["loc","r5s","r1s","r20","vrank","rngrel"]})
    # book
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    DD=pd.concat(dd)
    bk=DD.groupby(["w","day"])["book_return"].mean().dropna()
    out["book_by_window"]=bk.groupby(level=0).agg(["mean","std","count"])
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=coin; tr.append(t)
    T=pd.concat(tr)
    out["trades_by_coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median"])
    T["dur_d"]=T["duration_minutes"]/1440
    out["trades_by_dur"]=T.groupby(pd.cut(T["dur_d"],[0,3,4,6,10,100]))["net_profit_loss_percent"].agg(["count","mean"])
    return out
