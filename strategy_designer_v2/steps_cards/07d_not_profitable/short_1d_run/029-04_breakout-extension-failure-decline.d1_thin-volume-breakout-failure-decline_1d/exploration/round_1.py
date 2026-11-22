def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    out={}
    # coin drift over 5 bars (grid, all windows)
    drift={}; usual={}
    for c in data["bars"]:
        rs=[]
        for w,b in data["bars"][c].items():
            cl=b["close"].values
            idx=np.arange(0,len(cl)-H,H)
            rs+=list(cl[idx+H]/cl[idx]-1)
        drift[c]=np.mean(rs); usual[c]=np.std(rs)
    rows=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True)
            n=len(b)
            cl=b["close"].values; hi=b["high"].values; vol=b["volume"].values
            for P in (10,20):
                ph=pd.Series(hi).rolling(P).max().shift(1).values
                vr=vol/pd.Series(vol).rolling(20).mean().shift(1).values
                bo=cl>ph
                ret5=np.full(n,np.nan)
                ret5[:n-H]=cl[H:]/cl[:n-H]-1
                r20=np.full(n,np.nan); r20[20:]=cl[20:]/cl[:-20]-1
                for t in range(n):
                    if t%H!=0: continue
                    fail=False; ratio=np.nan; depth=np.nan
                    for k in range(0,4):
                        bb=t-k
                        if bb<0: break
                        if bo[bb] and not np.isnan(ph[bb]):
                            if cl[t]<ph[bb]:
                                fail=True; ratio=vr[bb]; depth=cl[t]/ph[bb]-1
                            break
                    rows.append(dict(coin=c,w=w,P=P,fail=fail,ratio=ratio,depth=depth,
                        um=-(ret5[t]-drift[c]),tot=-ret5[t],fc=b["forecast"].iloc[t],r20=r20[t]))
    df=pd.DataFrame(rows).dropna(subset=["um"])
    def summ(g):
        return pd.Series(dict(n=len(g),mean_um=g.um.mean(),t=g.um.mean()/(g.um.std()/np.sqrt(len(g))) if len(g)>2 else np.nan,mean_tot=g.tot.mean()))
    out["fail_vs_all_by_P"]=df.groupby(["P","fail"]).apply(summ)
    f=df[df.fail]
    f=f.assign(vbin=pd.cut(f.ratio,[0,0.7,1.0,1.5,100]))
    out["fail_by_volratio"]=f.groupby(["P","vbin"]).apply(summ)
    f=f.assign(dbin=pd.qcut(f.depth,4,duplicates="drop"))
    out["fail20_by_depth"]=f[f.P==20].groupby("dbin").apply(summ)
    f=f.assign(tbin=pd.cut(f.r20,[-10,0,0.1,0.25,10]))
    out["fail20_by_r20"]=f[f.P==20].groupby("tbin").apply(summ)
    out["fail20_by_coin"]=f[f.P==20].groupby("coin").apply(summ)
    # book: exposure and per-window contribution
    act=[];pw={}
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            a=b["postRebalance_current_allocation"]
            act.append(dict(share_active=(a.abs()>1e-6).mean(),mean_abs_alloc_active=a[a.abs()>1e-6].abs().mean()))
            d=data["days"][c][w]
            pw.setdefault(w,[]).append(d["book_return"].sum())
    out["exposure"]=pd.DataFrame(act).mean()
    out["book_sumret_by_window"]=pd.Series({w:np.mean(v) for w,v in pw.items()})
    return out
