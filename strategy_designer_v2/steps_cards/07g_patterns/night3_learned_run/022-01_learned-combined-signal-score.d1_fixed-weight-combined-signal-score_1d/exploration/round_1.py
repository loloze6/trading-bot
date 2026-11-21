def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    comps = ["mom28","rev1","high90","vol30"]
    rows = []
    for coin, wins in data["bars"].items():
        # coin mean 5-day grid return
        recs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            r1 = pd.Series(c).pct_change().values
            vol = pd.Series(r1).rolling(30).std().values
            r28 = pd.Series(c).pct_change(28).values
            hi90 = pd.Series(c).rolling(90, min_periods=22).max().values
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n-5, 5):
                d = {"coin": coin, "w": w, "r5": c[i+5]/c[i]-1, "fc": b["forecast"].iloc[i],
                     "alloc": b["postRebalance_current_allocation"].iloc[i],
                     "r1": r1[i], "vol": vol[i], "r28": r28[i], "dh": c[i]/hi90[i]-1,
                     "wd": ts.iloc[i].weekday(), "yr": ts.iloc[i].year,
                     "r1z": r1[i]/vol[i] if vol[i] and not np.isnan(vol[i]) else np.nan}
                for k in comps:
                    col = f"debug_info.components.{k}.post_pipeline_value"
                    d[k] = b[col].iloc[i] if col in b else np.nan
                recs.append(d)
        df = pd.DataFrame(recs)
        df["u"] = df["r5"] - df["r5"].mean()
        df["usd"] = df["r5"].std()
        rows.append(df)
    G = pd.concat(rows, ignore_index=True)
    G["un"] = G["u"]/G["usd"]
    def tt(x):
        x = x.dropna(); return pd.Series({"mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))), "n": len(x)})
    # each component's own product t (normalized by coin usual move)
    out["component_product_t"] = pd.DataFrame({k: tt(G[k]*G["un"]) for k in comps + ["fc"]}).T
    # per coin component t
    pc = {}
    for k in comps+["fc"]:
        pc[k] = G.groupby("coin").apply(lambda g: tt(g[k]*g["un"])["t"])
    out["component_t_by_coin"] = pd.DataFrame(pc)
    # forecast quintiles
    G["fq"] = G.groupby("coin")["fc"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["fc_quintile_unusual"] = G.groupby("fq")["u"].agg(["mean","count"])
    # vol quintile (per coin)
    G["vq"] = G.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["vol_quintile"] = G.groupby("vq").agg(u=("u","mean"), un=("un","mean"), absu=("u", lambda x: x.abs().mean()), n=("u","count"))
    # after large 1-day moves, z-score buckets
    G["zb"] = pd.cut(G["r1z"], [-np.inf,-2,-1,0,1,2,np.inf])
    out["after_1d_z"] = G.groupby("zb").agg(un=("un","mean"), u=("u","mean"), n=("u","count"))
    # momentum quintiles and distance quintiles
    G["mq"] = G.groupby("coin")["r28"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    G["dq"] = G.groupby("coin")["dh"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["mom28_quint"] = G.groupby("mq").agg(un=("un","mean"), u=("u","mean"), n=("u","count"))
    out["dist90_quint"] = G.groupby("dq").agg(un=("un","mean"), u=("u","mean"), n=("u","count"))
    out["by_year_fc_t"] = G.groupby("yr").apply(lambda g: tt(g["fc"]*g["un"]))
    out["weekday_start"] = G.groupby("wd").agg(un=("un","mean"), n=("u","count"))
    # book: daily returns, largest gains/losses, coin's surrounding moves
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy().reset_index(drop=True)
            d["coin"] = coin; d["w"] = w
            d["c_prev5"] = d["close"]/d["close"].shift(5)-1
            d["c_next5"] = d["close"].shift(-5)/d["close"]-1
            D.append(d)
    D = pd.concat(D, ignore_index=True)
    bk = D.dropna(subset=["book_return"])
    q = bk["book_return"].quantile([0.02,0.98])
    out["book_extremes"] = pd.DataFrame({
        "top2pct": bk[bk.book_return>=q[0.98]][["book_return","coin_return","c_prev5","c_next5"]].mean(),
        "bottom2pct": bk[bk.book_return<=q[0.02]][["book_return","coin_return","c_prev5","c_next5"]].mean(),
        "all": bk[["book_return","coin_return","c_prev5","c_next5"]].mean()})
    # long vs short side contribution
    G["side"] = np.sign(G["alloc"])
    out["side"] = G.groupby("side").agg(r5=("r5","mean"), u=("u","mean"), n=("u","count"))
    return out
