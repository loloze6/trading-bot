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
            r2=pd.Series(c).pct_change(2)
            yr=pd.to_datetime(df["timestamp"]).dt.year.values
            day=pd.to_datetime(df["timestamp"]).dt.floor("D").values
            reg=df["regime"].values
            for i in range(n):
                d={"coin":coin,"w":w,"wn":int(w[1:]),"pos":i,"year":yr[i],"day":day[i],"z":z.iloc[i],
                   "inprof":reg[i]=="unknown"}
                for h in (1,2,3,4):
                    d[f"f{h}"]=c[i+h]/c[i]-1 if i+h<n else np.nan
                rows.append(d)
    A=pd.DataFrame(rows)
    for h in (1,2,3,4):
        g=A[A.pos%h==0]
        dr=g.groupby("coin")[f"f{h}"].mean()
        A[f"x{h}"]=A[f"f{h}"]-A.coin.map(dr)
    P=A[A.inprof & A.z.notna()].copy()
    out={}
    def clus_slope(g,y):
        x=g.z.values; yv=g[y].values
        X=np.column_stack([np.ones(len(x)),x])
        b=np.linalg.lstsq(X,yv,rcond=None)[0]
        e=yv-X@b
        XtXi=np.linalg.inv(X.T@X)
        S=pd.DataFrame(X*e[:,None]).groupby(g.day.values).sum().values
        G=len(S)
        V=XtXi@(S.T@S)@XtXi*G/(G-1)
        return b[1],b[1]/np.sqrt(V[1,1]),G
    res={}
    for side,m in (("up",P.z>0),("down",P.z<0)):
        for h in (1,2,3,4):
            g=P[m & (P.pos%h==0)].dropna(subset=[f"x{h}"])
            sl,t,G=clus_slope(g,f"x{h}")
            rho,p=stats.spearmanr(g.z,g[f"x{h}"])
            q=g[f"x{h}"].clip(g[f"x{h}"].quantile(.02),g[f"x{h}"].quantile(.98))
            st=stats.linregress(g.z,q)
            tm=g[f"x{h}"].mean()/g[f"x{h}"].std()*np.sqrt(len(g))
            res[f"{side}_h{h}"]=pd.Series({"n":len(g),"days":G,"slope":sl,"t_clus":t,"spearman":rho,"t_wins":st.slope/st.stderr,"mean":g[f"x{h}"].mean(),"t_mean":tm})
    out["slopes"]=pd.DataFrame(res).T
    # per coin, up h3 and down h2
    pc={}
    for coin in P.coin.unique():
        for side,m,h in (("up",P.z>0,3),("down",P.z<0,2),("down",P.z<0,1)):
            g=P[m&(P.coin==coin)&(P.pos%h==0)].dropna(subset=[f"x{h}"])
            if len(g)>10:
                s=stats.linregress(g.z,g[f"x{h}"]); rho=stats.spearmanr(g.z,g[f"x{h}"])[0]
                pc[f"{coin}_{side}_h{h}"]=pd.Series({"n":len(g),"t":s.slope/s.stderr,"rho":rho,"mean":g[f"x{h}"].mean()})
    out["per_coin"]=pd.DataFrame(pc).T
    # by window half
    P["half"]=np.where(P.wn<=12,"w1-12","w13-18")
    ph={}
    for hf in ("w1-12","w13-18"):
        for side,m,h in (("up",P.z>0,3),("down",P.z<0,2)):
            g=P[m&(P.half==hf)&(P.pos%h==0)].dropna(subset=[f"x{h}"])
            s=stats.linregress(g.z,g[f"x{h}"]); rho=stats.spearmanr(g.z,g[f"x{h}"])[0]
            ph[f"{hf}_{side}_h{h}"]=pd.Series({"n":len(g),"t":s.slope/s.stderr,"rho":rho,"mean":g[f"x{h}"].mean()})
    out["by_half"]=pd.DataFrame(ph).T
    # down side h2 buckets, all grid offsets pooled to show shape (overlap noted)
    D=P[P.z<0].copy(); D["zb"]=pd.qcut(D.z,4)
    out["down_quartile_x2_grid"]=D[D.pos%2==0].groupby("zb",observed=True)["x2"].agg(["count","mean"])
    out["down_quartile_x1"]=D.groupby("zb",observed=True)["x1"].agg(["count","mean"])
    U=P[P.z>0].copy(); U["zb"]=pd.qcut(U.z,4)
    out["up_quartile_x3_grid"]=U[U.pos%3==0].groupby("zb",observed=True)["x3"].agg(["count","mean","median"])
    return out
