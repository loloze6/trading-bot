def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            c = d["close"].values
            n = len(d)
            d["coin"] = coin; d["win"] = w; d["pos"] = np.arange(n)
            for h in (1, 5, 20):
                f = np.full(n, np.nan)
                if n > h: f[:n-h] = c[h:] / c[:n-h] - 1
                d[f"f{h}"] = f
            r1 = np.full(n, np.nan); r1[1:] = c[1:]/c[:-1]-1
            d["r1"] = r1
            d["r20past"] = pd.Series(c).pct_change(20).values
            d["vol20"] = pd.Series(r1).rolling(20).std().values
            d["dist"] = d.get("debug_info.components.above_ma.last_history_value")
            d["wd"] = pd.to_datetime(d["timestamp"]).dt.dayofweek
            rows.append(d[["coin","win","pos","f1","f5","f20","r1","r20past","vol20","dist","forecast","wd","postRebalance_current_allocation"]])
    B = pd.concat(rows, ignore_index=True)
    mu = B.groupby("coin")["f1"].mean()
    B["mu"] = B["coin"].map(mu)
    B["x20"] = B["f20"] - 20*B["mu"]
    B["x5"] = B["f5"] - 5*B["mu"]
    g20 = B[B["pos"] % 20 == 0].dropna(subset=["x20"])
    g5 = B[B["pos"] % 5 == 0].dropna(subset=["x5"])

    def tab(g, col, ycol, q=5):
        gg = g.dropna(subset=[col, ycol]).copy()
        gg["b"] = gg.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        r = gg.groupby("b")[ycol].agg(["mean","count","std"])
        r["t"] = r["mean"]/(r["std"]/np.sqrt(r["count"]))
        return r.round(4)
    out["dist quintile -> x20"] = tab(g20, "dist", "x20")
    out["dist quintile -> x5"] = tab(g5, "dist", "x5")
    out["past20 ret quintile -> x20"] = tab(g20, "r20past", "x20")
    out["past20 ret quintile -> x5"] = tab(g5, "r20past", "x5")
    out["vol20 quintile -> x20"] = tab(g20, "vol20", "x20")
    out["r1 quintile -> x5"] = tab(g5, "r1", "x5")
    # forecast>0 vs 0
    fp = g20[g20["forecast"]>0]["x20"]; f0 = g20[g20["forecast"]<=0]["x20"]
    out["x20 fc>0 vs fc=0"] = pd.DataFrame({"mean":[fp.mean(),f0.mean()],"n":[len(fp),len(f0)],
        "welch_t":[stats.ttest_ind(fp,f0,equal_var=False).statistic,np.nan]},index=["fc>0","fc=0"]).round(4)
    # dist bucket within above-SMA: sign of dist
    g20b = g20.dropna(subset=["dist"]).copy()
    g20b["above"] = g20b["dist"]>0
    out["x20 by above/below per coin"] = g20b.groupby(["coin","above"])["x20"].agg(["mean","count"]).round(4)
    # weekday daily excess (1-day returns non-overlap trivially)
    B["x1"] = B["f1"]-B["mu"]
    w = B.dropna(subset=["x1"]).groupby("wd")["x1"].agg(["mean","count","std"])
    w["t"] = w["mean"]/(w["std"]/np.sqrt(w["count"]))
    out["weekday x1"] = w.round(5)
    # book: daily returns, gain from market vs timing
    D = []
    for coin, wins in data["days"].items():
        for wn, df in wins.items():
            dd = df.copy(); dd["coin"]=coin; dd["win"]=wn; D.append(dd)
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby("coin").agg(book=("book_return","mean"), coin_r=("coin_return","mean"))
    al = B.groupby("coin")["postRebalance_current_allocation"].mean()
    bk["mean_alloc"] = al; bk["market_part"] = bk["mean_alloc"]*bk["coin_r"]; bk["timing"] = bk["book"]-bk["market_part"]
    out["book by coin"] = bk.round(6)
    # year
    D["year"] = pd.to_datetime(D["day"]).dt.year
    out["book by year"] = D.groupby("year")[["book_return","coin_return"]].mean().round(5)
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    T["dur_d"] = T["duration_minutes"]/1440
    T["db"] = pd.qcut(T["dur_d"].rank(method="first"), 4, labels=False)
    out["trades by duration quartile"] = T.groupby("db").agg(n=("coin","size"), dur=("dur_d","mean"), pl=("net_profit_loss_percent","mean"), win=("net_profit_loss_percent", lambda s:(s>0).mean())).round(3)
    return out
