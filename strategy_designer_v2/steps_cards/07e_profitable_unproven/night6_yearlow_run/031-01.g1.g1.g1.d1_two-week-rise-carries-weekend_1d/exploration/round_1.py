def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"]
            r2=c.shift(-2)/c-1
            r1=c.shift(-1)/c-1
            lr=np.log(c).diff()
            vol=lr.rolling(20).std()
            rise14=(np.log(c)-np.log(c.shift(14)))/(vol*np.sqrt(14))
            d=pd.DataFrame({"coin":coin,"w":w,"wd":ts.dt.weekday,"year":ts.dt.year,
                "r1":r1,"r2":r2,"fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],
                "rise14":rise14,"pos":np.arange(len(b))})
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    out={}
    # baseline 2-day returns by weekday (non-overlap per weekday automatically since weekly)
    g=A.dropna(subset=["r2"]).groupby("wd")["r2"]
    out["r2_by_weekday"]=pd.DataFrame({"mean":g.mean(),"n":g.size(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    fri=A[(A.wd==4)].dropna(subset=["r2"]).copy()
    fri["grp"]=np.where(fri.fc>0,"fc>0","fc=0")
    g=fri.groupby("grp")["r2"]
    out["fri_r2_by_fc"]=pd.DataFrame({"mean":g.mean(),"n":g.size(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    # raw rise14 quintiles on Fridays
    f2=fri.dropna(subset=["rise14"]).copy()
    f2["q"]=pd.qcut(f2.rise14,5,labels=False)
    g=f2.groupby("q")
    out["fri_r2_by_rise14_q"]=pd.DataFrame({"rise_mean":g.rise14.mean(),"r2":g.r2.mean(),"n":g.size(),
        "t":g.r2.mean()/(g.r2.std()/np.sqrt(g.size()))})
    # same quintiles on other weekdays (non-overlap grid pos%2==0)
    o=A[(A.wd!=4)&(A.pos%2==0)].dropna(subset=["r2","rise14"]).copy()
    o["q"]=pd.qcut(o.rise14,5,labels=False)
    g=o.groupby("q")
    out["other_r2_by_rise14_q"]=pd.DataFrame({"rise_mean":g.rise14.mean(),"r2":g.r2.mean(),"n":g.size(),
        "t":g.r2.mean()/(g.r2.std()/np.sqrt(g.size()))})
    # fc>0 terciles on Friday
    fp=fri[fri.fc>0].copy(); fp["q"]=pd.qcut(fp.fc,3,labels=False)
    g=fp.groupby("q")
    out["fri_r2_by_fc_tercile"]=pd.DataFrame({"fc":g.fc.mean(),"r2":g.r2.mean(),"n":g.size()})
    # book per coin, per year, market part
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dd=d.copy(); dd["coin"]=coin; dd["w"]=w; D.append(dd)
    D=pd.concat(D,ignore_index=True)
    D["year"]=pd.to_datetime(D["day"]).dt.year
    out["book_by_coin"]=D.groupby("coin").agg(book=("book_return","mean"),coin=("coin_return","mean"))
    out["book_by_year"]=D.groupby("year").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","size"))
    mu=A.groupby("coin")["r1"].mean()
    A["mkt"]=A.alloc.fillna(0)*A.coin.map(mu)
    A["gain"]=A.alloc.fillna(0)*A.r1
    out["gain_vs_market_per_bar"]=pd.Series({"mean_gain":A.gain.mean(),"market_part":A.mkt.mean(),"mean_alloc":A.alloc.fillna(0).mean()})
    out["gain_by_wd_of_bar"]=A.groupby("wd").gain.mean()
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()],ignore_index=True)
    p=T.net_profit_loss_percent.sort_values(ascending=False)
    out["trades"]=pd.Series({"n":len(p),"sum":p.sum(),"top10_sum":p.head(10).sum(),"top30_sum":p.head(30).sum(),"win":(p>0).mean(),"mean":p.mean(),"median":p.median()})
    out["trades_by_coin"]=T.groupby("coin").net_profit_loss_percent.agg(["mean","size","sum"])
    return out
