def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; d1=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sma=c.rolling(20).mean(); sd=r.rolling(20).std()
            z=(c-sma)/sma/sd
            ret5=c.shift(-5)/c-1
            ret1n=c.shift(-1)/c-1
            ret3=c.shift(-3)/c-1
            r5p=c/c.shift(5)-1
            ts=pd.to_datetime(b["timestamp"])
            chop=(b["regime"]=="unknown")
            for i in range(0,len(b),5):
                rows.append(dict(coin=coin,w=w,z=z[i],r5=ret5[i],chop=chop[i],sd=sd[i],r5p=r5p[i]/(sd[i]*np.sqrt(5)) if sd[i]>0 else np.nan,
                                 wd=ts[i].dayofweek,yr=ts[i].year,f=b["forecast"][i]))
            for i in range(len(b)):
                d1.append(dict(coin=coin,w=w,r=r[i],rn=ret1n[i],sd=sd[i],chop=chop[i],wd=ts[i].dayofweek,z=z[i]))
    g=pd.DataFrame(rows); D=pd.DataFrame(d1)
    g=g.dropna(subset=["r5"])
    drift=g.groupby("coin")["r5"].mean(); g["ex"]=g["r5"]-g["coin"].map(drift)
    g["usd"]=g["coin"].map(g.groupby("coin")["r5"].std()); g["st"]=g["ex"]/g["usd"]
    def summ(x,col="st"):
        x=x[col].dropna(); 
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    gz=g.dropna(subset=["z"]).copy()
    gz["zb"]=pd.cut(gz["z"],[-99,-1.5,-0.75,-0.25,0.25,0.75,1.5,99])
    out={}
    out["z_bins_chop"]=gz[gz.chop].groupby("zb").apply(summ)
    out["z_bins_nonchop"]=gz[~gz.chop].groupby("zb").apply(summ)
    out["corr_z_ex"]=pd.DataFrame({k:[stats.spearmanr(v["z"],v["st"])[0],len(v)] for k,v in [("chop",gz[gz.chop]),("nonchop",gz[~gz.chop])]},index=["rho","n"])
    gp=g.dropna(subset=["r5p"]).copy(); gp["pb"]=pd.qcut(gp["r5p"],5,labels=False)
    out["past5_scaled_quint_chop"]=gp[gp.chop].groupby("pb").apply(summ)
    out["past5_scaled_quint_nonchop"]=gp[~gp.chop].groupby("pb").apply(summ)
    gs=g.dropna(subset=["sd"]).copy(); gs["vrel"]=gs["sd"]/gs["coin"].map(gs.groupby("coin")["sd"].median())
    gs["vb"]=pd.qcut(gs["vrel"],4,labels=False)
    out["vol_quart_fwd5"]=gs.groupby("vb").apply(summ)
    out["year_chop_z<0"]=gz[gz.chop&(gz.z<0)].groupby("yr").apply(summ)
    D=D.dropna(subset=["rn","r","sd"]).copy(); D["rs"]=D["r"]/D["sd"]
    D["rb"]=pd.cut(D["rs"],[-99,-2.5,-1.5,-0.5,0.5,1.5,2.5,99])
    D["rnn"]=D["rn"]/D["sd"]
    out["next_day_after_scaled_move_chop"]=D[D.chop].groupby("rb").apply(lambda x:summ(x,"rnn"))
    out["next_day_after_scaled_move_nonchop"]=D[~D.chop].groupby("rb").apply(lambda x:summ(x,"rnn"))
    out["weekday_next"]=D.groupby("wd").apply(lambda x:summ(x,"rnn"))
    # book
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=coin; t["w"]=w; dd.append(t)
    dd=pd.concat(dd); dd=dd.dropna(subset=["book_return"])
    bk=dd.groupby(["w","day"]).agg(b=("book_return","mean"),c=("coin_return","mean")).reset_index()
    q=bk["b"].quantile([0.02,0.98])
    out["book_extremes"]=pd.DataFrame({"worst2%":bk[bk.b<=q.iloc[0]][["b","c"]].mean(),"best2%":bk[bk.b>=q.iloc[1]][["b","c"]].mean(),"all":bk[["b","c"]].mean()})
    out["book_by_window"]=bk.groupby("w")["b"].agg(["mean","std","count"])
    return out
