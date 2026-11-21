def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    bar_rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c, hi, lo = b["close"], b["high"], b["low"]
            rng = (hi - lo) / c
            fwd = c.shift(-H) / c - 1
            ph = hi.shift(1).rolling(12).max(); pl = lo.shift(1).rolling(12).min()
            up = (c / ph - 1).clip(lower=0); dn = (pl / c - 1).clip(lower=0)
            stretch = (ph - pl) / c
            narrow = rng.rolling(180, min_periods=60).mean() / stretch
            quiet = rng.rolling(180, min_periods=60).mean() / rng.rolling(42).mean()
            past3 = c / c.shift(18) - 1
            past1 = c / c.shift(6) - 1
            r1 = c.pct_change()
            vol7 = r1.rolling(42).std()
            hi30 = hi.rolling(180, min_periods=60).max()
            near = c / hi30 - 1
            g = pd.DataFrame({"coin": coin, "win": w, "fwd": fwd, "up": up, "dn": dn,
                              "narrow": narrow, "quiet": quiet, "past3": past3, "past1": past1,
                              "vol7": vol7, "near": near, "fc": b["forecast"],
                              "alloc": b["postRebalance_current_allocation"]})
            rows.append(g.iloc[::H])
            ts = pd.to_datetime(b["timestamp"])
            bar_rows.append(pd.DataFrame({"coin": coin, "r1n": r1.shift(-1), "hour": ts.dt.hour,
                                          "wd": ts.dt.weekday}))
    d = pd.concat(rows).dropna(subset=["fwd"])
    drift = d.groupby("coin")["fwd"].transform("mean")
    usual = d.groupby("coin")["fwd"].transform("std")
    d["ex"] = d["fwd"] - drift
    d["str"] = d["ex"] / usual
    def grp(col, q=5, sub=None):
        x = d if sub is None else d[sub]
        x = x.dropna(subset=[col]).copy()
        x["q"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        o = x.groupby("q").agg(n=("ex", "size"), mean_ex=("ex", "mean"), sd=("ex", "std"), strength=("str", "mean"), mid=(col, "median"))
        o["t"] = o["mean_ex"] / (o["sd"] / np.sqrt(o["n"]))
        return o.drop(columns="sd").round(5)
    out = {}
    out["n_grid_drift"] = d.groupby("coin").agg(n=("fwd", "size"), drift=("fwd", "mean"), usual=("fwd", "std")).round(5)
    out["by_past3"] = grp("past3")
    out["by_past1"] = grp("past1")
    out["by_narrow"] = grp("narrow")
    out["by_quiet"] = grp("quiet")
    out["by_vol7"] = grp("vol7")
    out["by_near30high"] = grp("near")
    out["upbreak_by_size"] = grp("up", 3, d["up"] > 0)
    out["dnbreak_by_size"] = grp("dn", 3, d["dn"] > 0)
    out["upbreak_by_quiet"] = grp("quiet", 3, d["up"] > 0)
    out["by_forecast_pos"] = grp("fc", 3, d["fc"] > 0)
    # per coin correlations of ex with features
    cc = {}
    for col in ["past3", "past1", "narrow", "quiet", "vol7", "near"]:
        cc[col] = d.dropna(subset=[col]).groupby("coin").apply(lambda x: stats.spearmanr(x[col], x["ex"])[0])
    out["spearman_by_coin"] = pd.DataFrame(cc).round(3)
    br = pd.concat(bar_rows).dropna()
    for k in ["hour", "wd"]:
        o = br.groupby(k)["r1n"].agg(["size", "mean", "std"])
        o["t"] = o["mean"] / (o["std"] / np.sqrt(o["size"]))
        out["next4h_by_" + k] = o.round(6)
    # book days
    dd = pd.concat([df.assign(coin=c, win=w) for c, ws in data["days"].items() for w, df in ws.items()]).dropna(subset=["book_return"])
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    out["book_by_year"] = dd.assign(y=pd.to_datetime(dd["day"]).dt.year).groupby("y")[["book_return", "coin_return"]].mean().round(5)
    tr = pd.concat([df.assign(coin=c) for c, ws in data["trades"].items() for w, df in ws.items()])
    out["trades_by_coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["size", "mean", "median"]).round(3)
    return out
