import pandas as pd, numpy as np
from scipy import stats

def tt(s):
    s = pd.Series(s).dropna()
    return (s.mean()/s.std()*np.sqrt(len(s))) if len(s) > 2 else np.nan

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        allr = {h: [] for h in (5,10)}
        for w, df in ws.items():
            c = df["close"].values.astype(float)
            for h in allr:
                idx = np.arange(0, len(c)-h, h)
                allr[h] += list(c[idx+h]/c[idx]-1)
        dr = {h: np.mean(v) for h, v in allr.items()}
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            o,hi,lo,c,v = [df[k].values.astype(float) for k in ("open","high","low","close","volume")]
            vm = pd.Series(v).shift(1).rolling(20).mean().values
            vr = v/vm
            body = np.abs(c-o)/o*100
            rng = hi-lo
            clv = np.where(rng>0,(c-lo)/rng,np.nan)
            r20 = pd.Series(c).pct_change(20).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(df)
            for t in range(n):
                if np.isnan(vr[t]) or np.isnan(clv[t]): continue
                rows.append(dict(coin=coin,w=w,t=t,cell=t//5,vr=vr[t],body=body[t],clv=clv[t],
                    r20=r20[t],year=yr[t],
                    x5=(c[t+5]/c[t]-1-dr[5]) if t+5<n else np.nan,
                    x10=(c[t+10]/c[t]-1-dr[10]) if t+10<n else np.nan))
    d = pd.DataFrame(rows)
    out = {}
    hv = d[(d.vr>=2)&(d.body<=1)].dropna(subset=["x5"]).groupby(["coin","w","cell"]).head(1)
    out["heavy_flat_all"] = pd.DataFrame({"mean_x5_pct":[hv.x5.mean()*100],"t5":[tt(hv.x5)],
        "mean_x10_pct":[hv.x10.mean()*100],"t10":[tt(hv.x10)],"n":[len(hv)]})
    out["heavy_flat_by_coin"] = hv.groupby("coin").agg(x5=("x5","mean"),x10=("x10","mean"),n=("x5","size"))
    out["heavy_flat_by_year"] = hv.groupby("year").agg(x5=("x5","mean"),x10=("x10","mean"),n=("x5","size"))
    hv = hv.assign(trend=np.where(hv.r20<0,"after_fall","after_rise"))
    g = hv.groupby("trend")
    out["heavy_flat_by_prior20"] = pd.DataFrame({"x5":g.x5.mean()*100,"t5":g.x5.apply(tt),
        "x10":g.x10.mean()*100,"t10":g.x10.apply(tt),"n":g.size()})
    out["heavy_flat_spearman_vr"] = pd.DataFrame({h:list(stats.spearmanr(hv.dropna(subset=[h]).vr,hv.dropna(subset=[h])[h]))+[hv[h].notna().sum()] for h in ["x5","x10"]},index=["rho","p","n"]).T
    # ordinary flat days: grading by clv
    od = d[(d.vr<2)&(d.body<=1)].dropna(subset=["x5"]).groupby(["coin","w","cell"]).head(1)
    out["ordinary_flat_spearman_clv"] = pd.DataFrame({h:list(stats.spearmanr(od.dropna(subset=[h]).clv,od.dropna(subset=[h])[h]))+[od[h].notna().sum()] for h in ["x5","x10"]},index=["rho","p","n"]).T
    od = od.assign(q=pd.qcut(od.clv,5,labels=False))
    g = od.groupby("q")
    out["ordinary_flat_clv_quintile"] = pd.DataFrame({"x5":g.x5.mean()*100,"t5":g.x5.apply(tt),"x10":g.x10.mean()*100,"t10":g.x10.apply(tt),"n":g.size()})
    out["ordinary_low_quintile_by_coin"] = od[od.q==0].groupby("coin").x5.agg(["mean","count"])
    # all heavy days, any body
    ha = d[d.vr>=2].dropna(subset=["x5"]).groupby(["coin","w","cell"]).head(1)
    out["heavy_any_spearman_clv"] = pd.DataFrame({h:list(stats.spearmanr(ha.dropna(subset=[h]).clv,ha.dropna(subset=[h])[h]))+[ha[h].notna().sum()] for h in ["x5","x10"]},index=["rho","p","n"]).T
    return out
