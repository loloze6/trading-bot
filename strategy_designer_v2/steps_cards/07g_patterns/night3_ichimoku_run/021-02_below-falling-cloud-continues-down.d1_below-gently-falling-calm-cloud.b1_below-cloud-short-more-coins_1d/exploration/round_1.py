def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 26
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            past26 = c / c.shift(26) - 1
            past13 = c / c.shift(13) - 1
            hi26 = b["high"].rolling(26).max(); lo26 = b["low"].rolling(26).min()
            pos26 = (c - lo26) / (hi26 - lo26)
            mid26 = (hi26 + lo26) / 2
            dmid = c / mid26 - 1
            fwd = c.shift(-H) / c - 1
            sl = b.get("debug_info.components.slope_size.last_history_value")
            vv = b.get("debug_info.components.vol30.last_history_value")
            for i in range(0, len(b), H):
                if i + H >= len(b):
                    break
                rows.append(dict(coin=coin, w=w, fwd=fwd[i], reg=b["regime"].iloc[i],
                                 fc=b["forecast"].iloc[i], vol20=vol20[i], past26=past26[i],
                                 past13=past13[i], pos26=pos26[i], dmid=dmid[i],
                                 slope=(sl.iloc[i] if sl is not None else np.nan),
                                 v30=(vv.iloc[i] if vv is not None else np.nan),
                                 wd=pd.Timestamp(b["timestamp"].iloc[i]).dayofweek))
            d = pd.DataFrame(dict(coin=coin, r=r1, nxt=r1.shift(-1), z=r1 / vol20.shift(1),
                                  wd=pd.to_datetime(b["timestamp"]).dt.dayofweek,
                                  reg=b["regime"], yr=pd.to_datetime(b["timestamp"]).dt.year))
            daily.append(d)
    df = pd.DataFrame(rows)
    st = df.groupby("coin")["fwd"].agg(["mean", "std"])
    df["drift"] = df["coin"].map(st["mean"]); df["usual"] = df["coin"].map(st["std"])
    df["ex"] = df["fwd"] - df["drift"]; df["sx"] = df["ex"] / df["usual"]
    out = {}
    def grp(col, q=4, sub=None):
        x = df if sub is None else sub
        x = x.dropna(subset=[col, "ex"]).copy()
        x["bin"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False) if len(s) >= q else np.nan)
        g = x.groupby("bin").agg(n=("ex", "size"), ex=("ex", "mean"), sx=("sx", "mean"),
                                 sd=("sx", "std"), fwd=("fwd", "mean"))
        g["t_sx"] = g["sx"] / (g["sd"] / np.sqrt(g["n"]))
        hi = x[x["bin"] == q - 1]["sx"]; lo = x[x["bin"] == 0]["sx"]
        g.loc["top-bottom t", "sx"] = stats.ttest_ind(hi, lo, equal_var=False).statistic
        return g.drop(columns="sd")
    out["regime"] = df.groupby("reg").agg(n=("ex", "size"), ex=("ex", "mean"), sx=("sx", "mean"), fwd=("fwd", "mean"))
    for col in ["past26", "past13", "pos26", "dmid", "vol20"]:
        out["by_" + col] = grp(col)
    mr = df[df["reg"] == "mean_reversion"]
    for col in ["slope", "v30", "dmid", "past26"]:
        out["inreg_" + col] = grp(col, 3, mr)
    dd = pd.concat(daily).dropna(subset=["r", "nxt", "z"])
    dd["zb"] = pd.cut(dd["z"], [-np.inf, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, np.inf])
    g = dd.groupby("zb").agg(n=("nxt", "size"), nxt=("nxt", "mean"), sd=("nxt", "std"))
    g["t"] = g["nxt"] / (g["sd"] / np.sqrt(g["n"])); out["next_day_after_z"] = g.drop(columns="sd")
    g = dd.groupby("wd").agg(n=("r", "size"), r=("r", "mean"), sd=("r", "std"))
    g["t"] = g["r"] / (g["sd"] / np.sqrt(g["n"])); out["weekday"] = g.drop(columns="sd")
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(d.assign(coin=coin, w=w))
    bk = pd.concat(bk).dropna(subset=["book_return"])
    out["book_by_coin"] = bk.groupby("coin").agg(mean=("book_return", "mean"), n=("book_return", "size")).sort_values("mean")
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    tr = pd.concat(tr)
    out["trades"] = tr.groupby("side").agg(n=("net_profit_loss_percent", "size"), mean=("net_profit_loss_percent", "mean"),
                                         med=("net_profit_loss_percent", "median"), win=("net_profit_loss_percent", lambda s: (s > 0).mean()))
    return out
