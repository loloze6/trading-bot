import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            sd20=r1.rolling(20,min_periods=15).std()
            z=r1/sd20
            r90=c/c.shift(90)-1
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":z,"sd20":sd20,"r90":r90,
                             "f1":c.shift(-1)/c-1,"f3":c.shift(-3)/c-1,"f5":c.shift(-5)/c-1,
                             "alloc":b["postRebalance_current_allocation"].astype(float),
                             "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                             "yr":pd.to_datetime(b["timestamp"]).dt.year,
                             "day":pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    for h in [1,3,5]:
        m=A[A.pos%h==0].groupby("coin")[f"f{h}"].mean()
        A[f"x{h}"]=A[f"f{h}"]-A["coin"].map(m)
    out={}
    # weekday: per coin, and day-clustered t (mean across coins per day first)
    wd=A.groupby(["wd","coin"])["x1"].mean().unstack().mul(100).round(3)
    out["weekday excess1 % by coin"]=wd
    dm=A.groupby(["day","wd"])["x1"].mean().reset_index()
    out["weekday day-averaged t"]=dm.groupby("wd")["x1"].agg(lambda x: x.mean()/(x.std()/np.sqrt(len(x)))).round(2)
    A["half"]=np.where(A.yr<=2021,"<=2021",">=2022")
    out["weekday excess1 % by half (day-avg)"]=A.groupby(["wd","half"])["x1"].mean().unstack().mul(100).round(3)
    # Thu+Fri minus Mon+Wed per year
    A["grp"]=A.wd.map({0:"MW",2:"MW",3:"TF",4:"TF"})
    yy=A.dropna(subset=["grp"]).groupby(["yr","grp"])["x1"].mean().unstack()
    yy["diff%"]=(yy["TF"]-yy["MW"])*100
    out["TF minus MW by year"]=yy[["diff%"]].round(3)
    # downtrend bounces, recomputed r90<0, graded z, horizons 1,3,5
    res={}
    for h in [1,3,5]:
        G=A[(A.pos%h==0)&(A.r90<0)&(A.z>0)].dropna(subset=[f"x{h}","z"])
        s=stats.linregress(G.z,G[f"x{h}"]); res[f"r90<0 z>0 h{h}"]=(s.slope*100,s.slope/s.stderr,len(G))
        G=A[(A.pos%h==0)&(A.r90>=0)&(A.z>0)].dropna(subset=[f"x{h}","z"])
        s=stats.linregress(G.z,G[f"x{h}"]); res[f"r90>=0 z>0 h{h}"]=(s.slope*100,s.slope/s.stderr,len(G))
    out["slopes by r90 sign"]=pd.DataFrame(res,index=["slope%/z","t","n"]).T.round(3)
    # graded by depth of fall: r90 terciles in r90<0 for z>1.5
    G=A[(A.pos%5==0)&(A.r90<0)&(A.z>1.5)].dropna(subset=["x5"])
    G["d"]=pd.qcut(G.r90,3,labels=["deep","mid","shallow"])
    out["r90<0 z>1.5 by depth -> x5"]=G.groupby("d",observed=True)["x5"].agg(["count","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))]).round(4)
    # vol level interaction for up-surges in uptrend
    G=A[(A.pos%5==0)&(A.r90>=0)&(A.z>1)].dropna(subset=["x5","sd20"])
    G["vb"]=G.groupby("coin")["sd20"].transform(lambda s: pd.qcut(s.rank(method="first"),2,labels=["lo","hi"]))
    out["uptrend z>1 by vol half"]=G.groupby("vb",observed=True)["x5"].agg(["count","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))]).round(4)
    # book losses: position held on the worst coin days
    A["pnl"]=A.alloc*A.f1
    q=A.pnl.quantile(0.01)
    W=A[A.pnl<=q]
    out["worst 1% position-bars"]=pd.Series({"n":len(W),"mean pnl%":W.pnl.mean()*100,"mean f1%":W.f1.mean()*100,
        "mean alloc":W.alloc.mean(),"share of total neg pnl":W.pnl.sum()/A.pnl[A.pnl<0].sum(),
        "total pnl sum":A.pnl.sum()}).round(4)
    # gain by allocation size bucket
    H=A[A.alloc>0].copy()
    H["ab"]=pd.qcut(H.alloc,4,labels=False)
    out["held bars by alloc quartile: f1 excess"]=H.groupby("ab")["x1"].agg(["count","mean",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))]).round(5)
    return out
