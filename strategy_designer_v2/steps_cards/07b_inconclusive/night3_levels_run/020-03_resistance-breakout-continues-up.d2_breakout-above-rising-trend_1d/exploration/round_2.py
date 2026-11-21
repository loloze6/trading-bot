def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=[5,10]
    rows=[]
    for coin,ws in data["bars"].items():
        dr={}
        for h in H:
            rr=[]
            for w,b in ws.items():
                c=b["close"].values
                idx=np.arange(0,len(c)-h,h)
                rr+=list(c[idx+h]/c[idx]-1)
            dr[h]=np.mean(rr)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].fillna(0).values
            tr=(b["regime"]=="trending").values
            n=len(c)
            piv=np.zeros(n,bool)
            for i in range(2,n-2):
                if c[i]>=c[i-2:i+3].max(): piv[i]=True
            sma=pd.Series(c).rolling(50,min_periods=20).mean().values
            r20=pd.Series(c).pct_change(20).values
            vol=pd.Series(c).pct_change().rolling(30,min_periods=10).std().values
            low=0; seen=set()
            for t in range(n):
                if f[t]<=0: low=0
                isbet=False
                if tr[t] and f[t]>0 and f[t]-low>=2:
                    isbet=True; low=f[t]
                cell=t//5
                if isbet and cell not in seen:
                    seen.add(cell)
                    # pivots confirmed by t (index <= t-2) within past 90
                    lo=max(0,t-90)
                    ps=[c[i] for i in range(lo,t-1) if piv[i] and c[i]<c[t]]
                    if ps:
                        top=max(ps)
                        cnt=sum(1 for p in ps if p>=top*0.98)
                        brk=c[t]/top-1
                    else:
                        cnt=np.nan; brk=np.nan
                    rec=dict(coin=coin,w=w,cnt=cnt,brk=brk,dist=c[t]/sma[t]-1,r20=r20[t],vol=vol[t],
                             above=(c[t]>sma[t]))
                    for h in H:
                        rec[f"x{h}"]=c[t+h]/c[t]-1-dr[h] if t+h<n else np.nan
                    rows.append(rec)
    d=pd.DataFrame(rows).dropna(subset=["x5"])
    def summ(g,col="x5"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"m5":x.mean(),"t5":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,
                          "m10":g["x10"].dropna().mean(),
                          "t10":g["x10"].dropna().mean()/(g["x10"].dropna().std()/np.sqrt(g["x10"].notna().sum())) if g["x10"].notna().sum()>2 else np.nan})
    out={}
    out["cnt_dist"]=d.cnt.value_counts().sort_index()
    d["cntg"]=d.cnt.clip(upper=4)
    out["by_cnt"]=d.groupby("cntg").apply(summ)
    d["bq"]=pd.qcut(d.brk.rank(method="first"),5,labels=False)
    out["by_break_q"]=d.groupby("bq").apply(lambda g: pd.concat([summ(g),pd.Series({"brk":g.brk.mean()})]))
    d["sbrk"]=d.brk/d.vol
    d["sq"]=pd.qcut(d.sbrk.rank(method="first"),5,labels=False)
    out["by_break_over_vol_q"]=d.groupby("sq").apply(lambda g: pd.concat([summ(g),pd.Series({"sbrk":g.sbrk.mean()})]))
    d["dvol"]=d.dist/d.vol
    d["dq"]=pd.qcut(d.dvol.rank(method="first"),5,labels=False)
    out["by_dist_over_vol_q"]=d.groupby("dq").apply(summ)
    cc=d.dropna(subset=["cnt","brk","x10"])
    out["spearman"]=pd.DataFrame({k:[stats.spearmanr(cc[k],cc.x5).correlation,stats.spearmanr(cc[k],cc.x10).correlation]
                                  for k in ["cnt","brk","sbrk","dist","dvol","r20"]},index=["x5","x10"]).T
    out["x10_slope_dist"]=stats.linregress(cc.dist,cc.x10).slope
    return out
