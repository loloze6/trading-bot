def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(b)
            ret1 = pd.Series(c).pct_change().values
            vol20 = pd.Series(ret1).rolling(20).std().values
            for i in range(0, n - 7, 7):
                if i < 7:
                    p7 = np.nan
                else:
                    p7 = c[i] / c[i-7] - 1
                p28 = c[i]/c[i-28]-1 if i >= 28 else np.nan
                rows.append(dict(coin=coin, w=w, f=b["forecast"].iloc[i],
                                 raw=b.get("debug_info.components.rsi_side.last_history_value", pd.Series([np.nan]*n)).iloc[i],
                                 pos=b["postRebalance_current_allocation"].iloc[i],
                                 fwd7=c[i+7]/c[i]-1, p7=p7, p28=p28, vol20=vol20[i],
                                 wd=pd.Timestamp(b["timestamp"].iloc[i]).dayofweek,
                                 yr=pd.Timestamp(b["timestamp"].iloc[i]).year))
    df = pd.DataFrame(rows)
    df["ex"] = df["fwd7"] - df.groupby("coin")["fwd7"].transform("mean")
    def tab(g):
        return pd.Series(dict(n=len(g), mean_ex=g["ex"].mean(),
                              t=g["ex"].mean()/(g["ex"].std()/np.sqrt(len(g))) if len(g)>2 else np.nan))
    df["fq"] = pd.qcut(df["f"], 5, labels=False, duplicates="drop")
    out["fwd7 excess by forecast quintile"] = df.groupby("fq").apply(tab)
    out["fwd7 excess by forecast quintile x coin"] = df.groupby(["coin","fq"]).apply(tab)
    d = df.dropna(subset=["p7"]).copy()
    d["pq"] = d.groupby("coin")["p7"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["fwd7 excess by past7 quintile"] = d.groupby("pq").apply(tab)
    d = df.dropna(subset=["p28"]).copy()
    d["pq"] = d.groupby("coin")["p28"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["fwd7 excess by past28 quintile"] = d.groupby("pq").apply(tab)
    d = df.dropna(subset=["vol20"]).copy()
    d["vq"] = d.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False))
    d["sx"] = np.sign(d["f"]) * d["ex"]
    out["fwd7 ex and signed ex by vol tercile"] = d.groupby("vq").agg(n=("ex","size"), mean_ex=("ex","mean"), signed_ex=("sx","mean"), sd=("sx","std"))
    df["sx"] = np.sign(df["f"]) * df["ex"]
    out["signed ex by year"] = df.groupby("yr").agg(n=("sx","size"), m=("sx","mean"), sd=("sx","std"))
    # days
    dl = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            dd = dd.copy(); dd["coin"]=coin; dd["w"]=w
            b = data["bars"][coin][w]
            pos = b.groupby(pd.to_datetime(b["timestamp"]).dt.floor("D"))["postRebalance_current_allocation"].last()
            dd["pos_prev"] = pd.Series(pos.values).shift(1).values[:len(dd)] if len(pos)==len(dd) else np.nan
            dl.append(dd)
    D = pd.concat(dl).dropna(subset=["book_return"])
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    out["book & coin by weekday"] = D.groupby("wd").agg(n=("book_return","size"), book=("book_return","mean"), coin=("coin_return","mean"), bsd=("book_return","std"))
    D["side"] = np.sign(D["pos_prev"])
    out["book by held side"] = D.groupby("side").agg(n=("book_return","size"), book=("book_return","mean"), coin=("coin_return","mean"), absz=("pos_prev", lambda s: s.abs().mean()))
    D["prev_coin"] = D.groupby(["coin","w"])["coin_return"].shift(1)
    D["pcq"] = pd.qcut(D["prev_coin"], 5, labels=False)
    out["next day coin & book by prev day coin ret quintile"] = D.groupby("pcq").agg(n=("coin_return","size"), coin=("coin_return","mean"), book=("book_return","mean"))
    # trades
    tl = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"]=coin; tl.append(t)
    T = pd.concat(tl)
    out["trades by side"] = T.groupby(["coin","side"]).agg(n=("net_profit_loss_percent","size"), net=("net_profit_loss_percent","mean"), win=("net_profit_loss_percent", lambda s:(s>0).mean()), dur_d=("duration_minutes", lambda s: s.mean()/1440))
    return out
