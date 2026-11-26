import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            d=pd.DataFrame({"w":w,"coin":coin,"ts":pd.to_datetime(b["timestamp"])})
            d["r"]=r; d["nxt"]=c.shift(-1)/c-1; d["nxt2"]=c.shift(-2)/c-1; d["nxt3"]=c.shift(-3)/c-1
            sd=r.rolling(30,min_periods=20).std(); d["sd"]=sd
            d["pct"]=sd.rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            d["width"]=(b["high"]-b["low"])/c/sd
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            d["low_near"]=(b["high"]-c)/rng
            d["tr60"]=c/c.shift(60)-1
            d["z"]=r/sd.shift(1)
            d["r3z"]=(c/c.shift(3)-1)/(sd.shift(3)*np.sqrt(3))
            d["pos"]=np.arange(len(d))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mr=D.groupby("coin")["r"].mean()
    for h,col in [(1,"nxt"),(2,"nxt2"),(3,"nxt3")]:
        D["ex%d"%h]=D[col]-h*D["coin"].map(mr)
    D["agit"]=np.where(D["pct"]>0.5,"agit",np.where(D["pct"].notna(),"calm",None))
    D["trend"]=pd.cut(D["tr60"],[-np.inf,-0.1,0.1,np.inf],labels=["fall","chop","rise"]).astype(str)
    D["prof"]=D["trend"]+"_"+D["agit"].astype(str)
    D=D[D.agit.notna()&D.tr60.notna()]
    D["day"]=D["ts"].dt.floor("D")
    def tday(g,col="ex1"):
        g=g.dropna(subset=[col])
        if len(g)<5: return pd.Series({"n":len(g),"days":np.nan,"mean":np.nan,"t":np.nan})
        s=g.groupby("day")[col].sum()
        return pd.Series({"n":len(g),"days":len(s),"mean":g[col].mean(),"t":s.mean()/(s.std()/np.sqrt(len(s)))})
    out={}
    D["sit"]="other"
    D.loc[(D.width>=2)&(D.low_near>=0.8),"sit"]="wide_low"
    D.loc[(D.width>=2)&(D.low_near<=0.2),"sit"]="wide_high"
    out["prof_sit_truepct"]=D[D.sit!="other"].groupby(["prof","sit"]).apply(tday).round(4)
    RC=D[D.prof=="rise_calm"].copy()
    WL=RC[RC.sit=="wide_low"].copy()
    WL["wq"]=pd.qcut(WL.width,2,labels=False)
    out["rc_widelow_width_half"]=WL.groupby("wq").apply(tday).round(4)
    WL["zq"]=pd.qcut(WL.z,2,labels=False)
    out["rc_widelow_z_half"]=WL.groupby("zq").apply(tday).round(4)
    out["rc_widelow_h2_h3"]=pd.DataFrame({"h2":tday(WL,"ex2"),"h3":tday(WL,"ex3")}).round(4)
    # rising calm: low close any width, graded by low_near
    RC["lnq"]=pd.cut(RC.low_near,[-0.01,0.2,0.4,0.6,0.8,1.01],labels=False)
    out["rc_lownear_bins"]=RC.groupby("lnq").apply(tday).round(4)
    RC["zq"]=pd.qcut(RC.z,5,labels=False)
    out["rc_z_quint"]=RC.groupby("zq").apply(tday).round(4)
    # choppy agitated: up days fade?
    for p in ["chop_agit","fall_agit","rise_agit","chop_calm","fall_calm"]:
        P=D[D.prof==p].copy()
        P["zq"]=pd.qcut(P.z,5,labels=False)
        out["z_quint_"+p]=P.groupby("zq").apply(tday).round(4)
    # rising calm 3 day fall z
    RC["r3q"]=pd.qcut(RC.r3z,5,labels=False)
    out["rc_r3z_quint_ex2"]=RC.groupby("r3q").apply(lambda g:tday(g,"ex2")).round(4)
    out["prof_counts"]=D.prof.value_counts()
    return out
