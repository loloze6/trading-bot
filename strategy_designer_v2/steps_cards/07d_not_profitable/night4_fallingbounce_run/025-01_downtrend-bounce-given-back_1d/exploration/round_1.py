import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars=data["bars"]; days=data["days"]
    rows=[]; drift5={}; dailymean={}
    for c in bars:
        allr5=[]; alld=[]
        for w,b in bars[c].items():
            cl=b["close"].values
            n=len(cl)
            idx=np.arange(0,n-5,5)
            allr5+=list(cl[idx+5]/cl[idx]-1)
            alld+=list(pd.Series(cl).pct_change().dropna())
        drift5[c]=np.mean(allr5); dailymean[c]=np.mean(alld)
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change(); v=r.rolling(20).std()
            z=r/v
            r90=cl/cl.shift(90)-1; r20=cl/cl.shift(20)-1
            lo90=cl/cl.rolling(90).min()-1
            n=len(b)
            f=b["forecast"].values
            for s in range(0,n,5):
                for t in range(s,min(s+5,n)):
                    if f[t]<=-2:
                        if t+10<n:
                            d=dict(coin=c,win=w,z=z[t],f=f[t],r90=r90[t],r20=r20[t],lo90=lo90[t],vol=v[t])
                            for h in (1,2,3,5,10):
                                d["u%d"%h]=-(cl[t+h]/cl[t]-1-drift5[c]*h/5)
                            d["tot5"]=-(cl[t+5]/cl[t]-1)
                            rows.append(d)
                        break
    df=pd.DataFrame(rows)
    out={}
    def summ(g):
        return pd.Series({"n":len(g),"u5":g.u5.mean(),"t5":g.u5.mean()/(g.u5.std()/np.sqrt(len(g))),"tot5":g.tot5.mean(),"u1":g.u1.mean(),"u3":g.u3.mean(),"u10":g.u10.mean()})
    out["all"]=summ(df)
    for col,q in [("z",5),("f",4),("r90",5),("r20",5),("lo90",5),("vol",4)]:
        df["b"]=pd.qcut(df[col],q,duplicates="drop")
        out["by_"+col]=df.groupby("b",observed=True).apply(summ)
    out["by_coin"]=df.groupby("coin").apply(summ)
    df["yr"]=0
    # book decomposition
    rec=[]
    for c in days:
        for w,d in days[c].items():
            b=bars[c][w].copy(); b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos=b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            dd=d.set_index(pd.to_datetime(d["day"]))
            dd["pos"]=pos.reindex(dd.index).values
            dd["coin"]=c; dd["win"]=w; dd["yr"]=dd.index.year
            rec.append(dd)
    R=pd.concat(rec)
    R["mkt"]=R["pos"]*R["coin"].map(dailymean)
    R["timing"]=R["pos"]*R["coin_return"]-R["mkt"]
    out["book"]=pd.Series({"book_mean":R.book_return.mean(),"pos_x_ret":(R.pos*R.coin_return).mean(),"mkt":R.mkt.mean(),"timing":R.timing.mean(),"share_days_short":(R.pos<0).mean(),"mean_pos_when_short":R.pos[R.pos<0].mean()})
    out["book_by_year"]=R.groupby("yr").agg(book=("book_return","mean"),coin=("coin_return","mean"),short=("pos",lambda x:(x<0).mean()))
    T=pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()])
    T["fb"]=pd.qcut(T.entry_forecast,4,duplicates="drop")
    out["trades_by_f"]=T.groupby("fb",observed=True).agg(n=("net_profit_loss_percent","size"),net=("net_profit_loss_percent","mean"),gross=("profit_loss_percent","mean"),dur_d=("duration_minutes",lambda x:x.mean()/1440),win=("profit_loss_percent",lambda x:(x>0).mean()))
    return out
