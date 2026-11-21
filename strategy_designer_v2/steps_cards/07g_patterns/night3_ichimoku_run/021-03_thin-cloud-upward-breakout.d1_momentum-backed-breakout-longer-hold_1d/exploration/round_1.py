import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    # 1. cross cases: all regime 'trending' bars, split by ret60 sign and by prior vol
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(cl)
            r1 = pd.Series(cl).pct_change()
            vol20 = r1.rolling(20, min_periods=10).std().values
            r20p = pd.Series(cl).pct_change(20).values
            hi = pd.Series(b["high"].values).rolling(30, min_periods=15).max().values
            lo = pd.Series(b["low"].values).rolling(30, min_periods=15).min().values
            for i in np.where(b["regime"].values == "trending")[0]:
                f40 = cl[i+40]/cl[i]-1 if i+40 < n else np.nan
                f20 = cl[i+20]/cl[i]-1 if i+20 < n else np.nan
                rv = b.get("debug_info.components.ret60.last_history_value")
                rows.append(dict(coin=c, win=w, f40=f40, f20=f20, fc=b["forecast"].values[i],
                                 ret60=rv.values[i] if rv is not None else np.nan,
                                 vol=vol20[i], r20=r20p[i],
                                 pos=(cl[i]-lo[i])/(hi[i]-lo[i]) if hi[i] > lo[i] else np.nan))
    cs = pd.DataFrame(rows)
    out["cross_counts"] = cs.groupby(cs.fc > 0).agg(n=("f40", "size"), n40=("f40", "count"),
                                                   mean40=("f40", "mean"), mean20=("f20", "mean"))
    for col in ["vol", "r20", "ret60", "pos"]:
        d = cs.dropna(subset=[col, "f20"])
        if len(d) > 10:
            r, p = stats.spearmanr(d[col], d["f20"])
            out["cross_spear_f20_" + col] = f"rho={r:.3f} p={p:.3f} n={len(d)}"
    # 2. all bars, non-overlapping 20-day grid: forward 20d vs prior 20d return, vol, range position
    g = []
    for c in bars:
        allr = []
        for w, b in bars[c].items():
            cl = b["close"].values; n = len(cl)
            r1 = pd.Series(cl).pct_change()
            vol = r1.rolling(20).std().values
            hi = pd.Series(b["high"].values).rolling(20).max().values
            lo = pd.Series(b["low"].values).rolling(20).min().values
            for i in range(0, n-20, 20):
                if i < 20: continue
                g.append(dict(coin=c, f=cl[i+20]/cl[i]-1, p=cl[i]/cl[i-20]-1, vol=vol[i],
                              pos=(cl[i]-lo[i])/(hi[i]-lo[i]) if hi[i] > lo[i] else np.nan))
    G = pd.DataFrame(g)
    G["fa"] = G["f"] - G.groupby("coin")["f"].transform("mean")
    G["vs"] = G["vol"] / G.groupby("coin")["vol"].transform("median")
    for col in ["p", "vs", "pos"]:
        G["q"] = G.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        t = G.groupby("q")["fa"].agg(["mean", "count", "std"])
        t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
        out["grid20_by_" + col] = t
        r, pv = stats.spearmanr(G[col], G["fa"], nan_policy="omit")
        out["grid20_spear_" + col] = f"rho={r:.3f} p={pv:.4f} n={G[col].notna().sum()}"
    # 3. daily: weekday, and next-day after large moves
    D = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy(); d["coin"] = c; d["win"] = w
            d["wd"] = pd.to_datetime(d["day"]).dt.dayofweek
            d["next"] = d["coin_return"].shift(-1)
            d["z"] = d["coin_return"]/d["coin_return"].rolling(20, min_periods=10).std().shift(1)
            D.append(d)
    D = pd.concat(D)
    t = D.groupby("wd")["coin_return"].agg(["mean", "count", "std"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["weekday_coin"] = t
    D["zq"] = pd.cut(D["z"], [-99, -2, -1, 1, 2, 99])
    t = D.groupby("zq")["next"].agg(["mean", "count", "std"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["next_after_z"] = t
    # 4. book: in vs out, drift vs timing, by year
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    bk = D.groupby(["yr"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    out["by_year"] = bk
    tr = []
    for c in data["trades"]:
        for w, t_ in data["trades"][c].items():
            if len(t_): tr.append(t_.assign(coin=c))
    T = pd.concat(tr)
    out["trades"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
