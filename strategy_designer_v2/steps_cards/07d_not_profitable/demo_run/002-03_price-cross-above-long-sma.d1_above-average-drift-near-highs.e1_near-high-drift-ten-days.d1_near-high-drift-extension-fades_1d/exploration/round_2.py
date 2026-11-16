def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        allr=[]
        for w,b in wins.items():
            c=b["close"].values; allr.append(c[1:]/c[:-1]-1)
        mu=np.nanmean(np.concatenate(allr))
        allf=[]
        for w,b in wins.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-10,10)
            allf.append(c[idx+10]/c[idx]-1)
        mu10=np.nanmean(np.concatenate(allf))
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values
            r1=np.append(c[1:]/c[:-1]-1,np.nan)
            pos=b["postRebalance_current_allocation"].values
            f10=np.full(len(c),np.nan); f10[:-10]=c[10:]/c[:-10]-1
            s=pd.Series(c)
            hi=s.rolling(20).max(); lo=s.rolling(20).min()
            comp=b.get("debug_info.components")
            d=pd.DataFrame({"coin":coin,"w":w,"pos":pos,"r1":r1,"g":pos*r1,"fc":b["forecast"].values,
                            "reg":b["regime"].values,"f10x":f10-mu10,
                            "grid":np.arange(len(c))%10==0,
                            "rng":((s-lo)/(hi-lo)).values,"ret30":s.pct_change(30).values})
            for k in ["range20","ext30"]:
                for v in ["last_history_value","post_pipeline_value"]:
                    col=f"debug_info.components.{k}.{v}"
                    d[f"{k}_{v[:4]}"]=b[col].values if col in b.columns else np.nan
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    T=D[D.reg=="trending"]
    out["trending_side_share"]=pd.Series({"n":len(T),"short":(T.pos<0).mean(),"long":(T.pos>0).mean(),
        "fc_neg":(T.fc<0).mean(),"range20_post_neg":(T.range20_post<0).mean(),
        "ext30_post_pos":(T.ext30_post>0).mean(),"mean_range20_post":T.range20_post.mean(),
        "mean_ext_post":T.ext30_post.mean(),"cols_present":float(T.range20_post.notna().mean())})
    G=T[T.grid & T.f10x.notna()]
    def tt(x,y):
        m=x.notna()&y.notna()
        r=stats.linregress(x[m],y[m]); return pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":m.sum()})
    out["slopes"]=pd.DataFrame({"raw_range":tt(G.rng,G.f10x),"range20_post":tt(G.range20_post,G.f10x),
        "ext30_post":tt(G.ext30_post,G.f10x),"ret30":tt(G.ret30,G.f10x),"forecast":tt(G.fc,G.f10x)})
    G=G.copy(); G["rp"]=pd.qcut(G.range20_post,5,duplicates="drop")
    out["post_range_f10x"]=G.groupby("rp").agg(n=("f10x","size"),f10x=("f10x","mean"),rawrng=("rng","mean"))
    # daily-ish book variants from bar gains (1d bars)
    def sh(g):
        g=g.dropna(); return pd.Series({"mean":g.mean(),"sharpe":g.mean()/g.std()*np.sqrt(365)})
    D["g_long"]=np.where(D.pos>0,D.g,0.0)
    D["g_hold_trend"]=np.where(D.reg=="trending",D.r1,0.0)
    D["g_rngraw"]=np.where(D.reg=="trending",(D.rng-0.5)*2*D.r1,0.0)
    bk=lambda col: D.groupby(["w",D.groupby(["coin","w"]).cumcount()])[col].mean()
    out["variants"]=pd.DataFrame({k:sh(bk(k)) for k in ["g","g_long","g_hold_trend","g_rngraw"]})
    out["short_by_year"]=D[D.pos<0].assign(y=D.w).groupby("coin").agg(n=("g","size"),g=("g","mean"),r1=("r1","mean"))
    return out
