import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1,3,6,12]
    drift = {}
    for c in bars:
        for h in H:
            rs=[]
            for w,df in bars[c].items():
                cl=df["close"].values
                for i in range(0,len(cl)-h,h):
                    rs.append(cl[i+h]/cl[i]-1)
            drift[(c,h)] = np.mean(rs) if rs else np.nan
    rows=[]
    for c in bars:
        for w,df in bars[c].items():
            df=df.reset_index(drop=True)
            cl=df["close"].values; hi=df["high"].values; lo=df["low"].values
            rng=hi-lo
            loc=np.where(rng>0,(cl-lo)/np.where(rng>0,rng,1),np.nan)
            reg=df["regime"].astype(str).values
            ts=pd.to_datetime(df["timestamp"])
            yr=ts.dt.year.values; dstr=ts.dt.strftime("%Y%m%d").values
            n=len(df)
            for t in range(1,n):
                r={"coin":c,"w":w,"year":yr[t],"day":dstr[t],"pos":t,"cl_lag":loc[t-1],
                   "agit":reg[t]!="chop",
                   "tr":cl[t]/cl[t-60]-1 if t>=60 else np.nan}
                for h in H:
                    r[f"f{h}"]=cl[t+h]/cl[t]-1-drift[(c,h)] if t+h<n else np.nan
                r["raw6"]=cl[t+6]/cl[t]-1 if t+6<n else np.nan
                rows.append(r)
    d=pd.DataFrame(rows)
    g=d[(d["pos"]%6)==0].copy()
    def tt(x):
        x=x.dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    def dayt(sub,col):
        sub=sub.dropna(subset=[col]); n=len(sub)
        m=sub[col].mean(); dev=(sub[col]-m).groupby(sub["day"]).sum()
        se=np.sqrt((dev**2).sum())/n
        return pd.Series({"n":n,"days":sub["day"].nunique(),"mean":m,"t_day":m/se})
    out={}
    lc=g[g.agit & (g.cl_lag<0.4)]
    out["lowclose_dayt"]=pd.DataFrame({h:dayt(lc,h) for h in ["f1","f3","f6","f12","raw6"]}).T
    out["lowclose_year"]=lc.groupby("year")["f6"].apply(tt).unstack()
    out["lowclose_coin"]=lc.groupby("coin")["f6"].apply(tt).unstack()
    lc2=lc.copy(); lc2["trend"]=pd.cut(lc2["tr"],[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    out["lowclose_trend"]=lc2.groupby("trend")["f6"].apply(tt).unstack()
    lc2["b"]=pd.cut(lc2["cl_lag"],[-0.01,0.1,0.2,0.3,0.4])
    out["lowclose_grade"]=lc2.groupby("b")["f6"].apply(tt).unstack()
    a=g[g.agit & (g.cl_lag<0.5)].dropna(subset=["f6","cl_lag"])
    s=stats.linregress(a["cl_lag"],a["f6"])
    out["lowhalf_slope"]=pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(a)})
    a=g[g.agit & (g.cl_lag>=0.5)].dropna(subset=["f6","cl_lag"])
    s=stats.linregress(a["cl_lag"],a["f6"])
    out["highhalf_slope"]=pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(a)})
    hc=g[g.agit & (g.cl_lag>=0.8)]
    out["highclose_dayt"]=pd.DataFrame({h:dayt(hc,h) for h in ["f6","raw6"]}).T
    return out
