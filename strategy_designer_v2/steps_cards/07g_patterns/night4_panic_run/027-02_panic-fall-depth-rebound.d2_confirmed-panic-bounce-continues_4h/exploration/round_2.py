def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    H = 84
    out = {}
    G = []; Hr = []; Dd = []
    for coin, wins in bars.items():
        nonov = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            nonov += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(nonov); sd = np.std(nonov)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; r1 = c.pct_change()
            ts = pd.to_datetime(df["timestamp"])
            fwd = c.shift(-H) / c - 1
            vol42 = r1.rolling(42).std(); vol180 = r1.rolling(180).std()
            d = pd.DataFrame({"coin": coin, "w": w, "year": ts.dt.year, "pos": np.arange(len(df)),
                              "r42": c / c.shift(42) - 1, "r42z": (c / c.shift(42) - 1) / (vol180 * np.sqrt(42)),
                              "r84": c / c.shift(84) - 1,
                              "volratio": vol42 / vol180, "ex": fwd - drift, "exs": (fwd - drift) / sd,
                              "fwd42": c.shift(-42) / c - 1, "alloc": df["postRebalance_current_allocation"]})
            G.append(d[d["pos"] % H == 0])
            Hr.append(pd.DataFrame({"coin": coin, "year": ts.dt.year, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                                    "r": c.shift(-1) / c - 1, "alloc": df["postRebalance_current_allocation"]}))
    G = pd.concat(G).dropna(subset=["ex"])
    def reg(df, x, y):
        df = df.dropna(subset=[x, y])
        if len(df) < 10: return [len(df), np.nan, np.nan]
        r = stats.linregress(df[x], df[y]); return [len(df), r.slope, r.slope / r.stderr]
    out["r42z on exs by coin (n,slope,t)"] = pd.DataFrame({k: reg(v, "r42z", "exs") for k, v in G.groupby("coin")}, index=["n","slope","t"]).T
    out["r42z on exs by year"] = pd.DataFrame({k: reg(v, "r42z", "exs") for k, v in G.groupby("year")}, index=["n","slope","t"]).T
    out["r42z / r84 / volratio pooled"] = pd.DataFrame({x: reg(G, x, "exs") for x in ["r42z", "r84", "volratio"]}, index=["n","slope","t"]).T
    gg = G.dropna(subset=["r42z"]); q = pd.qcut(gg["r42z"], 5, labels=False)
    t = gg.groupby(q)["ex"].agg(["count", "mean", "std"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["quintile r42z excess 14d"] = t[["count","mean","t"]]
    # vol-expanding with direction: volratio x sign of r42
    gg = G.dropna(subset=["volratio","r42"]).copy(); gg["vxs"] = (gg["volratio"]-1)*np.sign(gg["r42"])
    out["(volratio-1)*sign(r42) on exs"] = str(reg(gg, "vxs", "exs"))
    H2 = pd.concat(Hr).dropna(subset=["r"])
    h16 = H2.assign(is16=(H2["hour"] == 16)).groupby(["coin","is16"])["r"].mean().unstack()
    out["hour16 vs other mean by coin"] = h16
    def tt(v): return v.mean()/(v.std()/np.sqrt(len(v)))
    out["hour16 t by year"] = H2[H2["hour"]==16].groupby("year")["r"].agg(["count","mean", tt])
    out["hour20 t by year"] = H2[H2["hour"]==20].groupby("year")["r"].agg(["count","mean", tt])
    out["hour by coin t"] = H2.groupby(["hour","coin"])["r"].apply(tt).unstack()
    D = pd.concat([df.assign(coin=c, w=w) for c, ws in days.items() for w, df in ws.items()]).dropna(subset=["coin_return"])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday; D["year"] = pd.to_datetime(D["day"]).dt.year
    out["weekday t by coin"] = D.groupby(["wd","coin"])["coin_return"].apply(tt).unstack()
    out["saturday t by year"] = D[D["wd"]==5].groupby("year")["coin_return"].agg(["count","mean",tt])
    # book: long vs short gain per bar
    H2["g"] = H2["alloc"]*H2["r"]
    H2["side"] = np.sign(H2["alloc"].fillna(0))
    out["book bar gain by side"] = H2.groupby("side")["g"].agg(["count","sum","mean"])
    # book days: worst/best decile and coin return
    D["bq"] = pd.qcut(D["book_return"].rank(method="first"), 10, labels=False)
    out["book return decile vs coin return"] = D.groupby("bq")[["book_return","coin_return"]].mean()
    T = pd.concat([df.assign(coin=c) for c, ws in trades.items() for w, df in ws.items()])
    T["fq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 5, labels=False)
    out["trades by entry forecast quintile"] = T.groupby("fq").agg(n=("net_profit_loss_percent","count"), f=("entry_forecast","mean"), pl=("net_profit_loss_percent","mean"), med=("net_profit_loss_percent","median"))
    return out
