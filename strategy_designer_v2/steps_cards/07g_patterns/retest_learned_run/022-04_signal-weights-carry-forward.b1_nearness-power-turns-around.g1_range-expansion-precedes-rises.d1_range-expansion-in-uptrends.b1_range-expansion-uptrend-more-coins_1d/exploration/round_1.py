def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            if len(b)<40: continue
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            rng=(h-l)/c
            rr=rng/rng.rolling(30,min_periods=20).mean()
            ret20=c/c.shift(20)-1
            r1=c/c.shift(1)-1
            vol20=r1.rolling(20).std()
            volrel=vol20/r1.rolling(60,min_periods=40).std()
            hi30=c/h.rolling(30).max()-1
            clv=((c-l)/(h-l)).where(h>l)
            f5=c.shift(-5)/c-1
            idx=np.arange(0,len(b),5)
            d=pd.DataFrame({"coin":coin,"win":w,"rr":rr,"ret20":ret20,"r1":r1,"vol20":vol20,"volrel":volrel,
                            "hi30":hi30,"clv":clv,"f5":f5,"fc":b["forecast"],
                            "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                            "year":pd.to_datetime(b["timestamp"]).dt.year}).iloc[idx]
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["f5"])
    D["ex"]=D["f5"]-D.groupby("coin")["f5"].transform("mean")
    D["z1"]=D["r1"]/D["vol20"]
    out={}
    def qtab(df,col,q=5):
        x=df.dropna(subset=[col,"ex"]).copy()
        x["q"]=x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),q,labels=False) if s.notna().sum()>=q*3 else np.nan)
        g=x.groupby("q")["ex"]
        t=g.mean()/(g.std()/np.sqrt(g.count()))
        return pd.DataFrame({"n":g.count(),"mean_ex":g.mean(),"t":t})
    up=D[D.ret20>0]; dn=D[D.ret20<=0]
    out["rr_up"]=qtab(up,"rr"); out["rr_dn"]=qtab(dn,"rr")
    out["z1_up"]=qtab(up,"z1"); out["z1_dn"]=qtab(dn,"z1")
    out["clv_up"]=qtab(up,"clv"); out["clv_dn"]=qtab(dn,"clv")
    out["hi30_all"]=qtab(D,"hi30"); out["volrel_all"]=qtab(D,"volrel")
    out["ret20_all"]=qtab(D,"ret20")
    # wide range days split by direction of day
    x=up[up.rr>1.5]
    out["wide_up_by_daysign"]=x.groupby(x.r1>0)["ex"].agg(["count","mean"])
    x=dn[dn.rr>1.5]
    out["wide_dn_by_daysign"]=x.groupby(x.r1>0)["ex"].agg(["count","mean"])
    out["up_by_year"]=up.groupby("year")["ex"].agg(["count","mean"])
    # book days
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=coin; d["win"]=w; dd.append(d)
    DD=pd.concat(dd)
    DD["wd"]=pd.to_datetime(DD["day"]).dt.weekday
    out["book_by_wd"]=DD.groupby("wd")[["book_return","coin_return"]].mean()
    out["book_by_year"]=DD.groupby(pd.to_datetime(DD["day"]).dt.year)[["book_return","coin_return"]].mean()
    # trades
    tt=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values() if len(t)])
    tt["fq"]=pd.qcut(tt["entry_forecast"],5,labels=False,duplicates="drop")
    out["trades_by_entryfc"]=tt.groupby("fq")["net_profit_loss_percent"].agg(["count","mean","median"])
    out["trades_dur_days"]=tt["duration_minutes"].describe()/1440
    return out
