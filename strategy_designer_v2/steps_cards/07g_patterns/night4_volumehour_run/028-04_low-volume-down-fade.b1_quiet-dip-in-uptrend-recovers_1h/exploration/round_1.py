def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    hourrows = []
    for coin in data["bars"]:
        frames = []
        for w, b in data["bars"][coin].items():
            b = b.copy()
            c = b["close"]
            b["r1"] = c.pct_change()
            b["ma"] = b["r1"].abs().rolling(720, min_periods=240).mean()
            b["z"] = b["r1"] / b["ma"]
            b["vr"] = b["volume"] / b["volume"].rolling(720, min_periods=240).mean()
            b["r168"] = c / c.shift(168) - 1
            b["r24"] = c / c.shift(24) - 1
            b["f6"] = c.shift(-6) / c - 1
            b["f1"] = c.shift(-1) / c - 1
            b["pos"] = np.arange(len(b))
            b["hour"] = pd.to_datetime(b["timestamp"]).dt.hour
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["w"] = w
            frames.append(b)
        a = pd.concat(frames)
        g = a[a["pos"] % 6 == 0].dropna(subset=["f6"])
        drift = g["f6"].mean()
        g = g.assign(u6=g["f6"] - drift, coin=coin)
        rows.append(g)
        h = a.dropna(subset=["f1"]).assign(coin=coin, u1=lambda x: x["f1"] - x["f1"].mean())
        hourrows.append(h)
    G = pd.concat(rows).dropna(subset=["z", "vr"])
    H = pd.concat(hourrows)

    def summ(df, by, col="u6"):
        r = df.groupby(by, observed=True)[col].agg(["mean", "std", "count"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        r["mean"] = r["mean"] * 100
        return r.drop(columns="std").round(3)

    G["zb"] = pd.cut(G["z"], [-99, -4, -2.5, -1, 1, 2.5, 4, 99])
    G["vb"] = pd.cut(G["vr"], [0, 0.67, 1.5, 3, 99])
    out["u6 % by move z x volume ratio"] = summ(G, ["zb", "vb"])
    G["tb"] = pd.cut(G["r168"], [-9, -0.1, -0.03, 0, 0.03, 0.1, 9])
    out["u6 % by 7d return"] = summ(G, ["tb"])
    G["db"] = pd.cut(G["r24"], [-9, -0.05, -0.02, 0, 0.02, 0.05, 9])
    out["u6 % by 24h return"] = summ(G, ["db"])
    G["mab"] = pd.qcut(G["ma"], 4, labels=["v1low", "v2", "v3", "v4high"])
    out["u6 % by vol quartile x zsign"] = summ(G.assign(zs=np.sign(G["z"].clip(-1, 1).round())), ["mab", "zs"])
    out["u1 % by hour (all bars)"] = summ(H, ["hour"], "u1")
    # book
    D = []
    for coin in data["days"]:
        for w, d in data["days"][coin].items():
            D.append(d.assign(coin=coin, w=w))
    D = pd.concat(D).dropna(subset=["book_return"])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["ex"] = D["book_return"]
    out["book daily % by weekday"] = summ(D, ["wd"], "ex")
    T = []
    for coin in data["trades"]:
        for w, t in data["trades"][coin].items():
            T.append(t.assign(coin=coin))
    T = pd.concat(T)
    T["eh"] = pd.to_datetime(T["entry_time"]).dt.hour
    T["fb"] = pd.qcut(T["entry_forecast"], 4, duplicates="drop")
    out["trade net % by entry forecast"] = summ(T, ["fb"], "net_profit_loss_percent")
    T["hb"] = T["eh"] // 4
    out["trade net % by entry 4h block"] = summ(T, ["hb"], "net_profit_loss_percent")
    return out
