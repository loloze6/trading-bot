import numpy as np
import pandas as pd
from scipy import stats

def explore(data):
    H = 5
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            n = len(c)
            for i in range(0, n - H, H):
                allr.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(allr) if allr else np.nan
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ret28": c / c.shift(28) - 1,
                "prox": c / c.rolling(28).max(),
                "ret7": c / c.shift(7) - 1,
                "r1": r1,
                "vol20": r1.rolling(20).std(),
                "rng_ratio": ((b["high"] - b["low"]) / c).rolling(5).mean() / ((b["high"] - b["low"]) / c).rolling(40).mean(),
                "volu_ratio": b["volume"].rolling(5).mean() / b["volume"].rolling(40).mean(),
                "fwd": c.shift(-H) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "regime": b["regime"],
                "alloc": b["postRebalance_current_allocation"],
                "pos": np.arange(len(b)),
            })
            df["vol_rank"] = df["vol20"] / df["vol20"].rolling(120, min_periods=40).median()
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    G = A[(A["pos"] % H == 0) & A["fwd"].notna()].copy()
    out = {}

    def bucket(df, col, q=5, name=None):
        d = df.dropna(subset=[col, "ex"]).copy()
        d["q"] = pd.qcut(d[col].rank(method="first"), q, labels=False)
        t = d.groupby("q").agg(lo=(col, "min"), hi=(col, "max"), n=("ex", "size"),
                               mean_ex=("ex", "mean"), sd=("ex", "std"))
        t["t"] = t["mean_ex"] / (t["sd"] / np.sqrt(t["n"]))
        top = d[d["q"] == q - 1]["ex"]; bot = d[d["q"] == 0]["ex"]
        tw = stats.ttest_ind(top, bot, equal_var=False).statistic
        t = t.drop(columns="sd").round(4)
        t.loc["top-bot", "mean_ex"] = round(top.mean() - bot.mean(), 4)
        t.loc["top-bot", "t"] = round(tw, 2)
        return t

    out["ret28 quintiles all"] = bucket(G, "ret28")
    out["prox quintiles trending"] = bucket(G[G["ret28"] > 0], "prox")
    out["prox quintiles falling"] = bucket(G[G["ret28"] <= 0], "prox")
    out["ret28 quint falling, calm(vol_rank<1)"] = bucket(G[(G["ret28"] <= 0) & (G["vol_rank"] < 1)], "ret28")
    out["ret28 quint falling, wild(vol_rank>=1)"] = bucket(G[(G["ret28"] <= 0) & (G["vol_rank"] >= 1)], "ret28")
    out["vol_rank quintiles all"] = bucket(G, "vol_rank")
    out["range ratio quintiles"] = bucket(G, "rng_ratio")
    out["volume ratio quintiles"] = bucket(G, "volu_ratio")
    out["ret7 quintiles all"] = bucket(G, "ret7")
    out["ret7 quintiles trending"] = bucket(G[G["ret28"] > 0], "ret7")
    # weekday, next-day return excess of coin mean daily
    D = A.dropna(subset=["fwd1"]).copy()
    md = D.groupby("coin")["fwd1"].mean()
    D["ex1"] = D["fwd1"] - D["coin"].map(md)
    wd = D.groupby("wd")["ex1"].agg(["size", "mean", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"]))
    out["weekday next-day excess"] = wd.round(5)
    # book: largest gains/losses
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.reset_index(drop=True).copy()
            d["c_prev5"] = d["close"] / d["close"].shift(5) - 1
            d["c_prev28"] = d["close"] / d["close"].shift(28) - 1
            d["win"] = w
            bd.append(d)
    B = pd.concat(bd, ignore_index=True).dropna(subset=["book_return"])
    nz = B[B["book_return"] != 0]
    qs = pd.qcut(nz["book_return"].rank(method="first"), 10, labels=False)
    out["book decile vs prior moves"] = nz.groupby(qs).agg(n=("book_return", "size"),
        book=("book_return", "mean"), coin_same=("coin_return", "mean"),
        prev5=("c_prev5", "mean"), prev28=("c_prev28", "mean")).round(4)
    yr = B.copy()
    out["book by window"] = B.groupby("win").agg(n=("book_return", "size"), mean=("book_return", "mean"),
                                                coin=("coin_return", "mean")).round(5)
    return out
