def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []; hrs = []
    for coin, wins in bars.items():
        tmp = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float); v = df["volume"].astype(float)
            r1 = c.pct_change()
            mar = r1.abs().rolling(720, min_periods=120).mean()
            s = r1 / mar
            vr = v / v.rolling(720, min_periods=120).mean()
            r24 = c / c.shift(24) - 1
            s24 = r24 / (mar * np.sqrt(24))
            volreg = r1.abs().rolling(24).mean() / mar
            f6 = c.shift(-6) / c - 1
            f24 = c.shift(-24) / c - 1
            ts = pd.to_datetime(df["timestamp"])
            g = pd.DataFrame({"coin": coin, "s": s, "vr": vr, "s24": s24, "volreg": volreg,
                              "f6": f6, "f24": f24, "pos": np.arange(len(df)), "hour": ts.dt.hour,
                              "f1": c.shift(-1) / c - 1})
            tmp.append(g)
        g = pd.concat(tmp)
        g6 = g[g["pos"] % 6 == 0].dropna(subset=["f6"])
        d6 = g6["f6"].mean(); sd6 = g6["f6"].std()
        g24 = g[g["pos"] % 24 == 0].dropna(subset=["f24"])
        d24 = g24["f24"].mean(); sd24 = g24["f24"].std()
        g6 = g6.assign(u6=(g6["f6"] - d6) / sd6)
        g24 = g24.assign(u24=(g24["f24"] - d24) / sd24)
        rows.append((g6, g24))
        h = g.dropna(subset=["f1"]); hrs.append(h.assign(u1=(h["f1"] - h["f1"].mean()) / h["f1"].std()))
    G6 = pd.concat([r[0] for r in rows]); G24 = pd.concat([r[1] for r in rows]); H = pd.concat(hrs)
    def summ(df, col, by):
        x = df.dropna(subset=[col] + by)
        a = x.groupby(by, observed=True)[col].agg(["mean", "std", "count"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.drop(columns="std").round(4)
    G6["sb"] = pd.cut(G6["s"], [-np.inf, -4, -2, -1, 1, 2, 4, np.inf])
    G6["vb"] = pd.cut(G6["vr"], [0, 0.67, 1.5, 3, np.inf])
    G24["s24b"] = pd.cut(G24["s24"], [-np.inf, -3, -1.5, -0.5, 0.5, 1.5, 3, np.inf])
    G24["volb"] = pd.qcut(G24["volreg"], 4)
    G6["volb"] = pd.qcut(G6["volreg"], 4)
    out = {}
    out["u6 by 1h move x volume"] = summ(G6, "u6", ["sb", "vb"])
    out["u6 by 1h move"] = summ(G6, "u6", ["sb"])
    out["u24 by 24h scaled return"] = summ(G24, "u24", ["s24b"])
    out["u24 by 24h ret x vol quartile"] = summ(G24, "u24", ["volb", "s24b"]).loc[lambda a: a["count"] > 50]
    out["u1 by hour UTC"] = summ(H, "u1", ["hour"])
    out["u24 by 24h ret, per coin"] = summ(G24.assign(dirr=np.sign(G24["s24"])), "u24", ["coin", "dirr"])
    return out
