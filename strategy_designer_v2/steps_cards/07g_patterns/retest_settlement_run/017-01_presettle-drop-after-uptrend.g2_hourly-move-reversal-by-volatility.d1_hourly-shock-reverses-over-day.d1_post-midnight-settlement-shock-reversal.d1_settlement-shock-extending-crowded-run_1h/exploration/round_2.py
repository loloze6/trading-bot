import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        g=[]
        for w,b in ws.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-24,24)
            g.extend(c[idx+24]/c[idx]-1)
        dr=np.mean(g)
        for w,b in ws.items():
            ts=pd.to_datetime(b["timestamp"])
            cl=b["close"]; r1=cl/cl.shift(1)-1
            sd=r1.rolling(24).std()
            f=pd.DataFrame({"hour":ts.dt.hour.values,"year":ts.dt.year.values,
                "z":r1/sd,"p23z":(cl.shift(1)/cl.shift(24)-1)/(sd*np.sqrt(23)),
                "r24z":(cl/cl.shift(24)-1)/(sd*np.sqrt(24)),
                "r3z":(cl/cl.shift(3)-1)/(sd*np.sqrt(3)),
                "volrel":sd/r1.rolling(720).std(),
                "fwd":(cl.shift(-24)/cl-1)-dr,"fwd8":(cl.shift(-8)/cl-1)-dr/3})
            f["coin"]=coin; rows.append(f)
    d=pd.concat(rows).dropna(subset=["z","p23z","fwd","volrel"])
    def reg(s,x,y="fwd"):
        s=s.dropna(subset=[x,y])
        sl=stats.linregress(s[x],s[y]); m=np.sign(s[x])*s[y]
        return pd.Series({"n":float(len(s)),"slope_bp":sl.slope*1e4,"t":sl.slope/sl.stderr,
            "signmean_pct":m.mean()*100,"t_sign":m.mean()/(m.std()/np.sqrt(len(s)))})
    d["xr24"]=-d["r24z"]; d["xp23"]=-d["p23z"]; d["xz"]=-d["z"]; d["xr3"]=-d["r3z"]
    out={}
    out["fade_r24_by_hour"]=d.groupby("hour").apply(lambda s:reg(s,"xr24"))
    out["fade_p23_by_hour"]=d.groupby("hour").apply(lambda s:reg(s,"xp23"))
    h0=d[d.hour==0].copy()
    h0["vq"]=pd.qcut(h0["volrel"],3,labels=["low","mid","high"])
    out["h0_fade_r24_by_vol"]=h0.groupby("vq").apply(lambda s:reg(s,"xr24"))
    oth=d[d.hour!=0].copy()
    oth["vq"]=pd.qcut(oth["volrel"],3,labels=["low","mid","high"])
    out["other_fade_r24_by_vol"]=oth.groupby("vq").apply(lambda s:reg(s,"xr24"))
    out["h0_fade_r24_by_year"]=h0.groupby("year").apply(lambda s:reg(s,"xr24"))
    out["h0_fade_r24_by_coin"]=h0.groupby("coin").apply(lambda s:reg(s,"xr24"))
    # opposed hours 1-3: does the counter-hour continue? use 3h return vs p23 opposed
    for h in [3,9,15,21]:
        s=d[(d.hour==h)&(np.sign(d.r3z)!=np.sign(d.p23z))]
        out[f"h{h}_opposed_r3_cont"]=reg(s.assign(c3=s.r3z),"c3").to_frame().T
    # book: largest gain/loss days
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; dd.append(x)
    D=pd.concat(dd).dropna(subset=["book_return"])
    D["dow"]=pd.to_datetime(D["day"]).dt.dayofweek
    D["q"]=pd.qcut(D["book_return"].rank(method="first"),10,labels=False)
    out["book_deciles"]=D.groupby("q").agg(br=("book_return","mean"),cr=("coin_return","mean"),absc=("coin_return",lambda v:v.abs().mean()))
    return out
