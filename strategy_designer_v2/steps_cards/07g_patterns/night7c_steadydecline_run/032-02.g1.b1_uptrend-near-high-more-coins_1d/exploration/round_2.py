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
            for i in range(0, len(c) - H, H):
                allr.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(allr) if allr else np.nan
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            rng = (b["high"] - b["low"]) / c
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ret28": c / c.shift(28) - 1,
                "prox": c / c.rolling(28).max(),
                "brk": c / c.shift(1).rolling(27).max() - 1,
                "ret7": c / c.shift(7) - 1,
                "ret14": c / c.shift(14) - 1,
                "rng_ratio": rng.rolling(20).mean() / rng.rolling(90, min_periods=40).mean(),
                "volu_ratio": b["volume"].rolling(20).mean() / b["volume"].rolling(90, min_periods=40).mean(),
                "vol20": r1.rolling(20).std(),
                "fwd": c.shift(-H) / c - 1,
                "pos": np.arange(len(b)),
            })
            df["vol_rank"] = df["vol20"] / df["vol20"].rolling(120, min_periods=40).median()
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    G = A[(A["pos"] % H == 0) & A["fwd"].notna()].copy()
    out = {}

    def bucket(df, col, q=5):
        d = df.dropna(subset=[col, "ex"]).copy()
        d["q"] = pd.qcut(d[col].rank(method="first"), q, labels=False)
        t = d.groupby("q").agg(lo=(col, "min"), hi=(col, "max"), n=("ex", "size"),
                               mean_ex=("ex", "mean"), sd=("ex", "std"))
        t["t"] = t["mean_ex"] / (t["sd"] / np.sqrt(t["n"]))
        top = d[d["q"] == q - 1]["ex"]; bot = d[d["q"] == 0]["ex"]
        t = t.drop(columns="sd").round(4)
        t.loc["top-bot", "mean_ex"] = round(top.mean() - bot.mean(), 4)
        t.loc["top-bot", "t"] = round(stats.ttest_ind(top, bot, equal_var=False).statistic, 2)
        return t

    def corr_by_win(df, col):
        d = df.dropna(subset=[col, "ex"])
        r = d.groupby("win").apply(lambda g: pd.Series({"n": len(g),
              "spearman": stats.spearmanr(g[col], g["ex"]).correlation if len(g) > 5 else np.nan}))
        r.loc["pooled", "n"] = len(d)
        r.loc["pooled", "spearman"] = stats.spearmanr(d[col], d["ex"]).correlation
        return r.round(3)

    T = G[G["ret28"] > 0]
    F = G[G["ret28"] <= 0]
    out["trending prox by window (spearman)"] = corr_by_win(T, "prox")
    out["trending breakout size (brk>0 only)"] = bucket(T[T["brk"] > 0], "brk", 4)
    out["trending brk all quintiles"] = bucket(T, "brk")
    out["falling: ret28 quint, calm range (rng_ratio<1)"] = bucket(F[F["rng_ratio"] < 1], "ret28")
    out["falling: ret28 quint, wide range (rng_ratio>=1)"] = bucket(F[F["rng_ratio"] >= 1], "ret28")
    out["falling: ret28 quint, low volume (volu<1)"] = bucket(F[F["volu_ratio"] < 1], "ret28")
    out["falling: prox>0.64 quintiles"] = bucket(F[F["prox"] > 0.64], "prox")
    out["falling prox>0.64 by window (spearman)"] = corr_by_win(F[F["prox"] > 0.64], "prox")
    out["all: ret28 by window (spearman)"] = corr_by_win(G, "ret28")
    out["trending ret14 quintiles"] = bucket(T, "ret14")
    out["all vol_rank quint in trending"] = bucket(T, "vol_rank")
    out["all vol_rank quint in falling"] = bucket(F, "vol_rank")
    return out
