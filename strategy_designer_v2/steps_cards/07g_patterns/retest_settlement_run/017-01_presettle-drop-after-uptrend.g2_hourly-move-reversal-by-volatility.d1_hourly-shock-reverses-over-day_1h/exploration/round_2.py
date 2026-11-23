def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = df[["timestamp","close","volume"]].copy().reset_index(drop=True)
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            c = d["close"]; r1 = c.pct_change()
            v24 = r1.rolling(24).std()
            d["z1"] = r1 / v24
            d["vlev"] = v24 / r1.rolling(720, min_periods=200).std()
            d["volr"] = d["volume"]/d["volume"].rolling(168).median()
            for h in (4,8,24,48):
                d[f"f{h}"] = c.shift(-h)/c - 1
            d["hour"] = d["ts"].dt.hour; d["year"] = d["ts"].dt.year; d["wd"]=d["ts"].dt.weekday
            d["coin"] = coin; d["win"] = w
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    for h in (4,8,24,48):
        A[f"e{h}"] = A[f"f{h}"] - A.groupby("coin")[f"f{h}"].transform("mean")
    H0 = A[A["hour"]==0].dropna(subset=["z1","e24"]).copy()
    Hx = A[A["hour"]!=0].dropna(subset=["z1","e24"]).copy()
    def sl(s, y="e24", x="z1"):
        s = s.dropna(subset=[x,y])
        r = stats.linregress(s[x], s[y]); return pd.Series({"slope_pct": r.slope*100, "t": r.slope/r.stderr, "n": len(s)})
    out["hour0 slope by horizon"] = pd.DataFrame({f"h{h}": sl(H0, f"e{h}") for h in (4,8,24,48)}).T.round(3)
    out["hour0 slope by coin"] = H0.groupby("coin").apply(sl).round(3)
    out["hour0 slope by year"] = H0.groupby("year").apply(sl).round(3)
    H0["vb"] = pd.qcut(H0["vlev"], 3, labels=["low","mid","high"])
    out["hour0 slope by vol tercile"] = H0.groupby("vb").apply(sl).round(3)
    out["other hours slope by year"] = Hx.groupby("year").apply(sl).round(3)
    # size: hour0 signal-side move by |z1| quintile
    H0["side"] = -np.sign(H0["z1"])
    H0["mv"] = H0["side"]*H0["e24"]; H0["tot"] = H0["side"]*H0["f24"]
    H0["q"] = pd.qcut(H0["z1"].abs(), 5, labels=False)
    out["hour0 signed move by |z1| quintile"] = H0.groupby("q").agg(absz=("z1", lambda s: s.abs().mean()),
        unusual_pct=("mv", lambda s: s.mean()*100), total_pct=("tot", lambda s: s.mean()*100),
        t=("mv", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))), n=("mv","size")).round(3)
    H0h = H0[H0["vb"]=="high"]
    out["hour0 high-vol signed move by |z1| tercile"] = H0h.groupby(pd.qcut(H0h["z1"].abs(),3,labels=False)).agg(
        unusual_pct=("mv", lambda s: s.mean()*100), t=("mv", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))), n=("mv","size")).round(3)
    # hour 0 by weekday (does the Monday/Friday weekend boundary drive it)
    out["hour0 slope by weekday"] = H0.groupby("wd").apply(sl).round(3)
    # neighbouring hours 22,23,0,1 slope with 4-hour return as situation? hour0 volume interaction
    H0["vq"] = pd.qcut(H0["volr"], 3, labels=["lowV","midV","highV"])
    out["hour0 slope by volume tercile"] = H0.groupby("vq").apply(sl).round(3)
    # whole day: does the 00-01 move reverse within the hour-0 cases but what of 8h settlement hours 8,16 (z1 at hour 8,16)
    out["slope at 8 and 16 h24"] = pd.DataFrame({hr: sl(A[A["hour"]==hr]) for hr in (7,8,15,16,23)}).T.round(3)
    return out
