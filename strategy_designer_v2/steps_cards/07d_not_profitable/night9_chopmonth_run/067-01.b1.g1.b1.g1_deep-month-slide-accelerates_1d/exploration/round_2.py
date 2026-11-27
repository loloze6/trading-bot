def explore(data):
    import numpy as np, pandas as pd
    bars=data["bars"]; days=data["days"]; trades=data["trades"]
    out={}
    # trades: price-based short return vs recorded
    rows=[]
    for c in trades:
        for w,t in trades[c].items():
            if len(t)==0: continue
            t=t.copy(); t["w"]=w; t["c"]=c; rows.append(t)
    tr=pd.concat(rows)
    tr["px_short"]=-(tr.exit_price/tr.entry_price-1)*100
    tr["dur_d"]=tr.duration_minutes/1440
    tr["durq"]=pd.cut(tr.dur_d,[-1,1,3,6,9,12,1000])
    out["trades_px_vs_rec"]=pd.Series(dict(px_short=tr.px_short.mean(),rec_gross=tr.profit_loss_percent.mean(),net=tr.net_profit_loss_percent.mean(),comm=tr.total_commission.mean(),n=len(tr)))
    out["trades_by_dur"]=tr.groupby("durq").agg(n=("px_short","size"),px_short=("px_short","mean"),net=("net_profit_loss_percent","mean"))
    out["trades_by_window"]=tr.groupby("w").agg(n=("px_short","size"),px_short=("px_short","mean"),net=("net_profit_loss_percent","mean"))
    # bar-level position gain, with drift
    drift={}
    for c in bars:
        r=[]
        for w,b in bars[c].items():
            cl=b["close"].values
            for i in range(0,len(cl)-1): r.append(cl[i+1]/cl[i]-1)
        drift[c]=np.mean(r)
    P=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True); cl=b["close"].values; n=len(cl)
            a=b["postRebalance_current_allocation"].fillna(0).values
            chg=np.abs(np.diff(np.r_[0,a]))
            for i in range(n-1):
                if a[i]!=0 or chg[i]>0:
                    r60=cl[i]/cl[i-60]-1 if i>=60 else np.nan
                    r30=cl[i]/cl[i-30]-1 if i>=30 else np.nan
                    v10=np.std(np.diff(np.log(cl[max(0,i-10):i+1]))) if i>=10 else np.nan
                    v30=np.std(np.diff(np.log(cl[max(0,i-30):i+1]))) if i>=30 else np.nan
                    P.append(dict(c=c,w=w,a=a[i],chg=chg[i],g=a[i]*(cl[i+1]/cl[i]-1),mkt=a[i]*drift[c],r60=r60,r30=r30,vr=v10/v30 if v30 else np.nan,rg=b["regime"].iloc[i]))
    P=pd.DataFrame(P)
    P["fee"]=P.chg*0.0022/2
    out["pos_bars"]=pd.Series(dict(n=len(P),mean_abs_alloc=P.a.abs().mean(),gain_sum=P.g.sum(),mkt_sum=P.mkt.sum(),fee_est_sum=P.fee.sum(),share_regime_trending=(P.rg=="trending").mean()))
    out["pos_by_regime"]=P.groupby("rg").agg(n=("g","size"),g=("g","mean"),a=("a","mean"))
    def sm(x): return pd.Series(dict(n=len(x),g=x.g.mean(),t=x.g.mean()/(x.g.std()/np.sqrt(len(x))),a=x.a.mean()))
    P["r60q"]=pd.qcut(P.r60.rank(method="first"),3,labels=["r60lo","r60mid","r60hi"])
    out["pos_by_r60"]=P.groupby("r60q").apply(sm)
    P["vrq"]=pd.qcut(P.vr.rank(method="first"),3,labels=["vr_lo","vr_mid","vr_hi"])
    out["pos_by_volratio"]=P.groupby("vrq").apply(sm)
    # cases on 10 grid in chop: short after down month, graded by r30, split by r60 sign and vol ratio; and condition-alone check
    S=[]
    d10={}
    for c in bars:
        r=[]
        for w,b in bars[c].items():
            cl=b["close"].values
            for i in range(0,len(cl)-10,10): r.append(cl[i+10]/cl[i]-1)
        d10[c]=np.mean(r)
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True); cl=b["close"].values; n=len(cl)
            for i in range(0,n-10,10):
                if i<60: 
                    r60=np.nan
                else: r60=cl[i]/cl[i-60]-1
                rg=b["regime"].iloc[i]
                if rg=="chop": continue
                r30=cl[i]/cl[i-30]-1 if i>=30 else np.nan
                v10=np.std(np.diff(np.log(cl[max(0,i-10):i+1]))) if i>=10 else np.nan
                v30=np.std(np.diff(np.log(cl[max(0,i-30):i+1]))) if i>=30 else np.nan
                S.append(dict(c=c,w=w,rg=rg,r30=r30,r60=r60,vr=v10/v30 if v30 else np.nan,fwd=cl[i+10]/cl[i]-1-d10[c],a=b["postRebalance_current_allocation"].iloc[i]))
    S=pd.DataFrame(S).dropna(subset=["r30"])
    S["mom"]=np.sign(S.r30)*S.fwd  # continuation unusual move
    def sm2(x): return pd.Series(dict(n=len(x),cont=x.mom.mean(),t=x.mom.mean()/(x.mom.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    S["r30q"]=pd.qcut(S.r30.rank(method="first"),5,labels=["q1dn","q2","q3","q4","q5up"])
    out["cases_by_r30_quint"]=S.groupby("r30q").apply(sm2)
    dn=S[S.r30<0].copy()
    dn["vrq"]=pd.qcut(dn.vr.rank(method="first"),2,labels=["vr_lo","vr_hi"])
    out["down_by_volratio"]=dn.groupby("vrq").apply(sm2)
    dn["r60s"]=np.where(dn.r60<0,"r60neg","r60pos")
    out["down_by_r60sign"]=dn.groupby("r60s").apply(sm2)
    return out
