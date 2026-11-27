def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    trows = []
    drows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            b["loc"] = (c - b["low"]) / rng
            b["ret5"] = c / c.shift(5) - 1
            b["rng"] = rng / c
            b["ret1"] = c / c.shift(1) - 1
            b["fwd5"] = c.shift(-5) / c - 1
            b["fwd1"] = c.shift(-1) / c - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["fwd1"]
            b["coin"] = coin; b["w"] = w
            b["grid"] = (np.arange(len(b)) % 5 == 0)
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b[["coin","w","year","regime","loc","ret5","rng","ret1","fwd5","fwd1","pos","gain","grid","forecast"]])
        for w, t in data["trades"].get(coin, {}).items():
            if len(t):
                t = t.copy(); t["coin"] = coin; t["w"] = w
                trows.append(t)
        for w, d in data["days"].get(coin, {}).items():
            d = d.copy(); d["coin"] = coin; d["w"] = w
            drows.append(d)
    B = pd.concat(rows, ignore_index=True)
    out["regime counts"] = B["regime"].value_counts()
    drift5 = B.loc[B.grid, "fwd5"].mean()
    out["drift5 all grid"] = float(drift5)
    G = B[B.grid & B.fwd5.notna()].copy()
    G["short_move"] = -(G["fwd5"])
    def summ(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out["grid short move by regime"] = G.groupby("regime")["short_move"].apply(summ).unstack()
    # inside profile without situation: unknown; pieces of situation
    P = G[G.regime.isin(["mean_reversion","unknown"])].copy()
    P["locU"] = P["loc"] > 0.5
    P["r5neg"] = P["ret5"] < 0
    out["in profile by loc>0.5 x ret5<0"] = P.groupby(["locU","r5neg"])["short_move"].apply(summ).unstack()
    S = P[P.regime=="mean_reversion"].copy()
    S["r5q"] = pd.qcut(S["ret5"], 4, labels=False)
    out["situation by ret5 quartile"] = S.groupby("r5q").agg(n=("short_move","size"), mean=("short_move","mean"), r5=("ret5","mean"))
    S["locq"] = pd.qcut(S["loc"], 3, labels=False)
    out["situation by loc tercile"] = S.groupby("locq").agg(n=("short_move","size"), mean=("short_move","mean"), loc=("loc","mean"))
    S["rngq"] = pd.qcut(S["rng"], 3, labels=False)
    out["situation by range tercile"] = S.groupby("rngq").agg(n=("short_move","size"), mean=("short_move","mean"), rng=("rng","mean"))
    # unknown in profile, ret5 quartile (condition alone)
    U = P[P.regime=="unknown"].copy()
    U["r5q"] = pd.qcut(U["ret5"], 4, labels=False)
    out["profile no-situation by ret5 quartile"] = U.groupby("r5q").agg(n=("short_move","size"), mean=("short_move","mean"), r5=("ret5","mean"))
    # trades
    T = pd.concat(trows, ignore_index=True)
    T["dur_d"] = T["duration_minutes"]/1440
    out["trades summary"] = pd.Series({"n": len(T), "net_mean": T.net_profit_loss_percent.mean(), "gross_mean": T.profit_loss_percent.mean(),
        "win": (T.net_profit_loss_percent>0).mean(), "dur_mean": T.dur_d.mean(), "dur_med": T.dur_d.median(),
        "worst": T.net_profit_loss_percent.min(), "best": T.net_profit_loss_percent.max(), "short_share": (T.side=="SHORT").mean()})
    T["durb"] = pd.cut(T.dur_d, [0,4.5,5.5,8,15,1000])
    out["trades by duration"] = T.groupby("durb").agg(n=("net_profit_loss_percent","size"), net=("net_profit_loss_percent","mean"))
    out["trades by coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent","size"), net=("net_profit_loss_percent","mean"), sumnet=("net_profit_loss_percent","sum"))
    # book daily
    D = pd.concat(drows, ignore_index=True)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    bk = D.groupby(["w","day"])["book_return"].mean().reset_index()
    hold = D.groupby(["w","day"])["coin_return"].mean().reset_index()
    bk = bk.merge(hold, on=["w","day"]).sort_values(["w","day"]).reset_index(drop=True)
    bk = bk.dropna()
    v = (1+bk.book_return).cumprod()
    dd = v / v.cummax() - 1
    bk["dd"] = dd.values
    out["book stats"] = pd.Series({"days": len(bk), "mean": bk.book_return.mean(), "sd": bk.book_return.std(),
        "sharpe": bk.book_return.mean()/bk.book_return.std()*np.sqrt(365), "maxdd": dd.min(),
        "hold_sharpe": bk.coin_return.mean()/bk.coin_return.std()*np.sqrt(365)})
    out["book by window"] = bk.groupby("w").agg(mean=("book_return","mean"), sum=("book_return","sum"), hold=("coin_return","sum"), mindd=("dd","min"))
    # worst book days, and coin moves those days
    out["worst 10 book days: book, coins mean"] = bk.nsmallest(10,"book_return")[["w","book_return","coin_return"]].reset_index(drop=True)
    # gain per bar by regime and by position held while prof/regime
    H = B[B.pos.abs()>1e-9]
    out["held bars by regime"] = H.groupby("regime").agg(n=("gain","size"), gain=("gain","mean"), fwd1=("fwd1","mean"))
    # held bars: gain by days since entry? approx by ret1 previous day sign
    H = H.copy()
    H["ret1pos"] = H["ret1"] > 0
    out["held bars gain by today's ret1 sign"] = H.groupby("ret1pos").agg(n=("gain","size"), gain=("gain","mean"))
    return out
