import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H=18
    rows=[]
    drift={}; usual={}
    for coin,wins in data["bars"].items():
        rs=[]
        for w,df in wins.items():
            c=df["close"].values
            idx=np.arange(0,len(c)-H,H)
            rs+=list(c[idx+H]/c[idx]-1)
        drift[coin]=np.mean(rs); usual[coin]=np.std(rs)
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            f=df["forecast"].fillna(0).values
            c=df["close"].values; lo=df["low"].values; hi=df["high"].values
            n=len(f)
            s_lo=pd.Series(lo); s_hi=pd.Series(hi)
            span=(s_hi.shift(1).rolling(12).max()-s_lo.shift(1).rolling(12).min()).values
            mbr=((s_hi-s_lo).shift(1).rolling(180).mean()).values
            rawratio=span/mbr
            mom=pd.Series(c).pct_change(180).values
            vol30=pd.Series(c).pct_change().rolling(180).std().values
            ref=0.0; bets=[]
            for i in range(n):
                if f[i]==0:
                    ref=0.0; continue
                if f[i]-ref>=2:
                    bets.append(i); ref=f[i]
                else:
                    ref=min(ref,f[i])
            seen=set()
            for i in bets:
                cell=i//18
                if cell in seen: continue
                seen.add(cell)
                if i+H>=n: continue
                r={"coin":coin,"win":int(w[1:]),"fc":f[i],"raw":rawratio[i],"mom":mom[i],
                   "momz":mom[i]/(vol30[i]*np.sqrt(180)) if vol30[i]>0 else np.nan,
                   "year":pd.Timestamp(df["timestamp"].iloc[i]).year,
                   "ex":c[i+H]/c[i]-1-drift[coin],"str":(c[i+H]/c[i]-1-drift[coin])/usual[coin]}
                for h in [6,12,36]:
                    r[f"ex{h}"]=c[i+h]/c[i]-1-drift[coin] if i+h<n else np.nan
                rows.append(r)
    d=pd.DataFrame(rows)
    def summ(g,col="ex"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    q=d["fc"].quantile(0.75)
    top=d[d["fc"]>=q]
    out["fc_q75"]=q
    out["top_by_coin"]=top.groupby("coin").apply(summ)
    out["top_by_year"]=top.groupby("year").apply(summ)
    out["top_by_H"]=pd.DataFrame({h:summ(top,f"ex{h}") for h in [6,12,36]}).T
    out["top_strength"]=top["str"].mean()
    d["fcq"]=pd.qcut(d["fc"],4,labels=False,duplicates="drop")
    out["fcq_fc_mean"]=d.groupby("fcq")["fc"].agg(["min","mean","max"])
    d["rq"]=pd.qcut(d["raw"],5,labels=False,duplicates="drop")
    out["by_raw_quint"]=d.groupby("rq").apply(summ)
    out["raw_quint_vals"]=d.groupby("rq")["raw"].agg(["min","mean","max"])
    out["spearman_raw"]=stats.spearmanr(d["raw"],d["ex"],nan_policy="omit")[0]
    d["mzq"]=pd.qcut(d["momz"],3,labels=False,duplicates="drop")
    out["by_fcq_x_momz"]=d.groupby(["fcq","mzq"]).apply(summ)
    out["top_fold_half"]=top.assign(h=(top["win"]>12).astype(int)).groupby("h").apply(summ)
    out["fc_deciles"]=d.assign(dq=pd.qcut(d["fc"],10,labels=False,duplicates="drop")).groupby("dq").apply(summ)
    return out
