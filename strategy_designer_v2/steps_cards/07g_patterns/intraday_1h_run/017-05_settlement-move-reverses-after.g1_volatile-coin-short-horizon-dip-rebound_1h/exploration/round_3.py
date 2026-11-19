import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out={}
    recs=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            s=b["close"].astype(float)
            r1=s.pct_change()
            sd=r1.rolling(168).std()
            mam=r1.abs().rolling(168).mean()
            vr=mam.rolling(720,min_periods=200).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            yr=pd.to_datetime(b["timestamp"]).dt.year
            past=s/s.shift(24)-1
            z=past/(sd*np.sqrt(24))
            df=pd.DataFrame({"coin":coin,"w":w,"z":z,"vr":vr,"sd":sd,"yr":yr,
                             "f24":s.shift(-24)/s-1,"f48":s.shift(-48)/s-1,"f72":s.shift(-72)/s-1,
                             "f6":s.shift(-6)/s-1}).iloc[::72]
            recs.append(df)
    d=pd.concat(recs).dropna()
    for c in ["f6","f24","f48","f72"]:
        d[c]=d[c]-d.groupby("coin")[c].transform("mean")
    d["fall"]=(-d["z"]).clip(lower=0); d["rise"]=d["z"].clip(lower=0)
    d["sdq"]=d.groupby("coin")["sd"].transform(lambda x:pd.qcut(x,3,labels=False))
    def sl(x,col,y):
        r=stats.linregress(x[col],x[y]); return pd.Series({"slope_bp":r.slope*1e4,"t":r.slope/r.stderr,"n":len(x)})
    res={}
    for y in ["f6","f24","f48","f72"]:
        res[y+" fall"]=d.groupby("sdq").apply(sl,"fall",y)["t"]
        res[y+" rise"]=d.groupby("sdq").apply(sl,"rise",y)["t"]
    out["t of slope by own-sd tercile (72h grid)"]=pd.DataFrame(res).round(2)
    top=d[d.sdq==2]
    out["top sd tercile, f24 fall slope by year"]=top.groupby("yr").apply(sl,"fall","f24").round(2)
    out["top sd tercile, f24 rise slope by year"]=top.groupby("yr").apply(sl,"rise","f24").round(2)
    out["top sd tercile, f24 fall slope by coin"]=top.groupby("coin").apply(sl,"fall","f24").round(2)
    top=top.copy(); top["zq"]=pd.qcut(top["z"],5,labels=False)
    g=top.groupby("zq")["f24"]
    out["top sd tercile f24 bp by z quintile"]=pd.DataFrame({"bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()}).round(2)
    return out
