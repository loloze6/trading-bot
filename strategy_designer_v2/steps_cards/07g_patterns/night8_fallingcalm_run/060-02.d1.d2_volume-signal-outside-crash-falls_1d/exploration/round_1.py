def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; v=b["volume"].values
            n=len(b)
            for i in range(0,n-H,H):
                allr.append(c[i+H]/c[i]-1)
        drift=np.mean(allr); sd=np.std(allr)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; v=b["volume"]
            r20=c/c.shift(20)-1; r60=c/c.shift(60)-1
            lvr=np.log(v.rolling(30).mean()/v.shift(30).rolling(30).mean())
            r1=c/c.shift(1)-1
            vol30=r1.rolling(30).std()
            rng=(b["high"]-b["low"])/c
            wd=pd.to_datetime(b["timestamp"]).dt.weekday
            yr=pd.to_datetime(b["timestamp"]).dt.year
            for i in range(0,len(b)-H,H):
                fr=c[i+H]/c[i]-1
                rows.append(dict(coin=coin,w=w,yr=yr[i],wd=wd[i],regime=b["regime"][i],
                    fc=b["forecast"][i],alloc=b["postRebalance_current_allocation"][i],
                    r1=r1[i],r20=r20[i],r60=r60[i],lvr=lvr[i],vol30=vol30[i],rng=rng[i],
                    ex=fr-drift,fr=fr,z=(fr-drift)/sd,
                    rlvr=b.get("debug_info.components.vol_growth.last_history_value",pd.Series([np.nan]*len(b)))[i]))
    d=pd.DataFrame(rows)
    out={}
    def grp(df,col,q=5):
        df=df.dropna(subset=[col,"ex"]).copy()
        df["b"]=pd.qcut(df[col],q,duplicates="drop")
        g=df.groupby("b")["ex"].agg(["count","mean","std"])
        g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
        return g.reset_index().astype({"b":str})
    act=d[d.fc!=0]
    out["active_fc_quintiles"]=grp(act,"fc")
    out["active_rawlvr_quintiles"]=grp(act,"rlvr")
    out["active_r20_quintiles"]=grp(act,"r20")
    # signed excess by r20 bucket
    a=act.copy(); a["sx"]=np.sign(a.fc)*a.ex
    a["r20b"]=pd.cut(a.r20,[-0.21,-0.15,-0.1,-0.05,0])
    g=a.groupby("r20b")["sx"].agg(["count","mean","std"]);g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["signed_by_r20"]=g.reset_index().astype({"r20b":str})
    a["s"]=np.sign(a.fc)
    g=a.groupby("s")["ex"].agg(["count","mean","std"]);g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["long_vs_short_excess"]=g.reset_index()
    # volume ratio in other situations (recomputed)
    nf=d[(d.r60>=-0.10)]
    out["lvr_q_r60_ge_-10"]=grp(nf,"lvr")
    rs=d[(d.r60>0.10)]
    out["lvr_q_rising"]=grp(rs,"lvr")
    cr=d[(d.r60<-0.10)&(d.r20<-0.20)]
    out["lvr_q_falling_crash20"]=grp(cr,"lvr",3)
    # big moves
    out["r1_quintiles_all"]=grp(d,"r1")
    out["r20_quintiles_all"]=grp(d,"r20")
    out["rng_quintiles_all"]=grp(d,"rng")
    out["vol30_quintiles_all"]=grp(d,"vol30")
    g=d.groupby("wd")["ex"].agg(["count","mean","std"]);g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["weekday"]=g.reset_index()
    g=d.groupby("yr")["ex"].agg(["count","mean"]);out["year"]=g.reset_index()
    # book daily
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy();x["coin"]=coin;x["w"]=w;dd.append(x)
    dd=pd.concat(dd)
    bk=dd.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    g=bk.groupby(level=0)["book_return"].agg(["count","mean","std"]);out["book_by_window"]=g.reset_index()
    q=bk["book_return"]
    lo=bk[q<=q.quantile(0.02)];hi=bk[q>=q.quantile(0.98)]
    out["book_extremes"]=pd.DataFrame({"n":[len(lo),len(hi)],"book":[lo.book_return.mean(),hi.book_return.mean()],"coin":[lo.coin_return.mean(),hi.coin_return.mean()]},index=["worst2%","best2%"])
    return out
