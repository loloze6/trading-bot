import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            hh20 = b["high"].rolling(20).max()
            depth = (c - hh20) / hh20 / vol20
            ret_z = r1 / vol20.shift(1)
            pos = np.arange(len(b))
            for h in (1, 3, 5):
                b[f"f{h}"] = c.shift(-h) / c - 1
                b[f"g{h}"] = (pos % h == 0)
            b["depth"] = depth; b["r1"] = r1; b["rz"] = ret_z; b["vol20"] = vol20
            b["ret10"] = c / c.shift(10) - 1
            b["coin"] = coin; b["win"] = w
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["choppy"] = (b["regime"] == "unknown")
            rows.append(b[["coin","win","timestamp","close","depth","r1","rz","vol20","ret10","wd","choppy",
                           "f1","f3","f5","g1","g3","g5","postRebalance_current_allocation"]])
    df = pd.concat(rows, ignore_index=True)
    for h in (1,3,5):
        drift = df[df[f"g{h}"]].groupby("coin")[f"f{h}"].mean()
        df[f"x{h}"] = df[f"f{h}"] - df["coin"].map(drift)
    df["vrank"] = df.groupby("coin")["vol20"].rank(pct=True)
    df["day"] = pd.to_datetime(df["timestamp"]).dt.floor("D")

    def tab(sub, key, h, q=5):
        s = sub[sub[f"g{h}"]].dropna(subset=[key, f"x{h}"]).copy()
        s["bin"] = pd.qcut(s[key].rank(method="first"), q, labels=False)
        g = s.groupby("bin")
        out = pd.DataFrame({"key_mean": g[key].mean(), "n": g.size(),
                            "mean_x": g[f"x{h}"].mean(),
                            "t": g[f"x{h}"].apply(lambda v: v.mean()/(v.std(ddof=1)/np.sqrt(len(v))))})
        return out

    res = {}
    ch = df[df["choppy"]]
    nch = df[~df["choppy"]]
    res["choppy depth quint x1"] = tab(ch, "depth", 1)
    res["choppy depth quint x5"] = tab(ch, "depth", 5)
    res["choppy upday depth x1"] = tab(ch[ch["r1"] > 0], "depth", 1)
    res["choppy downday depth x1"] = tab(ch[ch["r1"] < 0], "depth", 1)
    res["nonchoppy depth quint x5"] = tab(nch, "depth", 5)
    res["all rz quint x1"] = tab(df, "rz", 1)
    res["choppy rz quint x3"] = tab(ch, "rz", 3)
    res["nonchoppy rz quint x3"] = tab(nch, "rz", 3)
    res["choppy hivol depth x5"] = tab(ch[ch["vrank"] > 0.5], "depth", 5)
    res["choppy lovol depth x5"] = tab(ch[ch["vrank"] <= 0.5], "depth", 5)
    res["choppy ret10 quint x5"] = tab(ch, "ret10", 5)
    s = df[df["g1"]].dropna(subset=["x1"])
    g = s.groupby("wd")["x1"]
    res["weekday x1"] = pd.DataFrame({"n": g.size(), "mean": g.mean(),
                                      "t": g.apply(lambda v: v.mean()/(v.std(ddof=1)/np.sqrt(len(v))))})
    # book
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dl.append(d)
    dd = pd.concat(dl)
    bk = dd.groupby("day")[["book_return","coin_return"]].mean().dropna()
    bk["wd"] = pd.to_datetime(bk.index).weekday
    res["book by weekday"] = bk.groupby("wd")["book_return"].agg(["mean","count"])
    bk["year"] = pd.to_datetime(bk.index).year
    res["book by year"] = bk.groupby("year").agg(book=("book_return","mean"), coin=("coin_return","mean"), n=("book_return","size"))
    q = bk["book_return"]
    top = bk[q >= q.quantile(0.98)]; bot = bk[q <= q.quantile(0.02)]
    res["book extremes coin_ret"] = pd.DataFrame({"top_book": [top["book_return"].mean(), top["coin_return"].mean(), len(top)],
                                                  "bot_book": [bot["book_return"].mean(), bot["coin_return"].mean(), len(bot)]},
                                                 index=["book","coin","n"])
    res["corr book coin"] = float(bk[["book_return","coin_return"]].corr().iloc[0,1])
    return res
