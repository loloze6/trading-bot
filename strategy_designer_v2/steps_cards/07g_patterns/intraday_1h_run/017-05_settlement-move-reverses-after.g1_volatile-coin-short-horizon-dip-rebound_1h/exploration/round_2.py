import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out={}
    recs={2:[],8:[],24:[]}
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            s=b["close"].astype(float)
            r1=s.pct_change()
            sd=r1.rolling(168).std()
            mam=r1.abs().rolling(168).mean()
            vr=mam.rolling(720,min_periods=200).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            wd=pd.to_datetime(b["timestamp"]).dt.weekday
            for h in [2,8,24]:
                past=s/s.shift(h)-1
                z=past/(sd*np.sqrt(h))
                f=s.shift(-h)/s-1
                df=pd.DataFrame({"coin":coin,"w":w,"z":z,"vr":vr,"f":f,"wd":wd,"sd":sd}).iloc[::h]
                recs[h].append(df)
    for h in [2,8,24]:
        d=pd.concat(recs[h]).dropna()
        d["f"]=d["f"]-d.groupby("coin")["f"].transform("mean")
        d["hi"]=d["vr"]>=0.5
        d["fall"]=(-d["z"]).clip(lower=0); d["rise"]=d["z"].clip(lower=0)
        def sl(x,col):
            r=stats.linregress(x[col],x["f"]); return pd.Series({"slope_bp":r.slope*1e4,"t":r.slope/r.stderr,"n":len(x)})
        out[f"h{h} fall slope by coin x hi"]=d.groupby(["coin","hi"]).apply(sl,"fall").round(2).unstack(1)
        out[f"h{h} rise slope by coin x hi"]=d.groupby(["coin","hi"]).apply(sl,"rise").round(2).unstack(1)
        dh=d[d.hi].copy()
        dh["zq"]=pd.qcut(dh["z"],10,labels=False)
        g=dh.groupby("zq")["f"]
        out[f"h{h} hi: excess bp by z decile"]=pd.DataFrame({"bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()}).round(2)
        # vol-normalised: forward return in units of sd
        dh["fn"]=dh["f"]/(dh["sd"]*np.sqrt(h))
        out[f"h{h} hi: fall slope on fn by sd tercile"]=dh.assign(sq=pd.qcut(dh["sd"],3,labels=False)).groupby("sq").apply(lambda x:pd.Series({"slope":stats.linregress(x["fall"],x["fn"]).slope,"t":stats.linregress(x["fall"],x["fn"]).slope/stats.linregress(x["fall"],x["fn"]).stderr,"mean_sd_bp":x["sd"].mean()*1e4})).round(3)
        if h==24:
            out["h24 hi fall slope by weekday"]=dh.groupby("wd").apply(sl,"fall").round(2)
    # trades
    tr=pd.concat([t for ws in data["trades"].values() for t in ws.values()])
    out["trades"]=pd.Series({"n":len(tr),"mean_gross_pct":tr["profit_loss_percent"].mean(),"mean_net_pct":tr["net_profit_loss_percent"].mean(),
                             "med_dur_h":tr["duration_minutes"].median()/60}).round(4)
    return out
