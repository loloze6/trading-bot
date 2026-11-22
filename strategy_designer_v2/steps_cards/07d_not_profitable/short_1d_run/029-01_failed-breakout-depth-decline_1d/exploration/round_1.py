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
        drift=np.mean(g)
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; n=len(c)
            ph=c.shift(1).rolling(20).max()
            brk=(c>ph)
            ret5=c.shift(-5)/c-1
            r1=c.pct_change()
            vol20=r1.rolling(20).std()
            ret20=c/c.shift(20)-1
            ma50=c/c.rolling(50,min_periods=30).mean()-1
            vr=b["volume"]/b["volume"].rolling(20).mean()
            seen=set()
            for t in range(n-5):
                cell=t//5
                if cell in seen: continue
                for lag in (1,2,3):
                    s=t-lag
                    if s>=0 and brk.iloc[s] and c.iloc[t]<ph.iloc[s]:
                        seen.add(cell); oh=ph.iloc[s]
                        rows.append(dict(coin=coin,
                          year=pd.Timestamp(b["timestamp"].iloc[t]).year,
                          ex=-(ret5.iloc[t]-drift), tot=-ret5.iloc[t],
                          rawdepth=(oh-c.iloc[t])/oh,
                          brksize=c.iloc[s]/oh-1, lag=lag,
                          ret20=ret20.iloc[t], ma50=ma50.iloc[t],
                          vol20=vol20.iloc[t], r1=r1.iloc[t], vratio=vr.iloc[s]))
                        break
    df=pd.DataFrame(rows).dropna(subset=["ex"])
    out={"n_cases":len(df),"mean_ex":df.ex.mean(),
         "t_ex":stats.ttest_1samp(df.ex,0).statistic,"mean_tot":df.tot.mean()}
    def grp(col,q=3):
        d=df.dropna(subset=[col]).copy()
        d["b"]=pd.qcut(d[col],q,labels=False,duplicates="drop")
        return d.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),n=("ex","size"),
            mean_ex=("ex","mean"),
            t=("ex",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))),
            mean_tot=("tot","mean"))
    for col in ["rawdepth","brksize","ret20","ma50","vol20","r1","vratio"]:
        out["by_"+col]=grp(col)
    out["by_lag"]=df.groupby("lag").ex.agg(["size","mean"])
    out["by_year"]=df.groupby("year").agg(n=("ex","size"),ex=("ex","mean"),tot=("tot","mean"))
    out["by_coin"]=df.groupby("coin").agg(n=("ex","size"),ex=("ex","mean"),tot=("tot","mean"))
    dl=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; dl.append(d)
    D=pd.concat(dl)
    D["year"]=pd.to_datetime(D["day"]).dt.year
    out["book_by_year"]=D.groupby("year").agg(book=("book_return","mean"),coin=("coin_return","mean"))
    T=pd.concat([t for wins in data["trades"].values() for t in wins.values() if len(t)])
    out["trades"]=pd.Series({"n":len(T),"gross_mean":T.profit_loss_percent.mean(),
        "net_mean":T.net_profit_loss_percent.mean(),
        "win_share":(T.profit_loss_percent>0).mean(),
        "dur_days_mean":T.duration_minutes.mean()/1440})
    return out
