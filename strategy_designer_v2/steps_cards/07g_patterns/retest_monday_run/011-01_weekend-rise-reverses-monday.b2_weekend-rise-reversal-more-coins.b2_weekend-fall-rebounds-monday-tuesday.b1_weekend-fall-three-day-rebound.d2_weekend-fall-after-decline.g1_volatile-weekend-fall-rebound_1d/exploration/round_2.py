import pandas as pd, numpy as np
from scipy import stats

def _panel(data):
    rows=[]
    for coin,wins in data["bars"].items():
        g3=[]
        for w,b in wins.items():
            c=b["close"].astype(float).values
            g3+=list(c[3::3]/c[:-3:3][:len(c[3::3])]-1)
        drift=np.mean(g3); sd=np.std(g3,ddof=1)
        for w,b in wins.items():
            d=b[["timestamp","close","volume"]].copy().reset_index(drop=True)
            d["pos"]=np.arange(len(d))
            d["ts"]=pd.to_datetime(d["timestamp"],utc=True)
            d["date"]=d["ts"].dt.floor("D")
            d["wd"]=d["ts"].dt.weekday; d["yr"]=d["ts"].dt.year
            d["r1"]=d["close"].pct_change()
            d["r2"]=d["close"].pct_change(2)
            d["vol20"]=d["r1"].rolling(20).std()
            d["relv"]=d["volume"]/d["volume"].rolling(20).mean().shift(1)
            d["f3"]=d["close"].shift(-3)/d["close"]-1
            d["ex3"]=(d["f3"]-drift)/1.0; d["sd3"]=sd
            d["coin"]=coin; d["win"]=w
            rows.append(d)
    return pd.concat(rows,ignore_index=True)

def _cl(df,col):
    # cluster by date: mean across coins each date, t over dates
    m=df.groupby("date")[col].mean().dropna()
    n=len(m)
    if n<3: return pd.Series(dict(cases=len(df),dates=n,mean=np.nan,t=np.nan))
    return pd.Series(dict(cases=len(df),dates=n,mean=m.mean(),t=m.mean()/(m.std()/np.sqrt(n))))

def explore(data):
    p=_panel(data).dropna(subset=["r1","vol20","ex3"]).copy()
    p["z"]=p["r1"]/p["vol20"]
    p["s"]=p["ex3"]/p["sd3"]
    out={}
    sun=p[p.wd==6].copy()
    sat=p[p.wd==5].copy()
    # A: Sunday rises -> fall (reversal), graded, by year, clustered
    sr=sun[sun.r1>0].copy(); sr["rev"]=-sr.ex3
    sr["zq"]=pd.qcut(sr.z,4,labels=False)
    out["A_sunrise_by_zq"]=sr.groupby("zq").apply(lambda g:_cl(g,"rev"))
    out["A_sunrise_by_year"]=sr.groupby("yr").apply(lambda g:_cl(g,"rev"))
    lr=stats.linregress(sr.z,-sr.s); out["A_sunrise_slope_t"]=float(lr.slope/lr.stderr)
    # Sunday falls clustered by year for comparison
    sf=sun[sun.r1<0]
    out["A2_sunfall_by_year"]=sf.groupby("yr").apply(lambda g:_cl(g,"ex3"))
    # B: Saturday falls -> continuation
    sa=sat[sat.r1<0].copy(); sa["cont"]=-sa.ex3
    sa["zq"]=pd.qcut(-sa.z,4,labels=False)
    out["B_satfall_by_zq"]=sa.groupby("zq").apply(lambda g:_cl(g,"cont"))
    out["B_satfall_by_year"]=sa.groupby("yr").apply(lambda g:_cl(g,"cont"))
    # C: non-weekend-sunday grid (positions 0,3,6..) large daily moves: continuation signed
    g=p[(p.pos%3==0)&(p.wd!=6)].copy()
    g["cont"]=np.sign(g.r1)*g.ex3
    g["azb"]=pd.cut(g.z.abs(),[0,0.5,1,1.5,2,99])
    out["C_grid_nonsun_absz_cont"]=g.groupby(["azb",g.r1>0],observed=True).apply(lambda q:_cl(q,"cont")).unstack()[["cases","mean","t"]]
    big=g[g.z>1.5]
    out["C_bigrise_by_year"]=big.groupby("yr").apply(lambda q:_cl(q,"ex3"))
    # D: falls by vol tercile on grid, non-Sunday, clustered
    g["vt"]=g.groupby("coin")["vol20"].transform(lambda v: pd.qcut(v,3,labels=False))
    gf=g[g.z<-1]
    out["D_fall_voltercile"]=gf.groupby("vt").apply(lambda q:_cl(q,"ex3"))
    out["D_all_voltercile_anyday"]=g.groupby("vt").apply(lambda q:_cl(q,"ex3"))
    # E: weekend 2-day return at Sunday close, signed reversal graded
    sun["rev2"]=-np.sign(sun.r2)*sun.ex3
    sun["z2"]=sun.r2/(sun.vol20*np.sqrt(2))
    sun["z2b"]=pd.cut(sun.z2,[-99,-1.5,-0.75,0,0.75,1.5,99])
    out["E_weekend2d_bucket"]=sun.groupby("z2b",observed=True).apply(lambda q:_cl(q,"ex3"))
    # F: sunday rise x relative volume
    sr2=sr.dropna(subset=["relv"]).copy()
    sr2["vq"]=pd.qcut(sr2.relv,3,labels=["low","mid","high"])
    out["F_sunrise_by_relvol"]=sr2.groupby("vq",observed=True).apply(lambda q:_cl(q,"rev"))
    return out
