def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    coin_mean = {}
    for c, ws in data["bars"].items():
        rs = []
        for w, b in ws.items():
            r = b["close"].pct_change().dropna()
            rs.append(r)
        coin_mean[c] = pd.concat(rs).mean()
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            a = b["postRebalance_current_allocation"].fillna(0).values
            nxt = np.r_[cl[1:] / cl[:-1] - 1, np.nan]
            r20 = pd.Series(cl).pct_change(20).values
            fc = b["forecast"].fillna(0).values
            ts = pd.to_datetime(b["timestamp"])
            for i in range(len(b) - 1):
                rows.append((c, w, ts[i].year, ts[i].normalize(), a[i], nxt[i], a[i]*nxt[i], a[i]*coin_mean[c], r20[i], fc[i], b["regime"].iloc[i]))
    df = pd.DataFrame(rows, columns=["coin","w","year","day","a","ret","gain","drift","r20","fc","regime"])
    # book-like daily: per day mean over coins
    day = df.groupby(["w","day"])[["gain","drift"]].mean()
    out["book_gain_split"] = pd.Series({"mean_gain": day["gain"].mean(), "mean_drift_part": day["drift"].mean(),
        "timing": day["gain"].mean()-day["drift"].mean(),
        "t_gain": day["gain"].mean()/day["gain"].std()*np.sqrt(len(day)),
        "t_timing": (day["gain"]-day["drift"]).mean()/(day["gain"]-day["drift"]).std()*np.sqrt(len(day)), "n_days": len(day)})
    # per coin contribution
    pc = df.groupby("coin").agg(gain_sum=("gain","sum"), drift_sum=("drift","sum"), share_in=("a", lambda x:(x.abs()>0).mean()))
    pc["share_of_total_gain"] = pc["gain_sum"]/pc["gain_sum"].sum()
    out["per_coin"] = pc.sort_values("gain_sum", ascending=False)
    py = df.groupby("year").agg(gain_sum=("gain","sum"), drift_sum=("drift","sum"), coin_ret_mean=("ret","mean"), in_share=("a", lambda x:(x.abs()>0).mean()))
    out["per_year"] = py
    # gain by r20 quintile where in position, and coin mean next ret by r20 quintile overall
    d2 = df.dropna(subset=["r20","ret"]).copy()
    d2["q"] = pd.qcut(d2["r20"], 5, labels=False)
    g = d2.groupby("q").agg(r20_mean=("r20","mean"), next1d_ret=("ret","mean"), n=("ret","size"),
                            in_share=("a", lambda x:(x>0).mean()), gain_sum=("gain","sum"))
    out["by_r20_quintile_all_bars"] = g
    # in position vs not, when r20>0
    pos = d2[d2["r20"]>0]
    g2 = pos.groupby(pos["a"]>0)["ret"].agg(["mean","count","std"])
    out["r20pos_in_vs_out_1d"] = g2
    # trades concentration
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t): tr.append(t.assign(coin=c, w=w))
    T = pd.concat(tr)
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(p), "sum": p.sum(), "top10_sum": p.head(10).sum(), "top5pct_sum": p.head(int(len(p)*0.05)).sum(),
        "winrate": (p>0).mean(), "mean": p.mean(), "median": p.median(), "mean_dur_days": T["duration_minutes"].mean()/1440})
    return out
