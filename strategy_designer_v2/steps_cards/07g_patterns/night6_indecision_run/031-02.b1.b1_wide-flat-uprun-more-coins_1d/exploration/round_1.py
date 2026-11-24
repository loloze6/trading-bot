def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","open","high","low","close"]].copy().reset_index(drop=True)
            if len(d) < 30: continue
            c = d["close"]; rng = (d["high"]-d["low"])
            d["r5"] = c/c.shift(5)-1
            d["r20"] = c/c.shift(20)-1
            d["rr"] = rng/rng.rolling(20).mean()
            d["body"] = (d["close"]-d["open"]).abs()/rng.replace(0,np.nan)
            d["sbody"] = (d["close"]-d["open"])/rng.replace(0,np.nan)
            d["r1"] = c/c.shift(1)-1
            d["vol20"] = d["r1"].rolling(20).std()
            d["vol60"] = d["r1"].rolling(60).std()
            d["clv"] = ((d["close"]-d["low"])/rng.replace(0,np.nan))
            for h in (3,5,10):
                d[f"f{h}"] = c.shift(-h)/c-1
            d["pos"] = np.arange(len(d))
            d["coin"]=coin; d["win"]=w
            d["wd"] = pd.to_datetime(d["timestamp"]).dt.weekday
            d["day"] = pd.to_datetime(d["timestamp"]).dt.floor("D")
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    # drift & usual move per coin on 10-grid
    g10 = A[(A.pos%10==0)].dropna(subset=["f10"])
    st = g10.groupby("coin")["f10"].agg(["mean","std"])
    A = A.join(st, on="coin")
    A["u10"] = (A["f10"]-A["mean"]); A["s10"] = A["u10"]/A["std"]
    A["cell"] = A.pos//10
    def tday(sub, col):
        sub = sub.dropna(subset=[col])
        n = len(sub)
        if n < 5: return pd.Series({"n":n,"days":sub.day.nunique(),"mean":np.nan,"t":np.nan})
        m = sub[col].mean()
        S = (sub[col]-m).groupby(sub["day"]).sum()
        se = np.sqrt((S**2).sum())/n
        return pd.Series({"n":n,"days":sub.day.nunique(),"mean":m,"t":m/se})
    def first_in_cell(mask):
        s = A[mask & A.f10.notna()]
        return s.groupby(["coin","win","cell"]).head(1)
    # event types
    A["z5"] = A["r5"]/(A["vol60"]*np.sqrt(5))
    wide = A.rr>=1.5; flat = A.body<=0.1; narrow = A.rr<=0.8
    ev = {
      "wideflat_up": wide&flat&(A.r5>0),
      "wideflat_down": wide&flat&(A.r5<0),
      "narrowflat_up": narrow&flat&(A.r5>0),
      "narrowflat_down": narrow&flat&(A.r5<0),
      "wide_bull_body_up": wide&(A.sbody>0.5)&(A.r5>0),
      "wide_bear_body_up": wide&(A.sbody<-0.5)&(A.r5>0),
      "wide_bull_body_down": wide&(A.sbody>0.5)&(A.r5<0),
      "wide_bear_body_down": wide&(A.sbody<-0.5)&(A.r5<0),
      "wide_any": wide,
      "all": A.rr.notna(),
    }
    res = {}
    for k,m in ev.items():
        s = first_in_cell(m)
        r = tday(s,"u10"); r["strength"]=s["s10"].mean(); res[k]=r
    out["events_u10"] = pd.DataFrame(res).T
    # grid-sample quintiles
    G = A[(A.pos%10==0)].dropna(subset=["u10","z5","rr","clv"])
    for col in ["z5","rr","clv","sbody","vol20"]:
        G["q"] = pd.qcut(G[col].rank(method="first"),5,labels=False)
        out[f"grid_by_{col}_q"] = G.groupby("q").apply(lambda s: pd.concat([tday(s,"s10"), pd.Series({"x":s[col].median()})]))
    G["z20"] = A.loc[G.index,"r20"]/(A.loc[G.index,"vol60"]*np.sqrt(20))
    G = G.dropna(subset=["z20"])
    G["q"] = pd.qcut(G["z20"].rank(method="first"),5,labels=False)
    out["grid_by_z20_q"] = G.groupby("q").apply(lambda s: tday(s,"s10"))
    return out
