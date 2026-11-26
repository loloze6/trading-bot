def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            r = c.pct_change()
            s30 = r.rolling(30).std()
            n1 = c.shift(-1)/c - 1
            n2 = c.shift(-2)/c - 1
            n3 = c.shift(-3)/c - 1
            fu = (r > 0) & (r.shift(1) <= 0)
            up = r > 0
            dist = (c - h)/c/s30
            ret60 = c/c.shift(60) - 1
            alloc = b["postRebalance_current_allocation"].fillna(0)
            d = pd.DataFrame(dict(coin=coin, w=w, ts=b["timestamp"], n1=n1, n2=n2, n3=n3, fu=fu, up=up,
                                  dist=dist, ret60=ret60, alloc=alloc, regime=b["regime"],
                                  s30=s30))
            d["pos"] = np.arange(len(d))
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    df["day"] = pd.to_datetime(df["ts"]).dt.floor("D")
    dr = df.groupby("coin")["n1"].mean()
    df["sx1"] = -(df["n1"] - df["coin"].map(dr))
    df["sx2"] = -(df["n2"] - 2*df["coin"].map(dr))
    df["sx3"] = -(df["n3"] - 3*df["coin"].map(dr))
    df["inprof"] = df["regime"].isin(["mean_reversion", "unknown"])
    df["case"] = df["regime"].eq("mean_reversion")
    def ct(x, col):
        x = x.dropna(subset=[col])
        if len(x) < 3: return (len(x), np.nan, np.nan, 0)
        g = (x[col] - x[col].mean()).groupby(x["day"]).sum()
        nd = len(g)
        se = np.sqrt((g**2).sum() * nd/(nd-1)) / len(x)
        return (len(x), x[col].mean(), x[col].mean()/se, nd)
    res = {}
    cs = df[df["case"]].copy()
    qs = cs["dist"].quantile([0.25, 0.5, 0.75]).values
    out["dist_quartile_cuts"] = pd.Series(qs, index=["q25","q50","q75"])
    cs["dq"] = pd.cut(cs["dist"], [-np.inf, qs[0], qs[1], qs[2], np.inf], labels=["Q1 deepest","Q2","Q3","Q4 at high"])
    for q, g in cs.groupby("dq", observed=True):
        for col in ["sx1","sx2","sx3"]:
            res[(str(q), col)] = ct(g, col)
    out["case_by_dist_q_t"] = pd.DataFrame(res, index=["n","mean","t","days"]).T
    # condition alone: deep dist in profile, not a first-up day
    res2 = {}
    ip = df[df["inprof"]]
    for name, g in [("in-profile not case, dist<=q25", ip[(~ip["case"]) & (ip["dist"] <= qs[0])]),
                    ("in-profile not case, up day dist<=q25", ip[(~ip["case"]) & ip["up"] & (ip["dist"] <= qs[0])]),
                    ("in-profile not case, all", ip[~ip["case"]]),
                    ("case dist<=q25", cs[cs["dist"] <= qs[0]]),
                    ("case dist>q25", cs[cs["dist"] > qs[0]]),
                    ("case ret60<-0.47", cs[cs["ret60"] < -0.47]),
                    ("case ret60>=-0.47", cs[cs["ret60"] >= -0.47]),
                    ("notcase inprof ret60<-0.47", ip[(~ip["case"]) & (ip["ret60"] < -0.47)])]:
        res2[name] = ct(g, "sx1")
    out["condition_alone_sx1"] = pd.DataFrame(res2, index=["n","mean","t","days"]).T
    # book-like: daily pnl if only Q1 traded, vs all; drawdown & sum per window, using actual alloc
    cs["pnl"] = cs["alloc"] * cs["n1"]
    for lab, g in [("all", cs), ("Q1", cs[cs["dist"] <= qs[0]]), ("Q1Q2", cs[cs["dist"] <= qs[1]])]:
        nb = df.groupby(["w"])["day"].nunique().sum()
        p = g.groupby(["w","day"])["pnl"].sum()/6
        wn = p.index.get_level_values(0).str[1:].astype(int)
        p = p.iloc[np.argsort(wn, kind="stable")]
        v = (1+p).cumprod(); ddm = (v/v.cummax()-1).min()
        out["sim_"+lab] = pd.Series(dict(sum=p.sum(), dd=ddm, n_days=len(p), ratio=p.sum()/abs(ddm) if ddm<0 else np.nan))
    # w14 concentrated loss: how many coins on loss day
    cs["loss"] = cs["pnl"] < -0.02
    out["big_loss_coins_per_day"] = cs[cs["loss"]].groupby("day").size().value_counts()
    out["big_loss_dist_q"] = cs[cs["loss"]]["dq"].value_counts()
    return out
