def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; allg={}
    for coin,wins in data["bars"].items():
        g1=[];g2=[];g3=[]
        for w,b in wins.items():
            c=pd.Series(b["close"].values)
            for h,L in ((1,g1),(2,g2),(3,g3)):
                s=c[::h]; L.extend(list((s.shift(-1)/s-1).dropna().values))
        allg[coin]=(np.mean(g1),np.mean(g2),np.mean(g3))
        for w,b in wins.items():
            b=b.reset_index(drop=True); c=pd.Series(b["close"].values)
            lr=c.pct_change(); vol=lr.rolling(20).std()
            ts=pd.to_datetime(b["timestamp"])
            wk=c/c.shift(2)-1
            vrel=pd.Series(b["volume"].values); vr=(vrel+vrel.shift(1))/ (vrel.rolling(30).mean()*2)
            for i in np.where(ts.dt.weekday.values==6)[0]:
                if i+3>=len(c) or np.isnan(vol[i]): continue
                rows.append(dict(coin=coin,z=lr[i]/vol[i],zw=wk[i]/vol[i],vol=vol[i],vr=vr[i],
                  ex1=c[i+1]/c[i]-1-allg[coin][0],ex2=c[i+2]/c[i]-1-allg[coin][1],ex3=c[i+3]/c[i]-1-allg[coin][2],
                  alloc=b["postRebalance_current_allocation"].iloc[i]))
    df=pd.DataFrame(rows).dropna(subset=["z","ex2"])
    out={}
    def s(x):
        return pd.Series({"n":len(x),"ex1":x.ex1.mean(),"ex2":x.ex2.mean(),"t_ex2":stats.ttest_1samp(x.ex2,0).statistic,"ex3":x.ex3.mean(),"alloc":x.alloc.mean()})
    df["zq"]=pd.qcut(df.z,6,labels=False)
    out["by sunday z sextile"]=df.groupby("zq").apply(s)
    df["vq"]=pd.qcut(df.vol,3,labels=False)
    df["side"]=np.where(df.z<0,"fall","rise")
    out["side x vol tercile"]=df.groupby(["side","vq"]).apply(s)
    r=[]
    for (sd,vq),x in df.groupby(["side","vq"]):
        sl=stats.linregress(x.z,x.ex2); r.append(dict(side=sd,vq=vq,slope=sl.slope,t=sl.slope/sl.stderr,n=len(x)))
    out["slope ex2 on z by side,vol"]=pd.DataFrame(r)
    sl=stats.linregress(df.z,df.ex2); out["slope all sundays z"]=pd.Series({"slope":sl.slope,"t":sl.slope/sl.stderr,"n":len(df)})
    d2=df.dropna(subset=["zw"]); sl=stats.linregress(d2.zw,d2.ex2); out["slope all weekend 2d z"]=pd.Series({"slope":sl.slope,"t":sl.slope/sl.stderr,"n":len(d2)})
    d3=df.dropna(subset=["vr"]).copy(); d3["vrq"]=pd.qcut(d3.vr,3,labels=False)
    r=[]
    for q,x in d3.groupby("vrq"):
        sl=stats.linregress(x.z,x.ex2); r.append(dict(vrq=q,slope=sl.slope,t=sl.slope/sl.stderr,n=len(x)))
    out["slope by weekend volume tercile"]=pd.DataFrame(r)
    D=pd.concat([d.assign(coin=c) for c,ws in data["days"].items() for d in ws.values()])
    br=D.book_return.dropna()
    out["book days"]=pd.Series({"share_days_nonzero":(br.abs()>1e-9).mean(),"mean_book":br.mean(),"mean_nonzero":br[br.abs()>1e-9].mean()})
    return out
