def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            r1 = c.pct_change()
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(n)})
            df["ret5p"] = c / c.shift(5) - 1
            df["ret10p"] = c / c.shift(10) - 1
            df["ret30p"] = c / c.shift(30) - 1
            df["dlow"] = c / c.shift(1).rolling(30).min() - 1
            df["dhigh"] = c / c.shift(1).rolling(30).max() - 1
            df["vol20"] = r1.rolling(20).std()
            df["r1p"] = r1
            for h in (1, 5, 10):
                df[f"f{h}"] = c.shift(-h) / c - 1
            df["fc"] = b["forecast"].astype(float)
            df["alloc"] = b["postRebalance_current_allocation"].astype(float)
            df["wd"] = pd.to_datetime(b["timestamp"]).dt.dayofweek
            df["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    # coin mean 10-bar return on grid
    g10 = D[D.pos % 10 == 0].dropna(subset=["f10"])
    cm10 = g10.groupby("coin")["f10"].mean()
    out["coin_mean_10d_grid"] = cm10
    g10 = g10.copy()
    g10["ex10"] = g10["f10"] - g10["coin"].map(cm10)

    def bucket(df, col, q=5, y="ex10"):
        d = df.dropna(subset=[col, y]).copy()
        d["b"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        res = d.groupby("b")[y].agg(["mean", "count", "std"])
        res["t"] = res["mean"] / (res["std"] / np.sqrt(res["count"]))
        res["x_mean"] = d.groupby("b")[col].mean()
        return res.drop(columns="std")
    out["ex10_by_ret10p_q"] = bucket(g10, "ret10p")
    out["ex10_by_ret30p_q"] = bucket(g10, "ret30p")
    out["ex10_by_dhigh_q"] = bucket(g10, "dhigh")
    out["ex10_by_vol20_q"] = bucket(g10, "vol20")
    # new-low depth graded
    nl = g10[g10.dlow < 0]
    out["newlow_grid_ex10"] = pd.Series({"n": len(nl), "mean": nl.ex10.mean(),
        "t": nl.ex10.mean()/(nl.ex10.std()/np.sqrt(len(nl))) if len(nl)>2 else np.nan,
        "corr_depth": stats.spearmanr(nl.dlow, nl.ex10)[0] if len(nl)>5 else np.nan})
    nh = g10[g10.dhigh > 0]
    out["newhigh_grid_ex10"] = pd.Series({"n": len(nh), "mean": nh.ex10.mean(),
        "t": nh.ex10.mean()/(nh.ex10.std()/np.sqrt(len(nh))) if len(nh)>2 else np.nan})
    # 1-day: weekday, after large 1d moves
    g1 = D.dropna(subset=["f1"]).copy()
    cm1 = g1.groupby("coin")["f1"].mean()
    g1["ex1"] = g1["f1"] - g1["coin"].map(cm1)
    wd = g1.groupby("wd")["ex1"].agg(["mean", "count", "std"])
    wd["t"] = wd["mean"]/(wd["std"]/np.sqrt(wd["count"]))
    out["ex1_by_weekday"] = wd.drop(columns="std")
    out["ex1_by_r1p_q"] = bucket(g1, "r1p", 5, "ex1")
    g5 = D[D.pos % 5 == 0].dropna(subset=["f5"]).copy()
    cm5 = g5.groupby("coin")["f5"].mean()
    g5["ex5"] = g5["f5"] - g5["coin"].map(cm5)
    out["ex5_by_ret5p_q"] = bucket(g5, "ret5p", 5, "ex5")
    out["ex5_by_vol20_q"] = bucket(g5, "vol20", 5, "ex5")
    # by coin x ret30p for robustness
    d = g10.dropna(subset=["ret30p"]).copy()
    d["b"] = d.groupby("coin")["ret30p"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["ex10_coin_by_ret30p_t3"] = d.groupby(["coin", "b"])["ex10"].agg(["mean", "count"]).unstack()
    out["ex10_year_by_ret30p_t3"] = d.groupby(["year", "b"])["ex10"].mean().unstack()
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; dd.append(x)
    DD = pd.concat(dd)
    out["book_by_coin"] = DD.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "std", "count"])
    act = D[D.fc > 0]
    out["active_counts"] = pd.Series({"bars_fc_pos": len(act), "share": len(act)/len(D),
                                      "mean_alloc_active": act.alloc.mean()})
    return out
