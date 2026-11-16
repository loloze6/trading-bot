def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = pd.concat([b["close"].shift(-1) / b["close"] - 1 for b in wins.values()])
        cmean = allr.mean()
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            b["fwd"] = b["close"].shift(-1) / b["close"] - 1
            for h in (3, 5):
                b[f"fwd{h}"] = b["close"].shift(-h) / b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gross"] = b["pos"] * b["fwd"]
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["net"] = b["gross"] - b["fee"]
            r1 = b["close"].pct_change()
            sd = r1.rolling(20, min_periods=10).std()
            b["vsr"] = r1 / sd
            sma50 = b["close"].rolling(50, min_periods=20).mean()
            b["trend"] = np.where(b["close"] > sma50, "above50", "below50")
            b["idx"] = np.arange(len(b))
            b["coin"] = coin; b["win"] = w; b["cmean"] = cmean
            rows.append(b)
    d = pd.concat(rows).dropna(subset=["fwd", "pos", "vsr"])
    d["side"] = np.where(d["pos"] > 0, "long", np.where(d["pos"] < 0, "short", "flat"))
    d["vq"] = pd.qcut(d["vsr"], 10, labels=False)
    out = {}
    out["net_by_vsr_decile"] = d.groupby("vq").agg(n=("net", "size"), vsr=("vsr", "mean"), gross=("gross", "mean"), fee=("fee", "mean"), net=("net", "mean"))
    out["net_by_trend_side"] = d.groupby(["trend", "side"]).agg(n=("net", "size"), gross=("gross", "mean"), fee=("fee", "mean"), net=("net", "mean"))
    # multi-day excess forward after moves, non-overlapping grid
    res = {}
    for h in (1, 3, 5):
        col = "fwd" if h == 1 else f"fwd{h}"
        s = d[(d["idx"] % h == 0)].dropna(subset=[col])
        y = s[col] - h * s["cmean"]
        for name, m in {"fall_all": s["vsr"] < 0, "rise_all": s["vsr"] > 0}.items():
            sl, ic, rr, p, se = stats.linregress(s.loc[m, "vsr"], y[m])
            res[f"h{h}_{name}"] = {"n": int(m.sum()), "slope": sl, "t": sl / se}
        for tr in ("above50", "below50"):
            for name, m in {"fall": s["vsr"] < 0, "rise": s["vsr"] > 0}.items():
                mm = m & (s["trend"] == tr)
                sl, ic, rr, p, se = stats.linregress(s.loc[mm, "vsr"], y[mm])
                res[f"h{h}_{tr}_{name}"] = {"n": int(mm.sum()), "slope": sl, "t": sl / se}
    out["slopes"] = pd.DataFrame(res).T
    # book daily metrics, actual and long-only-gross approximation
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin, win=w))
    D = pd.concat(dd)
    br = D.groupby(["win", "day"]).book_return.mean().dropna()
    out["book_by_year"] = br.groupby(pd.to_datetime(br.index.get_level_values("day")).year).agg(["mean", "std", "count"]).assign(sharpe=lambda z: z["mean"] / z["std"] * np.sqrt(365))
    # variant: long side only net
    d["net_long_only"] = np.where(d["pos"] > 0, d["net"], 0.0)
    d["net_bigmove"] = np.where(d["vsr"].abs() > d["vsr"].abs().median(), d["net"], 0.0)
    out["variants_mean_per_bar"] = pd.Series({"actual_net": d["net"].mean(), "long_only_net": d["net_long_only"].mean(),
                                              "big_moves_only_net": d["net_bigmove"].mean(),
                                              "short_net": d.loc[d.pos < 0, "net"].mean(), "long_net": d.loc[d.pos > 0, "net"].mean()})
    return out
