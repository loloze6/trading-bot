import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    recs=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"]
            rise=c/c.shift(72)-1
            z=(rise-rise.rolling(72,min_periods=20).mean())/rise.rolling(72,min_periods=20).std()
            f2=c.shift(-2)/c-1
            p2=c.shift(-4)/c.shift(-2)-1
            f8=c.shift(-8)/c-1
            hr=(ts+pd.Timedelta(hours=1)).dt.hour  # close hour
            df=pd.DataFrame({"coin":coin,"w":w,"ch":hr,"rise":rise,"z":z,"f2":f2,"p2":p2,"f8":f8})
            recs.append(df.iloc[::2])
    A=pd.concat(recs).dropna(subset=["rise","f2","p2"])
    m2=A.f2.mean()
    A["ex"]=A.f2-m2
    A["pex"]=A.p2-A.p2.mean()
    up=A[A.rise>0].copy()
    up["zc"]=up.z.clip(lower=0)
    out={}
    g=[]
    for h,s in up.groupby("ch"):
        s=s.dropna(subset=["zc"])
        if len(s)<50: continue
        sl=stats.linregress(s.zc,s.ex)
        g.append({"close_hour":h,"n":len(s),"mean ex f2":s.ex.mean(),"slope f2 on z":sl.slope,"t slope":sl.slope/sl.stderr,
                  "mean ex next2 after":s.pex.mean(),"top3rd-bot3rd":s.ex[s.zc>=s.zc.quantile(2/3)].mean()-s.ex[s.zc<=s.zc.quantile(1/3)].mean()})
    out["uptrend: 2h fwd by close hour (non-settle hours too)"]=pd.DataFrame(g).set_index("close_hour")
    # settlement episodes: close hour 22,6,14
    S=up[up.ch.isin([22,6,14])].dropna(subset=["zc"])
    S["q"]=pd.qcut(S.rise.rank(method="first"),5,labels=False)
    out["episodes by 72h-rise quintile"]=S.groupby("q").agg(rise=("rise","mean"),ex2=("ex","mean"),post2=("pex","mean"),n=("ex","size"),absmove=("f2",lambda x:x.abs().mean()))
    out["episode size vs fee"]=pd.Series({"mean |2h ret| at episodes":S.f2.abs().mean(),"mean ex2":S.ex.mean(),
        "t ex2":S.ex.mean()/(S.ex.std()/np.sqrt(len(S))),"round-trip fee per unit alloc":2*0.001066})
    # down-trend side for comparison
    dn=A[(A.rise<0)&A.ch.isin([22,6,14])]
    out["downtrend episodes"]=pd.Series({"n":len(dn),"mean ex2":dn.ex.mean(),"t":dn.ex.mean()/(dn.ex.std()/np.sqrt(len(dn)))})
    # by year
    return out
