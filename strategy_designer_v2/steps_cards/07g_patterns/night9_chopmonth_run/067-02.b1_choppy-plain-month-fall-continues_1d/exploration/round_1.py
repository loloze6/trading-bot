def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 7
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            n = len(c)
            raw = b.get("debug_info.components.fall30.last_history_value")
            r1 = pd.Series(c).pct_change().values
            vol30 = pd.Series(r1).rolling(30, min_periods=20).std().values
            r30p = pd.Series(c).pct_change(30).values
            r7p = pd.Series(c).pct_change(7).values
            for i in range(0, n - H, H):
                fwd = c[i + H] / c[i] - 1
                rows.append(dict(coin=coin, w=w, wn=int(w[1:]), i=i,
                                 day=str(b["timestamp"].iloc[i])[:10],
                                 wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday(),
                                 fwd=fwd, choppy=b["regime"].iloc[i] == "mean_reversion",
                                 raw=(raw.iloc[i] if raw is not None else np.nan),
                                 r30=r30p[i], r7=r7p[i], r1=r1[i], vol30=vol30[i],
                                 fc=b["forecast"].iloc[i]))
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby("coin")["fwd"].transform("mean")
    g["sd"] = g.groupby("coin")["fwd"].transform("std")
    g["ex"] = g["fwd"] - g["drift"]
    g["exs"] = g["ex"] / g["sd"]
    g["vrank"] = g.groupby("coin")["vol30"].rank(pct=True)
    def summ(df, col="ex"):
        d = df.dropna(subset=[col])
        s = d.groupby("day")[col].sum()
        D = len(s)
        if D < 3: return pd.Series(dict(n=len(d), days=D, mean=np.nan, t=np.nan))
        m = d[col].mean()
        se = np.sqrt((s - s.mean() * 0 - m * d.groupby("day")[col].size()).pow(2).sum() * D / (D - 1)) / len(d)
        return pd.Series(dict(n=len(d), days=D, mean=m, t=m / se if se > 0 else np.nan,
                              fwd=d["fwd"].mean()))
    out = {}
    out["raw_describe"] = g.loc[g.choppy, "raw"].describe()
    ch = g[g.choppy].copy()
    ch["q"] = pd.qcut(ch["r30"], 5, labels=False)
    out["choppy_by_r30_quintile"] = ch.groupby("q").apply(lambda d: pd.concat([summ(d), pd.Series(dict(r30=d.r30.mean()))]))
    nc = g[~g.choppy].copy()
    nc["q"] = pd.qcut(nc["r30"], 5, labels=False)
    out["nonchoppy_by_r30_quintile"] = nc.groupby("q").apply(lambda d: pd.concat([summ(d), pd.Series(dict(r30=d.r30.mean()))]))
    ch["vq"] = pd.cut(ch["vrank"], [0, .5, 1], labels=["calm", "agit"])
    ch["side"] = np.where(ch.r30 < 0, "fall", "rise")
    out["choppy_side_x_agit"] = ch.groupby(["side", "vq"]).apply(summ)
    # large 1-day / 7-day moves, scaled by vol
    g["z1"] = g["r1"] / g["vol30"]
    g["z7"] = g["r7"] / (g["vol30"] * np.sqrt(7))
    g["z1q"] = pd.qcut(g["z1"], 10, labels=False)
    out["all_by_z1_decile"] = g.groupby("z1q").apply(lambda d: pd.concat([summ(d), pd.Series(dict(z=d.z1.mean()))]))
    g["z7q"] = pd.qcut(g["z7"], 10, labels=False)
    out["all_by_z7_decile"] = g.groupby("z7q").apply(lambda d: pd.concat([summ(d), pd.Series(dict(z=d.z7.mean()))]))
    g["vq"] = pd.qcut(g["vrank"], 4, labels=False)
    out["all_by_volrank_q"] = g.groupby("vq").apply(summ)
    out["all_by_weekday"] = g.groupby("wd").apply(summ)
    out["by_window"] = g.groupby("wn").apply(summ)
    # book daily
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; dd.append(d)
    dd = pd.concat(dd)
    dd["dk"] = dd["day"].astype(str)
    book = dd.groupby("dk").agg(br=("book_return", "mean"), cr=("coin_return", "mean"))
    book = book.dropna()
    out["book_corr_with_coins"] = float(book.br.corr(book.cr))
    q = book.br.quantile([.02, .98])
    out["coin_ret_on_book_worst2pct"] = float(book.cr[book.br <= q.iloc[0]].mean())
    out["coin_ret_on_book_best2pct"] = float(book.cr[book.br >= q.iloc[1]].mean())
    out["choppy_share"] = float(g.choppy.mean())
    return out
