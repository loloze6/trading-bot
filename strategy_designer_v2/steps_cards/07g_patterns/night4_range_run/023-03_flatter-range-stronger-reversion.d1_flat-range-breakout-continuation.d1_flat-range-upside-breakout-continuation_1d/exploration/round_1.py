def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            hi30 = c.rolling(30).max(); lo30 = c.rolling(30).min()
            rng = hi30 - lo30
            pos = (c - lo30) / rng
            net = (c - c.shift(29))
            flat = 1 - net.abs() / rng
            ret1 = c.pct_change()
            ret5p = c / c.shift(5) - 1
            ret20p = c / c.shift(20) - 1
            vol20 = ret1.rolling(20).std()
            raw = b.get("debug_info.components.flat_range_pos.last_history_value")
            ts = pd.to_datetime(b["timestamp"])
            for t in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, wn=int(w[1:]),
                    fwd=c[t+H]/c[t]-1, fc=b["forecast"].iloc[t],
                    raw=(raw.iloc[t] if raw is not None else np.nan),
                    pos=pos[t], flat=flat[t], net=(net[t]/rng[t] if rng[t] else np.nan),
                    r1=ret1[t], r5=ret5p[t], r20=ret20p[t], vol=vol20[t],
                    wd=ts[t].dayofweek, yr=ts[t].year,
                    alloc=b["postRebalance_current_allocation"].iloc[t]))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["z"] = g["ex"] / g.groupby("coin")["fwd"].transform("std")
    def tab(col, q=5):
        d = g.dropna(subset=[col, "ex"]).copy()
        d["b"] = d.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        out = d.groupby("b").agg(n=("ex","size"), mean_ex=("ex","mean"), mean_z=("z","mean"), lo=(col,"mean"))
        out["t"] = d.groupby("b")["ex"].apply(lambda x: x.mean()/(x.std()/np.sqrt(len(x))))
        return out.round(4)
    def reg(col, sub=None):
        d = (g if sub is None else g[sub]).dropna(subset=[col,"ex"])
        r = stats.linregress(d[col], d["ex"]); return f"slope {r.slope:.4g} t {r.slope/r.stderr:.2f} n {len(d)}"
    res = {}
    res["raw_quint"] = tab("raw")
    res["pos_quint"] = tab("pos")
    res["flat_quint"] = tab("flat")
    res["netrange_quint"] = tab("net")
    res["r1_quint"] = tab("r1")
    res["r5_quint"] = tab("r5")
    res["r20_quint"] = tab("r20")
    res["vol_quint"] = tab("vol")
    # pos effect in flat vs trending halves
    d = g.dropna(subset=["pos","flat"]).copy()
    d["flathalf"] = d.groupby("coin")["flat"].transform(lambda x: x > x.median())
    res["pos_by_flat"] = pd.Series({f"flat={k}": reg("pos", (g.index.isin(v.index))) for k, v in d.groupby("flathalf")})
    res["r5_by_flat"] = pd.Series({f"flat={k}": reg("r5", (g.index.isin(v.index))) for k, v in d.groupby("flathalf")})
    res["wd"] = g.groupby("wd")["ex"].agg(["size","mean"]).round(4)
    res["by_coin_raw"] = pd.Series({c: reg("raw", g.coin==c) for c in g.coin.unique()})
    res["by_year_raw"] = pd.Series({y: reg("raw", g.yr==y) for y in sorted(g.yr.unique())})
    # book daily
    dl = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"]=coin; x["w"]=w; dl.append(x)
    D = pd.concat(dl)
    D["day"] = pd.to_datetime(D["day"])
    D["wd"] = D["day"].dt.dayofweek
    bk = D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    res["book_by_window"] = D.groupby("w")[["book_return","coin_return"]].mean().assign(
        n=D.groupby("w").size()/6).round(5).loc[[f"w{i}" for i in range(1,25)]]
    res["book_wd"] = D.groupby("wd")[["book_return","coin_return"]].mean().round(5)
    # trades
    tl = []
    for coin, wins in data["trades"].items():
        for w, tt in wins.items():
            if len(tt): x = tt.copy(); x["coin"]=coin; tl.append(x)
    T = pd.concat(tl)
    T["dur_d"] = T["duration_minutes"]/1440
    T["db"] = pd.qcut(T["dur_d"].rank(method="first"), 5, labels=False)
    res["trades_by_dur"] = T.groupby("db").agg(n=("dur_d","size"), dur=("dur_d","mean"), pl=("net_profit_loss_percent","mean"), win=("net_profit_loss_percent", lambda x:(x>0).mean())).round(3)
    T["fb"] = pd.qcut(T["entry_forecast"].rank(method="first"), 5, labels=False)
    res["trades_by_entryfc"] = T.groupby("fb").agg(n=("dur_d","size"), fc=("entry_forecast","mean"), pl=("net_profit_loss_percent","mean")).round(3)
    return res
