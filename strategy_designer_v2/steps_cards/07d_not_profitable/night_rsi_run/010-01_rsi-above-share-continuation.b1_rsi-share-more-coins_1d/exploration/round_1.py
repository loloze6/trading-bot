def explore(data):
    import numpy as np, pandas as pd
    out = {}
    days = data["days"]; bars = data["bars"]; trades = data["trades"]
    # per coin book vs hold daily
    rows = []
    allbook = []; allhold = []
    for c in days:
        b = pd.concat([days[c][w].assign(w=w) for w in days[c]])
        br = b["book_return"].dropna(); cr = b["coin_return"].dropna()
        rows.append({"coin": c, "book_mean": br.mean(), "book_sh": br.mean()/br.std()*np.sqrt(365),
                     "hold_mean": cr.mean(), "hold_sh": cr.mean()/cr.std()*np.sqrt(365), "n": len(br)})
    out["per_coin_daily"] = pd.DataFrame(rows)
    # bar-level: position gain, long vs short, market vs timing
    recs = []
    for c in bars:
        for w, df in bars[c].items():
            d = df.copy()
            d["r1"] = d["close"].shift(-1)/d["close"] - 1
            d["pos"] = d["postRebalance_current_allocation"]
            d["gain"] = d["pos"]*d["r1"]
            d["fee"] = (d["total_portfolio_value"] - d["postRebalance_total_value"]) / d["total_portfolio_value"]
            # trailing 30d return and 60d
            d["ret30"] = d["close"]/d["close"].shift(30) - 1
            d["ret90"] = d["close"]/d["close"].shift(90) - 1
            d["coin"] = c; d["w"] = w
            recs.append(d[["coin","w","pos","r1","gain","fee","forecast","ret30","ret90"]])
    A = pd.concat(recs).dropna(subset=["r1"])
    mu = A.groupby("coin")["r1"].transform("mean")
    A["mkt"] = A["pos"]*mu; A["timing"] = A["gain"]-A["mkt"]
    A["side"] = np.sign(A["pos"]).map({1:"long",-1:"short",0:"flat"})
    out["by_side"] = A.groupby("side").agg(n=("gain","size"), gain_mean=("gain","mean"), mkt=("mkt","mean"),
                                         timing=("timing","mean"), r1=("r1","mean"), pos=("pos","mean"), fee=("fee","mean"))
    out["totals"] = pd.Series({"gain": A.gain.mean(), "mkt": A.mkt.mean(), "timing": A.timing.mean(),
                               "fee": A.fee.mean(), "mean_abs_pos": A.pos.abs().mean(), "share_long": (A.pos>0).mean(),
                               "share_short": (A.pos<0).mean()})
    # forecast buckets vs next-14 non-overlapping returns
    g = []
    for c in bars:
        for w, df in bars[c].items():
            d = df.reset_index(drop=True)
            d["f14"] = d["close"].shift(-14)/d["close"] - 1
            d["ret30"] = d["close"]/d["close"].shift(30) - 1
            s = d.iloc[::14].dropna(subset=["f14"])
            s = s.assign(coin=c)
            g.append(s[["coin","forecast","f14","ret30"]])
    G = pd.concat(g)
    G["fb"] = pd.cut(G["forecast"], [-21,-10,-3,3,10,21])
    out["fwd14_by_forecast"] = G.groupby("fb", observed=True)["f14"].agg(["count","mean","median"])
    G["rb"] = pd.qcut(G["ret30"], 5)
    out["fwd14_by_ret30"] = G.groupby("rb", observed=True)["f14"].agg(["count","mean"])
    # by window, book daily mean pooled
    D = pd.concat([days[c][w].assign(w=w, coin=c) for c in days for w in days[c]])
    out["by_window"] = D.groupby("w").agg(book=("book_return","mean"), hold=("coin_return","mean")).T
    # trades
    T = pd.concat([trades[c][w].assign(coin=c) for c in trades for w in trades[c] if len(trades[c][w])])
    out["trades"] = T.groupby("side").agg(n=("side","size"), pl=("profit_loss_percent","mean"),
                                          net=("net_profit_loss_percent","mean"), dur_d=("duration_minutes", lambda x: x.mean()/1440))
    return out
