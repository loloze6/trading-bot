import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,wins in data["bars"].items():
        allr=[]
        for w,b in wins.items():
            allr.append(b["close"].pct_change())
        cm=pd.concat(allr).mean()
        for w,b in wins.items():
            b=b.copy()
            ts=pd.to_datetime(b["timestamp"])
            r=b["close"].pct_change()
            vol=r.rolling(20).std()
            z=r/vol
            r1=b["close"].shift(-1)/b["close"]-1
            r3=b["close"].shift(-3)/b["close"]-1
            rv=b["volume"]/b["volume"].rolling(20).median()
            volrank=vol/vol.rolling(60,min_periods=20).median()
            pos=b["postRebalance_current_allocation"]
            d=pd.DataFrame({"coin":coin,"win":w,"wd":ts.dt.weekday,"year":ts.dt.year,
                "z":z,"r1x":r1-cm,"r3x":r3-3*cm,"rv":rv,"volrank":volrank,"pos":pos,"r1":r1,"cm":cm})
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["z","r1x"])
    D["fade"]=-D["z"]*D["r1x"]
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out={}
    out["fade_by_weekday"]=D.groupby("wd")["fade"].apply(tt).unstack()
    # slope of next return on z by weekday
    def slope(g):
        s=stats.linregress(g["z"],g["r1x"]); return pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(g)})
    out["slope_by_weekday"]=D.groupby("wd").apply(slope)
    wk=D[D.wd.isin([5,6])]; wkd=D[~D.wd.isin([5,6])]
    out["wkend_fade_by_year"]=wk.groupby("year")["fade"].apply(tt).unstack()
    out["wkday_fade_by_year"]=wkd.groupby("year")["fade"].apply(tt).unstack()
    wk=wk.copy(); wk["rvq"]=pd.qcut(wk["rv"],3,labels=["lowvol","mid","high"])
    out["wkend_fade_by_relvolume"]=wk.groupby("rvq")["fade"].apply(tt).unstack()
    D["vq"]=pd.qcut(D["volrank"],3,labels=["calm","mid","wild"])
    D["we"]=D.wd.isin([5,6])
    out["fade_by_volregime_we"]=D.groupby(["vq","we"])["fade"].apply(tt).unstack()
    D["zq"]=pd.cut(D["z"],[-99,-2,-1,0,1,2,99])
    out["next_ret_by_zbin_we"]=D.groupby(["we","zq"])["r1x"].apply(tt).unstack()
    out["fade_by_coin_we"]=D[D.we].groupby("coin")["fade"].apply(tt).unstack()
    # book daily
    dd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; dd.append(d)
    B=pd.concat(dd); B["wd"]=pd.to_datetime(B["day"]).dt.weekday
    out["book_ret_by_weekday"]=B.groupby("wd")["book_return"].apply(tt).unstack()
    out["coin_ret_by_weekday"]=B.groupby("wd")["coin_return"].apply(tt).unstack()
    return out
