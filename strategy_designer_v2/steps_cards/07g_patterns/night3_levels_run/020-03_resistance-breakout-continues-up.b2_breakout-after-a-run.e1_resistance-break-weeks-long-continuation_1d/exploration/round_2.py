def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    recs = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            lr = np.log(c).diff()
            df = pd.DataFrame({"coin": coin, "win": w, "wn": int(w[1:]), "pos": np.arange(len(b)),
                               "r1": c.pct_change(), "r3": c / c.shift(3) - 1,
                               "vol20": lr.rolling(20).std(),
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday})
            for h in [1, 3, 5, 10, 20]:
                df[f"f{h}"] = c.shift(-h) / c - 1
            recs.append(df)
    D = pd.concat(recs, ignore_index=True)
    D["z"] = D["r1"] / D["vol20"]
    D["z3"] = D["r3"] / (D["vol20"] * np.sqrt(3))
    res = {}
    for h in [1, 3, 5, 10, 20]:
        g = D[D["pos"] % h == 0]
        drift = g.groupby("coin")[f"f{h}"].mean()
        usd = g.groupby("coin")[f"f{h}"].std()
        D[f"ex{h}"] = D[f"f{h}"] - D["coin"].map(drift)
        D[f"s{h}"] = D[f"ex{h}"] / D["coin"].map(usd)
    def qt(df, col, val, q):
        x = df.dropna(subset=[col, val]).copy()
        x["q"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = x.groupby("q")[val].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t.drop(columns="std")
    for h in [3, 5, 10]:
        g = D[D["pos"] % h == 0]
        out[f"ex{h}_by_z_decile(grid {h})"] = qt(g, "z", f"ex{h}", 10)
    g5 = D[D["pos"] % 5 == 0]
    out["s5_by_z3_decile(grid5)"] = qt(g5, "z3", "s5", 10)
    # top z quintile per coin and per window half
    x = g5.dropna(subset=["z", "ex5"]).copy()
    x["top"] = x.groupby("coin")["z"].transform(lambda s: s.rank(pct=True) > 0.8)
    x["half"] = np.where(x["wn"] <= 12, "w1-12", "w13-24")
    t = x[x["top"]].groupby("coin")["ex5"].agg(["mean", "count", "std"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["top_z_quint_ex5_by_coin"] = t.drop(columns="std")
    t = x[x["top"]].groupby("half")["ex5"].agg(["mean", "count", "std"]); t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["top_z_quint_ex5_by_half"] = t.drop(columns="std")
    # spearman of z vs ex5 within positive z only (graded?)
    pz = x[x["z"] > 0]
    out["spearman_z_ex5_posz_by_coin"] = pz.groupby("coin").apply(lambda y: stats.spearmanr(y["z"], y["ex5"])[0])
    # weekday stability
    E = D.dropna(subset=["ex1"]).copy()
    E["half"] = np.where(E["wn"] <= 12, "a", "b")
    out["next_day_ex_by_weekday_half"] = E.groupby(["wd", "half"])["ex1"].mean().unstack()
    out["next_day_ex_thu_fri_minus_mon_wed_by_coin"] = E.groupby("coin").apply(
        lambda y: y[y.wd.isin([3, 4])]["ex1"].mean() - y[y.wd.isin([0, 2])]["ex1"].mean())
    return out
