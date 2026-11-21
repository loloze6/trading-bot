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
            s = pd.DataFrame({
                "mom28": c / c.shift(28) - 1,
                "rev1": -(c / c.shift(1) - 1),
                "near90": c / c.rolling(90, min_periods=30).max() - 1,
                "lowvol30": -np.log(c).diff().rolling(30).std(),
                "comp": b.get("debug_info.components.composite.last_history_value"),
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            s["fwd5"] = c.shift(-5) / c - 1
            s["ret1"] = c.pct_change().shift(-1)
            s["year"] = pd.to_datetime(b["timestamp"]).dt.year
            s["coin"] = coin; s["win"] = w
            s["grid"] = (np.arange(n) % 5 == 0)
            rows.append(s)
    d = pd.concat(rows, ignore_index=True)
    mu = d[d.grid].groupby("coin")["fwd5"].mean()
    d["ex5"] = d["fwd5"] - d["coin"].map(mu)
    g = d[d.grid & d.fwd5.notna()].copy()
    # per-signal rank correlations per coin
    cor = {}
    for coin, gg in g.groupby("coin"):
        cor[coin] = {k: stats.spearmanr(gg[k], gg["ex5"], nan_policy="omit")[0] for k in ["mom28","rev1","near90","lowvol30","fc"]}
    cor["ALL"] = {k: stats.spearmanr(g[k], g["ex5"], nan_policy="omit")[0] for k in ["mom28","rev1","near90","lowvol30","fc"]}
    out["spearman_signal_vs_ex5_grid"] = pd.DataFrame(cor).T.round(3)
    # per-signal correlation by year
    cy = {}
    for y, gg in g.groupby("year"):
        cy[y] = {k: stats.spearmanr(gg[k], gg["ex5"], nan_policy="omit")[0] for k in ["mom28","rev1","near90","lowvol30","fc"]}
        cy[y]["n"] = len(gg)
    out["spearman_by_year"] = pd.DataFrame(cy).T.round(3)
    # forecast quintile vs excess 5d
    a = g[g.fc != 0].copy()
    a["q"] = pd.qcut(a.fc, 5, labels=False)
    out["fc_quintile"] = a.groupby("q").agg(fc=("fc","mean"), ex5=("ex5","mean"), fwd5=("fwd5","mean"), n=("ex5","size")).round(4)
    # long vs short gain
    a["gain"] = np.sign(a.fc) * a.ex5
    out["long_short"] = a.groupby(np.sign(a.fc)).agg(n=("gain","size"), ex5_signed=("gain","mean"), t=("gain", lambda x: x.mean()/x.std()*np.sqrt(len(x)))).round(4)
    # mom28 quintile per coin pooled
    for k in ["mom28","rev1","near90","lowvol30"]:
        gg = g.dropna(subset=[k]).copy()
        gg["q"] = gg.groupby("coin")[k].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        out[f"q_{k}"] = gg.groupby("q")["ex5"].agg(["mean","count", lambda x: x.mean()/x.std()*np.sqrt(len(x))]).round(4)
    # book decomposition on bars
    d["mkt_daily"] = d["coin"].map(d.groupby("coin")["ret1"].mean())
    out["book_parts_per_bar"] = pd.Series({
        "mean_alloc": d.alloc.mean(),
        "share_short": (d.alloc < 0).mean(),
        "gain_before_cost": (d.alloc * d.ret1).mean(),
        "from_market": (d.alloc * d.mkt_daily).mean(),
        "timing": (d.alloc * (d.ret1 - d.mkt_daily)).mean(),
        "turnover_per_bar": d.groupby(["coin","win"]).alloc.diff().abs().mean(),
    }).round(6)
    return out
