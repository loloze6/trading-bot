def explore(data):
    import numpy as np, pandas as pd
    out={}
    rows=[]
    for coin,ws in data["bars"].items():
        rs=[]
        for w,b in ws.items():
            c=b["close"].values; idx=np.arange(0,len(c)-18,18); rs+=list(c[idx+18]/c[idx]-1)
        dr=np.mean(rs); sd=np.std(rs)
        for w,b in ws.items():
            c=b["close"].values.astype(float); v=b["volume"].values.astype(float); n=len(c)
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            raw=b["debug_info.components.streak_loss.last_history_value"].values
            r1=np.abs(np.r_[np.nan,c[1:]/c[:-1]-1])
            usual=pd.Series(r1).rolling(180,min_periods=45).mean().values
            seen=set(); L=0
            for t in range(1,n):
                L=L+1 if c[t]<c[t-1] else 0
                if L<2 or t+18>=n or np.isnan(usual[t]): continue
                cell=t//18
                if cell in seen: continue
                seen.add(cell)
                s=t-L
                vv=v[s+1:t+1]; slope=np.polyfit(np.arange(L),vv,1)[0]
                loss=(1-c[t]/c[s])/usual[t]
                rows.append({"coin":coin,"yr":yr[t],"fade":slope<0,"loss":loss,"L":L,
                             "u":c[t+18]/c[t]-1-dr,"s":(c[t+18]/c[t]-1-dr)/sd,"rawrec":raw[t]})
    d=pd.DataFrame(rows)
    def st(g):
        x=g["u"].dropna(); return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)),"strength":g["s"].mean()})
    d["lq"]=pd.qcut(d["loss"],5,labels=False)
    out["loss_q_median"]=d.groupby("lq")["loss"].median()
    out["fade_by_lossq"]=d[d.fade].groupby("lq").apply(st)
    out["rising_by_lossq"]=d[~d.fade].groupby("lq").apply(st)
    top=d[d.lq==4]
    a=top[top.fade]["u"];b=top[~top.fade]["u"]
    from scipy import stats
    out["top_fade_minus_rising"]=pd.Series({"diff%":100*(a.mean()-b.mean()),"welch_t":stats.ttest_ind(a,b,equal_var=False)[0]})
    out["top_fade_by_coin"]=top[top.fade].groupby("coin").apply(st)
    out["top_fade_by_year"]=top[top.fade].groupby("yr").apply(st)
    out["corr_loss_u_fade"]=pd.Series({"spearman":stats.spearmanr(d[d.fade]["loss"],d[d.fade]["u"])[0],"n":int(d.fade.sum())})
    return out
