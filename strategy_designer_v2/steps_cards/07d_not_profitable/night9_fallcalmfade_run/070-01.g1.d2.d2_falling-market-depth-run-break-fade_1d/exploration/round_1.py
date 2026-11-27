def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; base=[]
    for coin, wd in data["bars"].items():
        for w, b in wd.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(c)
            r1=np.r_[c[1:]/c[:-1]-1, np.nan]
            r3=np.r_[c[3:]/c[:-3]-1, [np.nan]*3]
            r5=np.r_[c[5:]/c[:-5]-1, [np.nan]*5]
            dr=pd.Series(c).pct_change()
            ret60=pd.Series(c).pct_change(60).values
            sd30=dr.rolling(30).std()
            pct=sd30.rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True).values
            up=np.r_[False, c[1:]>c[:-1]]
            # run length and loss
            runlen=np.zeros(n); runloss=np.full(n,np.nan); upsize=np.r_[np.nan,c[1:]/c[:-1]-1]
            for t in range(1,n):
                if up[t]:
                    k=0; j=t-1
                    while j>=1 and c[j]<c[j-1] and k<30: k+=1; j-=1
                    runlen[t]=k
                    if k>0: runloss[t]=c[t-1]/c[t-1-k]-1
            fc=b["forecast"].values; al=b["postRebalance_current_allocation"].values
            for t in range(n):
                base.append(dict(coin=coin,w=w,r1=r1[t],r3=r3[t],r5=r5[t],fall=ret60[t]<-0.10 if not np.isnan(ret60[t]) else np.nan,
                                 brk=(up[t] and runlen[t]>0), fc=fc[t], al=al[t], pct=pct[t],runlen=runlen[t],runloss=runloss[t],up=upsize[t],day=t))
    df=pd.DataFrame(base)
    drift=df.r1.mean()
    act=df[df.fc<0].copy()
    out={}
    out["drift_all"]=drift
    out["active_n"]=len(act)
    act["s1"]=-(act.r1)
    out["active_stats"]=pd.Series({"mean_short_r1":act.s1.mean(),"t":stats.ttest_1samp(act.s1.dropna(),0)[0],
        "mean_short_r3":(-act.r3).mean(),"mean_short_r5":(-act.r5).mean(),"mean_abs_alloc":act.al.abs().mean(),"median_abs_alloc":act.al.abs().median(),"mean_fc":act.fc.mean()})
    act["lq"]=pd.qcut(act.runloss.rank(method="first"),5,labels=False)
    g=act.groupby("lq").agg(n=("s1","size"),loss=("runloss","mean"),s1=("s1","mean"),s3=("r3",lambda x:-x.mean()),alloc=("al",lambda x:x.abs().mean()),fc=("fc","mean"))
    out["by_runloss_q"]=g
    act["ag"]=np.where(act.pct>0.5,"agitated",np.where(act.pct<=0.5,"calm","na"))
    out["by_agit"]=act.groupby("ag").agg(n=("s1","size"),s1=("s1","mean"),s3=("r3",lambda x:-x.mean()),loss=("runloss","mean"))
    out["by_runlen"]=act.assign(L=act.runlen.clip(upper=5)).groupby("L").agg(n=("s1","size"),s1=("s1","mean"),s3=("r3",lambda x:-x.mean()))
    # condition alone: falling market, non-break days
    nb=df[(df.fall==True)&(~df.brk)]
    fb=df[(df.fall==True)&(df.brk)]
    out["cond_check"]=pd.Series({"fall_nonbreak_short_r1":-nb.r1.mean(),"n_nb":len(nb),"fall_break_short_r1":-fb.r1.mean(),"n_fb":len(fb),
        "allbreak_short_r1":-df[df.brk].r1.mean(),"nonfall_break_short_r1":-df[(df.fall==False)&df.brk].r1.mean()})
    # deep breaks: top 40% loss among falling breaks
    fb=fb.copy(); fb["lq"]=pd.qcut(fb.runloss.rank(method="first"),5,labels=False)
    out["fallbreak_by_lossq"]=fb.groupby("lq").agg(n=("r1","size"),loss=("runloss","mean"),s1=("r1",lambda x:-x.mean()),s2up=("up","mean"))
    # trades
    tr=pd.concat([t for wd in data["trades"].values() for t in wd.values()])
    out["trades"]=pd.Series({"n":len(tr),"gross_mean":tr.profit_loss_percent.mean(),"net_mean":tr.net_profit_loss_percent.mean(),"dur_days_mean":tr.duration_minutes.mean()/1440})
    days=pd.concat([d.assign(w=w) for wd in data["days"].values() for w,d in wd.items()])
    out["book_by_window"]=days.groupby("w").agg(br=("book_return","mean"),cr=("coin_return","mean"))
    return out
