def explore(data):
    import pandas as pd, numpy as np
    bars, days = data["bars"], data["days"]
    coins = list(days.keys()); wins = list(days[coins[0]].keys())
    out = {}
    feats = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.copy().reset_index(drop=True)
            cl = b["close"]
            r1 = cl.pct_change()
            b["dist"] = cl/cl.rolling(20).mean()-1
            b["ret20"] = cl.pct_change(20)
            b["vol20"] = r1.rolling(20).std()
            hi = cl.rolling(20).max(); lo = cl.rolling(20).min()
            b["pos"] = (cl-lo)/(hi-lo)
            b["dd_hi"] = cl/hi-1
            # bars since 20-bar closing high
            ish = (cl >= hi - 1e-12)
            idx = pd.Series(np.where(ish, np.arange(len(b)), np.nan)).ffill()
            b["bsh"] = np.arange(len(b)) - idx
            b["f5"] = cl.shift(-5)/cl-1
            b["f1"] = cl.shift(-1)/cl-1
            b["grid"] = (np.arange(len(b)) % 5 == 0)
            b["coin"] = c; b["w"] = w
            b["pos_alloc"] = b["postRebalance_current_allocation"]
            feats.append(b[["coin","w","forecast","dist","ret20","vol20","pos","dd_hi","bsh","f5","f1","grid","pos_alloc"]])
    F = pd.concat(feats, ignore_index=True)
    # coin mean 5-bar return over all windows
    cm = F[F["grid"]].groupby("coin")["f5"].mean()
    F["x5"] = F["f5"] - F["coin"].map(cm)
    A = F[(F["forecast"] > 0)].dropna(subset=["f5","dist","vol20","pos"])
    G = A[A["grid"]]
    def summ(g):
        x = g["x5"]; n = len(x)
        return pd.Series({"n": n, "mean_x5_bp": x.mean()*1e4, "t": x.mean()/x.std()*np.sqrt(n) if n>2 else np.nan,
                          "share_lt_-10pct": (g["f5"] < -0.10).mean(), "p5_f5": g["f5"].quantile(0.05)})
    out["by_bsh"] = G.groupby(pd.cut(G["bsh"], [-1,0,2,5,10,20])).apply(summ).round(3)
    out["by_pos"] = G.groupby(pd.cut(G["pos"], [-0.01,0.5,0.75,0.9,0.99,1.0])).apply(summ).round(3)
    out["by_dist"] = G.groupby(pd.qcut(G["dist"], 5)).apply(summ).round(3)
    out["by_vol20"] = G.groupby(pd.qcut(G["vol20"], 5)).apply(summ).round(3)
    out["by_ret20"] = G.groupby(pd.qcut(G["ret20"], 5)).apply(summ).round(3)
    # book daily and deepest 10-day falls
    rows = []
    for w in wins:
        fr = []
        for c in coins:
            d = days[c][w][["day","book_return"]].copy(); d["coin"] = c; fr.append(d)
        df = pd.concat(fr)
        b = df.groupby("day")["book_return"].mean().dropna().reset_index()
        b["w"] = w; b["k"] = np.arange(len(b))//10
        rows.append(b)
    bk = pd.concat(rows)
    blk = bk.groupby(["w","k"])["book_return"].apply(lambda s: (1+s).prod()-1)
    out["book_10d_blocks"] = pd.Series({"n": len(blk), "mean": blk.mean(), "p10": blk.quantile(0.1),
        "worst": blk.min(), "share_of_loss_in_worst10pct": blk[blk <= blk.quantile(0.1)].sum()/blk[blk<0].sum()})
    # daily book: worst days, which state were held coins in (prior close)
    F["day"] = None
    hd = []
    for c in coins:
        for w, b in bars[c].items():
            dd = pd.to_datetime(b["timestamp"]).dt.normalize()
            sub = F[(F["coin"]==c)&(F["w"]==w)].copy()
            sub["d1"] = (dd + pd.Timedelta(days=1)).values
            hd.append(sub)
    H = pd.concat(hd)
    H = H[H["forecast"] > 0].dropna(subset=["f1"])
    H["loss_day"] = H["f1"] < -0.08
    out["held_day_big_loss_share_by_bsh"] = H.groupby(pd.cut(H["bsh"], [-1,0,2,5,10,20]))["loss_day"].agg(["mean","count"]).round(3)
    out["held_day_big_loss_share_by_vol20"] = H.groupby(pd.qcut(H["vol20"], 5))["loss_day"].agg(["mean","count"]).round(3)
    out["held_day_f1_by_ret20"] = (H.groupby(pd.qcut(H["ret20"], 5))["f1"].agg(["mean","std"])*1e4).round(1)
    return out
