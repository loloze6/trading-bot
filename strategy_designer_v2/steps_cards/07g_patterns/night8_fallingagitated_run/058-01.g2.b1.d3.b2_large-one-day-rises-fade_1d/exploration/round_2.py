import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=30).std()
            z1=r/sd
            z3=(c/c.shift(3)-1)/(sd*np.sqrt(3))
            z5=(c/c.shift(5)-1)/(sd*np.sqrt(5))
            z10=(c/c.shift(10)-1)/(sd*np.sqrt(10))
            tr60=(c/c.shift(60)-1)*100
            f5=c.shift(-5)/c-1
            f3=c.shift(-3)/c-1
            inp=(b["regime"]!="chop")
            ts=pd.to_datetime(b["timestamp"])
            sdh=c.pct_change(5)
            for i in range(0,len(b),5):
                rows.append(dict(coin=coin,w=w,z1=z1[i],z3=z3[i],z5=z5[i],z10=z10[i],tr=tr60[i],
                                 f5=f5[i],f3=f3[i],inp=bool(inp[i]),day=ts[i].normalize(),yr=ts[i].year))
    d=pd.DataFrame(rows).dropna(subset=["f5"])
    d["u"]=d["f5"]-d.groupby("coin")["f5"].transform("mean")
    d["sd5"]=d.groupby("coin")["f5"].transform("std")
    d["s"]=d["u"]/d["sd5"]
    def trend(x):
        if pd.isna(x): return "na"
        return "rising" if x>10 else ("falling" if x<-10 else "choppy")
    d["trend"]=d["tr"].apply(trend)
    d["grp"]=np.where(d["inp"],"FA",np.where(d["trend"]=="falling","Fcalm",d["trend"]))
    out={}
    def daytab(df,col,bins,keys):
        df=df.dropna(subset=[col]).copy()
        df["b"]=pd.cut(df[col],bins)
        res=[]
        for k,g in df.groupby(keys+["b"],observed=True):
            dd=g.groupby("day")["u"].sum()
            t=dd.mean()/(dd.std()/np.sqrt(len(dd))) if len(dd)>2 else np.nan
            res.append(dict(k=str(k),n=len(g),days=len(dd),mean=g["u"].mean(),strength=g["s"].mean(),tday=t))
        return pd.DataFrame(res).set_index("k").round(4)
    out["z10_by_grp"]=daytab(d,"z10",[-99,-1,0,1,99],["grp"])
    out["z5_by_grp"]=daytab(d,"z5",[-99,-1,0,1,99],["grp"])
    out["z1_by_grp"]=daytab(d,"z1",[-99,-1.5,0,1.5,99],["grp"])
    # graded correlations within groups (spearman)
    cr=[]
    for k,g in d.groupby("grp"):
        for col in ["z1","z3","z5","z10"]:
            gg=g.dropna(subset=[col])
            if len(gg)>20:
                rho,p=stats.spearmanr(gg[col],gg["u"])
                cr.append(dict(grp=k,col=col,n=len(gg),rho=rho,p=p))
    out["spearman"]=pd.DataFrame(cr).round(4)
    # in profile, z10 by year
    fa=d[d["inp"]].dropna(subset=["z10"]).copy()
    fa["neg"]=fa["z10"]<-0.5
    g=fa.groupby(["yr","neg"])["u"]
    out["FA_z10_year"]=pd.DataFrame({"n":g.size(),"mean":g.mean()}).round(4)
    out["groups_n"]=d["grp"].value_counts()
    return out
