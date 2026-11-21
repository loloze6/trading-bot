def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    drows = []
    for coin, wins in data["bars"].items():
        # coin mean daily return over all windows
        allr = []
        for w, b in wins.items():
            r = b["close"].pct_change()
            allr.append(r.dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.copy()
            c = b["close"]
            b["r1"] = c.pct_change()
            b["fwd"] = c.shift(-1) / c - 1
            b["vol20"] = b["r1"].rolling(20).std()
            b["z"] = b["r1"] / b["vol20"]
            b["ret20"] = c / c.shift(20) - 1
            b["ret60"] = c / c.shift(60) - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["fwd"]
            b["mkt"] = b["pos"] * mu
            b["coin"] = coin; b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["mu"] = mu
            rows.append(b)
        for w, d in data["days"][coin].items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            drows.append(d)
    B = pd.concat(rows, ignore_index=True)
    D = pd.concat(drows, ignore_index=True)
    B["ex"] = B["fwd"] - B["mu"]
    out["coins"] = str(list(data["bars"].keys()))
    # time in market, avg pos
    out["exposure"] = B.groupby("coin").agg(share_long=("pos", lambda x: (x > 0.001).mean()),
                                           mean_pos=("pos", "mean"),
                                           gain=("gain", "mean"), mkt=("mkt", "mean"))
    # forecast buckets
    fb = pd.cut(B["forecast"], [-0.01, 0.0001, 1, 5, 20.1], labels=["0", "0-1", "1-5", "5+"])
    g = B.dropna(subset=["fwd"]).groupby(fb)
    out["by_forecast"] = g.agg(n=("ex", "size"), ex_mean=("ex", "mean"), fwd_mean=("fwd", "mean"),
                               pos=("pos", "mean"), gain=("gain", "mean"))
    # by z of fall bucket
    zb = pd.cut(B["z"], [-20, -3, -2, -1.5, -1, -0.5, 0, 20])
    out["by_z"] = B.dropna(subset=["fwd", "z"]).groupby(zb).agg(n=("ex", "size"), ex=("ex", "mean"),
                     t=("ex", lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    # falls z<-1 split by 20-day trend
    F = B[(B["z"] < -1)].dropna(subset=["fwd", "ret20", "ret60"])
    F["tr20"] = pd.qcut(F["ret20"], 3, labels=["down", "mid", "up"])
    F["tr60"] = pd.qcut(F["ret60"], 3, labels=["down", "mid", "up"])
    out["falls_by_ret20"] = F.groupby("tr20").agg(n=("ex", "size"), ex=("ex", "mean"),
                     t=("ex", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))), r20=("ret20", "mean"))
    out["falls_by_ret60"] = F.groupby("tr60").agg(n=("ex", "size"), ex=("ex", "mean"),
                     t=("ex", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    # multi-day forward after falls
    for h in [1, 2, 3, 5]:
        pass
    hr = []
    for (coin, w), b in B.groupby(["coin", "win"]):
        c = b["close"].values
        for h in [1, 3, 5, 10]:
            f = pd.Series(c).shift(-h).values / c - 1
            for i in range(len(b)):
                if b["z"].iloc[i] < -1.5 and not np.isnan(f[i]):
                    hr.append((h, f[i] - b["mu"].iloc[i] * h))
    H = pd.DataFrame(hr, columns=["h", "ex"])
    out["falls_z_lt_-1.5_by_h"] = H.groupby("h").agg(n=("ex", "size"), ex=("ex", "mean"),
                     t=("ex", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    # book by year
    B2 = B.dropna(subset=["gain"])
    out["gain_by_year"] = B2.groupby("year").agg(gain=("gain", "mean"), mkt=("mkt", "mean"),
                     coin_ex=("ex", "mean"), pos=("pos", "mean"))
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()], ignore_index=True)
    out["trades"] = T.groupby("coin").agg(n=("side", "size"), pl=("profit_loss_percent", "mean"),
                     net=("net_profit_loss_percent", "mean"), dur_h=("duration_minutes", lambda x: x.mean() / 60))
    # book daily
    dd = D.groupby("day")["book_return"].mean().dropna()
    out["book_daily"] = pd.Series({"mean": dd.mean(), "std": dd.std(), "n": len(dd)})
    return out
