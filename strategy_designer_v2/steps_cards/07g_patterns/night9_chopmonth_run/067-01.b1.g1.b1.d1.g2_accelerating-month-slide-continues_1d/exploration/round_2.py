import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            n=len(b)
            d=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(n)})
            d["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D").values
            d["regime"]=b["regime"].values
            d["r30"]=(c/c.shift(30)-1).values
            d["r60"]=(c/c.shift(60)-1).values
            d["r5"]=(c/c.shift(5)-1).values
            d["vol30"]=c.pct_change().rolling(30).std().values
            for h in (5,10):
                d[f"f{h}"]=(c.shift(-h)/c-1).values
            d["yr"]=pd.to_datetime(b["timestamp"]).dt.year.values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for h in (5,10):
        g=D[D.pos%h==0]
        dr=g.groupby("coin")[f"f{h}"].mean()
        D[f"u{h}"]=D[f"f{h}"]-D.coin.map(dr)
    D["choppy"]=D.regime!="chop"
    D["r30z"]=D.r30/(D.vol30*np.sqrt(30))
    out={}
    def clus(x,col):
        x=x.dropna(subset=[col])
        s=x.groupby("day")[col].sum(); n=x.groupby("day")[col].count()
        m=x[col].mean()
        dev=(x[col]-m).groupby(x.day).sum()
        se=np.sqrt((dev**2).sum())/len(x)
        return pd.Series({"n":len(x),"days":x.day.nunique(),"mean":m,"t_day":m/se if se>0 else np.nan})
    for h in (5,10):
        G=D[(D.pos%h==0)&D.choppy].dropna(subset=["r30",f"u{h}"]).copy()
        G["q"]=pd.qcut(G.r30,5,labels=False)
        out[f"choppy_u{h}_by_r30q"]=G.groupby("q").apply(lambda x: pd.concat([clus(x,f"u{h}"),pd.Series({"r30mean":x.r30.mean()})]))
        rho,p=stats.spearmanr(G.r30,G[f"u{h}"])
        out[f"choppy_spearman_r30_u{h}"]=f"rho {rho:.3f} p {p:.4f} n {len(G)}"
        G["sgn"]=np.sign(G.r30)
        G["u_dir"]=G[f"u{h}"]*G.sgn
        out[f"choppy_u{h}_signdir_by_side"]=G.groupby("sgn").apply(lambda x: clus(x,"u_dir"))
        G["qz"]=pd.qcut(G.r30z,5,labels=False)
        out[f"choppy_u{h}_by_r30z_q"]=G.groupby("qz").apply(lambda x: clus(x,"u"+str(h)))
    G=D[(D.pos%10==0)&D.choppy].dropna(subset=["r30","u10"]).copy()
    G["q"]=pd.qcut(G.r30,5,labels=False)
    out["choppy_u10_r30q_by_yr"]=G.groupby(["yr","q"]).u10.agg(["count","mean"]).unstack()
    out["choppy_u10_r30q_by_win"]=G.groupby(["win","q"]).u10.mean().unstack()
    G["vq"]=pd.qcut(G.vol30,2,labels=["calmer","wilder"])
    out["choppy_u10_r30q_by_volhalf"]=G.groupby(["vq","q"]).apply(lambda x: clus(x,"u10"))
    # non-choppy comparison graded
    H=D[(D.pos%10==0)&~D.choppy].dropna(subset=["r30","u10"])
    rho,p=stats.spearmanr(H.r30,H.u10)
    out["trend_spearman_r30_u10"]=f"rho {rho:.3f} p {p:.4f} n {len(H)}"
    return out
