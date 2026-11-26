def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    bookrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); v = b["volume"].astype(float)
            n = len(b)
            fwd = c.shift(-H) / c - 1
            r1 = c.pct_change()
            r20 = c / c.shift(20) - 1
            r60 = c / c.shift(60) - 1
            r5 = c / c.shift(5) - 1
            vr = np.log(v.rolling(30).mean() / v.shift(30).rolling(30).mean())
            vr10 = np.log(v.rolling(10).mean() / v.shift(10).rolling(20).mean())
            sd10 = r1.rolling(10).std(); sd30 = r1.rolling(30).std()
            rng = (b["high"] - b["low"]) / c
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            fc = b["forecast"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, fwd=fwd[i], r1=r1[i], r5=r5[i], r20=r20[i], r60=r60[i],
                                 vr=vr[i], vr10=vr10[i], vratio=sd10[i]/sd30[i] if sd30[i] else np.nan,
                                 rng=rng[i], clpos=clpos[i], fc=fc[i], wd=ts[i].dayofweek, yr=ts[i].year))
        for w, d in data["days"][coin].items():
            d = d.copy(); d["coin"] = coin; d["w"] = w
            bookrows.append(d[["coin","w","book_return","coin_return"]])
    df = pd.DataFrame(rows)
    drift = df.groupby("coin")["fwd"].transform("mean")
    df["ex"] = df["fwd"] - drift
    out = {}
    def tab(sub, col, q=5):
        s = sub.dropna(subset=[col, "ex"]).copy()
        s["q"] = pd.qcut(s[col], q, labels=False, duplicates="drop")
        g = s.groupby("q")["ex"].agg(["count","mean","std"])
        g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
        g["mid"] = s.groupby("q")[col].median()
        sp = stats.spearmanr(s[col], s["ex"])
        g.loc["spearman","mean"] = sp[0]; g.loc["spearman","t"] = sp[1]
        return g.round(4)
    df["prof"] = np.where(df.r60 < -0.1, "falling", np.where(df.r60 > 0.1, "rising", "choppy"))
    df.loc[df.r60.isna(), "prof"] = "na"
    out["n_cells_by_prof"] = df["prof"].value_counts()
    out["vr_falling"] = tab(df[df.prof=="falling"], "vr", 4)
    out["vr_rising"] = tab(df[df.prof=="rising"], "vr", 4)
    out["vr_choppy"] = tab(df[df.prof=="choppy"], "vr", 4)
    out["vr_all"] = tab(df, "vr", 5)
    out["vr10_all"] = tab(df, "vr10", 5)
    out["r20_all"] = tab(df, "r20", 5)
    out["r5_all"] = tab(df, "r5", 5)
    out["r1_all"] = tab(df, "r1", 5)
    out["vratio_all"] = tab(df, "vratio", 5)
    out["clpos_all"] = tab(df, "clpos", 5)
    out["rng_all"] = tab(df, "rng", 5)
    out["r20_rising"] = tab(df[df.prof=="rising"], "r20", 4)
    out["r20_falling"] = tab(df[df.prof=="falling"], "r20", 4)
    out["ex_by_wd"] = df.groupby("wd")["ex"].agg(["count","mean"]).round(4)
    # book
    bk = pd.concat(bookrows).dropna(subset=["book_return"])
    bk_pool = bk.groupby(["w", bk.index])  # not used
    bb = []
    for (coin, w), g in bk.groupby(["coin","w"]):
        pass
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                t = t.copy(); t["coin"]=coin; tr.append(t)
    tr = pd.concat(tr)
    out["trades_side"] = tr.groupby("side")["net_profit_loss_percent"].agg(["count","mean","median"]).round(3)
    tr["af"] = tr["entry_forecast"].abs()
    tr["q"] = pd.qcut(tr["af"], 4, labels=False, duplicates="drop")
    out["trades_by_absfc"] = tr.groupby(["side","q"])["net_profit_loss_percent"].agg(["count","mean"]).round(3)
    out["trades_by_coin"] = tr.groupby(["coin","side"])["net_profit_loss_percent"].agg(["count","mean"]).round(3)
    out["book_by_window"] = bk.groupby("w")[["book_return","coin_return"]].mean().mul(100).round(3)
    return out
