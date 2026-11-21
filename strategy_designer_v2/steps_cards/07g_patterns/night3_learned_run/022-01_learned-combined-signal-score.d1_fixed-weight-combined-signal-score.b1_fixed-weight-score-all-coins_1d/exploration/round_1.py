def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        recs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            r1 = pd.Series(c).pct_change().values
            vol30 = pd.Series(r1).rolling(30, min_periods=20).std().values
            ret28 = pd.Series(c).pct_change(28).values
            hi90 = pd.Series(c).rolling(90, min_periods=22).max().values
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                d = {"coin": coin, "win": w, "fwd": c[i + H] / c[i] - 1,
                     "fc": b["forecast"].iloc[i],
                     "alloc": b["postRebalance_current_allocation"].iloc[i],
                     "r1": r1[i], "vol": vol30[i], "r28": ret28[i],
                     "near": c[i] / hi90[i] - 1 if hi90[i] == hi90[i] else np.nan,
                     "year": ts.iloc[i].year, "wd": ts.iloc[i].weekday()}
                for k in ["mom28", "rev1", "high90", "vol30"]:
                    col = "debug_info.components.%s.post_pipeline_value" % k
                    d[k] = b[col].iloc[i] if col in b else np.nan
                recs.append(d)
        df = pd.DataFrame(recs)
        df["ex"] = df["fwd"] - df["fwd"].mean()
        df["z"] = df["ex"] / df["fwd"].std()
        rows.append(df)
    g = pd.concat(rows, ignore_index=True)
    out = {}
    def tline(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    comp = {}
    for k in ["mom28", "rev1", "high90", "vol30", "fc"]:
        s = g[[k, "z"]].dropna()
        rr, p = stats.spearmanr(s[k], s["z"])
        comp[k] = {"n": len(s), "spearman": rr, "t_approx": rr * np.sqrt(len(s))}
    out["component_rank_corr_with_z"] = pd.DataFrame(comp).T
    g["fq"] = g.groupby("coin")["fc"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["fc_quintile_ex"] = g.groupby("fq")["ex"].apply(tline).unstack()
    for k in ["r1", "vol", "r28", "near"]:
        g[k + "_q"] = g.groupby("coin")[k].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False) if x.notna().sum() > 20 else np.nan)
        out[k + "_quintile_ex"] = g.groupby(k + "_q")["ex"].apply(tline).unstack()
    out["by_year_fcXex"] = g.assign(p=g["fc"] / 10 * g["ex"]).groupby("year")["p"].apply(tline).unstack()
    out["weekday_ex"] = g.groupby("wd")["ex"].apply(tline).unstack()
    # vol-tercile interaction: momentum within vol level
    g["vt"] = g.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    tab = {}
    for v in [0, 1, 2]:
        s = g[g["vt"] == v]
        for k in ["mom28", "rev1", "high90"]:
            ss = s[[k, "z"]].dropna()
            rr, _ = stats.spearmanr(ss[k], ss["z"])
            tab[(v, k)] = rr * np.sqrt(len(ss))
    out["comp_t_by_vol_tercile"] = pd.Series(tab).unstack()
    # book: daily return by year, long vs short
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; dd.append(d)
    D = pd.concat(dd)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    out["book_by_year"] = D.groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    out["case_side_ex"] = g.assign(side=np.sign(g["fc"])).groupby("side")["ex"].apply(tline).unstack()
    return out
