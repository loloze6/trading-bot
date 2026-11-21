def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]
    rows = []
    mu = {}
    for c in bars:
        r = []
        for w, b in bars[c].items():
            r.append((b["close"].shift(-1)/b["close"]-1).dropna())
        mu[c] = pd.concat(r).mean()
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            pos = b["postRebalance_current_allocation"]
            f1 = cl.shift(-1)/cl-1
            hi = cl.rolling(60, min_periods=20).max()
            D = (1-cl/hi)*100
            r28 = cl/cl.shift(28)-1
            vol = cl.pct_change().rolling(20, min_periods=10).std()
            yr = pd.to_datetime(b["timestamp"]).dt.year
            df = pd.DataFrame({"coin": c, "win": w, "year": yr, "pos": pos, "f1": f1,
                               "fc": b["forecast"], "D": D, "r28": r28, "vol": vol, "i": np.arange(len(b)), "close": cl})
            df["gross"] = df.pos*df.f1
            df["mkt"] = df.pos*mu[c]
            df["timing"] = df.gross-df.mkt
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A = A.dropna(subset=["f1"])
    A["side"] = np.sign(A.pos).map({1: "long", -1: "short", 0: "flat"})
    A["Dq"] = pd.cut(A.D, [-0.01, 0.5, 5, 15, 30, 1000], labels=["at_high", "0.5-5", "5-15", "15-30", ">30"])
    A["volq"] = A.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    A["r28s"] = np.sign(A.r28)
    def agg(g):
        n_days = A.groupby(["win", "i"]).ngroups
        return pd.DataFrame({"gross_sum_per_day": g["gross"].sum()/n_days*1e4,
                             "mkt_per_day": g["mkt"].sum()/n_days*1e4,
                             "timing_per_day": g["timing"].sum()/n_days*1e4,
                             "bars": g.size(), "mean_abs_pos": g["pos"].apply(lambda s: s.abs().mean())})
    out = {}
    # contribution in bps/day of the book (sum over coin-bars / days / 6 coins)
    nd = A.groupby(["win", "i"]).ngroups*6
    def contr(key):
        g = A.groupby(key)
        return pd.DataFrame({"gross_bps": g["gross"].sum()/nd*1e4, "mkt_bps": g["mkt"].sum()/nd*1e4,
                             "timing_bps": g["timing"].sum()/nd*1e4, "bars": g.size(),
                             "abs_pos": g["pos"].apply(lambda s: s.abs().mean())}).round(3)
    out["total"] = contr(lambda x: 0)
    out["by_coin"] = contr("coin")
    out["by_year"] = contr("year")
    out["by_side"] = contr("side")
    out["by_dist_high"] = contr("Dq")
    out["by_side_dist"] = contr(["side", "Dq"])
    out["by_volq"] = contr("volq")
    wc = A.groupby("win")["gross"].sum()/nd*1e4
    out["windows_gross_sorted"] = wc.sort_values().round(3).reset_index(drop=True).to_frame("bps").T
    # slopes by horizon, non-overlapping
    res = []
    for h in [1, 3, 5, 10, 20, 30]:
        cs = []
        for c in bars:
            allr = []
            for w, b in bars[c].items():
                cl = b["close"].reset_index(drop=True)
                idx = np.arange(0, len(cl)-h, h)
                fr = cl.values[idx+h]/cl.values[idx]-1
                allr.append(pd.DataFrame({"fc": b["forecast"].values[idx], "fr": fr, "coin": c}))
            d = pd.concat(allr); d["ex"] = d.fr-d.fr.mean(); cs.append(d)
        d = pd.concat(cs).dropna()
        for nm, s in [("all", d), ("fc>0", d[d.fc > 0]), ("fc<0", d[d.fc < 0])]:
            if len(s) > 20:
                lr = stats.linregress(s.fc, s.ex)
                sg = np.sign(s.fc)*s.ex
                res.append({"h": h, "set": nm, "n": len(s), "slope_t": lr.slope/lr.stderr,
                            "signed_ex_mean_%": sg.mean()*100, "signed_t": sg.mean()/(sg.std()/np.sqrt(len(sg)))})
    out["slopes"] = pd.DataFrame(res).round(3)
    T = pd.concat([t.assign(coin=c) for c in trades for w, t in trades[c].items() if len(t)])
    T = T.sort_values("net_profit_loss_percent", ascending=False)
    tot = T.net_profit_loss_percent.sum()
    out["trades"] = pd.DataFrame({"n": [len(T)], "sum_net": [tot], "top10_share": [T.net_profit_loss_percent.head(10).sum()/tot],
                                  "top5pct_share": [T.net_profit_loss_percent.head(int(len(T)*0.05)).sum()/tot],
                                  "win_rate": [(T.net_profit_loss_percent > 0).mean()]}).round(3)
    out["trades_by_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "sum", "mean", "median"]).round(3)
    return out
