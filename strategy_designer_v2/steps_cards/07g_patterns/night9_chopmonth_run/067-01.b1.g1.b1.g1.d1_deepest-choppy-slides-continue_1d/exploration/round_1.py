import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            c=df["close"].astype(float).reset_index(drop=True)
            o=df["open"].astype(float).reset_index(drop=True)
            ts=pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r1=c.pct_change()
            d=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(c)),
                "r60":c/c.shift(60)-1,"r30":c/c.shift(30)-1,"r5":c/c.shift(5)-1,
                "r1":r1,"sd30":r1.rolling(30).std(),
                "f10":c.shift(-10)/c-1,"f5":c.shift(-5)/c-1,"f3":c.shift(-3)/c-1,"f1":c.shift(-1)/c-1,
                "wd":ts.dt.weekday,"clpos":(c-df["low"].values)/(df["high"].values-df["low"].values+1e-12)})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    # coin drift per horizon on non-overlapping grid
    out={}
    for h in [1,3,5,10]:
        g=D[D.pos%h==0]
        drift=g.groupby("coin")[f"f{h}"].mean()
        D[f"x{h}"]=D[f"f{h}"]-D.coin.map(drift)
    D["trend"]=np.where(D.r60>0.10,"rising",np.where(D.r60<-0.10,"falling","choppy"))
    D.loc[D.r60.isna(),"trend"]=np.nan
    med=D.groupby("coin")["sd30"].transform("median")
    D["agit"]=np.where(D.sd30>med,"agitated","calm")
    D["z30"]=D.r30/(D.sd30*np.sqrt(30))
    D["z1"]=D.r1/D.sd30.shift(1)
    D["day"]=D.coin+D.win+D.pos.astype(str)
    def tab(sub,feat,h,q=5):
        s=sub.dropna(subset=[feat,f"x{h}"]).copy()
        if len(s)<30: return None
        s["q"]=pd.qcut(s[feat],q,labels=False,duplicates="drop")
        t=s.groupby("q")[f"x{h}"].agg(["count","mean"])
        t["t"]=s.groupby("q")[f"x{h}"].apply(lambda v: v.mean()/(v.std()/np.sqrt(len(v))))
        rho,p=stats.spearmanr(s[feat],s[f"x{h}"])
        t["rho_all"]=rho; t["p_all"]=p
        return t
    for h in [5,10]:
        g=D[(D.pos%h==0)]
        for tr in ["choppy","rising","falling"]:
            out[f"z30->x{h} {tr}"]=tab(g[g.trend==tr],"z30",h)
    g=D[D.pos%10==0]
    out["z30->x10 choppy calm"]=tab(g[(g.trend=="choppy")&(g.agit=="calm")],"z30",10)
    out["z30->x10 choppy agit"]=tab(g[(g.trend=="choppy")&(g.agit=="agitated")],"z30",10)
    for h in [1,3]:
        g=D[D.pos%h==0]
        for tr in ["choppy","rising","falling"]:
            out[f"z1->x{h} {tr}"]=tab(g[g.trend==tr],"z1",h)
    g=D[D.pos%3==0]
    out["clpos->x3 all"]=tab(g,"clpos",3)
    g=D[D.pos%1==0].dropna(subset=["x1"])
    out["weekday x1"]=g.groupby("wd")["x1"].agg(["count","mean",lambda v:v.mean()/(v.std()/np.sqrt(len(v)))])
    out["profile counts"]=D.groupby(["trend","agit"]).size()
    tr=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items(): tr.append(len(t))
    out["n trades"]=int(sum(tr))
    return out
