import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    # normal drift per coin per horizon, non-overlapping grid
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
            yr=pd.to_datetime(df["timestamp"]).dt.year.values
            n=len(df)
            for t in range(1,n):
                r={"coin":c,"w":w,"year":yr[t],"pos":t,"cl_lag":loc[t-1],
                   "agit":reg[t]!="chop","regime":reg[t],
                   "ret1d_lag": cl[t-1]/cl[t-2]-1 if t>=2 else np.nan,
                   "tr":cl[t]/cl[t-60]-1 if t>=60 else np.nan}
                for h in H:
                    r[f"f{h}"]=cl[t+h]/cl[t]-1-drift[(c,h)] if t+h<n else np.nan
                # from high-close bar itself over 7 days
                r["f7from0"]=cl[t+6]/cl[t-1]-1-drift[(c,6)]*7/6 if t+6<n else np.nan
                rows.append(r)
    d=pd.DataFrame(rows)
    # grid 6 per window
    g=d[(d["pos"]%6)==0].copy()
    g["bin"]=pd.cut(g["cl_lag"],[-0.01,0.2,0.4,0.6,0.8,0.9,1.01])
    def tt(x):
        x=x.dropna(); 
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["agit_bins_f6"]=g[g.agit].groupby("bin")["f6"].apply(tt).unstack()
    out["calm_bins_f6"]=g[~g.agit].groupby("bin")["f6"].apply(tt).unstack()
    hc=g[g.agit & (g.cl_lag>=0.8)]
    out["hc_horizons"]=pd.DataFrame({h:tt(hc[h]) for h in ["f1","f3","f6","f12","f7from0"]}).T
    out["hc_year"]=hc.groupby("year")["f6"].apply(tt).unstack()
    out["hc_coin"]=hc.groupby("coin")["f6"].apply(tt).unstack()
    hc2=hc.copy(); hc2["trend"]=pd.cut(hc2["tr"],[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    out["hc_trend"]=hc2.groupby("trend")["f6"].apply(tt).unstack()
    hc2["daymove"]=pd.cut(hc2["ret1d_lag"],[-9,0,0.03,9],labels=["down","up<3%","up>3%"])
    out["hc_daymove"]=hc2.groupby("daymove")["f6"].apply(tt).unstack()
    # regression of f6 on cl_lag in agitated, all bins
    a=g[g.agit].dropna(subset=["f6","cl_lag"])
    s=stats.linregress(a["cl_lag"],a["f6"])
    out["agit_slope"]=pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(a)})
    return out
