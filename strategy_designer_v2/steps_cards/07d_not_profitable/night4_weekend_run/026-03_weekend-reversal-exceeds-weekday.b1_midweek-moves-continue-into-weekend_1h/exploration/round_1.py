def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; out={}
    rows=[]; drift={}; usual={}
    for c in bars:
        g=[]
        for w,df in bars[c].items():
            cl=df["close"].values
            idx=np.arange(0,len(cl)-48,48)
            g+=list(cl[idx+48]/cl[idx]-1)
        drift[c]=np.mean(g); usual[c]=np.std(g)
    for c in bars:
        for w,df in bars[c].items():
            df=df.reset_index(drop=True)
            ts=pd.to_datetime(df["timestamp"])
            cl=df["close"].values
            sel=np.where((ts.dt.weekday==3)&(ts.dt.hour==23)&(df["forecast"]!=0))[0]
            for i in sel:
                if i+48>=len(cl) or i<48: continue
                r=cl[i+48]/cl[i]-1; raw=cl[i]/cl[i-48]-1
                f=df["forecast"].iloc[i]; s=np.sign(f)
                rows.append(dict(coin=c,win=w,year=ts.iloc[i].year,f=f,raw_z=raw/usual[c],
                    tot=s*r,unu=s*(r-drift[c]),side="long" if s>0 else "short",
                    alloc=abs(df["postRebalance_current_allocation"].iloc[i]),
                    rawdir=np.sign(raw)==s))
    d=pd.DataFrame(rows)
    out["n,agree raw sign"]=pd.Series({"n":len(d),"forecast sign = raw sign share":d.rawdir.mean(),"mean |alloc|":d.alloc.mean()})
    d["fq"]=pd.qcut(d.f.abs(),5,labels=False)
    out["by |forecast| quintile"]=d.groupby("fq").agg(n=("tot","size"),absf=("f",lambda x:x.abs().mean()),tot=("tot","mean"),unu=("unu","mean"))
    d["rq"]=pd.qcut(d.raw_z.abs(),5,labels=False)
    d["rawtot"]=np.sign(d.raw_z)*d.tot*np.sign(d.f)
    out["by |raw 48h move / usual| quintile, in raw direction"]=d.groupby("rq").agg(n=("tot","size"),absraw=("raw_z",lambda x:x.abs().mean()),rawdir_tot=("rawtot","mean"),t=("rawtot",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    out["by side"]=d.groupby("side").agg(n=("tot","size"),tot=("tot","mean"),unu=("unu","mean"))
    out["by year"]=d.groupby("year").agg(n=("tot","size"),tot=("tot","mean"),t=("tot",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    out["by coin"]=d.groupby("coin").agg(n=("tot","size"),tot=("tot","mean"),unu=("unu","mean"),usual=("coin",lambda x:usual[x.iloc[0]]))
    # trades
    tr=pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()])
    out["trades"]=pd.Series({"n":len(tr),"gross mean %":tr.profit_loss_percent.mean(),"net mean %":tr.net_profit_loss_percent.mean(),"mean dur h":tr.duration_minutes.mean()/60})
    # book daily
    dd=pd.concat([x.assign(coin=c,win=w) for c in data["days"] for w,x in data["days"][c].items()])
    dd["wd"]=pd.to_datetime(dd["day"]).dt.weekday
    out["book daily by weekday"]=dd.groupby("wd").agg(book=("book_return","mean"),coin=("coin_return","mean"))
    return out
