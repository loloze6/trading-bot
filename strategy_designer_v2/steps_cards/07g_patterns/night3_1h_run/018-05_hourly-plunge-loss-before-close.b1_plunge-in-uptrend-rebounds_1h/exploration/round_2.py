def explore(data):
    import numpy as np, pandas as pd
    H = 72
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            lr = np.log(c).diff()
            r24 = c / c.shift(24) - 1
            scale = r24.abs().rolling(720, min_periods=120).mean().shift(1)
            ratio = r24 / scale
            r720 = c / c.shift(720) - 1
            vol24 = lr.rolling(24).std()
            vol72 = lr.rolling(72).std()
            vol720 = lr.rolling(720, min_periods=240).std()
            fwd = c.shift(-H) / c - 1
            fwd144 = c.shift(-144) / c - 1
            idx = np.arange(0, len(b), H)
            wn = int(w[1:])
            rows.append(pd.DataFrame({"coin": coin, "win": w, "half": "w1-12" if wn <= 12 else "w13-24",
                "ratio": ratio.iloc[idx].values, "r720": r720.iloc[idx].values,
                "vr24": (vol24 / vol720).iloc[idx].values, "vr72": (vol72 / vol720).iloc[idx].values,
                "fwd": fwd.iloc[idx].values, "fwd144": fwd144.iloc[idx].values}))
    G = pd.concat(rows)
    G = G.dropna(subset=["fwd", "vr24", "vr72", "ratio", "r720"]).copy()
    G["un"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    G["str"] = G["un"] / G.groupby("coin")["fwd"].transform("std")
    G["q24"] = G.groupby("coin")["vr24"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    G["q72"] = G.groupby("coin")["vr72"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    G["d10"] = G.groupby("coin")["vr24"].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
    G["dir"] = np.where(G["ratio"] > 0, "after_rise", "after_fall")
    G["up30"] = np.where(G["r720"] > 0, "up", "down")
    G["calm24"] = np.where(G["ratio"].abs() < 1, "small24", "big24")

    def summ(df, key, col="un"):
        o = df.groupby(key, observed=True).agg(n=(col, "size"), un=(col, "mean"), sd=(col, "std"),
                                               strength=("str", "mean"))
        o["t"] = o["un"] / (o["sd"] / np.sqrt(o["n"]))
        return o.drop(columns="sd").round(5)

    res = {}
    res["vr24_decile"] = summ(G, "d10")
    res["vr72_quint"] = summ(G, "q72")
    res["vr24_by_dir"] = summ(G, ["dir", "q24"])
    res["vr24_by_trend"] = summ(G, ["up30", "q24"])
    res["vr24_by_small24"] = summ(G, ["calm24", "q24"])
    res["vr24_by_half"] = summ(G, ["half", "q24"])
    res["vr24_top_by_coin"] = summ(G[G.q24 == 4], "coin")
    res["vr24_bottom_by_coin"] = summ(G[G.q24 == 0], "coin")
    # graded slope: rank correlation of vr24 with unusual move, per coin
    from scipy import stats
    sp = []
    for coin, g in G.groupby("coin"):
        r, p = stats.spearmanr(g["vr24"], g["un"])
        sp.append((coin, round(r, 4), round(p, 4), len(g)))
    res["vr24_spearman_coin"] = pd.DataFrame(sp, columns=["coin", "rho", "p", "n"])
    # plunge in uptrend: 144h vs 72h
    P = G[(G.up30 == "up") & (G.ratio <= -1)].dropna(subset=["fwd144"]).copy()
    P["un144"] = P["fwd144"] - G.dropna(subset=["fwd144"]).groupby("coin")["fwd144"].transform("mean").reindex(P.index).values if False else P["fwd144"] - P["coin"].map(G.dropna(subset=["fwd144"]).groupby("coin")["fwd144"].mean())
    res["plunge_up_72_vs_144"] = pd.Series({"n": len(P), "un72": P["un"].mean(), "t72": P["un"].mean() / (P["un"].std() / np.sqrt(len(P))),
                                            "un144": P["un144"].mean(), "t144": P["un144"].mean() / (P["un144"].std() / np.sqrt(len(P)))}).round(5)
    # book: days around largest losses/gains
    D = pd.concat([x.assign(coin=c, win=w) for c, ws in data["days"].items() for w, x in ws.items()]).dropna(subset=["book_return"])
    D = D.reset_index(drop=True)
    lo, hi = D["book_return"].quantile([0.02, 0.98])
    res["book_tail_coin_ret"] = pd.DataFrame({
        "worst2pct": [ (D["book_return"] <= lo).sum(), D.loc[D.book_return <= lo, "coin_return"].mean()],
        "best2pct": [ (D["book_return"] >= hi).sum(), D.loc[D.book_return >= hi, "coin_return"].mean()]},
        index=["n_days", "mean_coin_ret"]).round(5)
    return res
