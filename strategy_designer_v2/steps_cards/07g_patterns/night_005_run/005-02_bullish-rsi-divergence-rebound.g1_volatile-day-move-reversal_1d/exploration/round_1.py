def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.copy().reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            mabs = r.abs().shift(1).rolling(60, min_periods=20).mean()
            z = r / mabs
            vol20 = r.rolling(20).std()
            vrank = vol20.rolling(100, min_periods=30).apply(lambda x: (x[-1] >= x).mean(), raw=True)
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            f1 = c.shift(-1) / c - 1
            f3 = c.shift(-3) / c - 1
            f7 = c.shift(-7) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "r": r, "z": z, "vrank": vrank,
                              "r5": r5, "r20": r20, "f1": f1, "f3": f3, "f7": f7, "wd": ts.dt.weekday,
                              "regime": b["regime"], "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                              "rng": (b["high"] - b["low"]) / c, "vol": b["volume"]})
            d["volz"] = np.log(d["vol"] / d["vol"].shift(1).rolling(30, min_periods=10).mean())
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    g3 = D[D.pos % 3 == 0].dropna(subset=["f3", "z"]).copy()
    g3["ex3"] = g3["f3"] - g3.groupby("coin")["f3"].transform("mean")
    g3["hv"] = np.where(g3.vrank >= 0.5, "hiVol", "loVol")
    g3["zq"] = pd.qcut(g3.z, 5, labels=False)
    out["ex3 by z quintile x vol"] = g3.groupby(["hv", "zq"])["ex3"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # signed fade return by up/down
    g3["fade"] = -np.sign(g3.z) * g3.ex3
    g3["big"] = g3.z.abs() > g3.z.abs().quantile(0.8)
    out["fade ret big moves by dir x vol"] = g3[g3.big].groupby([np.sign(g3.z[g3.big]), "hv"])["fade"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # 20-day trend context
    g3["r20q"] = pd.qcut(g3.r20, 3, labels=["dn", "mid", "up"])
    out["fade ret big moves by r20 tercile"] = g3[g3.big].groupby("r20q")["fade"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # range / volume context on big moves
    gb = g3[g3.big].dropna(subset=["volz"])
    gb["vq"] = pd.qcut(gb.volz, 2, labels=["lowVolu", "hiVolu"])
    out["fade ret big moves by volume"] = gb.groupby("vq")["fade"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # 7-day horizon fade on grid of 7
    g7 = D[D.pos % 7 == 0].dropna(subset=["f7", "z"]).copy()
    g7["ex7"] = g7.f7 - g7.groupby("coin")["f7"].transform("mean")
    g7["zq"] = pd.qcut(g7.z, 5, labels=False)
    out["ex7 by z quintile"] = g7.groupby("zq")["ex7"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # 5-day return momentum/reversal on 3-day grid
    g3["r5q"] = pd.qcut(g3.r5, 5, labels=False)
    out["ex3 by r5 quintile"] = g3.groupby("r5q")["ex3"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # weekday daily returns
    g1 = D.dropna(subset=["f1"])
    out["next-day ret by weekday"] = g1.groupby("wd")["f1"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # book decomposition
    dd = []
    for coin in days:
        for w, x in days[coin].items():
            dd.append(x.assign(coin=coin, w=w))
    DD = pd.concat(dd, ignore_index=True)
    B = DD.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book vs coin daily"] = pd.Series({"book_mean": B.book_return.mean(), "coin_mean": B.coin_return.mean(),
        "corr": B.book_return.corr(B.coin_return), "book_sh": B.book_return.mean()/B.book_return.std()*np.sqrt(365),
        "coin_sh": B.coin_return.mean()/B.coin_return.std()*np.sqrt(365)})
    D["gain"] = D.alloc * D.f1
    mc = D.groupby("coin")["f1"].mean()
    D["mkt"] = D.alloc * D.coin.map(mc)
    out["gain decomposition per bar"] = pd.Series({"gain": D.gain.mean(), "mkt": D.mkt.mean(), "timing": D.gain.mean()-D.mkt.mean(), "mean_alloc": D.alloc.mean(), "share_long": (D.alloc>0).mean(), "share_short": (D.alloc<0).mean()})
    out["gain by side"] = D.groupby(np.sign(D.alloc))["gain"].agg(["mean", "sum", "count"])
    out["gain by year"] = D.groupby(pd.to_datetime(pd.concat([b["timestamp"] for c in bars for b in bars[c].values()], ignore_index=True)).dt.year.values)["gain"].agg(["mean","sum","count"])
    return out
