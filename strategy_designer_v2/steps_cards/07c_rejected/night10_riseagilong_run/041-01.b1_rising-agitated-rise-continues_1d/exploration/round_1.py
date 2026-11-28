import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            df=df.sort_values("timestamp").reset_index(drop=True)
            c=df["close"].astype(float).values
            n=len(c)
            r=pd.Series(c).pct_change()
            sd=r.rolling(30,min_periods=20).std(ddof=1).shift(1)
            z=r/sd
            yr=pd.to_datetime(df["timestamp"]).dt.year.values
            reg=df["regime"].values
            for i in range(n):
                d={"coin":coin,"w":w,"pos":i,"year":yr[i],"z":z.iloc[i],"r":r.iloc[i],
                   "inprof":reg[i]=="unknown"}
                for h in (1,2,3,5):
                    d[f"f{h}"]=c[i+h]/c[i]-1 if i+h<n else np.nan
                rows.append(d)
    A=pd.DataFrame(rows)
    for h in (1,2,3,5):
        g=A[A.pos%h==0]
        dr=g.groupby("coin")[f"f{h}"].mean()
        A[f"x{h}"]=A[f"f{h}"]-A.coin.map(dr)
    P=A[A.inprof & A.z.notna()].copy()
    P["zb"]=pd.cut(P.z,[-np.inf,-2,-1,-0.5,0,0.5,1,2,np.inf])
    out={}
    def tab(df,h):
        g=df[df.pos%h==0].dropna(subset=[f"x{h}"])
        return g.groupby("zb",observed=True)[f"x{h}"].agg(n="count",mean="mean",t=lambda s: s.mean()/s.std()*np.sqrt(len(s)))
    for h in (1,2,3,5):
        out[f"inprof_x{h}_by_z"]=tab(P,h)
    res={}
    for side,m in (("up",P.z>0),("down",P.z<0)):
        for h in (1,2,3,5):
            g=P[m & (P.pos%h==0)].dropna(subset=[f"x{h}"])
            s=stats.linregress(g.z,g[f"x{h}"])
            res[f"{side}_h{h}"]=pd.Series({"n":len(g),"slope":s.slope,"t":s.slope/s.stderr,"mean":g[f"x{h}"].mean()})
    out["slopes"]=pd.DataFrame(res).T
    P["side"]=np.where(P.z>0,"up","down")
    out["coin_side_h1"]=P.groupby(["coin","side"])["x1"].agg(["count","mean"])
    out["year_side_h1"]=P.groupby(["year","side"])["x1"].agg(["count","mean"]).unstack()
    O=A[~A.inprof & A.z.notna()].copy()
    O["zb"]=pd.cut(O.z,[-np.inf,-2,-1,0,1,2,np.inf])
    out["outprof_x1_by_z"]=O.groupby("zb",observed=True)["x1"].agg(["count","mean"])
    out["share_inprof"]=float(A.inprof.mean())
    out["regimes"]=A.groupby("inprof").size()
    return out
