def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            if len(b) < 40: continue
            hi = b["high"].rolling(20, min_periods=20).max()
            lo = b["low"].rolling(20, min_periods=20).min()
            b["rp"] = 2*(b["close"]-lo)/(hi-lo)-1
            b["r1"] = b["close"].pct_change()
            b["r5"] = b["close"]/b["close"].shift(5)-1
            b["r20"] = b["close"]/b["close"].shift(20)-1
            b["vol20"] = b["r1"].rolling(20).std()
            b["vol60"] = b["r1"].rolling(60, min_periods=40).std()
            b["vr"] = b["vol20"]/b["vol60"]
            b["f10"] = b["close"].shift(-10)/b["close"]-1
            b["f3"] = b["close"].shift(-3)/b["close"]-1
            b["inprof"] = (b["regime"]=="unknown").astype(int)
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            g = b.iloc[::10].copy()
            g["coin"]=coin; g["w"]=w
            g["day"]=pd.to_datetime(g["timestamp"]).dt.floor("D")
            rows.append(g)
    G = pd.concat(rows)
    G = G.dropna(subset=["f10","rp"])
    drift = G.groupby("coin")["f10"].mean()
    usual = G.groupby("coin")["f10"].std()
    G["ex10"] = G["f10"]-G["coin"].map(drift)
    G["z10"] = G["ex10"]/G["coin"].map(usual)
    def summ(df, key):
        r = df.groupby(key)["ex10"].agg(["count","mean","std"])
        r["t"] = r["mean"]/(r["std"]/np.sqrt(r["count"]))
        r["zmean"]=df.groupby(key)["z10"].mean()
        return r.round(4)
    G["rpq"] = pd.cut(G["rp"], [-1.01,-0.6,-0.2,0.2,0.6,1.01])
    out = {}
    out["rp bucket in profile"] = summ(G[G.inprof==1],"rpq")
    out["rp bucket out profile"] = summ(G[G.inprof==0],"rpq")
    G["vrq"] = pd.qcut(G["vr"], 3, labels=["lowvr","midvr","highvr"])
    G["sig"] = G["rp"]*G["ex10"]
    r = G.groupby(["inprof","vrq"])["sig"].agg(["count","mean","std"]); r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
    out["rp*ex10 by profile x vol ratio"]=r.round(4)
    G["r20q"] = pd.qcut(G["r20"], 5)
    out["ex10 by 20d return quintile all"] = summ(G,"r20q")
    G["r5q"] = pd.qcut(G["r5"], 5)
    out["ex10 by 5d return quintile all"] = summ(G,"r5q")
    out["ex10 by vr tercile all"] = summ(G,"vrq")
    # daily book
    D=[]
    for coin, ws in days.items():
        for w, d in ws.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; D.append(d)
    D=pd.concat(D).dropna(subset=["book_return"])
    bd = D.groupby("day").agg(book=("book_return","mean"), coin=("coin_return","mean"))
    bd["wd"]=pd.to_datetime(bd.index).weekday
    r = bd.groupby("wd")[["book","coin"]].agg(["mean","count"]); out["book by weekday"]=r.round(5)
    bd["yr"]=pd.to_datetime(bd.index).year
    out["book by year"]=bd.groupby("yr")[["book","coin"]].agg(["mean","count"]).round(5)
    return out
