import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,wins in data["bars"].items():
        cm=pd.concat([b["close"].pct_change() for b in wins.values()]).mean()
        for w,b in wins.items():
            ts=pd.to_datetime(b["timestamp"])
            c=b["close"]
            r=c.pct_change()
            vol=r.rolling(20).std()
            z=r/vol
            r1=c.shift(-1)/c-1
            r2=c.shift(-2)/c-1
            rv=b["volume"]/b["volume"].rolling(20).median()
            volrank=vol/vol.rolling(60,min_periods=20).median()
            mom20=c/c.shift(20)-1
            d=pd.DataFrame({"coin":coin,"win":w,"date":ts.dt.normalize(),"wd":ts.dt.weekday,"year":ts.dt.year,
                "z":z,"r1x":r1-cm,"r2x":r2-2*cm,"rv":rv,"volrank":volrank,"mom":mom20})
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["z","r1x"])
    D["cont"]=D["z"]*D["r1x"]
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out={}
    # date-clustered: average across coins per date, then t across dates
    dl=D.groupby(["date","wd"])["cont"].mean().reset_index()
    out["cont_dateclustered_by_wd"]=dl.groupby("wd")["cont"].apply(tt).unstack()
    fr=D[D.wd==4].copy()
    out["fri_cont_by_year"]=fr.groupby("year")["cont"].apply(tt).unstack()
    fr["rvq"]=pd.qcut(fr["rv"],3,labels=["lowv","mid","highv"])
    out["fri_cont_by_relvolume"]=fr.groupby("rvq")["cont"].apply(tt).unstack()
    fr["vq"]=pd.qcut(fr["volrank"],3,labels=["calm","mid","wild"])
    out["fri_cont_by_volregime"]=fr.groupby("vq")["cont"].apply(tt).unstack()
    fr["zq"]=pd.cut(fr["z"],[-99,-2,-1,0,1,2,99])
    out["fri_next_by_zbin"]=fr.groupby("zq")["r1x"].apply(tt).unstack()
    out["fri_cont_by_coin"]=fr.groupby("coin")["cont"].apply(tt).unstack()
    fr["cont2"]=fr["z"]*fr["r2x"]
    out["fri_cont_2day"]=tt(fr["cont2"])
    # weekend fade by rel volume, date clustered
    we=D[D.wd.isin([5,6])].copy()
    we["rvq"]=pd.qcut(we["rv"],3,labels=["lowv","mid","highv"])
    out["we_fade_relvol_clustered"]=we.groupby(["rvq","date"])["cont"].mean().groupby("rvq").apply(lambda x: tt(-x)).unstack()
    # graded: weekend fade slope on rv-weighted z
    s=stats.linregress(we["z"]*we["rv"].clip(upper=5),we["r1x"])
    out["we_slope_z_times_rv"]=pd.Series({"slope":s.slope,"t":s.slope/s.stderr})
    s=stats.linregress(we["z"],we["r1x"])
    out["we_slope_z"]=pd.Series({"slope":s.slope,"t":s.slope/s.stderr})
    # weekend fade by trend regime
    we["mq"]=pd.qcut(we["mom"],3,labels=["down","flat","up"])
    out["we_fade_by_mom"]=we.groupby("mq")["cont"].apply(lambda x: tt(-x)).unstack()
    fr["mq"]=pd.qcut(fr["mom"],3,labels=["down","flat","up"])
    out["fri_cont_by_mom"]=fr.groupby("mq")["cont"].apply(tt).unstack()
    return out
