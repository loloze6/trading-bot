def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    days = data["days"]; bars = data["bars"]
    # coin mean daily return over all windows
    rows = []
    for c in bars:
        allc = pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        cm = allc.mean()
        for w in bars[c]:
            b = bars[c][w].copy()
            d = days[c][w]
            b["ret1"] = b["close"].shift(-1)/b["close"]-1
            b["ret3"] = b["close"].shift(-3)/b["close"]-1
            b["pos"] = b["postRebalance_current_allocation"]
            b["coin"] = c; b["win"] = w; b["cm"] = cm
            b["vr"] = b["volume"]/b["volume"].rolling(30, min_periods=30).mean()
            b["r30"] = b["close"]/b["close"].shift(30)-1
            b["near"] = b["close"]/b["high"].rolling(30).max()
            b["idx"] = np.arange(len(b))
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    B["gain"] = B["pos"]*B["ret1"]
    B["mkt"] = B["pos"]*B["cm"]
    out["pos summary"] = B["pos"].describe()
    out["forecast summary"] = B["forecast"].describe()
    out["share long/short/flat"] = pd.Series({"long": (B.pos>0.01).mean(), "short": (B.pos<-0.01).mean(), "flat": (B.pos.abs()<=0.01).mean()})
    out["gain mean, mkt part, timing"] = pd.Series({"gain": B.gain.mean(), "mkt": B.mkt.mean(), "timing": B.gain.mean()-B.mkt.mean(), "coin mean": B.ret1.mean()})
    # grid of 3
    G = B[B.idx % 3 == 0].dropna(subset=["ret3", "forecast"]).copy()
    G["ex"] = G["ret3"] - G.groupby("coin")["ret3"].transform("mean")
    s = stats.linregress(G.forecast, G.ex)
    out["slope ex3 on forecast"] = pd.Series({"slope": s.slope, "t": s.slope/s.stderr, "n": len(G)})
    G["fbin"] = pd.qcut(G.forecast, 5, labels=False, duplicates="drop")
    out["by forecast quintile"] = G.groupby("fbin").agg(fmean=("forecast", "mean"), ex3=("ex", "mean"), n=("ex", "size"), pos=("pos", "mean"))
    G["vbin"] = pd.qcut(G.vr, 5, labels=False)
    out["by volratio quintile"] = G.groupby("vbin").agg(vr=("vr", "mean"), ex3=("ex", "mean"), r1today=("r30", "mean"), n=("ex", "size"))
    # heavy volume split by today's return sign
    G["d1"] = G.groupby(["coin", "win"])["close"].transform(lambda x: x)  # placeholder
    B["today"] = B.groupby(["coin", "win"])["close"].pct_change()
    G["today"] = B.loc[G.index, "today"]
    G["upday"] = G.today > 0
    out["ex3 by vr quintile x up/down day"] = G.groupby(["vbin", "upday"])["ex"].agg(["mean", "size"]).unstack()
    G["r30pos"] = G.r30 > 0
    out["ex3 by vr quintile x 30d trend"] = G.groupby(["vbin", "r30pos"])["ex"].agg(["mean", "size"]).unstack()
    # book daily
    D = []
    for c in days:
        for w in days[c]:
            d = days[c][w].copy(); d["coin"] = c; d["win"] = w; D.append(d)
    D = pd.concat(D)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    bk = bk.reset_index()
    bk["wn"] = bk.win.str[1:].astype(int)
    bk = bk.sort_values(["wn", "day"])
    def sh(x): return x.mean()/x.std()*np.sqrt(365)
    def calmar(x):
        v = (1+x).cumprod(); dd = (v/v.cummax()-1).min()
        yr = v.iloc[-1]**(365/len(x))-1
        return yr, dd
    out["book vs hold"] = pd.Series({"book sh": sh(bk.book_return), "hold sh": sh(bk.coin_return), "book mean": bk.book_return.mean(), "hold mean": bk.coin_return.mean(), "book yr": calmar(bk.book_return)[0], "book dd": calmar(bk.book_return)[1], "hold yr": calmar(bk.coin_return)[0], "hold dd": calmar(bk.coin_return)[1], "corr": bk.book_return.corr(bk.coin_return)})
    out["by window"] = bk.groupby("wn").agg(book=("book_return", "sum"), hold=("coin_return", "sum"), n=("day", "size"))
    # gain by year
    out["gain by year"] = B.groupby("year").agg(gain=("gain", "mean"), mkt=("mkt", "mean"), pos=("pos", "mean"), coin=("ret1", "mean"))
    # gain by coin
    out["gain by coin"] = B.groupby("coin").agg(gain=("gain", "mean"), mkt=("mkt", "mean"), pos=("pos", "mean"))
    # fees
    T = pd.concat([data["trades"][c][w] for c in data["trades"] for w in data["trades"][c]])
    out["trades"] = pd.Series({"n": len(T), "gross mean": T.profit_loss_percent.mean(), "net mean": T.net_profit_loss_percent.mean(), "comm mean": T.total_commission.mean()})
    return out
