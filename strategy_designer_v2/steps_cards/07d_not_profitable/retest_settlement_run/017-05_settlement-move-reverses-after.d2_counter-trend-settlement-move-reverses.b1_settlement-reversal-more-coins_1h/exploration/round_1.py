def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"].astype(float)
            nh=(ts+pd.Timedelta(hours=1)).dt.hour
            r1=c.pct_change()
            vol=r1.rolling(240,min_periods=100).std()
            r2=c/c.shift(2)-1; r24=c/c.shift(24)-1
            vrel=b["volume"]/b["volume"].rolling(240,min_periods=100).mean()
            d=pd.DataFrame({"coin":coin,"w":w,"nh":nh,"yr":ts.dt.year,"r2":r2,"r24":r24,"vol":vol,"vrel":vrel,
                            "fc":b["forecast"]})
            for h in (1,2,4,8,16,24):
                d[f"f{h}"]=c.shift(-h)/c-1
            # keep only bars every 4h positions-by-clock (next hour multiple of 4) to limit size
            d=d[d.nh%4==0]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    # drift per coin per h (on all these bars)
    out={}
    for h in (1,2,4,8,16,24):
        D[f"d{h}"]=D[f"f{h}"]-D.groupby("coin")[f"f{h}"].transform("mean")
    D["sgn"]=np.sign(D["r24"])
    D["against"]=(D.r2*D.r24<0)
    D["settle"]=D.nh.isin([0,8,16])
    D["z24"]=D.r24.abs()/(D.vol*np.sqrt(24))
    D["z2"]=D.r2.abs()/(D.vol*np.sqrt(2))
    def summ(g,h=8):
        x=(g["sgn"]*g[f"d{h}"]).dropna()
        return pd.Series({"n":len(x),"mean_pct":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    A=D[D.settle&D.against]
    hz=pd.DataFrame({f"h{h}":summ(A,h) for h in (1,2,4,8,16,24)}).T
    out["settle_against_by_horizon_trenddir"]=hz
    B=D[(~D.settle)&D.against]
    out["nonsettle_against_by_horizon"]=pd.DataFrame({f"h{h}":summ(B,h) for h in (1,2,4,8,16,24)}).T
    out["settle_against_by_nexthour_h8"]=D[D.against].groupby("nh").apply(summ)
    A=A.copy()
    A["q24"]=pd.qcut(A.z24,5,labels=False,duplicates="drop")
    A["q2"]=pd.qcut(A.z2,5,labels=False,duplicates="drop")
    out["settle_by_trend_strength_q_h8"]=A.groupby("q24").apply(summ)
    out["settle_by_premove_size_q_h8"]=A.groupby("q2").apply(summ)
    out["settle_by_premove_size_q_h24"]=A.groupby("q2").apply(lambda g: summ(g,24))
    out["settle_by_side_h8"]=A.groupby("sgn").apply(summ)
    out["settle_by_year_h8"]=A.groupby("yr").apply(summ)
    A["qv"]=pd.qcut(A.vrel,5,labels=False,duplicates="drop")
    out["settle_by_volume_q_h8"]=A.groupby("qv").apply(summ)
    # strong both: top quintile premove and top trend
    S=A[(A.q2>=3)&(A.q24>=3)]
    out["settle_strong_both"]=pd.DataFrame({f"h{h}":summ(S,h) for h in (4,8,16,24)}).T
    Bn=B.copy(); Bn["q2"]=pd.qcut(Bn.z2,5,labels=False,duplicates="drop")
    out["nonsettle_by_premove_q_h8"]=Bn.groupby("q2").apply(summ)
    # premove reversal sign independent of trend: all settle bars, sign=-r2
    E=D[D.settle].copy(); E["sgn"]=-np.sign(E.r2); E["q2"]=pd.qcut(E.z2,5,labels=False,duplicates="drop")
    out["settle_all_revert_premove_by_q2_h8"]=E.groupby("q2").apply(summ)
    # book
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            dd.append(x.assign(coin=coin,w=w))
    DD=pd.concat(dd); DD["yr"]=pd.to_datetime(DD.day).dt.year
    out["book_by_year"]=DD.groupby("yr").agg(book=("book_return","mean"),coin=("coin_return","mean"))
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items(): tr.append(t)
    T=pd.concat(tr)
    out["trades"]=pd.Series({"n":len(T),"gross_mean_pct":T.profit_loss_percent.mean(),"net_mean_pct":T.net_profit_loss_percent.mean(),
                             "dur_h_median":T.duration_minutes.median()/60})
    return out
