def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change(); vol20 = r1.rolling(20).std()
            z = r1 / vol20; vr = v / v.rolling(30).mean()
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "win": w, "wn": int(w[1:]), "pos": np.arange(len(b)), "z": z, "vr": vr,
                              "f1": c.shift(-1)/c-1, "f2": c.shift(-2)/c-1, "f3": c.shift(-3)/c-1,
                              "yr": ts.dt.year, "wd": ts.dt.dayofweek, "alloc": b["postRebalance_current_allocation"]})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for h in [1, 2, 3]:
        g = D[D.pos % h == 0]
        D["x%d" % h] = D["f%d" % h] - D.coin.map(g.groupby("coin")["f%d" % h].mean())
    def summ(df, col, by):
        gg = df.dropna(subset=[col]).groupby(by, observed=True)[col]
        out = gg.agg(["mean", "std", "count"]); out["t"] = out["mean"]/(out["std"]/np.sqrt(out["count"]))
        return out.round(4)
    out = {}
    dn = D[(D.z <= -1)].copy()
    dn["vrb"] = pd.cut(dn.vr, [0, 1, 1.5, 2, 3, 99])
    out["x1 after z<=-1 by vol ratio"] = summ(dn, "x1", ["vrb"])
    dn["zb"] = pd.cut(dn.z, [-99, -3, -2, -1])
    hv = dn[dn.vr >= 1.5]
    out["x1 heavy down by fall size"] = summ(hv, "x1", ["zb"])
    out["x1 heavy down by coin"] = summ(hv, "x1", ["coin"])
    out["x1 heavy down by year"] = summ(hv, "x1", ["yr"])
    out["x1 heavy down by window half"] = summ(hv.assign(h=(hv.wn > 12).astype(int)), "x1", ["h"])
    g2 = hv[hv.pos % 2 == 0]; g3 = hv[hv.pos % 3 == 0]
    out["x2 heavy down grid"] = summ(g2.assign(k=1), "x2", ["k"])
    out["x3 heavy down grid"] = summ(g3.assign(k=1), "x3", ["k"])
    sub = dn.dropna(subset=["x1", "vr"])
    out["spearman x1~vr (z<=-1)"] = round(stats.spearmanr(sub.vr, sub.x1)[0], 4)
    out["spearman x1~vr p"] = round(stats.spearmanr(sub.vr, sub.x1)[1], 5)
    up = D[D.z >= 1].copy(); up["vrb"] = pd.cut(up.vr, [0, 1, 1.5, 2, 3, 99])
    out["x1 after z>=1 by vol ratio"] = summ(up, "x1", ["vrb"])
    out["x1 weekday by year-half"] = summ(D.assign(h=(D.wn > 12).astype(int)), "x1", ["wd", "h"]).unstack("h")["t"]
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin)[["book_return", "coin_return"]].assign(coin=coin))
    B = pd.concat(dd).dropna()
    B["active"] = B.book_return.abs() > 1e-9
    out["book active days"] = B.groupby("active")[["book_return", "coin_return"]].agg(["mean", "count"]).round(5)
    return out
