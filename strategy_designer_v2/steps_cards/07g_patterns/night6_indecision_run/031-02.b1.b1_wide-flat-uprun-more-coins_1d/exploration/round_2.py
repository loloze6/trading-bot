def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","open","high","low","close"]].copy().reset_index(drop=True)
            if len(d) < 30: continue
            c = d["close"]; rng = (d["high"]-d["low"])
            mr = rng.rolling(20).mean()
            d["r5"] = c/c.shift(5)-1
            d["rr"] = rng/mr
            d["sbody"] = (d["close"]-d["open"])/rng.replace(0,np.nan)
            d["push"] = (d["close"]-d["open"])/mr   # day's net move in avg ranges
            d["r1"] = c/c.shift(1)-1
            d["vol60"] = d["r1"].rolling(60).std()
            for h in (5,10):
                d[f"f{h}"] = c.shift(-h)/c-1
            d["pos"] = np.arange(len(d))
            d["coin"]=coin; d["win"]=w
            ts = pd.to_datetime(d["timestamp"])
            d["day"] = ts.dt.floor("D"); d["year"] = ts.dt.year
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    g10 = A[(A.pos%10==0)].dropna(subset=["f10"])
    st = g10.groupby("coin")["f10"].agg(["mean","std"])
    A = A.join(st, on="coin")
    A["u10"] = A["f10"]-A["mean"]; A["s10"] = A["u10"]/A["std"]
    A["cell"] = A.pos//10
    A["z5"] = A["r5"]/(A["vol60"]*np.sqrt(5))
    def tday(sub, col):
        sub = sub.dropna(subset=[col]); n = len(sub)
        if n < 5: return pd.Series({"n":n,"days":sub.day.nunique(),"mean":np.nan,"t":np.nan})
        m = sub[col].mean(); S = (sub[col]-m).groupby(sub["day"]).sum()
        se = np.sqrt((S**2).sum())/n
        return pd.Series({"n":n,"days":sub.day.nunique(),"mean":m,"t":m/se})
    def first_in_cell(mask):
        s = A[mask & A.f10.notna()]
        return s.groupby(["coin","win","cell"]).head(1)
    # 1) graded: push (signed day move in avg ranges), all bars, first strongest per cell via grid sample
    G = A[(A.pos%10==0)].dropna(subset=["u10","push","z5"]).copy()
    G["q"] = pd.qcut(G["push"].rank(method="first"),5,labels=False)
    out["grid_by_push_q"] = G.groupby("q").apply(lambda s: pd.concat([tday(s,"u10"), pd.Series({"x":s.push.median()})]))
    # 2) event: large up push (push>=1) -- graded by push, after up and after down 5d
    for nm, m in {"bigup_push_r5up": (A.push>=1)&(A.r5>0),
                  "bigup_push_r5down": (A.push>=1)&(A.r5<=0),
                  "bigdown_push_r5down": (A.push<=-1)&(A.r5<0),
                  "bigdown_push_r5up": (A.push<=-1)&(A.r5>=0)}.items():
        s = first_in_cell(m); out["ev_"+nm] = tday(s,"u10")
    # 3) wide bull body up: by rr level, by z5 level, by year, coins
    s = first_in_cell((A.rr>=1.5)&(A.sbody>0.5)&(A.r5>0)).copy()
    s["rrq"] = pd.qcut(s.rr.rank(method="first"),3,labels=False)
    out["wbu_by_rr"] = s.groupby("rrq").apply(lambda x: pd.concat([tday(x,"u10"),pd.Series({"x":x.rr.median()})]))
    s["zq"] = pd.qcut(s.z5.rank(method="first"),3,labels=False)
    out["wbu_by_z5"] = s.groupby("zq").apply(lambda x: pd.concat([tday(x,"u10"),pd.Series({"x":x.z5.median()})]))
    out["wbu_by_year"] = s.groupby("year").apply(lambda x: tday(x,"u10"))
    pc = s.groupby("coin")["u10"].mean()
    out["wbu_coins_pos_share"] = f"{(pc>0).mean():.2f} of {len(pc)} coins"
    out["wbu_median_u10"] = float(s.u10.median())
    # spearman push vs u10 over all first-in-cell bars with push>0
    from scipy.stats import spearmanr
    p = first_in_cell((A.push>0)&(A.r5>0)).dropna(subset=["push","u10"])
    out["spearman_push_u10_upbars_r5up"] = f"rho {spearmanr(p.push,p.u10)[0]:.3f} n {len(p)}"
    n_ = first_in_cell((A.push<0)&(A.r5<0)).dropna(subset=["push","u10"])
    out["spearman_push_u10_downbars_r5down"] = f"rho {spearmanr(n_.push,n_.u10)[0]:.3f} n {len(n_)}"
    return out
