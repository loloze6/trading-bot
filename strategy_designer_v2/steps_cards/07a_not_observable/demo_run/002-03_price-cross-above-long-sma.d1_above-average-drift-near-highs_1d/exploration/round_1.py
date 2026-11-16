import pandas as pd, numpy as np
def explore(data):
    rows=[]
    for c,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            cl=b["close"].values; f=b["forecast"].values
            n=len(b)
            for i in range(0,n-20,20):
                r=cl[i+20]/cl[i]-1
                rows.append(dict(coin=c,window=w,year=pd.Timestamp(b["timestamp"].iloc[i]).year,n=n,f=f[i],r=r,trend=b["regime"].iloc[i]=="trending"))
    d=pd.DataFrame(rows)
    d["dm"]=d["r"]-d.groupby("coin")["r"].transform("mean")
    d["pos"]=d["f"]>0
    wl=d.groupby(["coin","window"])["n"].first()
    byc=d.groupby("coin").agg(cases=("r","size"),pos=("pos","sum"),trend=("trend","sum"),sd=("dm","std"))
    byy=d.groupby("year").agg(cases=("r","size"),pos=("pos","sum"),trend=("trend","sum"))
    byw=d.groupby("window").agg(cases=("r","size"),pos=("pos","sum"),barsmean=("n","mean"))
    sl=np.polyfit(d.f,d.dm,1)
    return {"by coin":byc,"by year":byy,"by window":byw,
            "window length stats":wl.describe(),
            "total":len(d),"pos":int(d.pos.sum()),
            "forecast desc pos":d.loc[d.pos,"f"].describe(),
            "dm sd":d.dm.std(),"slope":sl[0],
            "share trending all bars":float(np.mean([ (b["regime"]=="trending").mean() for ws in data["bars"].values() for b in ws.values()]))}
