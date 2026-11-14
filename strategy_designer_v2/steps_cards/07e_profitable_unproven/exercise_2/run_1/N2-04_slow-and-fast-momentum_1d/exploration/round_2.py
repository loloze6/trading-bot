def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            df = pd.DataFrame({"close": b["close"].values, "alloc": b["postRebalance_current_allocation"].values,
                               "fc": b["forecast"].values})
            df["r60"] = df.close / df.close.shift(60) - 1
            df["r20"] = df.close / df.close.shift(20) - 1
            df["vol20"] = df.close.pct_change().rolling(20).std()
            df["n1"] = df.close.shift(-1) / df.close - 1
            df["f20"] = df.close.shift(-20) / df.close - 1
            df["gain"] = df.alloc * df.n1
            df["pos"] = np.arange(len(df))
            df["coin"] = coin; df["w"] = w
            df["year"] = pd.to_datetime(b["timestamp"]).dt.year.values
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["cm20"] = A.groupby("coin")["f20"].transform(lambda s: s[A.loc[s.index, "pos"] % 20 == 0].mean())
    A["ex20"] = A.f20 - A.cm20
    G = A[(A.pos % 20 == 0)].dropna(subset=["f20", "r60", "r20", "vol20"])
    def tt(s):
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan})
    # excess 20 bar by state, all grid bars (both up and not)
    G["state"] = np.where((G.r60 > 0) & (G.r20 > 0), "both up", np.where(G.r60 > 0, "r60 up only", np.where(G.r20 > 0, "r20 up only", "both down")))
    out["ex20 by state"] = G.groupby("state")["ex20"].apply(tt).unstack()
    G["volq"] = pd.qcut(G.vol20, 3, labels=["lowvol", "midvol", "hivol"])
    out["ex20 both-up by vol"] = G[G.state == "both up"].groupby("volq")["ex20"].apply(tt).unstack()
    out["ex20 not-both-up by vol"] = G[G.state != "both up"].groupby("volq")["ex20"].apply(tt).unstack()
    G["r60q"] = pd.qcut(G.r60, 5, labels=False)
    out["ex20 by r60 quintile"] = G.groupby("r60q")["ex20"].apply(tt).unstack().join(G.groupby("r60q")["r60"].mean())
    # daily gain while in market: per-unit return by vol, and gain share
    D = A.dropna(subset=["n1", "vol20"]).copy()
    D["volq"] = pd.qcut(D.vol20, 3, labels=["lowvol", "midvol", "hivol"])
    I = D[D.alloc > 0]
    out["active daily by vol"] = I.groupby("volq").agg(n=("n1", "size"), coin_n1=("n1", "mean"), alloc=("alloc", "mean"),
                                                       gain=("gain", "mean"), gain_sum=("gain", "sum"))
    out["active daily coin_n1 t by vol"] = I.groupby("volq")["n1"].apply(tt).unstack()
    # risk-adjusted next-day return (n1/vol) active vs not
    D["z"] = D.n1 / D.vol20
    out["z next day active vs not"] = D.groupby(D.alloc > 0)["z"].apply(tt).unstack()
    out["z next day active by volq"] = D[D.alloc > 0].groupby("volq")["z"].apply(tt).unstack()
    out["z next day inactive by volq"] = D[D.alloc <= 0].groupby("volq")["z"].apply(tt).unstack()
    # gain without top trades: year distribution of gain sum
    out["gain sum by year"] = D.groupby("year")["gain"].sum()
    out["gain sum by coin x volq share"] = D.groupby("volq")["gain"].sum() / D.gain.sum()
    # forecast size
    I2 = D[D.alloc > 0].copy()
    I2["fq"] = pd.qcut(I2.fc.rank(method="first"), 4, labels=False)
    out["active by forecast quartile"] = I2.groupby("fq").agg(fc=("fc", "mean"), n1=("n1", "mean"), gain=("gain", "mean"), alloc=("alloc", "mean"))
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    T["yr"] = pd.to_datetime(T.entry_time).dt.year
    top = T.sort_values("net_profit_loss_percent", ascending=False).head(10)
    out["top10 trades by coin"] = top.groupby("coin")["net_profit_loss_percent"].agg(["size", "sum"])
    out["top10 trades by year"] = top.groupby("yr")["net_profit_loss_percent"].agg(["size", "sum"])
    out["top10 duration days mean"] = top.duration_minutes.mean() / 1440
    return out
