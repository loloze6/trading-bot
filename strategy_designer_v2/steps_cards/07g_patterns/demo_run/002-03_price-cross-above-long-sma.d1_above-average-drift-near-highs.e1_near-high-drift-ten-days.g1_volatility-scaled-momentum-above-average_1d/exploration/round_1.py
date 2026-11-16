import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    H = 10
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            r10 = c / c.shift(10) - 1
            vsr = r10 / (vol20 * np.sqrt(10))
            r20 = c / c.shift(20) - 1
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(df["timestamp"])
            g = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(df)),
                              "regime": df["regime"].values, "fc": df["forecast"].astype(float).values,
                              "alloc": df["postRebalance_current_allocation"].astype(float).values,
                              "r1": r1.values, "vol20": vol20.values, "vsr": vsr.values, "r10": r10.values,
                              "r20": r20.values, "fwd": fwd.values, "fwd1": fwd1.values,
                              "wd": ts.dt.weekday.values, "yr": ts.dt.year.values})
            rows.append(g)
    A = pd.concat(rows, ignore_index=True)
    cm = A[A.pos % H == 0].groupby("coin")["fwd"].mean()
    A["xfwd"] = A["fwd"] - A["coin"].map(cm)
    G = A[(A.pos % H == 0)].dropna(subset=["xfwd"])
    out = {}
    out["regime share"] = A["regime"].value_counts(normalize=True)
    out["grid xfwd by regime"] = G.groupby("regime")["xfwd"].agg(["mean", "count"])
    def tbin(df, col, q=5, y="xfwd"):
        d = df.dropna(subset=[col, y]).copy()
        d["b"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        s = d.groupby("b")[y].agg(["mean", "count", "std"])
        s["t"] = s["mean"] / (s["std"] / np.sqrt(s["count"]))
        return s
    T = G[G.regime == "trending"]; U = G[G.regime != "trending"]
    out["trend: xfwd by vsr quintile"] = tbin(T, "vsr")
    out["nontrend: xfwd by vsr quintile"] = tbin(U, "vsr")
    out["trend: xfwd by vol20 tercile"] = tbin(T, "vol20", 3)
    out["nontrend: xfwd by vol20 tercile"] = tbin(U, "vol20", 3)
    out["all: xfwd by r20 quintile"] = tbin(G, "r20")
    # slope of xfwd on vsr in non-trending
    def slope(d, x):
        d = d.dropna(subset=[x, "xfwd"])
        res = stats.linregress(d[x], d["xfwd"])
        return pd.Series({"slope": res.slope, "t": res.slope / res.stderr, "n": len(d)})
    out["slopes"] = pd.DataFrame({"trend vsr": slope(T, "vsr"), "nontrend vsr": slope(U, "vsr"),
                                  "trend vol20": slope(T, "vol20"), "nontrend vol20": slope(U, "vol20")}).T
    # per coin trend slope
    out["trend vsr slope by coin"] = pd.DataFrame({c: slope(T[T.coin == c], "vsr") for c in T.coin.unique()}).T
    # daily: next-day return by today's return quintile (all bars, independent-ish 1-bar)
    A["xfwd1"] = A["fwd1"] - A["coin"].map(A.groupby("coin")["fwd1"].mean())
    out["next-day xret by today r1 quintile"] = tbin(A, "r1", 5, "xfwd1")
    out["next-day xret by weekday"] = A.dropna(subset=["xfwd1"]).groupby("wd")["xfwd1"].agg(["mean", "count", "std"]).assign(t=lambda s: s["mean"]/(s["std"]/np.sqrt(s["count"])))
    # book days
    D = []
    for coin, ws in days.items():
        for w, df in ws.items():
            d = df.copy(); d["coin"] = coin; d["w"] = w
            d["wd"] = pd.to_datetime(d["day"]).dt.weekday; d["yr"] = pd.to_datetime(d["day"]).dt.year
            D.append(d)
    D = pd.concat(D, ignore_index=True)
    bk = D.dropna(subset=["book_return"]).groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"), wd=("wd", "first"), yr=("yr", "first")).reset_index()
    out["book by year"] = bk.groupby("yr").agg(br=("br", "mean"), cr=("cr", "mean"), n=("br", "count"), sd=("br", "std"))
    out["book by weekday"] = bk.groupby("wd").agg(br=("br", "mean"), cr=("cr", "mean"), n=("br", "count"))
    q = bk["br"].quantile([0.02, 0.98])
    out["book tails"] = pd.Series({"share of total gain from top2%": bk.loc[bk.br >= q[0.98], "br"].sum() / bk["br"].sum(),
                                   "share from bottom2%": bk.loc[bk.br <= q[0.02], "br"].sum() / bk["br"].sum(),
                                   "skew": stats.skew(bk["br"]), "mean": bk.br.mean()})
    # position size vs xfwd in trending grid
    out["trend: xfwd by forecast>0 quintile"] = tbin(T[T.fc > 0], "fc")
    out["trend fc==0 vs >0"] = T.groupby(T.fc > 0)["xfwd"].agg(["mean", "count"])
    return out
