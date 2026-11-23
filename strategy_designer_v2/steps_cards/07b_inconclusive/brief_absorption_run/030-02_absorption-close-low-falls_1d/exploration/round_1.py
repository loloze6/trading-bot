import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        allr = {h: [] for h in (1,3,5,10)}
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            for h in allr:
                idx = np.arange(0, len(df)-h, h)
                allr[h] += list(c[idx+h]/c[idx]-1)
        drift[coin] = {h: np.mean(v) for h, v in allr.items()}
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            o,hi,lo,c,v = [df[k].values.astype(float) for k in ("open","high","low","close","volume")]
            vm = pd.Series(v).shift(1).rolling(20).mean().values
            vr = v/vm
            body = np.abs(c-o)/o*100
            rng = hi-lo
            clv = np.where(rng>0,(c-lo)/rng,np.nan)
            n=len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for t in range(n):
                if np.isnan(vr[t]) or np.isnan(clv[t]): continue
                rec = dict(coin=coin, w=w, t=t, cell=t//5, vr=vr[t], body=body[t], clv=clv[t], year=yr[t],
                           heavy=(vr[t]>=2) and (body[t]<=1))
                for h in (1,3,5,10):
                    rec[f"x{h}"] = (c[t+h]/c[t]-1-drift[coin][h]) if t+h<n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}
    hv = d[d.heavy].dropna(subset=["x5"])
    hv1 = hv.groupby(["coin","w","cell"]).head(1)
    out["n_heavy_cells"] = len(hv1)
    # by close location tercile on heavy flat days
    hv1 = hv1.assign(clq=pd.cut(hv1.clv,[0,1/3,2/3,1.0001],right=False,labels=["low","mid","high"]))
    g = hv1.groupby("clq")
    res = pd.DataFrame({h: g[h].mean()*100 for h in ["x1","x3","x5","x10"]})
    res["n"]=g.size()
    res["t5"]=g["x5"].apply(lambda s: s.mean()/s.std()*np.sqrt(len(s)))
    res["t10"]=g["x10"].apply(lambda s: s.dropna().mean()/s.dropna().std()*np.sqrt(s.notna().sum()))
    out["heavy_by_clv_excess_pct"]=res
    # correlation of clv with x on heavy days
    cr = {}
    for h in ["x1","x3","x5","x10"]:
        s=hv1.dropna(subset=[h]); r,p=stats.spearmanr(s.clv,s[h]); cr[h]=(round(r,3),round(p,3),len(s))
    out["heavy_spearman_clv_vs_excess"]=pd.DataFrame(cr,index=["rho","p","n"]).T
    # ordinary days comparison
    od = d[(~d.heavy)&(d.body<=1)].dropna(subset=["x5"]).groupby(["coin","w","cell"]).head(1)
    od = od.assign(clq=pd.cut(od.clv,[0,1/3,2/3,1.0001],right=False,labels=["low","mid","high"]))
    g=od.groupby("clq")
    out["flat_ordinary_by_clv"]=pd.DataFrame({"x5":g.x5.mean()*100,"x10":g.x10.mean()*100,"n":g.size(),
        "t5":g.x5.apply(lambda s:s.mean()/s.std()*np.sqrt(len(s)))})
    # by coin and year: low-close heavy days x5
    low=hv1[hv1.clq=="low"]; high=hv1[hv1.clq=="high"]
    out["low_by_coin"]=low.groupby("coin").x5.agg(["mean","count"])
    out["high_by_coin"]=high.groupby("coin").x5.agg(["mean","count"])
    out["low_by_year"]=low.groupby("year").x5.agg(["mean","count"])
    # heavier volume
    hv1=hv1.assign(vq=pd.qcut(hv1.vr,3,labels=["v_lo","v_mid","v_hi"]))
    out["clv_x_vol_x5"]=hv1.pivot_table(index="clq",columns="vq",values="x5",aggfunc="mean")*100
    out["clv_x_vol_n"]=hv1.pivot_table(index="clq",columns="vq",values="x5",aggfunc="count")
    return out
