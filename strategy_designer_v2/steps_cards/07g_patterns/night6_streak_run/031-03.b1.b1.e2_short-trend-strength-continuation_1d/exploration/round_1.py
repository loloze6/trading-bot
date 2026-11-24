import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    rows = []
    daily = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","close","postRebalance_current_allocation","forecast"]].copy().reset_index(drop=True)
            c = d["close"]
            d["r1"] = c.pct_change()
            d["vol"] = d["r1"].rolling(60, min_periods=20).std()
            d["r10"] = c / c.shift(10) - 1
            d["r3"] = c / c.shift(3) - 1
            d["r30"] = c / c.shift(30) - 1
            d["sc10"] = d["r10"] / (d["vol"] * np.sqrt(10))
            d["sc3"] = d["r3"] / (d["vol"] * np.sqrt(3))
            d["sc30"] = d["r30"] / (d["vol"] * np.sqrt(30))
            d["z1"] = d["r1"] / d["vol"]
            d["dd60"] = c / c.rolling(60, min_periods=20).max() - 1
            d["ddz"] = d["dd60"] / d["vol"]
            s = np.sign(d["r1"]).fillna(0)
            st = []
            cur = 0
            for v in s:
                if v == 0: cur = 0
                elif cur * v > 0: cur += v
                else: cur = v
                st.append(cur)
            d["streak"] = st
            d["fwd5"] = c.shift(-5) / c - 1
            d["fwd1"] = c.shift(-1) / c - 1
            d["coin"] = coin; d["win"] = w
            d["pos"] = np.arange(len(d))
            d["wd"] = pd.to_datetime(d["timestamp"]).dt.weekday
            d["year"] = pd.to_datetime(d["timestamp"]).dt.year
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    g = A[(A["pos"] % 5 == 0) & A["fwd5"].notna()].copy()
    drift = g.groupby("coin")["fwd5"].mean()
    g["ex5"] = g["fwd5"] - g["coin"].map(drift)
    drift1 = A.groupby("coin")["fwd1"].mean()
    A["ex1"] = A["fwd1"] - A["coin"].map(drift1)
    # vol level relative to coin median
    medv = A.groupby("coin")["vol"].median()
    g["vrel"] = g["vol"] / g["coin"].map(medv)
    A["vrel"] = A["vol"] / A["coin"].map(medv)

    def summ(df, col, by):
        x = df.dropna(subset=[col, by] if isinstance(by, str) else [col])
        r = x.groupby(by)[col].agg(["mean","std","count"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        r["mean%"] = r["mean"] * 100
        return r[["mean%","t","count"]].round(3)

    out = {}
    for f in ["sc10","sc3","sc30","ddz"]:
        gg = g.dropna(subset=[f]).copy()
        gg["b"] = pd.qcut(gg[f], 6, labels=False)
        out["ex5 by "+f+" sextile"] = summ(gg, "ex5", "b")
    gg = g.copy(); gg["sb"] = gg["streak"].clip(-5,5)
    out["ex5 by streak"] = summ(gg, "ex5", "sb")
    gg = g.dropna(subset=["vrel"]).copy(); gg["vb"] = pd.qcut(gg["vrel"], 4, labels=False)
    out["ex5 by vol quartile"] = summ(gg, "ex5", "vb")
    gg["sb10"] = pd.qcut(gg["sc10"], 3, labels=False)
    out["ex5 by vol x sc10"] = summ(gg, "ex5", ["vb","sb10"])
    aa = A.dropna(subset=["z1","ex1"]).copy(); aa["zb"] = pd.cut(aa["z1"], [-99,-2.5,-1.5,-0.5,0.5,1.5,2.5,99])
    out["ex1 by z1 bucket"] = summ(aa, "ex1", "zb")
    out["r1 by weekday of next day"] = summ(A.assign(wd2=(A["wd"]+1)%7), "ex1", "wd2")
    out["ex5 by year"] = summ(g, "ex5", "year")
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df.copy(); x["coin"] = coin; x["win"] = w; D.append(x)
    D = pd.concat(D, ignore_index=True)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    bd = D.groupby("day")[["book_return","coin_return"]].mean().dropna()
    bd["year"] = pd.to_datetime(bd.index).year
    yr = bd.groupby("year").agg(book=("book_return","mean"), hold=("coin_return","mean"), n=("book_return","count"))
    yr[["book","hold"]] *= 100
    out["book vs hold by year (%/day)"] = yr.round(3)
    # allocation decomposition
    al = A.dropna(subset=["fwd1"]).copy()
    al["gain"] = al["postRebalance_current_allocation"] * al["fwd1"]
    al["mkt"] = al["postRebalance_current_allocation"] * al["coin"].map(drift1)
    out["gain vs market part (%/bar)"] = pd.Series({"gain": al["gain"].mean()*100, "market": al["mkt"].mean()*100, "timing": (al["gain"]-al["mkt"]).mean()*100, "mean alloc": al["postRebalance_current_allocation"].mean()})
    return out
