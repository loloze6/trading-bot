def explore(data):
    import numpy as np, pandas as pd
    from scipy.stats import spearmanr
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
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            ret5=np.full(n,np.nan); ret5[:n-H]=cl[H:]/cl[:n-H]-1
            vr=vol/pd.Series(vol).rolling(20).mean().shift(1).values
            for P in (10,20):
                ph=pd.Series(hi).rolling(P).max().shift(1).values
                bo=cl>ph
                for t in range(0,n,H):
                    for k in range(0,4):
                        bb=t-k
                        if bb<0: break
                        if bo[bb] and not np.isnan(ph[bb]):
                            if cl[t]<ph[bb]:
                                rows.append(dict(coin=c,w=w,P=P,yr=yr[t],ratio=vr[bb],
                                  depth=cl[t]/ph[bb]-1,um=-(ret5[t]-drift[c]),tot=-ret5[t]))
                            break
    df=pd.DataFrame(rows).dropna(subset=["um"])
    def summ(g):
        return pd.Series(dict(n=len(g),mean_um=g.um.mean(),t=g.um.mean()/(g.um.std()/np.sqrt(len(g))) if len(g)>2 else np.nan,mean_tot=g.tot.mean()))
    df["shallow"]=df.depth>-0.0231
    out["by_P_shallow"]=df.groupby(["P","shallow"]).apply(summ)
    out["spearman_depth_um_by_P"]=df.groupby("P").apply(lambda g: spearmanr(g.depth,g.um).correlation)
    d=df[df.P==10].copy()
    d["half"]=np.where(d.w.str[1:].astype(int)<=12,"w1-12","w13-24")
    out["P10_shallow_by_half"]=d.groupby(["half","shallow"]).apply(summ)
    out["P10_shallow_by_coin"]=d[d.shallow].groupby("coin").apply(summ)
    d["thin"]=d.ratio<1
    out["P10_shallow_x_thin"]=d.groupby(["shallow","thin"]).apply(summ)
    # trades: entry depth vs net
    tr=[]
    for c in data["trades"]:
        for w,t in data["trades"][c].items():
            if not len(t): continue
            b=data["bars"][c][w].reset_index(drop=True)
            ph=pd.Series(b.high.values).rolling(20).max().shift(1)
            ts=pd.to_datetime(b.timestamp)
            for _,r in t.iterrows():
                i=ts.searchsorted(pd.to_datetime(r.entry_time))
                i=min(i,len(b)-1)
                # depth vs highest prior-20 high among last 4 bars
                dp=np.nan
                for k in range(4):
                    bb=i-k
                    if bb>=0 and not np.isnan(ph.iloc[bb]) and b.close.iloc[bb]>ph.iloc[bb]:
                        dp=b.close.iloc[i]/ph.iloc[bb]-1; break
                tr.append(dict(net=r.net_profit_loss_percent,depth=dp))
    T=pd.DataFrame(tr).dropna()
    T["shallow"]=T.depth>-0.0231
    out["trades_by_shallow"]=T.groupby("shallow").net.agg(["count","mean","median"])
    return out
