def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float).values
            ts=pd.to_datetime(b["timestamp"])
            ch=((ts.dt.hour+1)%24).values
            n=len(c)
            def fwd(h):
                r=np.full(n,np.nan); r[:n-h]=c[h:]/c[:n-h]-1; return r
            def back(h):
                r=np.full(n,np.nan); r[h:]=c[h:]/c[:n-h]-1; return r
            r1=np.r_[np.nan,np.diff(np.log(c))]
            vol=pd.Series(r1).rolling(720,min_periods=168).std().values
            pos=np.arange(n)
            df=pd.DataFrame({"coin":coin,"w":w,"yr":ts.dt.year.values,"ch":ch,"pos":pos,
              "f2":fwd(2),"f24":fwd(24),"f48":fwd(48),"f72":fwd(72),
              "b2":back(2),"b24":back(24),"b72":back(72),"vol":vol})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    out={}
    def summ(g):
        m=g.mean(); s=g.std(); k=g.count()
        return pd.DataFrame({"mean_bp":m*1e4,"t":m/(s/np.sqrt(k)),"n":k}).round(2)
    # 24h reversal, 24h grid from window start, z = b24/(vol*sqrt24)
    d=D[(D.pos%24==0)].copy()
    d["z"]=d.b24/(d.vol*np.sqrt(24))
    d["rev24"]=-np.sign(d.b24)*d.f24
    d["zq"]=d.groupby("coin")["z"].transform(lambda x:pd.qcut(x.abs(),5,labels=False,duplicates="drop"))
    out["rev24_by_absz_quintile"]=summ(d.groupby("zq")["rev24"])
    top=d[d.zq==4]
    out["rev24_top_by_coin"]=summ(top.groupby("coin")["rev24"])
    out["rev24_top_by_year"]=summ(top.groupby("yr")["rev24"])
    out["rev24_top_by_direction"]=summ(top.groupby(np.sign(top.b24))["rev24"])
    out["corr_z_f24_strength"]=float(np.corrcoef(d.dropna(subset=["z","f24"]).z,d.dropna(subset=["z","f24"]).f24)[0,1])
    d["usual24"]=d.groupby("coin")["f24"].transform("std")
    d["drift24"]=d.groupby("coin")["f24"].transform("mean")
    top=d[d.zq==4]
    out["rev24_top_strength"]=float(((-np.sign(top.b24)*(top.f24-top.drift24))/top.usual24).mean())
    # 48h grid, 48h horizon
    e=D[(D.pos%48==0)].copy(); e["z"]=e.b24/(e.vol*np.sqrt(24)); e["rev48"]=-np.sign(e.b24)*e.f48
    e["zq"]=e.groupby("coin")["z"].transform(lambda x:pd.qcut(x.abs(),5,labels=False,duplicates="drop"))
    out["rev48_after24_by_absz_q"]=summ(e.groupby("zq")["rev48"])
    # 72h move -> next 72h
    f=D[(D.pos%72==0)].copy(); f["z"]=f.b72/(f.vol*np.sqrt(72)); f["rev72"]=-np.sign(f.b72)*f.f72
    f["zq"]=f.groupby("coin")["z"].transform(lambda x:pd.qcut(x.abs(),5,labels=False,duplicates="drop"))
    out["rev72_by_absz_q"]=summ(f.groupby("zq")["rev72"])
    # 2h reversal top decile z, by coin and by year
    g=D[D.pos%2==0].copy(); g["z"]=g.b2/(g.vol*np.sqrt(2)); g["rev2"]=-np.sign(g.b2)*g.f2
    g["zq"]=g.groupby("coin")["z"].transform(lambda x:pd.qcut(x.abs(),10,labels=False,duplicates="drop"))
    out["rev2_by_absz_decile"]=summ(g.groupby("zq")["rev2"])
    t9=g[g.zq==9]
    out["rev2_topdecile_by_year"]=summ(t9.groupby("yr")["rev2"])
    # hour 21-22 close drift by year (2h fwd from close hour 21)
    h=D[(D.ch==21)]
    out["f2_from_close21_by_year"]=summ(h.groupby("yr")["f2"])
    return out
