def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    H = 20
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(b)
            raw = b.get("debug_info.components.low_prox.last_history_value")
            post = b.get("debug_info.components.low_prox.post_pipeline_value")
            r1 = pd.Series(c).pct_change()
            vol20 = r1.rolling(20).std()
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, i=i,
                                 fwd=c[i+H]/c[i]-1,
                                 fc=b["forecast"].iloc[i],
                                 raw=raw.iloc[i] if raw is not None else np.nan,
                                 post=post.iloc[i] if post is not None else np.nan,
                                 past5=(c[i]/c[i-5]-1) if i >= 5 else np.nan,
                                 past20=(c[i]/c[i-20]-1) if i >= 20 else np.nan,
                                 vol20=vol20.iloc[i],
                                 r1=r1.iloc[i]))
    df = pd.DataFrame(rows)
    drift = df.groupby("coin")["fwd"].mean()
    df["ex"] = df["fwd"] - df["coin"].map(drift)
    out["raw_desc"] = df["raw"].describe()
    out["post_desc"] = df["post"].describe()
    df["absfc"] = df["fc"].abs()
    df["fq"] = pd.qcut(df["absfc"].rank(method="first"), 5, labels=False)
    g = df.groupby("fq").agg(n=("ex","size"), absfc=("absfc","mean"), raw=("raw","mean"),
                             fwd=("fwd","mean"), ex=("ex","mean"), ex_sd=("ex","std"))
    g["t"] = g["ex"]/(g["ex_sd"]/np.sqrt(g["n"]))
    out["by_forecast_quintile_20d_long_side"] = g
    # raw proximity quintile
    df["rq"] = pd.qcut(df["raw"].rank(method="first"), 5, labels=False)
    g2 = df.groupby("rq").agg(n=("ex","size"), raw=("raw","mean"), ex=("ex","mean"), sd=("ex","std"))
    g2["t"] = g2["ex"]/(g2["sd"]/np.sqrt(g2["n"]))
    out["by_raw_quintile"] = g2
    # past 20d return quintile
    d2 = df.dropna(subset=["past20"]).copy()
    d2["pq"] = pd.qcut(d2["past20"], 5, labels=False)
    g3 = d2.groupby("pq").agg(n=("ex","size"), past20=("past20","mean"), ex=("ex","mean"), sd=("ex","std"))
    g3["t"] = g3["ex"]/(g3["sd"]/np.sqrt(g3["n"]))
    out["by_past20_quintile"] = g3
    d3 = df.dropna(subset=["vol20"]).copy()
    d3["vq"] = d3.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    g4 = d3.groupby("vq").agg(n=("ex","size"), ex=("ex","mean"), sd=("ex","std"))
    g4["t"] = g4["ex"]/(g4["sd"]/np.sqrt(g4["n"]))
    out["by_vol_tercile"] = g4
    # interaction: near low (top raw quintile) x past20 sign
    d4 = d2.copy(); d4["near"] = d4["rq"] >= 4
    d4["down"] = d4["past20"] < 0
    g5 = d4.groupby(["near","down"]).agg(n=("ex","size"), ex=("ex","mean"), sd=("ex","std"))
    g5["t"] = g5["ex"]/(g5["sd"]/np.sqrt(g5["n"]))
    out["near_x_past20down"] = g5
    out["by_window_ex_nearlow"] = df[df["rq"]>=4].groupby("w")["ex"].agg(["size","mean"])
    # daily: weekday, large moves next-day
    dl = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"]=coin; d["w"]=w
            d["next"] = d["coin_return"].shift(-1)
            d["next5"] = d["close"].shift(-5)/d["close"]-1
            dl.append(d)
    D = pd.concat(dl)
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    out["weekday_coinret"] = D.groupby("wd")["coin_return"].agg(["size","mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["weekday_book"] = D.groupby("wd")["book_return"].agg(["mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    D["z"] = D.groupby("coin")["coin_return"].transform(lambda s: (s - s.mean())/s.std())
    D["zb"] = pd.cut(D["z"], [-99,-2,-1,1,2,99])
    out["next1_after_move"] = D.groupby("zb")["next"].agg(["size","mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    D5 = D.groupby(["coin","w"]).apply(lambda x: x.iloc[::5]).reset_index(drop=True)
    out["next5_after_move_nonoverlap"] = D5.groupby("zb")["next5"].agg(["size","mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    return out
