import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        grids = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            v = b["volume"].astype(float).values
            n = len(c)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            absr = pd.Series(np.abs(r1)).rolling(180, min_periods=90).mean().values
            # signed streak (count of same-direction closes) and its loss from start
            sgn = np.sign(np.nan_to_num(r1))
            cnt = np.zeros(n); start = np.zeros(n, dtype=int)
            for i in range(1, n):
                if sgn[i] != 0 and sgn[i] == sgn[i-1]:
                    cnt[i] = cnt[i-1] + 1; start[i] = start[i-1]
                else:
                    cnt[i] = 1 if sgn[i] != 0 else 0; start[i] = i - 1
            streak_ret = c / c[start] - 1
            streak_um = streak_ret / absr
            ret30 = np.full(n, np.nan); ret30[180:] = c[180:] / c[:-180] - 1
            ret1d = np.full(n, np.nan); ret1d[6:] = c[6:] / c[:-6] - 1
            ret3d = np.full(n, np.nan); ret3d[18:] = c[18:] / c[:-18] - 1
            vol30 = pd.Series(r1).rolling(180, min_periods=90).std().values
            vratio = pd.Series(v).rolling(6).mean().values / pd.Series(v).rolling(180, min_periods=90).mean().values
            ts = pd.to_datetime(b["timestamp"])
            for t in range(0, n - H, H):
                grids.append(dict(coin=coin, w=w, fwd=c[t+H]/c[t]-1, streak_um=streak_um[t], cnt=cnt[t]*sgn[t],
                                  ret30=ret30[t], ret1d=ret1d[t], ret3d=ret3d[t], vol30=vol30[t], vratio=vratio[t],
                                  hour=ts.iloc[t].hour, wd=ts.iloc[t].weekday(), fc=b["forecast"].iloc[t]))
        g = pd.DataFrame(grids)
        g["usual"] = g["fwd"].std(); g["drift"] = g["fwd"].mean()
        g["s"] = (g["fwd"] - g["drift"]) / g["usual"]
        g["ret3d_z"] = g["ret3d"] / g["usual"]
        g["ret1d_z"] = g["ret1d"] / g["usual"]
        g["ret30_z"] = g["ret30"] / (g["usual"] * np.sqrt(10))
        g["vol_rank"] = g["vol30"].rank(pct=True)
        rows.append(g)
    G = pd.concat(rows, ignore_index=True)
    out = {}
    def q(col, k=5):
        d = G.dropna(subset=[col, "s"]).copy()
        d["q"] = pd.qcut(d[col].rank(method="first"), k, labels=False)
        a = d.groupby("q").agg(n=("s", "size"), mean_s=("s", "mean"), sd=("s", "std"), xmean=(col, "mean"))
        a["t"] = a["mean_s"] / (a["sd"] / np.sqrt(a["n"]))
        return a.drop(columns="sd").round(4)
    def slope(col, d=None):
        d = (G if d is None else d).dropna(subset=[col, "s"])
        res = []
        for coin, x in list(d.groupby("coin")) + [("ALL", d)]:
            lr = stats.linregress(x[col], x["s"])
            res.append(dict(coin=coin, n=len(x), slope=lr.slope, t=lr.slope / lr.stderr))
        return pd.DataFrame(res).set_index("coin").round(4)
    for col in ["ret30_z", "ret3d_z", "ret1d_z", "streak_um", "vratio", "vol_rank"]:
        out["q_" + col] = q(col)
        out["slope_" + col] = slope(col)
    neg = G[G["ret30"] < 0]
    out["slope_ret3d_z_in_neg_month"] = slope("ret3d_z", neg)
    out["slope_ret3d_z_in_pos_month"] = slope("ret3d_z", G[G["ret30"] >= 0])
    h = G.groupby("hour")["s"].agg(["size", "mean", "std"]); h["t"] = h["mean"] / (h["std"] / np.sqrt(h["size"]))
    out["by_hour"] = h.round(4)
    d = G.groupby("wd")["s"].agg(["size", "mean", "std"]); d["t"] = d["mean"] / (d["std"] / np.sqrt(d["size"]))
    out["by_weekday"] = d.round(4)
    # book daily
    D = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            D.append(x.assign(coin=coin, w=w))
    D = pd.concat(D)
    out["book_by_coin"] = D.groupby("coin").agg(book=("book_return", "mean"), coin_r=("coin_return", "mean"),
                                                 corr=("book_return", lambda s: s.corr(D.loc[s.index, "coin_return"]) if False else np.nan)).round(6)
    out["corr_book_coin"] = float(D[["book_return", "coin_return"]].corr().iloc[0, 1])
    return out
