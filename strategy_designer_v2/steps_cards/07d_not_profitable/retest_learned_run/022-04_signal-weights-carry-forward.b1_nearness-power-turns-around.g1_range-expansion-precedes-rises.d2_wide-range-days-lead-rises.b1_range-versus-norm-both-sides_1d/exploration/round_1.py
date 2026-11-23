def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    # grid cases, coin mean 3-bar return over all windows
    for c in bars:
        recs = []
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            rng = (b["high"] - b["low"]) / b["close"]
            ratio = (b["high"] - b["low"]) / (b["high"] - b["low"]).rolling(30).mean()
            r1 = b["close"].pct_change()
            r30 = b["close"] / b["close"].shift(30) - 1
            for i in range(0, len(b) - 3, 3):
                recs.append(dict(coin=c, w=w, f=b["forecast"].iloc[i], ratio=ratio.iloc[i],
                                 r1=r1.iloc[i], r30=r30.iloc[i],
                                 alloc=b["postRebalance_current_allocation"].iloc[i],
                                 fwd=cl[i + 3] / cl[i] - 1, year=pd.Timestamp(b["timestamp"].iloc[i]).year))
        df = pd.DataFrame(recs)
        df["ex"] = df["fwd"] - df["fwd"].mean()
        rows.append(df)
    g = pd.concat(rows)
    g["fb"] = pd.cut(g["f"], [-100, -3, -1.5, -0.5, 0.5, 1.5, 3, 100])
    out = {}
    out["by_forecast_bucket"] = g.groupby("fb").agg(n=("ex", "size"), mean_ex=("ex", "mean"), mean_fwd=("fwd", "mean"),
                                                    mean_alloc=("alloc", "mean"))
    g["dir_ex"] = np.sign(g["f"]) * g["ex"]
    out["side"] = g[g.f != 0].groupby(np.sign(g["f"])).agg(n=("ex", "size"), mean_ex=("ex", "mean"),
                                                           t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    # wide day: up-day vs down-day
    g["wide"] = g["f"] > 1.5
    g["up"] = g["r1"] > 0
    out["wide_by_dayside"] = g.groupby(["wide", "up"]).agg(n=("ex", "size"), mean_ex=("ex", "mean"),
                                                           t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    g["trend"] = g["r30"] > 0
    out["wide_by_trend"] = g.groupby(["wide", "trend"]).agg(n=("ex", "size"), mean_ex=("ex", "mean"),
                                                            t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    out["by_year_dirgain"] = g[g.f.abs() > 1.5].groupby("year")["dir_ex"].agg(["size", "mean"])
    out["coin_dirgain_strong"] = g[g.f.abs() > 1.5].groupby("coin")["dir_ex"].agg(["size", "mean"])
    # book: position gain by side on daily book
    pos = []
    for c in bars:
        for w, b in bars[c].items():
            a = b["postRebalance_current_allocation"].values[:-1]
            r = b["close"].pct_change().shift(-1).values[:-1]
            fee = b["postRebalance_total_value"].values / b["total_portfolio_value"].values - 1
            pos.append(pd.DataFrame(dict(a=a, g=a * r, fee=fee[:-1], f=b["forecast"].values[:-1])))
    p = pd.concat(pos)
    p["side"] = np.sign(p["a"])
    p["fb"] = pd.cut(p["f"], [-100, -3, -1.5, -0.5, 0.5, 1.5, 3, 100])
    out["bar_gain_by_fb"] = p.groupby("fb").agg(n=("g", "size"), gain=("g", "sum"), fee=("fee", "sum"),
                                                mean_abs_a=("a", lambda x: x.abs().mean()))
    out["share_f_abs_lt_0.5"] = float((p.f.abs() < 0.5).mean())
    # drawdown of book
    dd = []
    for w in days[list(days)[0]]:
        br = pd.concat([days[c][w].set_index("day")["book_return"] for c in days if w in days[c]], axis=1).mean(axis=1)
        dd.append(pd.DataFrame(dict(w=w, r=br.values)))
    d = pd.concat(dd).dropna()
    v = (1 + d["r"]).cumprod()
    d["dd"] = v / v.cummax() - 1
    out["dd_by_window"] = d.groupby("w")["dd"].min().sort_values().head(8)
    out["mean_ret_by_window"] = d.groupby("w")["r"].mean().sort_values().head(8)
    return out
