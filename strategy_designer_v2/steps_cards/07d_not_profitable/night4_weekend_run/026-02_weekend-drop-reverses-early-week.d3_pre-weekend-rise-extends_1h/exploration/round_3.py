def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]
    rows=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]); cl=pd.Series(b["close"].values); n=len(b)
            endt=ts+pd.Timedelta(hours=1); clv=cl.values
            r48=cl.pct_change(48).values; r168=cl.pct_change(168).values; r720=cl.pct_change(720).values
            lr=np.log(cl).diff(); vol=lr.rolling(720,min_periods=300).std().values*np.sqrt(48)
            idx=np.where(endt.dt.hour==0)[0]
            for i in idx:
                if i+48>=n: continue
                rows.append({"coin":c,"wd":int(endt.iat[i].weekday()),"r48":r48[i],"r168":r168[i],"r720":r720[i],
                             "vol":vol[i],"f48":clv[i+48]/clv[i]-1,"f24":clv[i+24]/clv[i]-1,"s24":clv[i+48]/clv[i+24]-1})
    d=pd.DataFrame(rows).dropna()
    def reg(g,x,y):
        r=stats.linregress(g[x],g[y]); return r.slope/r.stderr
    out={}
    # non-overlapping per weekday (one 48h case per week per weekday)
    out["by_wd_t"]=d.groupby("wd").apply(lambda g: pd.Series({"t_r720_f48":reg(g,"r720","f48"),"t_r168_f48":reg(g,"r168","f48"),
        "t_r720_f24":reg(g,"r720","f24"),"f48_up30":g[g.r720>0].f48.mean(),"f48_dn30":g[g.r720<=0].f48.mean(),"n":len(g)}))
    f=d[d.wd==4].copy()
    f["z720"]=f.r720/(f.vol*np.sqrt(15))
    f["q"]=pd.qcut(f["r720"],5,labels=False)
    out["fri_by_r720_quintile"]=f.groupby("q").agg(r720=("r720","mean"),f48=("f48","mean"),f24=("f24","mean"),s24=("s24","mean"),n=("f48","size"))
    f["both"]=(f.r48>0)&(f.r720>0)
    out["fri_both"]=f.groupby("both").agg(f48=("f48","mean"),s24=("s24","mean"),n=("f48","size"))
    m=f[f.r720>0]
    out["fri_up30_slopes"]=pd.Series({"t_r48_f48":reg(m,"r48","f48"),"t_r48_s24":reg(m,"r48","s24"),"t_r720_f48":reg(m,"r720","f48"),"n":len(m)})
    return out
