import numpy as np, pandas as pd

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r=c/c.shift(1)-1
            vr=v/v.shift(1).rolling(20,min_periods=20).mean()-1
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"f":b["forecast"].astype(float),
                "vr":vr,"dayret":r,"tr60":c/c.shift(60)-1,
                "sd30":r.rolling(30).std(),"alloc":b["postRebalance_current_allocation"].astype(float)})
            for h in (1,2,3,5):
                d[f"r{h}"]=c.shift(-h)/c-1
            d["ret3p"]=c/c.shift(3)-1
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for h in (1,2,3,5):
        g=D[D.pos%h==0]; dr=g.groupby("coin")[f"r{h}"].mean()
        D[f"x{h}"]=D[f"r{h}"]-D.coin.map(dr)
    out={}
    D["fq"]=pd.qcut(D.f.rank(method="first"),5,labels=False)
    dn=D[D.dayret<0].copy()
    # graded within down days by forecast quintile, horizons, total move and unusual move vs cost 0.22%
    res=[]
    for h in (1,2,3,5):
        g=dn[(dn.pos%h==0)&dn[f"x{h}"].notna()]
        for q,s in g.groupby("fq"):
            res.append({"h":h,"q":q,"n":len(s),"tot":s[f"r{h}"].mean(),"unus":s[f"x{h}"].mean(),
                        "t":s[f"x{h}"].mean()/(s[f"x{h}"].std()/np.sqrt(len(s)))})
    out["down_by_fq_h"]=pd.DataFrame(res).pivot_table(index="q",columns="h",values=["tot","unus","t"])
    # trend profile split, heavy down days (fq4) vs other down days
    dn["trend"]=np.where(dn.tr60>0.1,"rising",np.where(dn.tr60<-0.1,"falling","choppy"))
    dn.loc[dn.tr60.isna(),"trend"]="na"
    out["heavy_down_by_trend"]=dn.groupby(["trend",dn.fq==4]).agg(n=("x1","count"),x1=("x1","mean"),x3=("x3","mean"))
    # size of fall grading within heavy volume: dayret / sd30
    hv=dn[dn.fq==4].copy()
    hv["z"]=hv.dayret/hv.sd30
    hv["zq"]=pd.qcut(hv.z.rank(method="first"),4,labels=False)
    out["heavy_down_by_fallz"]=hv.groupby("zq").agg(n=("x1","count"),z=("z","mean"),x1=("x1","mean"),x2=("x2","mean"),x3=("x3","mean"))
    # book falls: actual book daily mean over coins, drawdown episodes
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            dd.append(pd.DataFrame({"w":w,"day":t["day"].values,"br":t["book_return"].values,"cr":t["coin_return"].values}))
    B=pd.concat(dd).dropna().groupby(["w","day"]).mean().reset_index()
    B=B.sort_values(["w","day"])
    out["book_by_window"]=B.groupby("w").agg(days=("br","count"),bk=("br","mean"),coin=("cr","mean"),
        bk_sd=("br","std"),corr=("br",lambda s: np.corrcoef(s,B.loc[s.index,"cr"])[0,1]))
    # short vs long contribution on coin bars by window
    D["g"]=D.alloc*D.r1
    out["gain_by_side_window"]=D.groupby(["w",np.sign(D.alloc)]).g.mean().unstack()
    return out
