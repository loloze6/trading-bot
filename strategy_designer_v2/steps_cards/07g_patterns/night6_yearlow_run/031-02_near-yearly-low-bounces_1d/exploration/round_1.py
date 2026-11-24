import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            prox = b["debug_info.components.low_prox.last_history_value"].values
            n = len(c)
            lr = np.log(c)
            r1 = np.r_[np.nan, np.diff(lr)]
            for i in range(0, n - 20, 20):
                past20 = c[i]/c[i-20]-1 if i >= 20 else np.nan
                past5 = c[i]/c[i-5]-1 if i >= 5 else np.nan
                vol20 = np.nanstd(r1[i-19:i+1]) if i >= 20 else np.nan
                rows.append(dict(coin=coin, w=w, i=i, prox=prox[i], fwd=c[i+20]/c[i]-1,
                                 fwd5=c[i+5]/c[i]-1, past20=past20, past5=past5, vol20=vol20,
                                 wd=pd.Timestamp(b["timestamp"].iloc[i]).dayofweek,
                                 yr=pd.Timestamp(b["timestamp"].iloc[i]).year))
    df = pd.DataFrame(rows)
    df["D"] = 1/df["prox"] - 1
    df["ex"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    df["ex5"] = df["fwd5"] - df.groupby("coin")["fwd5"].transform("mean")
    out = {}
    def tab(col, q=5, y="ex"):
        d = df.dropna(subset=[col, y]).copy()
        d["g"] = pd.qcut(d[col].rank(method="first"), q, labels=False)
        g = d.groupby("g").agg(lo=(col, "min"), hi=(col, "max"), n=(y, "size"), mean=(y, "mean"), sd=(y, "std"))
        g["t"] = g["mean"]/(g["sd"]/np.sqrt(g["n"]))
        return g
    out["D quintiles ex20"] = tab("D")
    out["past20 quintiles ex20"] = tab("past20")
    out["vol20 quintiles ex20"] = tab("vol20")
    out["past5 quintiles ex5"] = tab("past5", y="ex5")
    out["D quintiles ex5"] = tab("D", y="ex5")
    for col in ["D", "past20", "vol20", "past5"]:
        d = df.dropna(subset=[col, "ex"])
        s = stats.linregress(d[col], d["ex"])
        out[f"reg ex20 on {col}: slope,t,n"] = f"{s.slope:.4f}, {s.slope/s.stderr:.2f}, {len(d)}"
    # new low events (D near 0)
    d = df.copy()
    d["atlow"] = d["D"] < 0.02
    out["at/near low (D<2%) vs rest ex20"] = d.groupby("atlow")["ex"].agg(["size", "mean", "std"])
    # interaction: D x vol
    d = df.dropna(subset=["vol20"]).copy()
    d["vq"] = pd.qcut(d["vol20"], 3, labels=False); d["dq"] = pd.qcut(d["D"], 3, labels=False)
    out["ex20 by Dtercile x voltercile mean"] = d.pivot_table(index="dq", columns="vq", values="ex", aggfunc="mean")
    out["ex20 by Dtercile x voltercile n"] = d.pivot_table(index="dq", columns="vq", values="ex", aggfunc="size")
    d = df.dropna(subset=["past20"]).copy()
    d["pq"] = pd.qcut(d["past20"], 3, labels=False); d["dq"] = pd.qcut(d["D"], 3, labels=False)
    out["ex20 by Dtercile x past20tercile mean"] = d.pivot_table(index="dq", columns="pq", values="ex", aggfunc="mean")
    out["ex20 by coin x Dtercile"] = df.assign(dq=pd.qcut(df["D"], 3, labels=False)).pivot_table(index="coin", columns="dq", values="ex", aggfunc="mean")
    out["ex20 by year"] = df.groupby("yr")["ex"].agg(["size", "mean"])
    # daily coin returns by weekday, book by weekday
    dd = pd.concat([x.assign(coin=c) for c, ws in data["days"].items() for x in ws.values()])
    dd["wd"] = pd.to_datetime(dd["day"]).dt.dayofweek
    g = dd.groupby("wd").agg(n=("coin_return", "count"), coin=("coin_return", "mean"), csd=("coin_return", "std"), book=("book_return", "mean"))
    g["t_coin"] = g["coin"]/(g["csd"]/np.sqrt(g["n"]))
    out["weekday daily"] = g
    return out
