def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    daysall = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["ret1"] = b["close"].shift(-1) / b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["ret1"]
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["coin"] = coin; b["w"] = w
            b["r10p"] = b["close"] / b["close"].shift(10) - 1
            b["vol20"] = b["close"].pct_change().rolling(20).std()
            rows.append(b[["coin","w","pos","ret1","gain","fee","forecast","r10p","vol20","close"]])
            d = data["days"][coin][w].copy(); d["coin"]=coin; d["w"]=w
            daysall.append(d)
    B = pd.concat(rows, ignore_index=True).dropna(subset=["ret1"])
    D = pd.concat(daysall, ignore_index=True)
    B["side"] = np.sign(B["pos"]).map({1:"long",-1:"short",0:"flat"})
    mu = B.groupby("coin")["ret1"].mean()
    B["mu"] = B["coin"].map(mu)
    B["drift"] = B["pos"]*B["mu"]
    g = B.groupby("side").agg(n=("gain","size"), mean_gain=("gain","mean"), drift=("drift","mean"),
                              mean_ret=("ret1","mean"), mean_pos=("pos","mean"), fee=("fee","mean"))
    out["by_side"] = g
    out["totals"] = pd.Series({"mean_gain": B["gain"].mean(), "drift": B["drift"].mean(),
                               "timing": B["gain"].mean()-B["drift"].mean(), "fee": B["fee"].mean(),
                               "mean_abs_pos": B["pos"].abs().mean(), "share_long": (B["pos"]>0).mean(),
                               "share_short": (B["pos"]<0).mean()})
    # per coin book vs hold
    pc = D.groupby("coin").agg(book=("book_return","mean"), hold=("coin_return","mean"),
                               bsd=("book_return","std"), hsd=("coin_return","std"))
    pc["bS"] = pc.book/pc.bsd*np.sqrt(365); pc["hS"]=pc.hold/pc.hsd*np.sqrt(365)
    out["per_coin"] = pc
    # gain by forecast quintile
    B["fq"] = pd.qcut(B["forecast"].rank(method="first"), 5, labels=False)
    out["by_fq"] = B.groupby("fq").agg(fc=("forecast","mean"), pos=("pos","mean"), ret=("ret1","mean"),
                                       gain=("gain","mean"), fee=("fee","mean"))
    # by vol tercile
    B["vq"] = B.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["by_vol_side"] = B.groupby(["vq","side"]).agg(n=("gain","size"), gain=("gain","mean"), ret=("ret1","mean"), pos=("pos","mean")).reset_index()
    # by window
    out["by_window"] = D.groupby("w").agg(book=("book_return","mean"), hold=("coin_return","mean"))
    return out
