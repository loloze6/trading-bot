import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]; book=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(c)
            r1=pd.Series(c).pct_change()
            sd=r1.rolling(168).std()
            mam=r1.abs().rolling(168).mean()
            vr=mam.rolling(720,min_periods=200).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            r2=pd.Series(c).pct_change(2)
            z=r2/(sd*np.sqrt(2))
            def fwd(a,h): 
                s=pd.Series(c); return s.shift(-(a+h))/s.shift(-a)-1
            hrs=pd.to_datetime(b["timestamp"]).dt.hour
            vol=b["volume"]; vz=vol/vol.rolling(168).mean()
            df=pd.DataFrame({"coin":coin,"w":w,"z":z,"vr":vr,"f2":fwd(0,2),"f1":fwd(0,1),"f12":fwd(1,2),
                             "f8":fwd(0,8),"f24":fwd(0,24),"hour":hrs,"vz":vz,"pos":b["postRebalance_current_allocation"],
                             "nxt":fwd(0,1)})
            df=df.iloc[::2]
            rows.append(df)
            g=(b["postRebalance_current_allocation"]*(b["close"].shift(-1)/b["close"]-1)).sum()
            fee=((b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]).sum()
            turn=b["postRebalance_current_allocation"].diff().abs().sum()
            book.append((coin,g,fee,turn,len(b)))
    d=pd.concat(rows).dropna(subset=["z","f2","vr"])
    d["hi"]=d["vr"]>=0.5
    d["zq"]=pd.qcut(d["z"],10,labels=False)
    def tab(g,col):
        return g[col].agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    out={}
    for h in ["f1","f12","f2","f8","f24"]:
        t=d.groupby(["hi","zq"])[h].mean().unstack(0)*1e4
        out["bp "+h+" by z decile x hivol"]=t.round(2)
    out["count z dec"]=d.groupby("zq")["z"].agg(["mean","count"]).round(2)
    bk=pd.DataFrame(book,columns=["coin","gross","fee","turn","n"]).groupby("coin").sum()
    out["book gross/fee per coin"]=bk.round(3)
    d["vzq"]=pd.qcut(d["vz"],5,labels=False)
    d["fall"]=(-d["z"]).clip(lower=0)
    def slope(x):
        x=x.dropna(subset=["vz"])
        r=stats.linregress(x["fall"],x["f2"]); return pd.Series({"slope_bp":r.slope*1e4,"t":r.slope/r.stderr,"n":len(x)})
    out["slope by volume quintile"]=d.groupby("vzq").apply(slope).round(2)
    out["slope by hour group"]=d.assign(hg=d["hour"]//4).groupby("hg").apply(slope).round(2)
    out["slope by coin"]=d.groupby("coin").apply(slope).round(2)
    d["rise"]=d["z"].clip(lower=0)
    def sl2(x):
        r=stats.linregress(x["rise"],x["f2"]); return pd.Series({"slope_bp":r.slope*1e4,"t":r.slope/r.stderr,"n":len(x)})
    out["rise slope hi/lo"]=d.groupby("hi").apply(sl2).round(2)
    return out
