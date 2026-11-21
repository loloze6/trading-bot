def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            n = len(c)
            lhv = b.get("debug_info.components.rise28.last_history_value")
            ret1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            lr = np.r_[np.nan, np.diff(np.log(c))]
            vol20 = pd.Series(lr).rolling(20, min_periods=10).std().values
            r5past = np.r_[[np.nan]*5, c[5:] / c[:-5] - 1] if n > 5 else np.full(n, np.nan)
            r10past = np.r_[[np.nan]*10, c[10:] / c[:-10] - 1] if n > 10 else np.full(n, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            alloc = b["postRebalance_current_allocation"].values
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, pos=i, fwd=c[i+H]/c[i]-1,
                                 fc=b["forecast"].iloc[i],
                                 lhv=(lhv.iloc[i] if lhv is not None else np.nan),
                                 r1=ret1[i], vol=vol20[i], r5=r5past[i], r10=r10past[i],
                                 wd=ts.iloc[i].weekday(), yr=ts.iloc[i].year, alloc=alloc[i]))
    df = pd.DataFrame(rows)
    drift = df.groupby("coin")["fwd"].mean()
    sd = df.groupby("coin")["fwd"].std()
    df["adj"] = df["fwd"] - df["coin"].map(drift)
    df["z"] = df["adj"] / df["coin"].map(sd)
    out = {}
    def grp(key):
        g = df.dropna(subset=[key, "adj"]).groupby(key)["adj"]
        r = g.agg(["count", "mean", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.round(5)
    out["lhv_describe"] = df["lhv"].describe().round(3)
    df["lhv_q"] = pd.qcut(df["lhv"], 8, labels=False, duplicates="drop")
    out["by_lhv_octile"] = grp("lhv_q")
    df["fc_bin"] = pd.cut(df["fc"], [-0.01, 0.001, 5, 10, 15, 19.99, 20.01], labels=["0","0-5","5-10","10-15","15-20","20"])
    out["by_fc_bin"] = grp("fc_bin")
    for k in ["r1", "r5", "r10", "vol"]:
        df[k+"_q"] = df.groupby("coin")[k].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        out["by_"+k+"_quintile"] = grp(k+"_q")
    out["by_weekday"] = grp("wd")
    out["by_year"] = grp("yr")
    # vol x forecast interaction
    df["on"] = (df["fc"] > 0).astype(int)
    g = df.dropna(subset=["vol_q"]).groupby(["vol_q", "on"])["adj"].agg(["count", "mean"])
    out["vol_x_on"] = g.round(5)
    # per coin slope of adj on r5 (short reversal) and on lhv
    res = []
    for coin, d in df.groupby("coin"):
        for k in ["r5", "r10", "lhv"]:
            dd = d.dropna(subset=[k, "adj"])
            s = stats.linregress(dd[k], dd["adj"])
            res.append(dict(coin=coin, x=k, slope=s.slope, t=s.slope/s.stderr, n=len(dd)))
    out["per_coin_slopes"] = pd.DataFrame(res).round(4)
    # book daily: largest gains/losses and what follows in coin returns
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.reset_index(drop=True)
            br = d["book_return"].values; cr = d["coin_return"].values
            for i in range(len(d)):
                nxt = np.nansum(cr[i+1:i+6]) if i+6 <= len(d) else np.nan
                dl.append(dict(coin=coin, br=br[i], cr=cr[i], nxt5=nxt))
    dd = pd.DataFrame(dl).dropna()
    dd["brq"] = pd.qcut(dd["br"].rank(method="first"), 10, labels=False)
    out["book_decile_then_coin_next5"] = dd.groupby("brq")[["br", "cr", "nxt5"]].mean().round(5)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    tr = pd.concat(tr)
    tr["efq"] = pd.qcut(tr["entry_forecast"].rank(method="first"), 5, labels=False)
    out["trades_by_entry_fc"] = tr.groupby("efq").agg(n=("net_profit_loss_percent", "size"),
        fc=("entry_forecast", "mean"), net=("net_profit_loss_percent", "mean"),
        dur_days=("duration_minutes", lambda s: s.mean()/1440)).round(3)
    out["trades_by_coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["size", "mean", "median"]).round(3)
    return out
