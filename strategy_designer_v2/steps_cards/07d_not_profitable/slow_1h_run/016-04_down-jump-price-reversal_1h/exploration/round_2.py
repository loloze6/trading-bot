def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; days=data["days"]
    grid=[]; mk=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].values; n=len(b)
            r=np.r_[np.nan,cl[1:]/cl[:-1]-1]
            al=b["postRebalance_current_allocation"].fillna(0).values
            for i in range(72,n-72,72):
                past=cl[i]/cl[i-72]-1
                if past>=0: continue
                h=r[i-71:i+1]
                lo=np.sort(h[h<0])[:3]
                s3=-lo.sum()
                sabs=np.abs(h).sum(); sneg=-h[h<0].sum()
                vol=np.std(h)
                grid.append(dict(coin=c,past=past,share=s3/(-past),
                    shneg=s3/sneg if sneg>0 else np.nan,
                    eff=-past/sabs, z=past/(vol*np.sqrt(72)),
                    fut=cl[i+72]/cl[i]-1, al=al[i]))
            # allocation change stats
            mk.append(dict(coin=c,n=n,chg=(np.abs(np.diff(al))>1e-9).sum(),
                           medchg=np.median(np.abs(np.diff(al))[np.abs(np.diff(al))>1e-9]) if (np.abs(np.diff(al))>1e-9).any() else np.nan))
    G=pd.DataFrame(grid)
    allr=[]
    for c in bars:
        for w,b in bars[c].items():
            cl=b["close"].values
            for i in range(0,len(cl)-72,72): allr.append((c,cl[i+72]/cl[i]-1))
    A=pd.DataFrame(allr,columns=["coin","r"]); mu=A.groupby("coin").r.mean()
    G["ex"]=G.fut-G.coin.map(mu)
    out={}
    def tt(x): return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/x.std()*np.sqrt(len(x))))
    for col in ["share","shneg","eff","z"]:
        G["q"]=pd.qcut(G[col].rank(method="first"),5,labels=False)
        out["ex_by_"+col]=G.groupby("q").ex.apply(tt).unstack().round(4)
    G["pq"]=pd.qcut(G.past.rank(method="first"),3,labels=["big","mid","small"])
    G["sq"]=G.groupby("pq",observed=True).shneg.transform(lambda x:pd.qcut(x.rank(method="first"),3,labels=False))
    out["fall_x_shneg"]=G.groupby(["pq","sq"],observed=True).ex.mean().unstack().round(4)
    out["corr_share_past"]=float(np.corrcoef(np.log(G.share),np.log(-G.past))[0,1])
    M=pd.DataFrame(mk).groupby("coin").sum()
    M["chg_per_day"]=M.chg/M.n*24
    out["rebal"]=M.round(3)
    return out
