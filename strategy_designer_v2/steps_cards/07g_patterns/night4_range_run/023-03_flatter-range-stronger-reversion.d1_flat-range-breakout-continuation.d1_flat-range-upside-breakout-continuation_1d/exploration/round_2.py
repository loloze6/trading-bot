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
            net = (c - c.shift(29)) / rng
            ret1 = c.pct_change()
            vol20 = ret1.rolling(20).std()
            ts = pd.to_datetime(b["timestamp"])
            hi60 = c.rolling(60).max()
            for t in range(0, n - H, H):
                rows.append(dict(coin=coin, wn=int(w[1:]), fwd=c[t+H]/c[t]-1,
                    pos=pos[t], net=net[t], r1=ret1[t], r1z=(ret1[t]/vol20[t] if vol20[t] else np.nan),
                    dd60=c[t]/hi60[t]-1, wd=ts[t].dayofweek, yr=ts[t].year))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["sd"] = g.groupby("coin")["fwd"].transform("std")
    g["z"] = g["ex"]/g["sd"]
    g["p2"] = 2*g["pos"]-1
    g["flat"] = 1-g["net"].abs()
    def reg(col, d, y="ex"):
        d = d.dropna(subset=[col, y])
        r = stats.linregress(d[col], d[y]); return f"slope {r.slope:.4g} t {r.slope/r.stderr:.2f} n {len(d)}"
    def multi(cols, d):
        d = d.dropna(subset=cols+["ex"])
        X = np.column_stack([np.ones(len(d))]+[d[c].values for c in cols]); y = d["ex"].values
        b, *_ = np.linalg.lstsq(X, y, rcond=None); e = y-X@b
        s2 = e@e/(len(y)-X.shape[1]); se = np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
        return pd.DataFrame({"coef": b, "t": b/se}, index=["const"]+cols).round(4)
    res = {}
    g["p2_trend"] = g["p2"]*(1-g["flat"]); g["p2_flat"] = g["p2"]*g["flat"]
    res["multi_pos_trend_flat"] = multi(["p2_trend","p2_flat"], g)
    res["multi_net_pos"] = multi(["net","p2"], g)
    res["net_all"] = reg("net", g)
    res["net_by_yrhalf"] = pd.Series({"2018-21": reg("net", g[g.yr<=2021]), "2022-25": reg("net", g[g.yr>=2022])})
    res["net_by_coin"] = pd.Series({c: reg("net", g[g.coin==c]) for c in g.coin.unique()})
    res["r1z_all"] = reg("r1z", g)
    res["r1z_by_yrhalf"] = pd.Series({"2018-21": reg("r1z", g[g.yr<=2021]), "2022-25": reg("r1z", g[g.yr>=2022])})
    res["r1z_by_coin"] = pd.Series({c: reg("r1z", g[g.coin==c]) for c in g.coin.unique()})
    g["r1z_abs"] = g["r1z"].abs()
    res["absr1z"] = reg("r1z_abs", g)
    res["dd60"] = reg("dd60", g)
    # weekday: Mon-Tue vs rest
    a = g[g.wd.isin([0,1])]["ex"]; bb = g[~g.wd.isin([0,1])]["ex"]
    tt = stats.ttest_ind(a, bb, equal_var=False)
    res["wd_montue_vs_rest"] = f"diff {a.mean()-bb.mean():.4f} t {tt.statistic:.2f} n {len(a)}/{len(bb)}"
    res["wd_by_yrhalf"] = g.assign(h=np.where(g.yr<=2021,"early","late")).groupby(["h","wd"])["ex"].mean().unstack().round(4)
    # book largest days: what preceded
    dl = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"]=coin; x["w"]=w; dl.append(x)
    D = pd.concat(dl)
    bk = D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    q = bk["book_return"].quantile([0.02, 0.98])
    res["book_tails"] = pd.DataFrame({
        "worst2pct": bk[bk.book_return<=q.iloc[0]].mean(),
        "best2pct": bk[bk.book_return>=q.iloc[1]].mean(),
        "all": bk.mean()}).round(4)
    res["book_share_from_top5pct_days"] = float(bk.book_return[bk.book_return>=bk.book_return.quantile(0.95)].sum()/bk.book_return.sum())
    return res
