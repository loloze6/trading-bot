def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; blocks=[]
    for coin,ws in data["bars"].items():
        # pooled mean daily return over all windows
        rs=[]
        for w,df in ws.items():
            c=df["close"].astype(float).values
            rs.append(np.diff(c)/c[:-1])
        mu=np.nanmean(np.concatenate(rs))
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float).values
            n=len(c)
            fwd=np.full(n,np.nan)
            if n>20: fwd[:-20]=c[20:]/c[:-20]-1
            ex=fwd-20*mu
            a=df["postRebalance_current_allocation"].astype(float).values
            f=df["forecast"].astype(float).values
            raw=df["debug_info.components.above_ma.last_history_value"].astype(float).values
            # trailing 60-bar coin return as regime
            tr=np.full(n,np.nan)
            if n>60: tr[60:]=c[60:]/c[:-60]-1
            for i in range(n):
                rows.append((coin,w,i,f[i],a[i],raw[i],fwd[i],ex[i],tr[i]))
            v=~np.isnan(ex)
            for b in range(0,n,20):
                sl=slice(b,b+20); m=v[sl]
                if m.sum()==0: continue
                aa=a[sl][m]; ee=ex[sl][m]
                blocks.append((coin,w,(aa*ee).sum(),(aa!=0).any(),np.nanmean(f[sl]),np.nanmean(ee)))
    d=pd.DataFrame(rows,columns=["coin","w","i","f","a","raw","fwd","ex","tr"])
    B=pd.DataFrame(blocks,columns=["coin","w","pnl","act","fmean","exmean"])
    Ba=B[B.act]
    def tstat(x): x=np.asarray(x); return x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x)>2 else np.nan
    out={}
    out["blocks_by_coin"]=Ba.groupby("coin")["pnl"].agg(["count","mean","std",tstat])
    out["blocks_by_window"]=Ba.groupby("w")["pnl"].agg(["count","mean",tstat])
    dv=d.dropna(subset=["ex"])
    act=dv[dv.f>0].copy()
    act["fq"]=pd.qcut(act.f,5,labels=False,duplicates="drop")
    out["by_fq"]=act.groupby("fq").agg(n=("ex","size"),f=("f","mean"),raw=("raw","mean"),ex=("ex","mean"),hit=("ex",lambda x:(x>0).mean()),fwd=("fwd","mean"))
    dv=dv.copy(); dv["on"]=dv.f>0
    out["on_vs_off"]=dv.groupby(["coin","on"])["ex"].agg(["size","mean","median",lambda x:(x>0).mean()])
    act["trq"]=pd.qcut(act.tr,4,labels=False,duplicates="drop")
    out["by_trailing60"]=act.groupby("trq").agg(n=("ex","size"),tr=("tr","mean"),ex=("ex","mean"),hit=("ex",lambda x:(x>0).mean()))
    out["ex_dist_active"]=act["ex"].describe(percentiles=[.1,.25,.5,.75,.9])
    out["block_pnl_dist"]=Ba["pnl"].describe(percentiles=[.05,.25,.5,.75,.95])
    return out
