import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []
    allret2 = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(20).std()
            z = r1 / vol
            r30 = c / c.shift(30) - 1
            r90 = c / c.shift(90) - 1
            n = len(b)
            for h in [1, 2, 3, 5]:
                b[f"f{h}"] = c.shift(-h) / c - 1
            grid = np.arange(0, n, 2)
            allret2 += list(b.loc[grid, "f2"].dropna())
            fc = b["forecast"].astype(float)
            for i in grid:
                if fc.iloc[i] <= -2:
                    rows.append(dict(coin=coin, w=w, year=pd.Timestamp(b.loc[i, "timestamp"]).year,
                                     fc=fc.iloc[i], z=z.iloc[i], r1=r1.iloc[i], r30=r30.iloc[i], r90=r90.iloc[i],
                                     vol=vol.iloc[i], f1=b.loc[i, "f1"], f2=b.loc[i, "f2"], f3=b.loc[i, "f3"],
                                     f5=b.loc[i, "f5"], alloc=b.loc[i, "postRebalance_current_allocation"]))
    d = pd.DataFrame(rows)
    drift = np.mean(allret2)
    d["u2"] = -(d["f2"] - drift)
    d["s1"] = -d["f1"]; d["s3"] = -d["f3"]; d["s5"] = -d["f5"]
    def agg(g):
        x = g["u2"].dropna()
        return pd.Series(dict(n=len(x), mean_u2=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              mean_s1=g["s1"].mean(), mean_s5=g["s5"].mean(), mean_z=g["z"].mean()))
    out = {}
    out["drift2"] = drift
    out["by_z"] = d.groupby(pd.cut(d["z"], [0, 1, 1.5, 2, 2.5, 3, 10])).apply(agg)
    out["by_fc"] = d.groupby(pd.cut(d["fc"], [-20.1, -19.9, -10, -5, -1.9])).apply(agg)
    out["by_r90"] = d.groupby(pd.qcut(d["r90"], 4)).apply(agg)
    out["by_r30"] = d.groupby(pd.qcut(d["r30"], 4)).apply(agg)
    out["by_vol"] = d.groupby(pd.qcut(d["vol"], 4)).apply(agg)
    out["by_coin"] = d.groupby("coin").apply(agg)
    out["by_year"] = d.groupby("year").apply(agg)
    # book daily
    dl = []
    for coin in days:
        for w, dd in days[coin].items():
            b = bars[coin][w]
            x = dd.copy(); x["coin"] = coin
            al = b.groupby(pd.to_datetime(b["timestamp"]).dt.floor("D"))["postRebalance_current_allocation"].last()
            x["alloc_prev"] = al.shift(1).values[:len(x)] if len(al) == len(x) else np.nan
            x["year"] = pd.to_datetime(x["day"]).dt.year
            dl.append(x)
    D = pd.concat(dl)
    D["state"] = np.where(D["alloc_prev"] < 0, "short", "flat")
    out["book_by_state"] = D.groupby("state").agg(n=("book_return", "count"), mean=("book_return", "mean"),
                                                 coin_mean=("coin_return", "mean"), alloc=("alloc_prev", "mean"))
    out["book_by_year"] = D.groupby("year")["book_return"].agg(["count", "mean", "std"])
    out["book_by_coin"] = D.groupby("coin")["book_return"].agg(["count", "mean", "std"])
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()])
    T["days"] = T["duration_minutes"] / 1440
    out["trades"] = pd.Series(dict(n=len(T), mean_gross=T["profit_loss_percent"].mean(), mean_net=T["net_profit_loss_percent"].mean(),
                                   median_days=T["days"].median(), mean_days=T["days"].mean(), win=(T["profit_loss_percent"] > 0).mean()))
    T["dur"] = pd.cut(T["days"], [0, 1.5, 2.5, 4, 1000])
    out["trades_by_dur"] = T.groupby("dur")[["profit_loss_percent", "net_profit_loss_percent"]].agg(["count", "mean"])
    return out
