def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []; day_rows = []; book = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; r1 = c.pct_change()
            sd20 = r1.rolling(20).std()
            z = r1 / sd20
            vr = b["volume"] / b["volume"].rolling(30).mean()
            r5p = c / c.shift(5) - 1
            r20p = c / c.shift(20) - 1
            f5 = c.shift(-5) / c - 1
            f1 = c.shift(-1) / c - 1
            pos = np.arange(len(b))
            df = pd.DataFrame({"coin": coin, "w": w, "z": z, "vr": vr, "sd20": sd20,
                               "r5p": r5p, "r20p": r20p, "f5": f5, "f1": f1,
                               "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "year": pd.to_datetime(b["timestamp"]).dt.year,
                               "grid": pos % 5 == 0})
            rows.append(df)
        for w, d in data["days"][coin].items():
            dd = d[["book_return", "coin_return"]].copy(); dd["coin"] = coin; dd["w"] = w
            book.append(dd)
    A = pd.concat(rows, ignore_index=True)
    g = A[A.grid & A.f5.notna()].copy()
    g["ex5"] = g.f5 - g.groupby("coin").f5.transform("mean")
    A["ex1"] = A.f1 - A.groupby("coin").f1.transform("mean")
    def summ(s):
        s = s.dropna(); n = len(s)
        return pd.Series({"mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan, "n": n})
    out = {}
    gg = g.dropna(subset=["z", "vr"]).copy()
    gg["zq"] = pd.qcut(gg.z, 5, labels=False)
    gg["vq"] = pd.qcut(gg.vr, 3, labels=False)
    out["ex5 by z quintile x vol tercile"] = gg.groupby(["zq", "vq"]).ex5.apply(summ).unstack()
    out["ex5 by z quintile"] = gg.groupby("zq").ex5.apply(summ).unstack()
    out["ex5 by vol tercile"] = gg.groupby("vq").ex5.apply(summ).unstack()
    gs = g.dropna(subset=["sd20"]).copy(); gs["sq"] = pd.qcut(gs.sd20.rank(pct=True), 3, labels=False)
    gs["sq"] = gs.groupby("coin").sd20.transform(lambda x: pd.qcut(x, 3, labels=False))
    out["ex5 by own-coin vol tercile"] = gs.groupby("sq").ex5.apply(summ).unstack()
    for col in ["r5p", "r20p"]:
        gx = g.dropna(subset=[col]).copy()
        gx["q"] = gx.groupby("coin")[col].transform(lambda x: pd.qcut(x, 5, labels=False))
        out[f"ex5 by own-coin {col} quintile"] = gx.groupby("q").ex5.apply(summ).unstack()
        out[f"spearman {col} vs ex5"] = str(stats.spearmanr(gx[col], gx.ex5))
    out["ex1 by weekday"] = A.groupby("wd").ex1.apply(summ).unstack()
    out["ex5 by fc>0 coin"] = g[g.fc >= 2].groupby("coin").ex5.apply(summ).unstack()
    out["ex5 fc>=2 by year"] = g[g.fc >= 2].groupby("year").ex5.apply(summ).unstack()
    B = pd.concat(book, ignore_index=True).dropna()
    out["book vs coin daily by coin"] = B.groupby("coin").agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
                                                             sd_book=("book_return", "std"))
    out["share days flat"] = float((A.alloc.fillna(0).abs() < 1e-9).mean())
    return out
