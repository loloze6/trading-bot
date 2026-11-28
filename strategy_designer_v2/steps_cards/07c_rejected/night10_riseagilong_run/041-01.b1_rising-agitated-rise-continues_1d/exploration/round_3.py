import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            df=df.sort_values("timestamp").reset_index(drop=True)
            c=df["close"].astype(float).values; n=len(c)
            r=pd.Series(c).pct_change()
            sd=r.rolling(30,min_periods=20).std(ddof=1).shift(1)
            z=r/sd
            yr=pd.to_datetime(df["timestamp"]).dt.year.values
            day=pd.to_datetime(df["timestamp"]).dt.floor("D").values
            reg=df["regime"].values
            for i in range(n):
                d={"coin":coin,"wn":int(w[1:]),"pos":i,"year":yr[i],"day":day[i],"z":z.iloc[i],"inprof":reg[i]=="unknown"}
                for h in (1,2,3):
                    d[f"f{h}"]=c[i+h]/c[i]-1 if i+h<n else np.nan
                rows.append(d)
    A=pd.DataFrame(rows)
    for h in (1,2,3):
        dr=A[A.pos%h==0].groupby("coin")[f"f{h}"].mean()
        A[f"x{h}"]=A[f"f{h}"]-A.coin.map(dr)
    P=A[A.inprof & A.z.notna()].copy()
    out={}
    def cl(g,y):
        x=g.z.values; yv=g[y].values
        X=np.column_stack([np.ones(len(x)),x]); b=np.linalg.lstsq(X,yv,rcond=None)[0]; e=yv-X@b
        XtXi=np.linalg.inv(X.T@X); S=pd.DataFrame(X*e[:,None]).groupby(g.day.values).sum().values; G=len(S)
        V=XtXi@(S.T@S)@XtXi*G/(G-1); return b[1],b[1]/np.sqrt(V[1,1]),G
    res={}
    for side,m in (("up",P.z>0),("down",P.z<0)):
        for h in (1,2,3):
            for off in range(h):
                g=P[m&(P.pos%h==off)].dropna(subset=[f"x{h}"])
                sl,t,G=cl(g,f"x{h}")
                gt=g.sort_values(f"x{h}").iloc[3:-3]
                st=stats.linregress(gt.z,gt[f"x{h}"])
                res[f"{side}_h{h}_off{off}"]=pd.Series({"n":len(g),"days":G,"t_clus":t,"spearman":stats.spearmanr(g.z,g[f"x{h}"])[0],"t_trim3":st.slope/st.stderr,"mean":g[f"x{h}"].mean()})
    out["offsets"]=pd.DataFrame(res).T
    U=P[(P.z>0)&(P.pos%3==0)].dropna(subset=["x3"]).copy()
    U["zb"]=pd.cut(U.z,[0,0.5,1,1.5,2,np.inf])
    out["up_x3_zb"]=U.groupby("zb",observed=True)["x3"].agg(["count","mean","median",lambda s:(s>0).mean()])
    out["up_x3_top_by_year"]=U[U.z>1.177].groupby("year")["x3"].agg(["count","mean","median"])
    D=P[P.z<0].copy()
    out["down_x2_all_offsets_tert"]=D.dropna(subset=["x2"]).groupby(pd.qcut(D.z,3),observed=True)["x2"].agg(["count","mean","median"])
    out["down_x1_by_year"]=D.groupby("year")["x1"].agg(["count","mean"])
    return out
