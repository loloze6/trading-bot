import pandas as pd, numpy as np
from scipy import stats

def ct(d, col):
    d = d.dropna(subset=[col])
    n = len(d)
    if n < 5: return pd.Series({"n": n, "days": d["ts"].nunique(), "mean": np.nan, "t": np.nan})
    m = d[col].mean()
    e = (d[col] - m).groupby(d["ts"]).sum()
    se = np.sqrt((e**2).sum()) / n
    return pd.Series({"n": n, "days": d["ts"].nunique(), "mean": m, "t": m/se if se > 0 else np.nan})

def explore(data):
    bars = data["bars"]; out = {}
    drift = {}
    for c, ws in bars.items():
        g = {20: [], 5: [], 1: []}
        for w, df in ws.items():
            cl = df["close"].values; n = len(cl)
            for h in g:
                g[h] += [cl[i+h]/cl[i]-1 for i in range(0, n-h, h)]
        drift[c] = {h: np.mean(v) for h, v in g.items()}
        drift[c]["sd20"] = np.std(g[20], ddof=1)
    frames = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"]; n = len(cl)
            r1 = cl.pct_change()
            sgn = np.sign(r1).fillna(0).values
            st = np.zeros(n)
            for i in range(1, n):
                if sgn[i] == 0: st[i] = 0
                elif sgn[i] == np.sign(st[i-1]): st[i] = st[i-1] + sgn[i]
                else: st[i] = sgn[i]
            f = pd.DataFrame({"coin": c, "win": w, "ts": pd.to_datetime(df["timestamp"]), "pos": np.arange(n),
                              "r1": r1, "streak": st, "fc": df["forecast"], "regime": df["regime"],
                              "alloc": df["postRebalance_current_allocation"]})
            f["vol20"] = r1.rolling(20).std()
            f["z1"] = r1 / f["vol20"].shift(1)
            f["past20"] = cl / cl.shift(20) - 1
            f["past30"] = cl / cl.shift(30) - 1
            for h in (20, 5):
                fw = cl.shift(-h) / cl - 1
                f[f"u{h}"] = np.where(f["pos"] % h == 0, fw - drift[c][h], np.nan)
                f[f"s{h}"] = f[f"u{h}"] / drift[c]["sd20"] if h == 20 else np.nan
            f["u1"] = r1.shift(-1) - drift[c][1]
            frames.append(f)
    A = pd.concat(frames, ignore_index=True)
    A["sb"] = A["streak"].clip(-5, 5)
    out["by streak (clip +-5): u20"] = A.groupby("sb").apply(lambda d: ct(d, "u20"))
    out["by streak: u5"] = A.groupby("sb").apply(lambda d: ct(d, "u5"))
    out["by streak x regime: u20"] = A.groupby(["regime", "sb"]).apply(lambda d: ct(d, "u20"))
    act = A[A["fc"] > 0].copy()
    act["fq"] = act.groupby("coin")["fc"].transform(lambda x: pd.qcut(x.rank(method="first"), 4, labels=False))
    out["active forecast quartile: u20"] = act.groupby("fq").apply(lambda d: ct(d, "u20"))
    A["vq"] = A.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["vol quintile: u20"] = A.groupby("vq").apply(lambda d: ct(d, "u20"))
    out["vol quintile: u5"] = A.groupby("vq").apply(lambda d: ct(d, "u5"))
    A["pq"] = A.groupby("coin")["past20"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["past20 quintile: u20"] = A.groupby("pq").apply(lambda d: ct(d, "u20"))
    out["past20 quintile: u5"] = A.groupby("pq").apply(lambda d: ct(d, "u5"))
    A["zb"] = pd.cut(A["z1"], [-99, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 99])
    out["1d move z bucket: u1"] = A.groupby("zb").apply(lambda d: ct(d, "u1"))
    out["1d move z bucket: u5"] = A.groupby("zb").apply(lambda d: ct(d, "u5"))
    A["wd"] = A["ts"].dt.weekday
    out["weekday: u1 (next day)"] = A.groupby("wd").apply(lambda d: ct(d, "u1"))
    # book by year
    D = []
    for c, ws in data["days"].items():
        for w, df in ws.items():
            d = df.copy(); d["coin"] = c; D.append(d)
    D = pd.concat(D, ignore_index=True)
    D["day"] = pd.to_datetime(D["day"])
    bk = D.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    bk["yr"] = bk.index.year
    out["book vs hold by year (mean daily)"] = bk.groupby("yr").agg(book=("book_return", "mean"), hold=("coin_return", "mean"), n=("book_return", "size"))
    # trades
    T = []
    for c, ws in data["trades"].items():
        for w, df in ws.items():
            if len(df): d = df.copy(); d["coin"] = c; T.append(d)
    T = pd.concat(T, ignore_index=True)
    T["yr"] = pd.to_datetime(T["entry_time"]).dt.year
    out["trades by year"] = T.groupby("yr")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    T["eq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades by entry forecast quartile"] = T.groupby("eq").agg(n=("net_profit_loss_percent", "size"), mean=("net_profit_loss_percent", "mean"), fc=("entry_forecast", "mean"), days=("duration_minutes", lambda x: x.mean()/1440))
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
