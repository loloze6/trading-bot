def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(20,min_periods=15).std()
            r2=c/c.shift(2)-1
            sd2=sd*np.sqrt(2)
            df=pd.DataFrame({"coin":coin,"w":w,"year":ts.dt.year,"dow":ts.dt.dayofweek,
                             "z":r/sd,"zw":r2/sd2,"pos":np.arange(len(b))})
            for h in (1,2,3,4):
                df[f"f{h}"]=c.shift(-h)/c-1
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    for h in (1,2,3,4):
        m=d[d.pos%h==0].groupby("coin")[f"f{h}"].mean()
        d[f"x{h}"]=d[f"f{h}"]-d["coin"].map(m)
    def reg(s,x,y):
        s=s[[x,y]].dropna()
        if len(s)<10: return (np.nan,np.nan,len(s))
        res=stats.linregress(s[x],s[y]); return (res.slope,res.slope/res.stderr,len(s))
    out={}
    sun=d[d.dow==6]
    t=[]
    for h in (1,2,3,4):
        f=sun[sun.z<0][f"x{h}"].dropna(); ri=sun[sun.z>0][f"x{h}"].dropna()
        tf=f.mean()/(f.std()/np.sqrt(len(f))); tr=ri.mean()/(ri.std()/np.sqrt(len(ri)))
        tw=stats.ttest_ind(ri,f,equal_var=False).statistic
        t.append({"h":h,"fall_mean":f.mean(),"fall_t":tf,"rise_mean":ri.mean(),"rise_t":tr,"rise_minus_fall_t":tw,"nf":len(f),"nr":len(ri)})
    out["sunday side means"]=pd.DataFrame(t).round(4)
    # same for other weekdays: rise-minus-fall Welch at h=3
    t=[]
    for dw in range(7):
        s=d[d.dow==dw]; f=s[s.z<0]["x3"].dropna(); ri=s[s.z>0]["x3"].dropna()
        t.append({"dow":dw,"fall_x3":f.mean(),"rise_x3":ri.mean(),"welch_t":stats.ttest_ind(ri,f,equal_var=False).statistic,
                  "slope3_t":reg(s,"z","x3")[1],"weekend2d_slope3_t":reg(s,"zw","x3")[1]})
    out["by weekday h3"]=pd.DataFrame(t).round(4)
    rs=sun[sun.z>0].dropna(subset=["z","x3"]).copy(); rs["q"]=pd.qcut(rs.z,4,labels=False)
    out["sunday rises quartile"]=rs.groupby("q").agg(z=("z","mean"),x1=("x1","mean"),x2=("x2","mean"),x3=("x3","mean"),n=("x3","size")).round(4)
    t=[]
    for k,s in sun.groupby("year"):
        ri=s[s.z>0]["x3"].dropna(); t.append({"year":k,"slope3_t":reg(s,"z","x3")[1],"rise_x3":ri.mean(),"rise_t":ri.mean()/(ri.std()/np.sqrt(len(ri))),"zw_slope3_t":reg(s,"zw","x3")[1]})
    out["sunday by year h3"]=pd.DataFrame(t).round(3)
    t=[]
    for k,s in sun.groupby("coin"):
        ri=s[s.z>0]["x3"].dropna(); t.append({"coin":k,"rise_x3":ri.mean(),"rise_t":ri.mean()/(ri.std()/np.sqrt(len(ri))),"rise_slope3_t":reg(s[s.z>0],"z","x3")[1]})
    out["sunday rise by coin"]=pd.DataFrame(t).round(3)
    return out
