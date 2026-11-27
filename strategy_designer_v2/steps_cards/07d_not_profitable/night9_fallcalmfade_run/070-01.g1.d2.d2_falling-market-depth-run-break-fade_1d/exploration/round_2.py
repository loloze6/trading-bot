def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    base=[]
    for coin, wd in data["bars"].items():
        for w, b in wd.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(c)
            r1=np.r_[c[1:]/c[:-1]-1, np.nan]
            r2=np.r_[c[2:]/c[:-2]-1, [np.nan]*2]
            ret60=pd.Series(c).pct_change(60).values
            dn=np.r_[False, c[1:]<c[:-1]]; up=np.r_[False, c[1:]>c[:-1]]
            runlen=np.zeros(n); runloss=np.full(n,np.nan)
            # for every bar: loss of the down run ending at t-1 (break) or ending at t (continuing)
            curloss=np.full(n,np.nan)
            for t in range(1,n):
                k=0; j=t
                while j>=1 and c[j]<c[j-1] and k<30: k+=1; j-=1
                if k>0: curloss[t]=c[t]/c[t-k]-1
                if up[t]:
                    k=0; j=t-1
                    while j>=1 and c[j]<c[j-1] and k<30: k+=1; j-=1
                    runlen[t]=k
                    if k>0: runloss[t]=c[t-1]/c[t-1-k]-1
            bs=np.r_[np.nan,c[1:]/c[:-1]-1]
            al=b["postRebalance_current_allocation"].values
            for t in range(n):
                base.append(dict(coin=coin,w=w,t=t,r1=r1[t],r2=r2[t],fall=(ret60[t]<-0.10) if not np.isnan(ret60[t]) else False,
                    brk=bool(up[t] and runlen[t]>0),cont=bool(dn[t]),runloss=runloss[t],curloss=curloss[t],bounce=bs[t],al=al[t]))
    df=pd.DataFrame(base); drift=df.r1.mean()
    out={}
    fb=df[df.fall&df.brk].copy()
    bins=[-1,-0.15,-0.10,-0.07,-0.04,0]
    fb["lb"]=pd.cut(fb.runloss,bins)
    out["fallbreak_by_loss_bin"]=fb.groupby("lb").agg(n=("r1","size"),s1=("r1",lambda x:-(x-drift).mean()),
        t=("r1",lambda x:stats.ttest_1samp(-(x.dropna()-drift),0)[0] if len(x)>2 else np.nan),s2=("r2",lambda x:-x.mean()),alloc=("al",lambda x:x.abs().mean()))
    # condition alone: deep down run in falling market, the day is a down day (no break)
    fc=df[df.fall&df.cont].copy(); fc["lb"]=pd.cut(fc.curloss,bins)
    out["fall_downday_by_runloss_bin"]=fc.groupby("lb").agg(n=("r1","size"),s1=("r1",lambda x:-(x-drift).mean()))
    # non falling breaks, by loss
    nf=df[(~df.fall)&df.brk].copy(); nf["lb"]=pd.cut(nf.runloss,bins)
    out["nonfall_break_by_loss_bin"]=nf.groupby("lb").agg(n=("r1","size"),s1=("r1",lambda x:-(x-drift).mean()))
    # bounce size relative to run loss among deep falling breaks
    d=fb[fb.runloss<-0.10].copy()
    d["rec"]=d.bounce/(-d.runloss)
    d["rq"]=pd.qcut(d.rec.rank(method="first"),3,labels=["small","mid","large"])
    out["deep_by_bounce_share"]=d.groupby("rq").agg(n=("r1","size"),rec=("rec","mean"),s1=("r1",lambda x:-(x-drift).mean()))
    out["deep_by_window"]=d.groupby("w").agg(n=("r1","size"),s1=("r1",lambda x:-(x-drift).mean()))
    out["deep_by_coin"]=d.groupby("coin").agg(n=("r1","size"),s1=("r1",lambda x:-(x-drift).mean()))
    # book daily stats
    days=pd.concat([dd.assign(coin=cn,w=w) for cn,wd in data["days"].items() for w,dd in wd.items()])
    dm=days.groupby(["w","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).dropna()
    out["book_daily"]=pd.Series({"mean":dm.br.mean(),"sd":dm.br.std(),"sharpe":dm.br.mean()/dm.br.std()*np.sqrt(365),
        "hold_sharpe":dm.cr.mean()/dm.cr.std()*np.sqrt(365),"worst_day":dm.br.min()})
    return out
