import pandas as pd, numpy as np
from scipy import stats

def _ts(s):
    if pd.api.types.is_numeric_dtype(s):
        return pd.to_datetime(s, unit="ms", utc=True)
    return pd.to_datetime(s, utc=True, errors="coerce")

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            d=b[["timestamp","close","volume","forecast","regime"]].copy().reset_index(drop=True)
            d["ts"]=_ts(d["timestamp"])
            d["dow"]=d.ts.dt.dayofweek; d["year"]=d.ts.dt.year
            r=d.close.pct_change(); d["r1"]=r
            sd=r.rolling(20).std()
            d["z"]=r/sd
            d["z2"]=d.close.pct_change(2)/(sd*np.sqrt(2))
            d["vr"]=d.volume/d.volume.rolling(20).mean()
            for h in [1,2,3,5]:
                d[f"f{h}"]=d.close.shift(-h)/d.close-1
            d["coin"]=coin; d["w"]=w; d["pos"]=np.arange(len(d))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for h in [1,2,3,5]:
        m=D[D.pos%h==0].groupby("coin")[f"f{h}"].mean()
        D[f"x{h}"]=D[f"f{h}"]-D.coin.map(m)
    def summ(g,col="x2",zc="z"):
        g=g.dropna(subset=[col,zc])
        dn=g[g[zc]<0]; up=g[g[zc]>0]
        p=(-dn[zc])*dn[col]
        sl=stats.linregress(g[zc],g[col]) if len(g)>5 else None
        return pd.Series({"n_drop":len(dn),"mean_x_drop":dn[col].mean(),"t_drop":stats.ttest_1samp(dn[col],0).statistic,
                          "t_prod_drop":stats.ttest_1samp(p,0).statistic,"n_rise":len(up),"mean_x_rise":up[col].mean(),"t_rise":stats.ttest_1samp(up[col],0).statistic,
                          "slope_all":sl.slope if sl else np.nan,"t_slope":(sl.slope/sl.stderr) if sl else np.nan})
    out={}
    try: out["by_dow_x2_z"]=D.groupby("dow").apply(summ)
    except Exception as e: out["by_dow_err"]=str(e)
    S=D[D.dow==6]
    try: out["sun_by_h"]=pd.DataFrame({h:summ(S,f"x{h}") for h in [1,2,3,5]}).T
    except Exception as e: out["sun_h_err"]=str(e)
    try: out["sun_by_coin"]=S.groupby("coin").apply(summ)
    except Exception as e: out["sun_coin_err"]=str(e)
    try: out["sun_by_year"]=S.groupby("year").apply(summ)
    except Exception as e: out["sun_year_err"]=str(e)
    try: out["sun_weekend2d_z2"]=summ(S,"x2","z2")
    except Exception as e: out["z2_err"]=str(e)
    try:
        S2=S.dropna(subset=["vr","z","x2"]); S2=S2[S2.z<0].copy()
        S2["vt"]=pd.qcut(S2.vr,3,labels=["lowvol","mid","highvol"])
        out["sun_drop_by_volterc"]=S2.groupby("vt").apply(lambda g: pd.Series({"n":len(g),"mean_x2":g.x2.mean(),"t":stats.ttest_1samp(g.x2,0).statistic,"t_prod":stats.ttest_1samp(-g.z*g.x2,0).statistic}))
        S2["zt"]=pd.qcut(S2.z,4,labels=["deepest","q2","q3","shallow"])
        out["sun_drop_by_depth"]=S2.groupby("zt").apply(lambda g: pd.Series({"n":len(g),"mean_z":g.z.mean(),"mean_x2":g.x2.mean(),"t":stats.ttest_1samp(g.x2,0).statistic}))
    except Exception as e: out["vol_err"]=str(e)
    try:
        M=S[(S.forecast>0)].dropna(subset=["x2"])
        M=M.assign(p=M.forecast/10*M.x2)
        tt=lambda s: stats.ttest_1samp(s,0).statistic if len(s)>2 else np.nan
        out["main_by_coin"]=M.groupby("coin").p.agg(["count","mean",tt])
        out["main_by_year"]=M.groupby("year").p.agg(["count","mean",tt])
        out["main_all"]=pd.Series({"n":len(M),"mean":M.p.mean(),"t":tt(M.p),"mean_x2":M.x2.mean(),"t_x2":tt(M.x2)})
        # weekday drops of similar size for comparison: any weekday close where z<0, x2
        W=D[(D.dow<5)].dropna(subset=["z","x2"]); W=W[W.z<0]
        out["weekday_drop_vs_sun"]=pd.Series({"wk_n":len(W),"wk_mean_x2":W.x2.mean(),"sun_n":int((S.z<0).sum()),"sun_mean_x2":S[S.z<0].x2.mean(),
            "welch_t_sun_minus_wk":stats.ttest_ind(S[S.z<0].x2.dropna(),W.x2,equal_var=False).statistic})
    except Exception as e: out["main_err"]=str(e)
    return out
