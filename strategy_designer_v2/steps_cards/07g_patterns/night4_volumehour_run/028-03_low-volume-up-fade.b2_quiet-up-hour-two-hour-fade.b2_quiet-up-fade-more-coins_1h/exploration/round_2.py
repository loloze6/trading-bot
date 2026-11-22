import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","close","volume"]].copy().reset_index(drop=True)
            d["ret1"] = d["close"].pct_change()
            d["ma"] = d["ret1"].abs().rolling(720, min_periods=240).mean()
            d["z"] = d["ret1"] / d["ma"]
            d["vr"] = d["volume"] / d["volume"].rolling(720, min_periods=240).mean()
            d["r6"] = d["close"]/d["close"].shift(6)-1
            d["z6"] = d["r6"]/(d["ma"]*np.sqrt(6))
            for h in (1,2,4):
                d[f"f{h}"] = d["close"].shift(-h)/d["close"] - 1
            d["pos"] = np.arange(len(d)); d["coin"] = coin; d["win"] = w
            ts = pd.to_datetime(d["timestamp"], utc=True)
            d["hour"] = ts.dt.hour; d["year"] = ts.dt.year
            d["vq"] = d["ret1"].rolling(24).std() / d["ret1"].rolling(720, min_periods=240).std()
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    drift = {h: A[A.pos % h == 0].groupby("coin")[f"f{h}"].mean() for h in (1,2,4)}
    for h in (1,2,4):
        A[f"x{h}"] = A[f"f{h}"] - A["coin"].map(drift[h])
    def g3(s, key, col):
        g = s.groupby(key, observed=True)[col]
        return pd.DataFrame({"n": g.size(), "mean_bp": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.size()))}).round(2)
    S2 = A[A.pos % 2 == 0].dropna(subset=["x2","z","vr"]).copy()
    F = S2[S2.z < -2.5].copy()
    F["vb"] = pd.cut(F.vr, [0,0.8,1.25,2,3,np.inf])
    out["fall z<-2.5 h2 by vol"] = g3(F, "vb", "x2")
    out["fall z<-2.5 h2 by coin"] = g3(F, "coin", "x2")
    out["fall z<-2.5 h2 by year"] = g3(F, "year", "x2")
    F["wn"] = F.win.str[1:].astype(int); F["wg"] = pd.cut(F.wn, [0,6,12,18,24])
    out["fall z<-2.5 h2 by window group"] = g3(F, "wg", "x2")
    F["vqb"] = pd.qcut(F.vq, 3, labels=False, duplicates="drop")
    out["fall z<-2.5 h2 by vol regime tercile"] = g3(F, "vqb", "x2")
    # total move incl drift, falls
    out["fall z<-2.5 h2 raw total bp"] = round(F.f2.mean()*1e4, 2)
    out["fall z<-4 h2 raw total bp"] = round(S2[S2.z < -4].f2.mean()*1e4, 2)
    # 6h cumulative fall -> 2h / 4h
    S4 = A[A.pos % 4 == 0].dropna(subset=["x4","z6"]).copy()
    S4["z6b"] = pd.cut(S4.z6, [-np.inf,-6,-4,-2.5,-1,1,2.5,4,6,np.inf])
    out["h4 by 6h move z"] = g3(S4, "z6b", "x4")
    # within falls, slope on |z|
    out["corr x2 with -z among falls"] = round(np.corrcoef(-F.z.clip(lower=-15), F.x2)[0,1], 4)
    # hour 20-21 effect by year
    S1 = A[A.pos % 1 == 0].dropna(subset=["x1"])
    H = S1[S1.hour.isin([20,21])]
    out["hours 20-21 h1 by year"] = g3(H, "year", "x1")
    out["hours 20-21 h1 by coin"] = g3(H, "coin", "x1")
    return out
