def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            if len(c) < 900:
                continue
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r1 = c.pct_change()
            r24 = c / c.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=360).mean()
            sc24 = r24 / mabs
            r168 = c / c.shift(168) - 1
            sc168 = r168 / (r168.abs().rolling(720, min_periods=360).mean())
            r720 = c / c.shift(720) - 1
            depth = c / c.rolling(720, min_periods=360).max() - 1
            hi = c.rolling(720, min_periods=360).max(); lo = c.rolling(720, min_periods=360).min()
            pos = (c - lo) / (hi - lo)
            vr = r1.rolling(24).std() / r1.rolling(720, min_periods=360).std()
            vlev = r1.rolling(720, min_periods=360).std()
            for h in (72, 168):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(c), h)
                d = pd.DataFrame({"coin": coin, "w": w, "h": h, "fwd": fwd.iloc[idx].values,
                                  "sc24": sc24.iloc[idx].values, "sc168": sc168.iloc[idx].values,
                                  "r720": r720.iloc[idx].values, "depth": depth.iloc[idx].values,
                                  "pos": pos.iloc[idx].values, "vr": vr.iloc[idx].values,
                                  "vlev": vlev.iloc[idx].values,
                                  "wd": ts.iloc[idx].dt.weekday.values, "hr": ts.iloc[idx].dt.hour.values})
                rows.append(d)
    D = pd.concat(rows).dropna(subset=["fwd"])
    g = D.groupby(["coin", "h"])["fwd"]
    D["unus"] = D["fwd"] - g.transform("mean")
    D["str"] = D["unus"] / g.transform("std")
    out = {}
    def tab(var, h, q=5):
        x = D[D.h == h].dropna(subset=[var]).copy()
        x["b"] = x.groupby("coin")[var].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = x.groupby("b").agg(n=("unus", "size"), mean_var=(var, "mean"), unus=("unus", "mean"),
                               strength=("str", "mean"), sd=("unus", "std"))
        t["t"] = t.unus / (t.sd / np.sqrt(t.n))
        return t.drop(columns="sd").round(4)
    for var in ["sc24", "sc168", "r720", "depth", "pos", "vr", "vlev"]:
        for h in (72, 168):
            out[f"{var}_h{h}"] = tab(var, h)
    # per coin rank corr of r720 and sc168 with 168h fwd
    pc = []
    for coin, x in D[D.h == 168].groupby("coin"):
        for var in ["r720", "sc168", "pos", "vlev"]:
            y = x.dropna(subset=[var])
            rho, p = stats.spearmanr(y[var], y["unus"])
            pc.append({"coin": coin, "var": var, "n": len(y), "rho": round(rho, 3), "p": round(p, 3)})
    out["percoin_corr_h168"] = pd.DataFrame(pc)
    x = D[D.h == 72]
    out["weekday_h72"] = x.groupby("wd").agg(n=("unus", "size"), unus=("unus", "mean"), strength=("str", "mean")).round(4)
    # book: daily returns around largest losses
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bd.append(d.assign(coin=coin, w=w))
    B = pd.concat(bd)
    out["book_by_coin"] = B.groupby("coin").agg(mean_book=("book_return", "mean"), mean_coin=("coin_return", "mean"), sd_book=("book_return", "std")).round(5)
    return out
