def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    out = {}
    # book activity
    rows=[]
    for c in bars:
        for w,df in bars[c].items():
            a = df["postRebalance_current_allocation"].fillna(0)
            rows.append(dict(coin=c, bars=len(df), in_pos=(a.abs()>1e-9).sum(), active=(df["forecast"]<0).sum()))
    r=pd.DataFrame(rows).groupby("coin").sum()
    out["activity_by_coin"]=r
    tr=[]
    for c in trades:
        for w,t in trades[c].items():
            if t is not None and len(t): 
                t=t.copy(); t["coin"]=c; tr.append(t)
    if tr:
        T=pd.concat(tr)
        out["trades_summary"]=T.groupby("side").agg(n=("net_profit_loss_percent","size"),mean_net=("net_profit_loss_percent","mean"),
            mean_gross=("profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda x:(x>0).mean()),
            dur_days=("duration_minutes",lambda x:x.mean()/1440))
    # variants from prices
    def variant(period, fw, ref, h=5):
        res=[]; drifts={}
        allr={}
        for c in bars:
            gr=[]
            for w,df in bars[c].items():
                cl=df["close"].values; n=len(cl)
                idx=np.arange(0,n-h,h)
                gr.append(cl[idx+h]/cl[idx]-1)
            drifts[c]=np.concatenate(gr).mean() if gr else 0
            sd=np.concatenate(gr).std()
            for w,df in bars[c].items():
                hi=df["high"]; lo=df["low"].values; cl=df["close"].values; n=len(cl)
                ph=hi.rolling(period).max().shift(1).values
                bo=cl>ph
                sig=np.zeros(n)
                for t in range(n):
                    for k in range(1,fw+1):
                        b=t-k
                        if b<0: break
                        if bo[b]:
                            lvl = lo[b] if ref=="low" else ph[b]
                            if cl[t]<lvl: sig[t]=lvl/cl[t]-1
                            break
                idx=np.arange(0,n-h,h)
                for i in idx:
                    if sig[i]>0:
                        ret=cl[i+h]/cl[i]-1
                        res.append((c,sig[i],-(ret-drifts[c]),-ret,-(ret-drifts[c])/sd))
        R=pd.DataFrame(res,columns=["coin","depth","unusual","total","strength"])
        if len(R)<3: return dict(n=len(R))
        from scipy import stats
        m=R.unusual.mean(); s=R.unusual.std()
        return dict(n=len(R),unusual=m,t=m/(s/np.sqrt(len(R))),total=R.total.mean(),strength=R.strength.mean(),
                    spearman=stats.spearmanr(R.depth,R.unusual)[0])
    vs={}
    for p in [10,20]:
        for fw in [3,5,10]:
            for ref in ["low","high"]:
                vs[f"p{p}_fw{fw}_{ref}"]=variant(p,fw,ref)
    out["variants"]=pd.DataFrame(vs).T
    return out
