def explore(data):
    import numpy as np, pandas as pd
    rows = []
    book = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            r1 = c.pct_change()
            hi = c.rolling(20, min_periods=20).max()
            sd = r1.rolling(20, min_periods=20).std()
            depth = (c / hi - 1) / sd
            tr60 = c / c.shift(60) - 1
            tr20 = c / c.shift(20) - 1
            fwd5 = c.shift(-5) / c - 1
            fwd1 = c.shift(-1) / c - 1
            alloc = b["postRebalance_current_allocation"].astype(float)
            for i in range(0, n, 5):
                if i + 5 >= n:
                    break
                rows.append(dict(coin=coin, w=w, up=r1.iloc[i] > 0, depth=depth.iloc[i],
                                 tr60=tr60.iloc[i], tr20=tr20.iloc[i], fwd5=fwd5.iloc[i],
                                 fc=b["forecast"].iloc[i]))
            pv = b["postRebalance_total_value"].astype(float)
            br = pv.pct_change()
            for i in range(1, n):
                book.append(dict(coin=coin, w=w, br=br.iloc[i], alloc=alloc.iloc[i-1],
                                 cr=c.iloc[i] / c.iloc[i-1] - 1, tr60=tr60.iloc[i-1], tr20=tr20.iloc[i-1]))
    d = pd.DataFrame(rows)
    drift = d.groupby("coin")["fwd5"].mean()
    d["drift"] = d["coin"].map(drift)
    d["unus_short"] = -(d["fwd5"] - d["drift"])
    d["tot_short"] = -d["fwd5"]
    d["trend"] = pd.cut(d["tr60"], [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
    d["t20"] = pd.cut(d["tr20"], [-np.inf, -0.1, 0.0, 0.1, np.inf], labels=["<-10", "-10..0", "0..10", ">10"])
    def summ(g):
        x = g["tot_short"].dropna(); u = g["unus_short"].dropna()
        return pd.Series(dict(n=len(x), tot=x.mean(), t_tot=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,
                              unus=u.mean(), t_un=u.mean()/(u.std()/np.sqrt(len(u))) if len(u)>2 else np.nan))
    d["sig"] = d["up"] & d["depth"].notna() & (d["depth"] < 0)
    d["dq"] = np.where(d["sig"], pd.qcut(d["depth"].where(d["sig"]), 3, labels=False, duplicates="drop"), np.nan)
    out = {}
    out["by_trend_sig"] = d.groupby(["trend", "sig"]).apply(summ)
    out["by_t20_sig"] = d.groupby(["t20", "sig"]).apply(summ)
    out["sig_depth_tercile_by_trend"] = d[d.sig].groupby(["trend", "dq"]).apply(summ)
    out["down_days_by_trend"] = d[(~d.up)].groupby("trend").apply(summ)
    out["sig_by_year_w"] = d[d.sig].groupby("w").apply(summ)
    bk = pd.DataFrame(book)
    bk["trend"] = pd.cut(bk["tr60"], [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
    bk["t20"] = pd.cut(bk["tr20"], [-np.inf, -0.1, 0.0, 0.1, np.inf], labels=["<-10", "-10..0", "0..10", ">10"])
    bk["inpos"] = bk["alloc"].abs() > 1e-6
    out["book_by_trend"] = bk.groupby("trend").agg(n=("br", "size"), mean_br=("br", "mean"), share_in=("inpos", "mean"),
                                                   mean_alloc=("alloc", "mean"), coin_mean=("cr", "mean"))
    out["book_by_t20"] = bk.groupby("t20").agg(n=("br", "size"), mean_br=("br", "mean"), share_in=("inpos", "mean"),
                                               mean_alloc=("alloc", "mean"), coin_mean=("cr", "mean"))
    out["book_nan_trend"] = bk[bk.tr60.isna()].agg({"br": ["size", "mean"]})
    tr = pd.concat([t.assign(coin=c, w=w) for c, ws in data["trades"].items() for w, t in ws.items()])
    out["trades"] = pd.Series(dict(n=len(tr), gross=tr["profit_loss_percent"].mean(), net=tr["net_profit_loss_percent"].mean(),
                                   dur_days=tr["duration_minutes"].mean()/1440, side_short=(tr["side"]=="SHORT").mean()))
    return out
