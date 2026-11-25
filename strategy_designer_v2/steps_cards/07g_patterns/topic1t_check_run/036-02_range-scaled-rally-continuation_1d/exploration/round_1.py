import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    daily = []
    wlen = {}
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            wlen[(coin, w)] = len(b)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rr = ((h - l) / c).rolling(30, min_periods=20).mean()
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "w": w,
                "pos": np.arange(len(b)),
                "s3": (c / c.shift(3) - 1) / rr,
                "s1": r1 / sd30,
                "r60": c / c.shift(60) - 1,
                "r20": c / c.shift(20) - 1,
                "sd30": sd30,
                "f7": c.shift(-7) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "f1": c.shift(-1) / c - 1,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            df["sdrank"] = df["sd30"].rank(pct=True)  # within-window proxy
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out["window_len"] = pd.Series(list(wlen.values())).describe()
    m7 = A[A.pos % 7 == 0].groupby("coin")["f7"].mean()
    A["x7"] = A["f7"] - A["coin"].map(m7)
    m3 = A[A.pos % 3 == 0].groupby("coin")["f3"].mean()
    A["x3"] = A["f3"] - A["coin"].map(m3)
    m1 = A.groupby("coin")["f1"].mean()
    A["x1"] = A["f1"] - A["coin"].map(m1)
    G7 = A[(A.pos % 7 == 0)].dropna(subset=["s3", "x7"]).copy()
    G3 = A[(A.pos % 3 == 0)].dropna(subset=["s3", "x3"]).copy()
    def tab(G, col, y, q=5):
        G = G.copy()
        G["bin"] = pd.qcut(G[col], q, labels=False, duplicates="drop")
        r = G.groupby("bin").agg(lo=(col, "min"), hi=(col, "max"), n=(y, "size"), mean=(y, "mean"), sd=(y, "std"))
        r["t"] = r["mean"] / (r["sd"] / np.sqrt(r["n"]))
        return r.drop(columns="sd").round(4)
    out["s3_quint_x7"] = tab(G7, "s3", "x7")
    out["s3_quint_x3"] = tab(G3, "s3", "x3")
    G1 = A.dropna(subset=["s1", "x1"])
    out["s1_dec_x1"] = tab(G1, "s1", "x1", 10)
    # by trend (60d where available)
    T = G7.dropna(subset=["r60"]).copy()
    T["trend"] = np.where(T.r60 > .1, "rising", np.where(T.r60 < -.1, "falling", "choppy"))
    T["agit"] = np.where(T.sdrank > .5, "agit", "calm")
    T["s3pos"] = np.where(T.s3 > T.s3.quantile(.8), "bigup", np.where(T.s3 < T.s3.quantile(.2), "bigdn", "mid"))
    g = T.groupby(["trend", "s3pos"])["x7"].agg(["size", "mean", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"]))
    out["trend_x_s3_x7"] = g.drop(columns="std").round(4)
    g = T.groupby(["agit", "s3pos"])["x7"].agg(["size", "mean", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"]))
    out["agit_x_s3_x7"] = g.drop(columns="std").round(4)
    # weekday next day
    g = A.dropna(subset=["x1"]).groupby("wd")["x1"].agg(["size", "mean", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"]))
    out["weekday_x1"] = g.drop(columns="std").round(5)
    # vol level next 7
    g = G7.dropna(subset=["sdrank"]).copy(); g["vq"] = pd.qcut(g.sdrank, 4, labels=False)
    r = g.groupby("vq")["x7"].agg(["size", "mean", "std"]); r["t"] = r["mean"] / (r["std"] / np.sqrt(r["size"]))
    out["volq_x7"] = r.drop(columns="std").round(4)
    # 20d return quintile -> x7
    out["r20_quint_x7"] = tab(G7.dropna(subset=["r20"]), "r20", "x7")
    # book days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = bk.groupby(level=0).agg(["mean", "count"]).round(5)
    return out
