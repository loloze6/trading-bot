import pandas as pd, numpy as np

def explore(data):
    rows=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30).std()
            vsr=(c/c.shift(14)-1)/(sd*np.sqrt(14))
            yr=pd.to_datetime(b["timestamp"]).dt.year
            inprof=(b["regime"]!="chop")
            act=b["regime"]=="trending"
            fc=b["forecast"].astype(float)
            n=len(b); h=7
            for i in range(0,n-h,h):
                # first active bar in the grid cell (a case like step 5)
                cell=[j for j in range(i,min(i+h,n-h)) if act[j] and fc[j]>0]
                rows.append(dict(coin=coin,w=w,i=i,year=yr[i],ret=c[i+h]/c[i]-1,vsr=vsr[i],prof=inprof[i],
                    day=str(b["timestamp"][i])[:10],case=len(cell)>0,
                    cret=(c[cell[0]+h]/c[cell[0]]-1) if cell else np.nan,
                    cvsr=vsr[cell[0]] if cell else np.nan,cfc=fc[cell[0]] if cell else np.nan,
                    cday=str(b["timestamp"][cell[0]])[:10] if cell else None,
                    cyear=yr[cell[0]] if cell else np.nan))
    d=pd.DataFrame(rows)
    d["drift"]=d.groupby("coin")["ret"].transform("mean")
    d["u"]=d["ret"]-d["drift"]
    d["cu"]=d["cret"]-d["drift"]
    def summ(g,col="u",dcol="day",x="vsr"):
        g=g.dropna(subset=[col])
        dd=g.groupby(dcol)[col].sum()
        t=dd.mean()/(dd.std(ddof=1)/np.sqrt(len(dd))) if len(dd)>1 else np.nan
        return pd.Series(dict(n=len(g),days=len(dd),mean=g[col].mean(),median=g[col].median(),
              share_pos=(g[col]>0).mean(),t=t,corr=g[col].corr(g[x]) if len(g)>2 else np.nan))
    out={}
    cs=d[d.case]
    out["cases_all"]=summ(cs,"cu","cday","cvsr")
    out["cases_by_year"]=cs.groupby("cyear").apply(lambda g: summ(g,"cu","cday","cvsr"))
    out["cases_by_coin"]=cs.groupby("coin").apply(lambda g: summ(g,"cu","cday","cvsr"))
    cs=cs.assign(fq=pd.qcut(cs["cfc"].rank(method="first"),3,labels=["low","mid","high"]))
    out["cases_by_forecast_tercile"]=cs.groupby("fq",observed=True).apply(lambda g: summ(g,"cu","cday","cvsr"))
    cs=cs.assign(vq=pd.cut(cs["cvsr"],[-99,2.5,3,99]))
    out["cases_by_vsr"]=cs.groupby("vq",observed=True).apply(lambda g: summ(g,"cu","cday","cvsr"))
    x=d[d.prof&(d.vsr>=1)]
    out["grid_inprof_vsr>=1_by_year"]=x.groupby("year").apply(summ)
    out["grid_inprof_vsr>=1_by_coin"]=x.groupby("coin").apply(summ)
    out["cases_without_top_day"]=summ(cs[cs.cday!=cs.groupby("cday")["cu"].sum().idxmax()],"cu","cday","cvsr")
    return out
