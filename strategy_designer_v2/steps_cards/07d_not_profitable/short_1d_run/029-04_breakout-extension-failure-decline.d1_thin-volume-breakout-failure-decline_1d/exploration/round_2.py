def explore(data):
    import numpy as np, pandas as pd
    H=5; out={}
    drift={}
    for c in data["bars"]:
        rs=[]
        for w,b in data["bars"][c].items():
            cl=b["close"].values; idx=np.arange(0,len(cl)-H,H)
            rs+=list(cl[idx+H]/cl[idx]-1)
        drift[c]=np.mean(rs)
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True); n=len(b)
            cl=b["close"].values; hi=b["high"].values; vol=b["volume"].values
            ph=pd.Series(hi).rolling(20).max().shift(1).values
            vr=vol/pd.Series(vol).rolling(20).mean().shift(1).values
            bo=cl>ph
            ret5=np.full(n,np.nan); ret5[:n-H]=cl[H:]/cl[:n-H]-1
            fc=b["forecast"].values
            for t in range(0,n,H):
                for L in (4,10):
                    for k in range(0,L):
                        bb=t-k
                        if bb<0: break
                        if bo[bb] and not np.isnan(ph[bb]):
                            if cl[t]<ph[bb]:
                                ext=hi[bb:t+1].max()/ph[bb]-1
                                rows.append(dict(coin=c,w=w,L=L,ratio=vr[bb],depth=cl[t]/ph[bb]-1,
                                  ext=ext,age=k,um=-(ret5[t]-drift[c]),tot=-ret5[t],sig=fc[t]<0))
                            break
    df=pd.DataFrame(rows).dropna(subset=["um"])
    def summ(g):
        return pd.Series(dict(n=len(g),mean_um=g.um.mean(),t=g.um.mean()/(g.um.std()/np.sqrt(len(g))) if len(g)>2 else np.nan,mean_tot=g.tot.mean()))
    out["by_window_len"]=df.groupby("L").apply(summ)
    d10=df[df.L==10].copy()
    d10["dbin"]=pd.qcut(d10.depth,4)
    out["L10_by_depth"]=d10.groupby("dbin").apply(summ)
    d10["age_bin"]=pd.cut(d10.age,[-1,3,6,9])
    out["L10_by_age"]=d10.groupby("age_bin").apply(summ)
    d10["ebin"]=pd.qcut(d10.ext,3)
    out["L10_by_extension"]=d10.groupby("ebin").apply(summ)
    d4=df[df.L==4].copy()
    d4["shallow"]=d4.depth>-0.0231
    d4["thin"]=d4.ratio<1
    out["L4_shallow_x_thin"]=d4.groupby(["shallow","thin"]).apply(summ)
    from scipy.stats import spearmanr
    out["spearman_depth_um_L10"]=spearmanr(d10.depth,d10.um).correlation
    out["spearman_depth_um_L4"]=spearmanr(d4.depth,d4.um).correlation
    # trades
    tr=[]
    for c in data["trades"]:
        for w,t in data["trades"][c].items():
            if len(t): tr.append(t.assign(coin=c,w=w))
    T=pd.concat(tr)
    out["trades"]=pd.Series(dict(n=len(T),mean_net=T.net_profit_loss_percent.mean(),med_net=T.net_profit_loss_percent.median(),
        win=(T.net_profit_loss_percent>0).mean(),mean_days=T.duration_minutes.mean()/1440,
        worst=T.net_profit_loss_percent.min(),best=T.net_profit_loss_percent.max()))
    # book daily
    br=pd.concat([data["days"][c][w][["book_return"]].assign(w=w) for c in data["days"] for w in data["days"][c]])
    out["book_daily_by_window_count_active"]=br.groupby("w").book_return.apply(lambda s:(s.abs()>1e-9).mean()).describe()
    return out
