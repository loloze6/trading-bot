def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"].astype(float); r=c.pct_change()
            vr=r.rolling(20).std()/r.rolling(60).std()
            r14=c/c.shift(14)-1
            df=pd.DataFrame({"coin":coin,"w":w,"i":np.arange(len(b)),"day":ts.dt.floor("D"),
                "wd":ts.dt.weekday,"year":ts.dt.year,"vr":vr,"r14":r14,
                "f1":c.shift(-1)/c-1,"f2":c.shift(-2)/c-1,"f3":c.shift(-3)/c-1,"f4":c.shift(-4)/c-1})
            df["z14"]=r14/(r.rolling(60).std()*np.sqrt(14))
            df["r7"]=c/c.shift(7)-1; df["z7"]=df.r7/(r.rolling(60).std()*np.sqrt(7))
            df["r28"]=c/c.shift(28)-1; df["z28"]=df.r28/(r.rolling(60).std()*np.sqrt(28))
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    for h in [1,2,3,4]:
        d=D[D.i%h==0].groupby("coin")[f"f{h}"].mean(); D[f"u{h}"]=D[f"f{h}"]-D.coin.map(d)
    def cslope(g,x,y):
        g=g.dropna(subset=[x,y])
        X=g[x]-g[x].mean(); b=(X*g[y]).sum()/(X*X).sum()
        e=g[y]-g[y].mean()-b*X
        s=(X*e).groupby(g.day).sum()
        se=np.sqrt((s**2).sum())/(X*X).sum()
        return b,b/se,len(g),g.day.nunique()
    out={}
    res=[]
    for wd in range(7):
        for h in [1,2,3]:
            for x in ["z7","z14","z28"]:
                b,t,n,nd=cslope(D[D.wd==wd],x,f"u{h}"); res.append([wd,h,x,b,t,n,nd])
    R=pd.DataFrame(res,columns=["wd","h","x","slope","t_clus","n","days"])
    out["slope_z14_by_wd_h"]=R[R.x=="z14"].drop(columns="x")
    out["slope_h2_by_lookback"]=R[R.h==2].pivot(index="wd",columns="x",values="t_clus")
    # Thu->Sun (3d) by year and vr
    T=D[D.wd==3]
    res=[]
    for y,g in T.groupby("year"):
        b,t,n,nd=cslope(g,"z14","u3"); res.append([y,b,t,n])
    out["thu_z14_u3_by_year"]=pd.DataFrame(res,columns=["year","slope","t","n"])
    res=[]
    for lab,g in [("vr>1",T[T.vr>1]),("vr<=1",T[T.vr<=1])]:
        b,t,n,nd=cslope(g,"z14","u3"); res.append([lab,b,t,n])
    F=D[D.wd==4]
    for lab,g in [("fri vr>1",F[F.vr>1]),("fri vr<=1",F[F.vr<=1])]:
        b,t,n,nd=cslope(g,"z14","u2"); res.append([lab,b,t,n])
    out["slope_by_vr"]=pd.DataFrame(res,columns=["grp","slope","t","n"])
    # Thu next-day (Fri) vs Fri next day (Sat) vs Sat next day (Sun) separately
    # book concentration
    br=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dd=d[["day","book_return"]].copy(); dd["coin"]=coin; br.append(dd)
    B=pd.concat(br).dropna()
    daily=B.groupby("day").book_return.mean().sort_values()
    out["book_total_sum"]=float(daily.sum())
    out["book_sum_top5_days"]=float(daily.tail(5).sum())
    out["book_sum_bottom5_days"]=float(daily.head(5).sum())
    out["book_sum_excl_top5"]=float(daily.iloc[:-5].sum())
    out["book_top5_values"]=daily.tail(5).reset_index(drop=True)
    return out
