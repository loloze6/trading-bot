import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            r1 = c / c.shift(1) - 1
            nxt = c.shift(-1) / c - 1
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            nl = (b["high"] - c) / rng
            ret20 = c / c.shift(20) - 1
            ret5 = c / c.shift(5) - 1
            vol = r1.rolling(20).std()
            volz = r1 / vol
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "r1": r1, "nxt": nxt, "nl": nl,
                               "ret20": ret20, "ret5": ret5, "rvol": b["sizing_realised_vol"], "volz": volz,
                               "alloc": b["postRebalance_current_allocation"],
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            df["gain"] = df["alloc"] * df["nxt"]
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].mean()
    d["unus"] = d["nxt"] - d["coin"].map(drift)
    dn = d[(d["r1"] < 0) & d["nl"].notna() & d["nxt"].notna()].copy()
    dn["nlq"] = dn.groupby("coin")["nl"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=[1,2,3]))
    dn["szq"] = dn.groupby("coin")["volz"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=["big_fall","mid","small_fall"]))
    dn["tr20"] = pd.cut(dn["ret20"], [-9, -0.1, 0.1, 9], labels=["fall20", "chop20", "rise20"])
    dn["vq"] = dn.groupby("coin")["rvol"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=["lowvol","midvol","hivol"]))
    def agg(g):
        return pd.Series({"n": len(g), "mean_nxt%": 100*g["nxt"].mean(), "unus%": 100*g["unus"].mean(),
                          "t": g["unus"].mean()/(g["unus"].std()/np.sqrt(len(g))), "gain%": 100*g["gain"].mean(),
                          "alloc": g["alloc"].mean(), "sd%": 100*g["nxt"].std()})
    out["by_nl_tercile"] = dn.groupby("nlq").apply(agg)
    out["trend20_x_nl"] = dn.groupby(["tr20","nlq"]).apply(agg)
    out["fallsize_x_nl"] = dn.groupby(["szq","nlq"]).apply(agg)
    out["vol_x_nl"] = dn.groupby(["vq","nlq"]).apply(agg)
    # trend alone on all bars (condition without signal)
    d["tr20"] = pd.cut(d["ret20"], [-9, -0.1, 0.1, 9], labels=["fall20","chop20","rise20"])
    out["all_bars_by_trend20"] = d[d["nxt"].notna()].groupby("tr20").apply(agg)
    out["by_year_nl"] = dn.groupby(["year","nlq"]).apply(agg)
    # book drawdowns
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd[["day","book_return","coin_return"]].copy(); x["win"]=w; x["coin"]=coin; bk.append(x)
    bk = pd.concat(bk)
    bk["wn"] = bk["win"].str[1:].astype(int)
    daily = bk.groupby(["wn","day"])[["book_return","coin_return"]].mean().dropna().sort_index()
    v = (1+daily["book_return"]).cumprod(); dd_ = v/v.cummax()-1
    out["book_maxdd%"] = 100*dd_.min()
    daily["dd"] = dd_.values
    daily["c20"] = daily.groupby(level=0)["coin_return"].transform(lambda s: (1+s).rolling(20).apply(np.prod, raw=True)-1)
    daily["ddbin"] = pd.cut(daily["dd"], [-1,-0.2,-0.1,-0.05,0.001], labels=["<-20","-20..-10","-10..-5",">-5"])
    out["book_by_dd_state"] = daily.groupby("ddbin").agg(n=("book_return","size"), book=("book_return","mean"), coin=("coin_return","mean"), c20=("c20","mean"))
    out["book_by_window"] = daily.groupby(level=0).agg(book=("book_return","mean"), coin=("coin_return","mean"), sd=("book_return","std"), mindd=("dd","min"))
    return out
