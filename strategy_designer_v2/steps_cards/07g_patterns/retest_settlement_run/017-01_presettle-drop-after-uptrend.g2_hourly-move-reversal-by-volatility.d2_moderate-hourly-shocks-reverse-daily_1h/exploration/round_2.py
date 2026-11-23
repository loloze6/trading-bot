def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","close","volume","postRebalance_current_allocation"]].copy().reset_index(drop=True)
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            c = d["close"]
            r1 = c/c.shift(1)-1
            d["r1"] = r1
            d["vol24"] = r1.rolling(24).std()
            d["shock"] = d["r1"]/d["vol24"]
            for h in (1,4,8,24,48):
                d[f"f{h}"] = c.shift(-h)/c-1
            d["vrel"] = d["volume"]/d["volume"].rolling(168).mean()
            d["coin"] = coin; d["win"] = w
            d["hour"] = d["timestamp"].dt.hour; d["year"] = d["timestamp"].dt.year
            d["wd"] = d["timestamp"].dt.weekday
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    # drift per coin per horizon: mean over all bars of the coin (approx of grid mean)
    for h in (1,4,8,24,48):
        mu = A.groupby("coin")[f"f{h}"].mean()
        A[f"x{h}"] = A[f"f{h}"] - A["coin"].map(mu)
    def summ(s):
        s = s.dropna(); n=len(s)
        return pd.Series({"n": n, "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(n)) if n>2 else np.nan})
    H0 = A[(A["hour"]==0)].dropna(subset=["shock"]).copy()
    Hx = A[A["hour"].isin([8,16])].dropna(subset=["shock"]).copy()
    for nm, G in (("hour0", H0), ("hours8_16", Hx)):
        G["sb"] = pd.cut(G["shock"], [-99,-3,-2,-1,-0.5,0,0.5,1,2,3,99])
        out[f"{nm}: x24 by shock bucket"] = G.groupby("sb", observed=True)["x24"].apply(summ).unstack()
    # horizons for hour 0, |shock|<3, fade in shock direction scaled
    H0m = H0[H0["shock"].abs()<3].copy()
    hz = {}
    for h in (1,4,8,24,48):
        hz[h] = summ(-np.sign(H0m["shock"])*H0m[f"x{h}"])
    out["hour0 |shock|<3: fade by horizon"] = pd.DataFrame(hz).T
    out["hour0 fade24 by year"] = H0m.groupby("year").apply(lambda g: summ(-np.sign(g["shock"])*g["x24"])).unstack() if False else H0m.groupby("year").apply(lambda g: summ(-np.sign(g["shock"])*g["x24"]))
    out["hour0 fade24 by coin"] = H0m.groupby("coin").apply(lambda g: summ(-np.sign(g["shock"])*g["x24"]))
    out["hour0 fade24 by weekday"] = H0m.groupby("wd").apply(lambda g: summ(-np.sign(g["shock"])*g["x24"]))
    # mean abs shock and rel volume by hour
    out["by hour: mean |shock|, mean vrel"] = A.groupby("hour").agg(abs_shock=("shock", lambda s: s.abs().mean()), vrel=("vrel","mean"))
    # graded: correlation of shock with x24 at hour 0 by shock-magnitude terciles
    H0m["tq"] = pd.qcut(H0m["shock"].abs(), 3, labels=False)
    out["hour0 fade24 by |shock| tercile"] = H0m.groupby("tq").apply(lambda g: summ(-np.sign(g["shock"])*g["x24"]))
    # fade24 of hour0 return scaled raw (not sign): regression slope t
    s = H0m.dropna(subset=["x24"])
    b = np.polyfit(s["shock"], s["x24"], 1)
    out["hour0 slope x24 on shock"] = float(b[0])
    return out
