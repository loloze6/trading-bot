def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily returns, pooled
    drows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = c; d["w"] = w; drows.append(d)
    D = pd.concat(drows)
    book = D.groupby(["w", "day"])["book_return"].mean()
    hold = D.groupby(["w", "day"])["coin_return"].mean()
    out["book_hold_daily"] = pd.DataFrame({"book_mean": [book.mean()], "book_sh": [book.mean()/book.std()*np.sqrt(365)],
                                           "hold_mean": [hold.mean()], "hold_sh": [hold.mean()/hold.std()*np.sqrt(365)], "ndays": [len(book)]})
    # per bar: gross gain, fees, market part, by coin
    rows = []; grid = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            r1 = b["close"].shift(-1)/b["close"] - 1
            pos = b["postRebalance_current_allocation"].fillna(0)
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            rows.append(pd.DataFrame({"coin": c, "w": w, "pos": pos, "r1": r1, "gain": pos*r1, "fee": fee,
                                      "fc": b["forecast"], "turn": (pos - b["previous_allocation"].fillna(0)).abs()}))
            cl = b["close"].values; n = len(cl)
            lr = np.log(b["close"]).diff()
            for i in range(72, n-72, 72):
                past = cl[i]/cl[i-72]-1; fwd = cl[i+72]/cl[i]-1
                h = (b["close"].pct_change().values[i-71:i+1])
                gains = np.sort(h[h > 0])[::-1]
                top3 = gains[:3].sum()
                netlog = lr.values[i-71:i+1].sum()
                share = top3/netlog if netlog > 0 else np.nan
                grid.append((c, w, past, fwd, share, b["forecast"].iloc[i], pos.iloc[i]))
    R = pd.concat(rows)
    R = R.dropna(subset=["r1"])
    mu = R.groupby("coin")["r1"].mean()
    R["mkt"] = R["pos"] * R["coin"].map(mu)
    out["bar_decomp"] = pd.DataFrame({"gross_per_bar": [R["gain"].mean()], "fee_per_bar": [R["fee"].mean()],
                                      "market_part": [R["mkt"].mean()], "timing": [R["gain"].mean()-R["mkt"].mean()],
                                      "mean_pos": [R["pos"].mean()], "share_in": [(R["pos"].abs()>1e-6).mean()],
                                      "turnover_per_bar": [R["turn"].mean()]})
    bc = R.groupby("coin").agg(gross=("gain","mean"), fee=("fee","mean"), mkt=("mkt","mean"), pos=("pos","mean"), turn=("turn","mean"))
    out["by_coin_per_bar"] = bc*24
    # by forecast bin
    R["fb"] = pd.cut(R["fc"], [-0.01, 0.01, 5, 10, 15, 20.01])
    out["by_forecast_bin"] = R.groupby("fb").agg(n=("gain","size"), r1_mean=("r1","mean"), gain=("gain","mean"), fee=("fee","mean"), turn=("turn","mean"))
    G = pd.DataFrame(grid, columns=["coin","w","past","fwd","share","fc","pos"])
    cm = G.groupby("coin")["fwd"].mean()
    G["ex"] = G["fwd"] - G["coin"].map(cm)
    up = G[G["past"]>0].copy()
    up["sq"] = pd.qcut(up["share"], 4, labels=False, duplicates="drop")
    out["up_by_topshare_q"] = up.groupby("sq").agg(n=("ex","size"), share=("share","mean"), past=("past","mean"), ex=("ex","mean"), t=("ex", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    G["pq"] = pd.qcut(G["past"], 5, labels=False)
    out["all_by_past_q"] = G.groupby("pq").agg(n=("ex","size"), past=("past","mean"), ex=("ex","mean"), t=("ex", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    # 2-way: past size tercile x share half among up
    up["pt"] = pd.qcut(up["past"], 3, labels=False)
    up["sh"] = pd.qcut(up["share"], 2, labels=False)
    out["up_past_x_share"] = up.groupby(["pt","sh"]).agg(n=("ex","size"), ex=("ex","mean"))
    # trades
    T = pd.concat([t for ws in data["trades"].values() for t in ws.values()])
    out["trades"] = pd.DataFrame({"n": [len(T)], "dur_h_med": [T["duration_minutes"].median()/60], "pl": [T["profit_loss_percent"].mean()],
                                  "net": [T["net_profit_loss_percent"].mean()], "win": [(T["profit_loss_percent"]>0).mean()]})
    out["book_by_window"] = book.groupby(level=0).mean().describe()
    return out
