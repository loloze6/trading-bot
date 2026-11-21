import numpy as np, pandas as pd

def explore(data):
    out = {}
    H = 24
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr.append(c[idx + H] / c[idx] - 1)
        allr = np.concatenate(allr); drift = allr.mean(); usual = allr.std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            s = pd.Series(c)
            r24 = s.pct_change(24).values; r240 = s.pct_change(240).values
            absr = pd.Series(np.abs(s.pct_change().values))
            vol24 = absr.rolling(24).sum().values; vol240 = absr.rolling(240).sum().values / 10
            f = b["forecast"].values
            for i in np.arange(0, n - H, H):
                if f[i] > 0 and not np.isnan(r24[i]):
                    rows.append(dict(coin=coin, w=w, f=f[i], ex=c[i+H]/c[i]-1-drift, fwd=c[i+H]/c[i]-1,
                                     usual=usual, r240=r240[i], vr=vol24[i]/vol240[i] if vol240[i] > 0 else np.nan))
    d = pd.DataFrame(rows).dropna()
    d["fq"] = pd.qcut(d["f"], 3, labels=False)
    d["rq"] = pd.qcut(d["r240"], 3, labels=False)
    d["vq"] = pd.qcut(d["vr"], 3, labels=False)
    t = lambda s: s.mean() / (s.std() / np.sqrt(len(s)))
    g = d.groupby(["fq", "rq"]).agg(n=("ex", "size"), ex=("ex", "mean"), fwd=("fwd", "mean"))
    g["t"] = d.groupby(["fq", "rq"])["ex"].apply(t)
    out["f_x_r240"] = g
    g = d.groupby(["fq", "vq"]).agg(n=("ex", "size"), ex=("ex", "mean"), fwd=("fwd", "mean"))
    g["t"] = d.groupby(["fq", "vq"])["ex"].apply(t)
    out["f_x_volratio"] = g
    # graded combo: depth of 24h fall x depth of 10-day fall
    d["combo"] = (d["f"] / 10) * np.clip(-d["r240"] / d["usual"], 0, None)
    dc = d[d["combo"] > 0].copy()
    dc["q"] = pd.qcut(dc["combo"], 4, labels=False)
    g = dc.groupby("q").agg(n=("ex", "size"), ex=("ex", "mean"), fwd=("fwd", "mean"))
    g["strength"] = dc.assign(st=dc["ex"] / dc["usual"]).groupby("q")["st"].mean()
    out["combo_quartiles"] = g
    top = d[(d["fq"] == 2) & (d["rq"] == 0)]
    out["deepdeep_by_coin"] = top.groupby("coin")["ex"].agg(["size", "mean"])
    wk = top.groupby("w")["ex"].mean()
    out["deepdeep_windows"] = pd.Series({"windows": len(wk), "share_positive": (wk > 0).mean(), "median": wk.median()})
    # book falls: drawdown of daily mean book return chained
    dr = []
    for coin, wins in data["days"].items():
        for w, dy in wins.items():
            dr.append(dy.assign(coin=coin, w=w))
    D = pd.concat(dr)
    worst = D.groupby(["w", "coin"])["book_return"].apply(lambda s: (1 + s.fillna(0)).cumprod().div((1 + s.fillna(0)).cumprod().cummax()).min() - 1)
    out["worst_dd_by_coin"] = worst.groupby("coin").min()
    out["book_mean_by_coin_bps"] = D.groupby("coin")[["book_return", "coin_return"]].mean().mul(1e4)
    return out
