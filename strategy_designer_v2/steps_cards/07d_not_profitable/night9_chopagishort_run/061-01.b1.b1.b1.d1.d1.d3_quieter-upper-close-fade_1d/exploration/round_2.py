def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    out = {}
    cs=[]; grid=[]
    for c in bars:
        for w, b in bars[c].items():
            b=b.reset_index(drop=True); cl=b.close.values; n=len(b)
            r1=b.close.pct_change(); ret5=b.close/b.close.shift(5)-1
            vol20=r1.rolling(20).std()
            z5=ret5/(vol20*np.sqrt(5))
            ret60=b.close/b.close.shift(60)-1
            loc=(b.close-b.low)/(b.high-b.low)
            for i in range(0,n,5):
                cell=b.iloc[i:i+5]; idx=cell.index[cell.forecast<0]
                if len(idx)>0:
                    j=idx[0]
                    cs.append(dict(coin=c,w=w,f=b.forecast[j],z5=z5[j],alloc=b.postRebalance_current_allocation[j],
                        s5=-(cl[j+5]/cl[j]-1) if j+5<n else np.nan))
                # grid all bars: condition-alone check
                if i+5<n and not np.isnan(z5[i]):
                    grid.append(dict(w=w,z5=z5[i],choppy=abs(ret60[i])<=0.10 if not np.isnan(ret60[i]) else np.nan,
                        upper=loc[i]>0.5, sig=b.forecast[i]<0, s5=-(cl[i+5]/cl[i]-1)))
    C=pd.DataFrame(cs); G=pd.DataFrame(grid)
    def summ(x):
        x=x.dropna(); return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan))
    C["fq"]=pd.qcut(C.f,4,labels=False)
    out["fq_excl_w16"]=C[C.w!="w16"].groupby("fq").s5.apply(summ).unstack().round(4)
    out["fq_alloc"]=C.groupby("fq").alloc.agg(["mean","min","max"]).round(4)
    C["deep"]=C.z5<-1.5
    out["deep_z_cases"]=C.groupby("deep").s5.apply(summ).unstack().round(4)
    out["deep_z_excl_w16"]=C[C.w!="w16"].groupby("deep").s5.apply(summ).unstack().round(4)
    # condition alone: deep fall without signal
    G["deep"]=G.z5<-1.5
    G["grp"]=np.where(G.sig,"signal",np.where(G.deep&(G.choppy==True)&G.upper,"deep_choppy_upper_nosig",
            np.where(G.deep&(G.choppy==True),"deep_choppy_lowclose",np.where(G.deep,"deep_other","rest"))))
    out["cond_alone"]=G.groupby("grp").s5.apply(summ).unstack().round(4)
    # book: deepest days and trades by entry forecast
    T=[]
    for c in data["trades"]:
        for w,t in data["trades"][c].items():
            t=t.copy(); t["w"]=w; T.append(t)
    T=pd.concat(T)
    T["fq"]=pd.qcut(T.entry_forecast,4,labels=False,duplicates="drop")
    out["trades_by_fq"]=T.groupby("fq").agg(n=("net_profit_loss_percent","size"),net=("net_profit_loss_percent","mean"),
        dur_days=("duration_minutes",lambda x:(x/1440).mean()),ef=("entry_forecast","median")).round(3)
    out["trades_by_w"]=T.groupby("w").agg(n=("net_profit_loss_percent","size"),net=("net_profit_loss_percent","mean")).round(3)
    rows=[]
    for c in days:
        for w,d in days[c].items():
            dd=d[["day","book_return"]].copy(); dd["w"]=w; rows.append(dd)
    D=pd.concat(rows); B=D.groupby(["w","day"]).book_return.mean().dropna()
    out["book_neg_days_share_loss"]=pd.Series(dict(sum_neg=B[B<0].sum(),sum_pos=B[B>0].sum(),worst5=B.nsmallest(5).sum(),best5=B.nlargest(5).sum())).round(4)
    return out
