def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; days=data["days"]
    rows=[]; sat=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]); cl=pd.Series(b["close"].values); n=len(b)
            endt=ts+pd.Timedelta(hours=1)
            lr=np.log(cl).diff()
            vol30=lr.rolling(720,min_periods=300).std().values*np.sqrt(48)
            r48=cl.pct_change(48).values; r24=cl.pct_change(24).values; r72=cl.pct_change(72).values
            r168=cl.pct_change(168).values; r720=cl.pct_change(720).values
            clv=cl.values
            fri=np.where((endt.dt.weekday==4)&(endt.dt.hour==0))[0]
            for i in fri:
                if i<48 or i+48>=n: continue
                rows.append({"coin":c,"win":w,"year":endt.iat[i].year,"past48":r48[i],"vol":vol30[i],
                    "r720":r720[i],"r168":r168[i],"f48":clv[i+48]/clv[i]-1,"f24":clv[i+24]/clv[i]-1,
                    "sat":clv[i+48]/clv[i+24]-1,"z":r48[i]/vol30[i] if vol30[i]>0 else np.nan})
            sa=np.where((endt.dt.weekday==5)&(endt.dt.hour==0))[0]
            for i in sa:
                if i<72 or i+24>=n: continue
                sat.append({"coin":c,"past72":r72[i],"past24":r24[i],"past48pre":clv[i-24]/clv[i-72]-1,"f24":clv[i+24]/clv[i]-1,"vol":vol30[i]})
    d=pd.DataFrame(rows).dropna(); s=pd.DataFrame(sat).dropna()
    out={}
    def reg(g,x,y):
        r=stats.linregress(g[x],g[y]); return {"slope":r.slope,"t":r.slope/r.stderr,"n":len(g)}
    out["fri_slopes"]=pd.DataFrame({k:reg(d,x,y) for k,(x,y) in {"p48->f24":("past48","f24"),"p48->sat":("past48","sat"),"p48->f48":("past48","f48"),"z->f48":("z","f48"),"r168->f48":("r168","f48"),"r720->f48":("r720","f48")}.items()}).T
    out["sat_slopes"]=pd.DataFrame({k:reg(s,x,"f24") for k,x in {"p72":"past72","p24":"past24","p48pre":"past48pre"}.items()}).T
    p=d[d.past48>0].copy()
    p["volq"]=pd.qcut(p["vol"],3,labels=False)
    out["pos_by_volq"]=p.groupby("volq").apply(lambda g: pd.Series({"vol":g.vol.mean(),"past48":g.past48.mean(),"f48":g.f48.mean(),"sat":g.sat.mean(),"n":len(g),**{"t_slope":reg(g,"past48","f48")["t"]}}))
    p["trend"]=p["r720"]>0
    out["pos_by_30d_trend"]=p.groupby("trend").apply(lambda g: pd.Series({"f48":g.f48.mean(),"n":len(g),"t_slope":reg(g,"past48","f48")["t"]}))
    out["pos_by_year"]=p.groupby("year").apply(lambda g: pd.Series({"f48":g.f48.mean(),"n":len(g)}))
    # book daily by weekday
    bd=[]
    for c in days:
        for w,dd in days[c].items():
            x=dd.copy(); x["wd"]=pd.to_datetime(x["day"]).dt.weekday; bd.append(x)
    bd=pd.concat(bd)
    out["book_by_weekday"]=bd.groupby("wd")[["book_return","coin_return"]].mean()
    return out
