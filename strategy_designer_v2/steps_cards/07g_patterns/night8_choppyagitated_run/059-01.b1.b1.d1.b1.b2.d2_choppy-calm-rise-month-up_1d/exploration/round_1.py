import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            r7 = c / c.shift(7) - 1
            mabs = r7.abs().rolling(30, min_periods=20).mean()
            sd30 = r1.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "regime": b["regime"].astype(str),
                "fc": b["forecast"].astype(float),
                "s7": r7 / mabs,
                "r1": r1, "r1s": r1 / sd30.shift(1),
                "sd30": sd30,
                "f7": c.shift(-7) / c - 1,
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "ret30": c / c.shift(30) - 1,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    cm7 = A[A.pos % 7 == 0].groupby("coin")["f7"].mean()
    A["x7"] = A["f7"] - A["coin"].map(cm7)
    cm1 = A.groupby("coin")["f1"].mean()
    A["x1"] = A["f1"] - A["coin"].map(cm1)
    G = A[(A.pos % 7 == 0)].dropna(subset=["f7", "s7"])

    def summ(g, col="x7"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    out["grid by regime"] = G.groupby("regime").apply(summ)
    G = G.copy()
    G["s7b"] = pd.cut(G["s7"], [-99, -1.5, -0.75, 0, 0.75, 1.5, 99])
    G["inprof"] = G.regime.isin(["trending", "unknown"])
    out["x7 by s7 bucket, in profile"] = G[G.inprof].groupby("s7b").apply(summ)
    out["x7 by s7 bucket, out profile"] = G[~G.inprof].groupby("s7b").apply(summ)
    out["x7 by s7 bucket, all"] = G.groupby("s7b").apply(summ)
    G["volq"] = G.groupby("coin")["sd30"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["x7 by vol quartile (per coin)"] = G.groupby("volq").apply(summ)
    G["r30b"] = pd.cut(G["ret30"], [-9, -0.2, -0.05, 0.05, 0.2, 9])
    out["x7 by 30d return bucket"] = G.groupby("r30b").apply(summ)
    # daily: big scaled daily moves
    D = A.dropna(subset=["r1s", "f1"]).copy()
    D["r1b"] = pd.cut(D["r1s"], [-99, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 99])
    out["next-day x1 by scaled daily move"] = D.groupby("r1b").apply(lambda g: summ(g, "x1"))
    out["next-3d f3 by scaled daily move (grid3)"] = D[D.pos % 3 == 0].groupby("r1b").apply(lambda g: summ(g, "f3"))
    out["daily coin return by weekday"] = D.groupby("wd").apply(lambda g: summ(g, "x1"))
    out["x7 by year"] = G.groupby("yr").apply(summ)
    # book days
    dd = []
    for coin, wins in days.items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dd.append(d)
    DD = pd.concat(dd)
    DD["day"] = pd.to_datetime(DD["day"])
    bk = DD.groupby("day").agg(br=("book_return", "mean"), cr=("coin_return", "mean")).dropna()
    bk["wd"] = bk.index.weekday
    out["book daily by weekday"] = bk.groupby("wd")["br"].agg(["count", "mean", "std"])
    q = bk["br"].quantile([0.02, 0.98])
    out["book extreme days: coin ret same day"] = pd.Series({
        "n_top": (bk.br >= q[0.98]).sum(), "coin_top": bk.loc[bk.br >= q[0.98], "cr"].mean(),
        "n_bot": (bk.br <= q[0.02]).sum(), "coin_bot": bk.loc[bk.br <= q[0.02], "cr"].mean(),
        "book_total_mean": bk.br.mean()})
    return out
