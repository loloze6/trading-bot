import numpy as np, pandas as pd
from scipy import stats

def tt(x):
    x=x.dropna()
    return x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan

def explore(data):
    rows=[]; bk=[]; dd=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            p2=c/c.shift(2)-1
            f2=c.shift(-2)/c-1
            f1=c.shift(-1)/c-1
            h2=c.shift(-2)/c.shift(-1)-1
            p24=c/c.shift(24)-1
            sc=p2.abs().rolling(500,min_periods=120).mean().shift(1)
            z=(p2/sc).clip(-20,20)
            hv=np.log(c).diff().rolling(168,min_periods=100).std()
            hvr=hv/hv.rolling(500,min_periods=120).median()
            lv=b["volume"].astype(float)
            vrel=lv/lv.rolling(168,min_periods=48).median()
            d=pd.DataFrame({"coin":coin,"w":w,"z":z,"f2":f2,"f1":f1,"h2":h2,"hour":ts.dt.hour,"wd":ts.dt.weekday,
                            "hvr":hvr,"vrel":vrel,"r1":c/c.shift(1)-1,"t24":p24/(hv*np.sqrt(24))})
            rows.append(d.iloc[::2])
            a=b["postRebalance_current_allocation"].astype(float)
            tpv=b["total_portfolio_value"].astype(float)
            fee=(tpv-b["postRebalance_total_value"].astype(float))/tpv
            turn=(a-b["previous_allocation"].astype(float)).abs()
            bk.append(pd.DataFrame({"gross":a*f1,"fee":fee,"turn":turn,"absalloc":a.abs()}))
            dy=data["days"][coin][w]
            dd.append(pd.DataFrame({"br":dy["book_return"].astype(float),"cr":dy["coin_return"].astype(float)}))
    D=pd.concat(rows,ignore_index=True).dropna(subset=["z","f2"])
    D["f2x"]=D["f2"]-D.groupby("coin")["f2"].transform("mean")
    D["fade"]=-np.sign(D["z"])*D["f2x"]
    D["fade1"]=-np.sign(D["z"])*D["f1"]
    D["fadeh2"]=-np.sign(D["z"])*D["h2"]
    out={}
    D["zq"]=pd.qcut(D["z"],10,labels=False,duplicates="drop")
    g=D.groupby("zq")
    out["by_z_decile"]=pd.DataFrame({"zmean":g["z"].mean(),"f2x_bp":g["f2x"].mean()*1e4,"t":g["f2x"].apply(tt),
                                    "fade_h1_bp":g["fade1"].mean()*1e4,"fade_h2_bp":g["fadeh2"].mean()*1e4,"n":g.size()})
    big=D["z"].abs()>=D["z"].abs().quantile(0.8)
    Db=D[big].copy()
    for col,nm in [("hour","hour"),("coin","coin"),("wd","wd")]:
        g=Db.groupby(col)
        out["fade_big_by_"+nm]=pd.DataFrame({"bp":g["fade"].mean()*1e4,"t":g["fade"].apply(tt),"n":g.size()})
    Db["hq"]=pd.qcut(Db["hvr"],5,labels=False,duplicates="drop")
    g=Db.dropna(subset=["hq"]).groupby("hq")
    out["fade_big_by_volratio_q"]=pd.DataFrame({"hvr":g["hvr"].mean(),"bp":g["fade"].mean()*1e4,"t":g["fade"].apply(tt),"n":g.size()})
    Db["vq"]=pd.qcut(Db["vrel"],5,labels=False,duplicates="drop")
    g=Db.dropna(subset=["vq"]).groupby("vq")
    out["fade_big_by_volume_q"]=pd.DataFrame({"vrel":g["vrel"].mean(),"bp":g["fade"].mean()*1e4,"t":g["fade"].apply(tt),"n":g.size()})
    # trend context: big move with or against 24h trend
    Db["with"]=np.sign(Db["z"])==np.sign(Db["t24"])
    Db["tq"]=pd.qcut(Db["t24"].abs(),4,labels=False,duplicates="drop")
    g=Db.dropna(subset=["tq"]).groupby(["with","tq"])
    out["fade_big_by_trend"]=pd.DataFrame({"bp":g["fade"].mean()*1e4,"t":g["fade"].apply(tt),"n":g.size()})
    B=pd.concat(bk,ignore_index=True)
    out["book_per_bar"]=pd.Series({"gross_bp":B["gross"].mean()*1e4,"fee_bp":B["fee"].mean()*1e4,"turnover":B["turn"].mean(),"abs_alloc":B["absalloc"].mean()})
    DD=pd.concat(dd,ignore_index=True).dropna()
    out["daily"]=pd.Series({"book_mean_bp":DD["br"].mean()*1e4,"coin_mean_bp":DD["cr"].mean()*1e4,"corr":DD["br"].corr(DD["cr"]),"n":len(DD)})
    g=D.groupby("hour")
    out["hour_ret_vol"]=pd.DataFrame({"r1_bp":g["r1"].mean()*1e4,"t":g["r1"].apply(tt),"vrel_med":g["vrel"].median()})
    return out
