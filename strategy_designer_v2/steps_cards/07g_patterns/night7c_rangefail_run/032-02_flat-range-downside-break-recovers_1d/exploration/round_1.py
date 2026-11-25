def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); h = df["high"].astype(float); l = df["low"].astype(float); v = df["volume"].astype(float)
            r = c.pct_change()
            f = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(df)),
                              "day": pd.to_datetime(df["timestamp"]).dt.floor("D"),
                              "wd": pd.to_datetime(df["timestamp"]).dt.weekday})
            f["ret1"] = r
            f["ret3"] = c / c.shift(3) - 1
            f["ret10"] = c / c.shift(10) - 1
            f["ret20"] = c / c.shift(20) - 1
            f["vol20"] = r.rolling(20).std()
            f["volchg"] = r.rolling(5).std() / r.rolling(20).std()
            lo20 = l.shift(1).rolling(20).min(); hi20 = h.shift(1).rolling(20).max()
            f["rangepos20"] = (c - lo20) / (hi20 - lo20)
            f["er20"] = (c - c.shift(20)).abs() / c.diff().abs().rolling(20).sum()
            f["vratio"] = v / v.shift(1).rolling(20).mean()
            f["clv"] = ((c - l) / (h - l)).where(h > l)
            f["barrange"] = (h - l) / c
            f["below20low"] = (c / lo20 - 1).clip(upper=0)
            f["above20high"] = (c / hi20 - 1).clip(lower=0)
            for H in (3, 10):
                f[f"fwd{H}"] = c.shift(-H) / c - 1
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def analyse(H):
        g = A[A["pos"] % H == 0].dropna(subset=[f"fwd{H}"]).copy()
        g["ex"] = g[f"fwd{H}"] - g.groupby("coin")[f"fwd{H}"].transform("mean")
        g["usual"] = g.groupby("coin")[f"fwd{H}"].transform("std")
        res = []
        feats = ["ret1","ret3","ret10","ret20","vol20","volchg","rangepos20","er20","vratio","clv","barrange","below20low","above20high"]
        for ft in feats:
            s = g.dropna(subset=[ft]).copy()
            s["q"] = s.groupby("coin")[ft].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
            s["z"] = s.groupby("coin")[ft].transform(lambda x: (x.rank()-x.rank().mean())/x.rank().std())
            # day-clustered slope t of ex on z
            s["xy"] = s["z"] * s["ex"]
            beta = (s["z"]*s["ex"]).sum()/(s["z"]**2).sum()
            s["u"] = s["z"]*(s["ex"]-beta*s["z"])
            G = s.groupby("day")["u"].sum()
            se = np.sqrt((G**2).sum()*len(G)/(len(G)-1))/(s["z"]**2).sum()
            qm = s.groupby("q")["ex"].mean()
            d = {"feat": ft, "n": len(s), "days": len(G), "beta%": beta*100, "t_cl": beta/se}
            for q in range(5): d[f"q{q}%"] = qm.get(q, np.nan)*100
            res.append(d)
        return pd.DataFrame(res).round(3)
    out["H10 features"] = analyse(10)
    out["H3 features"] = analyse(3)
    g = A[A["pos"] % 3 == 0].dropna(subset=["fwd3"]).copy()
    g["ex"] = g["fwd3"] - g.groupby("coin")["fwd3"].transform("mean")
    out["H3 weekday"] = g.groupby("wd")["ex"].agg(["mean","count", lambda x: x.mean()/x.std()*np.sqrt(len(x))]).round(4)
    out["H10 by coin mean fwd"] = A[A["pos"]%10==0].groupby("coin")["fwd10"].agg(["mean","std","count"]).round(4)
    return out
