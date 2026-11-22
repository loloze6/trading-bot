import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,wins in data["bars"].items():
        g=[]
        for w,b in wins.items():
            c=b["close"].values
            for i in range(0,len(c)-5,5):
                g.append(c[i+5]/c[i]-1)
        drift=np.mean(g); usual=np.std(g)
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; n=len(c)
            ph=c.shift(1).rolling(20).max()
            brk=(c>ph)
            ret5=c.shift(-5)/c-1
            r1=c.pct_change()
            vol20=r1.rolling(20).std()
            volrel=vol20/r1.rolling(120,min_periods=60).std()
            vr=b["volume"]/b["volume"].rolling(20).mean()
            fmax5=c[::-1].rolling(5).max()[::-1].shift(-1)
            seen=set()
            for t in range(n-5):
                cell=t//5
                if cell in seen: continue
                for lag in (1,2,3):
                    s=t-lag
                    if s>=0 and brk.iloc[s] and c.iloc[t]<ph.iloc[s]:
                        seen.add(cell); oh=ph.iloc[s]
                        rows.append(dict(coin=coin,
                          ex=-(ret5.iloc[t]-drift), tot=-ret5.iloc[t], usual=usual,
                          brksize=c.iloc[s]/oh-1, vol20=vol20.iloc[t], volrel=volrel.iloc[t],
                          vratio=vr.iloc[s], rebreak=float(fmax5.iloc[t]>c.iloc[s])))
                        break
    df=pd.DataFrame(rows).dropna(subset=["ex"])
    out={}
    out["rebreak_share"]=df.rebreak.mean()
    out["ex_by_rebreak"]=df.groupby("rebreak").ex.agg(["size","mean"])
    df["vb"]=pd.qcut(df.vol20,3,labels=False); df["vrb"]=pd.qcut(df.vratio,3,labels=False)
    out["vol_x_volume"]=df.groupby(["vb","vrb"]).agg(n=("ex","size"),ex=("ex","mean"),
        t=("ex",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))))
    d=df.dropna(subset=["volrel"]).copy(); d["b"]=pd.qcut(d.volrel,3,labels=False)
    out["by_volrel"]=d.groupby("b").agg(lo=("volrel","min"),hi=("volrel","max"),n=("ex","size"),
        ex=("ex","mean"),t=("ex",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))))
    df["str"]=df.ex/df.usual
    out["strength_by_vrb"]=df.groupby("vrb").str.mean()
    out["spearman_vratio_ex"]=stats.spearmanr(df.vratio,df.ex).correlation
    out["spearman_vol20_ex"]=stats.spearmanr(df.vol20,df.ex).correlation
    out["spearman_brk_ex"]=stats.spearmanr(df.brksize,df.ex).correlation
    # book falls
    res=[]
    for coin,wins in data["days"].items():
        for w,dd in wins.items():
            r=dd["book_return"].fillna(0).values
            v=np.cumprod(1+r); dd_=v/np.maximum.accumulate(v)-1
            res.append(dict(coin=coin,w=w,maxdd=dd_.min(),coinret=dd["close"].iloc[-1]/dd["close"].iloc[0]-1,book=v[-1]-1))
    R=pd.DataFrame(res)
    out["book_vs_coin_corr"]=R[["book","coinret"]].corr().iloc[0,1]
    out["worst_dd_windows"]=R.sort_values("maxdd").head(8)[["coin","w","maxdd","coinret","book"]]
    return out
