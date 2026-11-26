def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            sd=r1.rolling(20).std()
            sw=r1/sd
            tr=c/c.shift(60)-1
            vol30=r1.rolling(30).std()
            volrank=vol30.rolling(90,min_periods=60).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"sw":sw,"tr":tr,"vr":volrank,
                             "f3":c.shift(-3)/c-1,"f2":c.shift(-2)/c-1,"f1":c.shift(-1)/c-1,"f5":c.shift(-5)/c-1,
                             "day":ts.dt.strftime("%Y-%m-%d"),"yr":ts.dt.year,"wd":ts.dt.weekday,"pos":np.arange(len(b))})
            rows.append(df)
    d=pd.concat(rows)
    g=d[(d.pos%3==0)&d.f3.notna()].copy()
    drift=g.groupby("coin").f3.mean()
    g["ex"]=g.f3-g.coin.map(drift)
    def agg(x,col="ex"):
        x=x.dropna(subset=[col]); n=len(x)
        if n<2: return pd.Series({"n":n,"mean":x[col].mean() if n else np.nan,"t_day":np.nan,"days":n})
        m=x[col].mean()
        se=np.sqrt(((x[col]-m).groupby(x.day).sum()**2).sum())/n
        return pd.Series({"n":n,"mean":m,"t_day":m/se if se else np.nan,"days":x.day.nunique()})
    out={}
    fall=g[g.tr<-0.1].copy()
    rise=g[g.tr>0.1].copy()
    # fall, up days: graded?
    fu=fall[fall.sw>0].copy()
    fu["b"]=pd.cut(fu.sw,[0,0.5,1,1.5,2,3,99])
    out["fall_up_fine"]=fu.groupby("b").apply(agg)
    out["fall_up_corr_sw_ex"]=float(fu[["sw","ex"]].corr().iloc[0,1])
    f12=fall[(fall.sw>1)&(fall.sw<=2)]
    out["fall_1to2_by_coin"]=f12.groupby("coin").apply(agg)
    out["fall_1to2_by_year"]=f12.groupby("yr").apply(agg)
    # horizons
    hz={}
    for h in ["f1","f2","f3","f5"]:
        dd=g.groupby("coin")[h].mean()
        x=f12.copy(); x["e"]=x[h]-x.coin.map(dd)
        hz[h]=agg(x,"e")
    out["fall_1to2_horizons"]=pd.DataFrame(hz).T
    # all up days in fall, sw>1, by calm proxy
    f1p=fall[fall.sw>1].copy()
    f1p["calm"]=np.where(f1p.vr<=0.5,"calm","agit")
    out["fall_sw_gt1_by_calm"]=f1p.groupby("calm").apply(agg)
    # rising: down days rebound
    rd=rise[rise.sw<0].copy()
    rd["b"]=pd.cut(rd.sw,[-99,-2,-1.5,-1,-0.5,0])
    out["rise_down_fine"]=rd.groupby("b").apply(agg)
    out["rise_down_corr_sw_ex"]=float(rd[["sw","ex"]].corr().iloc[0,1])
    r21=rise[(rise.sw>-2)&(rise.sw<=-1)]
    out["rise_m2m1_by_coin"]=r21.groupby("coin").apply(agg)
    out["rise_m2m1_by_year"]=r21.groupby("yr").apply(agg)
    # weekday all
    out["weekday_all"]=g.groupby("wd").apply(agg)
    return out
