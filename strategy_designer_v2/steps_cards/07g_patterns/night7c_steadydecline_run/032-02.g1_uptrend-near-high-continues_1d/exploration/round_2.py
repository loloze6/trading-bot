def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            hl = (b["high"] - b["low"]) / c
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd5": c.shift(-5) / c - 1,
                "fwd2": c.shift(-2) / c - 1,
                "ret28": c / c.shift(28) - 1,
                "prox": c / c.rolling(28).max(),
                "prox56": c / c.rolling(56).max(),
                "lowd": c / c.rolling(28).min() - 1,
                "rng": hl.rolling(28).mean() / hl.rolling(90, min_periods=40).mean(),
                "maxdrop": r1.rolling(28).min(),
                "alloc": b["postRebalance_current_allocation"],
            })
            df["pos"] = np.arange(len(df))
            rows.append(df[df["pos"] % 5 == 0])
    g = pd.concat(rows).dropna(subset=["fwd5"])
    g["ex"] = g["fwd5"] - g.groupby("coin")["fwd5"].transform("mean")

    def grp(col, q=5, sub=None):
        d = (g if sub is None else sub).dropna(subset=[col])
        k = pd.qcut(d[col].rank(method="first"), q, labels=False)
        o = d.groupby(k)["ex"].agg(["count", "mean", "std"])
        o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
        o["xmean"] = d.groupby(k)[col].mean()
        return o.round(4)

    def slope(col, sub, y="ex"):
        d = sub.dropna(subset=[col, y])
        if len(d) < 8: return pd.Series({"n": len(d), "slope": np.nan, "t": np.nan})
        s = stats.linregress(d[col], d[y])
        return pd.Series({"n": len(d), "slope": s.slope, "t": s.slope / s.stderr})

    out = {}
    dn = g[g["ret28"] <= 0]; up = g[g["ret28"] > 0]
    all_ = g.dropna(subset=["prox"])
    out["prox_q_all"] = grp("prox", q=10, sub=all_)
    out["prox_slope_all_by_win"] = pd.DataFrame({w: slope("prox", all_[all_.win == w]) for w in sorted(all_.win.unique())}).T.round(3)
    out["prox_slope_all_by_coin"] = pd.DataFrame({c: slope("prox", all_[all_.coin == c]) for c in all_.coin.unique()}).T.round(3)
    out["prox56_slope"] = pd.DataFrame({"all": slope("prox56", g), "up": slope("prox56", up), "down": slope("prox56", dn)}).T.round(4)
    out["prox_fwd2_slope"] = pd.DataFrame({"all": slope("prox", g, "fwd2"), "up": slope("prox", up, "fwd2")}).T.round(4)
    out["lowd_q_down"] = grp("lowd", sub=dn)
    # calm vs violent declines
    dn2 = dn.dropna(subset=["rng"]).copy()
    dn2["calm"] = dn2["rng"] < dn2["rng"].median()
    out["calm_down_ret28_slope"] = pd.DataFrame({"calm": slope("ret28", dn2[dn2.calm]), "violent": slope("ret28", dn2[~dn2.calm])}).T.round(4)
    out["calm_down_mean"] = dn2.groupby("calm")["ex"].agg(["count", "mean"]).round(4)
    out["maxdrop_q_down"] = grp("maxdrop", sub=dn)
    # interaction prox x ret28 overall
    d = all_.copy()
    d["a"] = pd.qcut(d["ret28"].rank(method="first"), 3, labels=False)
    d["b"] = pd.qcut(d["prox"].rank(method="first"), 3, labels=False)
    out["ret28_x_prox_mean"] = d.pivot_table(index="a", columns="b", values="ex", aggfunc="mean").round(4)
    out["ret28_x_prox_n"] = d.pivot_table(index="a", columns="b", values="ex", aggfunc="count")
    # book: largest days
    dd = pd.concat([x.assign(coin=c, win=w) for c, ws in data["days"].items() for w, x in ws.items()])
    bk = dd.groupby(["win", "day"]).agg(b=("book_return", "mean"), h=("coin_return", "mean")).dropna()
    bk["nb"] = bk["b"].rank(pct=True)
    out["book_tails"] = pd.DataFrame({
        "top5pct_book_mean": [bk[bk.nb > .95]["b"].mean()], "top5pct_hold_mean": [bk[bk.nb > .95]["h"].mean()],
        "bot5pct_book_mean": [bk[bk.nb < .05]["b"].mean()], "bot5pct_hold_mean": [bk[bk.nb < .05]["h"].mean()],
        "share_gain_top5pct": [bk[bk.nb > .95]["b"].sum() / bk["b"].sum()],
    }).T.round(4)
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()])
    tr["k"] = pd.qcut(tr["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades_by_entry_fc"] = tr.groupby("k").agg(n=("net_profit_loss_percent", "count"), mean=("net_profit_loss_percent", "mean"), fc=("entry_forecast", "mean"), dur=("duration_minutes", "mean")).round(3)
    return out
