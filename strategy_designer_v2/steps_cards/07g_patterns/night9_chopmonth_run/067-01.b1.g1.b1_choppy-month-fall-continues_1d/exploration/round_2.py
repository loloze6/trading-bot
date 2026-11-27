def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); n = len(b)
            r1 = c.pct_change()
            r30 = c / c.shift(30) - 1
            r60 = c / c.shift(60) - 1
            r90 = c / c.shift(90) - 1
            hi30 = c.rolling(30).max(); lo30 = c.rolling(30).min()
            pos30 = (c - lo30) / (hi30 - lo30)
            vol30 = r1.rolling(30).std()
            fwd10 = c.shift(-10) / c - 1
            fwd5 = c.shift(-5) / c - 1
            for i in range(0, n, 10):
                if i + 10 >= n: continue
                rows.append(dict(coin=coin, w=w, ts=b["timestamp"].iloc[i],
                                 chop=b["regime"].iloc[i] == "unknown",
                                 r30=r30.iloc[i], r60=r60.iloc[i], r90=r90.iloc[i], pos=pos30.iloc[i],
                                 z30=r30.iloc[i] / (vol30.iloc[i] * np.sqrt(30)) if vol30.iloc[i] > 0 else np.nan,
                                 fwd=fwd10.iloc[i], fwd5=fwd5.iloc[i] if i + 5 < n else np.nan))
    d = pd.DataFrame(rows)
    drift = d.groupby("coin")["fwd"].mean()
    d["ex"] = d["fwd"] - d["coin"].map(drift)
    d["day"] = pd.to_datetime(d["ts"]).dt.floor("D")
    d["year"] = pd.to_datetime(d["ts"]).dt.year
    d["wd"] = pd.to_datetime(d["ts"]).dt.dayofweek
    def ct(x, col="ex"):
        x = x[[col, "day"]].dropna()
        if len(x) < 5: return pd.Series(dict(n=len(x), days=x["day"].nunique(), mean=np.nan, t_day=np.nan))
        m = x[col].mean()
        s = (x[col] - m).groupby(x["day"]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / len(x)
        return pd.Series(dict(n=len(x), days=G, mean=m, t_day=m / se))
    out = {}
    ch = d[d.chop].copy()
    ch["r30q"] = pd.qcut(ch["r30"], 5, labels=False)
    out["chop_r30q_clustered"] = ch.groupby("r30q").apply(ct)
    out["chop_rise_side_long"] = ct(ch[ch.r30 > 0])
    out["chop_fall_side_short"] = ct(ch[ch.r30 < 0].assign(ex=lambda x: -x.ex))
    # signed continuation: sign(r30)*ex, graded correlation
    ch["sig"] = np.sign(ch.r30) * ch.ex
    out["chop_signed_cont"] = ct(ch, "sig")
    cc = ch[["r30", "ex"]].dropna()
    out["chop_spearman_r30_ex"] = pd.Series(stats.spearmanr(cc.r30, cc.ex), index=["rho", "p"])
    cz = ch[["z30", "ex"]].dropna()
    out["chop_spearman_z30_ex"] = pd.Series(stats.spearmanr(cz.z30, cz.ex), index=["rho", "p"])
    cp = ch[["pos", "ex"]].dropna()
    out["chop_spearman_pos_ex"] = pd.Series(stats.spearmanr(cp.pos, cp.ex), index=["rho", "p"])
    # pos and r30 jointly in chop
    ch["posh"] = (ch.pos > 0.5).astype(int); ch["r30s"] = (ch.r30 > 0).astype(int)
    out["chop_pos_x_r30sign"] = ch.groupby(["r30s", "posh"]).apply(ct)
    out["chop_r30q_by_year"] = ch.assign(sig=np.sign(ch.r30) * ch.ex).groupby("year").apply(lambda g: ct(g, "sig"))
    # weekday clustered all
    out["weekday_clustered_all"] = d.groupby("wd").apply(ct)
    # whole sample: 90 day return quintile (longer trend), clustered
    a = d.dropna(subset=["r90"]).copy()
    a["q"] = pd.qcut(a.r90, 5, labels=False)
    out["all_r90q"] = a.groupby("q").apply(ct)
    # falling market deep r30
    f = d[(d.r60 < -0.1)].copy(); f["q"] = pd.qcut(f.r30, 5, labels=False)
    out["falling_r30q_clust"] = f.groupby("q").apply(ct)
    # book: largest day returns context
    br = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd[["day", "book_return", "coin_return"]].copy(); x["coin"] = coin; br.append(x)
    br = pd.concat(br)
    bd = br.groupby("day").agg(book=("book_return", "mean"), coin=("coin_return", "mean")).dropna()
    bd["bq"] = pd.qcut(bd.book.rank(method="first"), 10, labels=False)
    out["book_deciles_vs_coin"] = bd.groupby("bq").agg(book=("book", "mean"), coin=("coin", "mean"), n=("book", "count"))
    out["book_coin_corr"] = float(bd[["book", "coin"]].corr().iloc[0, 1])
    return out
