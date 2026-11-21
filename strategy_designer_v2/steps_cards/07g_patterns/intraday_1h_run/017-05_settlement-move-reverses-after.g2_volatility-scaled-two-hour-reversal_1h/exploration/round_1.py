import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]; bk=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            p2=c/c.shift(2)-1
            f2=c.shift(-2)/c-1
            f1=c.shift(-1)/c-1
            sc=p2.abs().rolling(500,min_periods=120).mean().shift(1)
            z=(p2/sc).clip(-20,20)
            hv=np.log(c).diff().rolling(168,min_periods=100).std()
            hvr=hv/hv.rolling(500,min_periods=120).median()
            lv=b["volume"].astype(float)
            vrel=lv/lv.rolling(168,min_periods=48).median()
            d=pd.DataFrame({"coin":coin,"w":w,"z":z,"f2":f2,"f1":f1,"hour":ts.dt.hour,"wd":ts.dt.weekday,"hvr":hvr,"vrel":vrel.shift(0),"r1":c/c.shift(1)-1})
            d=d.iloc[::2]
            rows.append(d)
            # book decomposition
            a=b["postRebalance_current_allocation"].astype(float)
            gross=a*f1
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            turn=(a-b["previous_allocation"].astype(float)).abs()
            bk.append(pd.DataFrame({"gross":gross,"fee":fee,"turn":turn}))
    D=pd.concat(rows).dropna(subset=["z","f2"])
    D["f2x"]=D["f2"]-D.groupby("coin")["f2"].transform("mean")
    D["fade"]=-np.sign(D["z"])*D["f2x"]
    out={}
    D["zq"]=pd.qcut(D["z"],10,labels=False,duplicates="drop")
    g=D.groupby("zq")
    out["by_z_decile"]=pd.DataFrame({"zmean":g["z"].mean(),"f2x_bp":g["f2x"].mean()*1e4,"t":g["f2x"].apply(lambda x:x.mean()/x.std()*np.sqrt(len(x))),"n":g.size()})
    def tt(x): return x.mean()/x.std()*np.sqrt(len(x))
    Dbig=D[D["z"].abs()>=D["z"].abs().quantile(0.8)]
    g=Dbig.groupby("hour")
    out["fade_big_by_hour"]=pd.DataFrame({"bp":g["fade"].mean()*1e4,"t":g["fade"].apply(tt),"n":g.size()})
    D["hq"]=pd.qcut(D["hvr"],5,labels=False,duplicates="drop")
    g=D.dropna(subset=["hq"]).groupby("hq")
    out["fade_by_volratio_q_all"]=pd.DataFrame({"bp":g["fade"].mean()*1e4,"t":g["fade"].apply(tt),"n":g.size()})
    g=Dbig.assign(hq=D["hq"]).dropna(subset=["hq"]).groupby("hq")
    out["fade_big_by_volratio_q"]=pd.DataFrame({"bp":g["fade"].mean()*1e4,"t":g["fade"].apply(tt),"n":g.size()})
    D["vq"]=pd.qcut(D["vrel"],5,labels=False,duplicates="drop")
    g=Dbig.assign(vq=D["vq"]).dropna(subset=["vq"]).groupby("vq")
    out["fade_big_by_volume_q"]=pd.DataFrame({"bp":g["fade"].mean()*1e4,"t":g["fade"].apply(tt),"n":g.size()})
    g=Dbig.groupby("coin")
    out["fade_big_by_coin"]=pd.DataFrame({"bp":g["fade"].mean()*1e4,"t":g["fade"].apply(tt),"n":g.size()})
    g=Dbig.groupby("wd")
    out["fade_big_by_wd"]=pd.DataFrame({"bp":g["fade"].mean()*1e4,"t":g["fade"].apply(tt),"n":g.size()})
    B=pd.concat(bk)
    out["book_per_bar_bp"]=pd.DataFrame({"mean_bp":[B["gross"].mean()*1e4,B["fee"].mean()*1e4,B["turn"].mean()]},index=["gross","fee","turnover"])
    # hourly return/volume pattern (all bars? grid only ok)
    g=D.groupby("hour")
    out["hour_ret_vol"]=pd.DataFrame({"r1_bp":g["r1"].mean()*1e4,"t":g["r1"].apply(tt),"vrel":g["vrel"].median()})
    return out
