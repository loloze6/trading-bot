import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H_list=[6,12,18,36]
    rows=[]
    drift={}
    usual={}
    for coin,wins in data["bars"].items():
        for H in H_list:
            rs=[]
            for w,df in wins.items():
                c=df["close"].values
                idx=np.arange(0,len(c)-H,H)
                rs+=list(c[idx+H]/c[idx]-1)
            drift[(coin,H)]=np.mean(rs); usual[(coin,H)]=np.std(rs)
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            f=df["forecast"].fillna(0).values
            c=df["close"].values; lo=df["low"].values; hi=df["high"].values
            n=len(f)
            lowmin=pd.Series(lo).shift(1).rolling(12).min().values
            mom=pd.Series(c).pct_change(180).values
            # bet detection
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
                r={"coin":coin,"win":int(w[1:]),"fc":f[i],
                   "depth":c[i]/lowmin[i]-1 if lowmin[i]>0 else np.nan,
                   "mom":mom[i],"hour":pd.Timestamp(df["timestamp"].iloc[i]).hour,
                   "year":pd.Timestamp(df["timestamp"].iloc[i]).year}
                for H in H_list:
                    if i+H<n:
                        r[f"ex{H}"]=c[i+H]/c[i]-1-drift[(coin,H)]
                        r[f"tot{H}"]=c[i+H]/c[i]-1
                    else:
                        r[f"ex{H}"]=np.nan; r[f"tot{H}"]=np.nan
                rows.append(r)
    d=pd.DataFrame(rows)
    def summ(g,col="ex18"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["overall_by_H"]=pd.DataFrame({H:summ(d,f"ex{H}") for H in H_list}).T
    out["by_coin"]=d.groupby("coin").apply(summ)
    out["by_year"]=d.groupby("year").apply(summ)
    d["fcq"]=pd.qcut(d["fc"],4,labels=False,duplicates="drop")
    out["by_fc_quart"]=d.groupby("fcq").apply(summ)
    d["dq"]=pd.qcut(d["depth"],4,labels=False,duplicates="drop")
    out["by_depth_quart(0=deepest)"]=d.groupby("dq").apply(summ)
    d["mq"]=pd.qcut(d["mom"],4,labels=False,duplicates="drop")
    out["by_mom_quart"]=d.groupby("mq").apply(summ)
    out["by_hour"]=d.groupby("hour").apply(summ)
    out["spearman_fc_ex18"]=stats.spearmanr(d["fc"],d["ex18"],nan_policy="omit")[0]
    out["spearman_depth_ex18"]=stats.spearmanr(d["depth"],d["ex18"],nan_policy="omit")[0]
    out["spearman_mom_ex18"]=stats.spearmanr(d["mom"],d["ex18"],nan_policy="omit")[0]
    out["by_window"]=d.groupby("win").apply(summ)
    return out
