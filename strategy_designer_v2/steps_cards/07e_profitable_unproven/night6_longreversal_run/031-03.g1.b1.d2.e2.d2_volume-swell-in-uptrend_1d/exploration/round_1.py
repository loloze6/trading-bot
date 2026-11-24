def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # ---- book daily returns, market part
    rows = []
    coin_mean_daily = {}
    for c in bars:
        allr = pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        coin_mean_daily[c] = allr.mean()
    for c in bars:
        for w in bars[c]:
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos = b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            d = days[c][w].copy()
            d["day"] = pd.to_datetime(d["day"]).dt.floor("D")
            d = d.merge(pos.rename("pos").reset_index(), on="day", how="left")
            d["coin"] = c; d["win"] = w
            d["mkt"] = d["pos"] * coin_mean_daily[c]
            d["year"] = d["day"].dt.year
            rows.append(d)
    D = pd.concat(rows).dropna(subset=["book_return"])
    daily = D.groupby("day").agg(book=("book_return","mean"), hold=("coin_return","mean"), mkt=("mkt","mean"), year=("year","first"))
    out["book mean daily, market part, timing"] = pd.Series({"book": daily.book.mean(), "market_part": daily.mkt.mean(), "timing": daily.book.mean()-daily.mkt.mean(), "hold": daily.hold.mean(), "n_days": len(daily)})
    yr = daily.groupby("year").agg(book=("book","mean"), hold=("hold","mean"), mkt=("mkt","mean"), n=("book","size"))
    yr["sharpe"] = daily.groupby("year")["book"].apply(lambda x: x.mean()/x.std()*np.sqrt(365))
    out["by year"] = yr
    # per coin contribution: sum over days of coin return / ncoins that day
    nc = D.groupby("day")["coin"].transform("count")
    D["contrib"] = D["book_return"]/nc
    cc = D.groupby("coin").agg(contrib=("contrib","sum"), mean_book=("book_return","mean"), mean_pos=("pos","mean"))
    cc["share"] = cc.contrib/cc.contrib.sum()
    out["by coin"] = cc.sort_values("share", ascending=False)
    # ---- trades
    T = pd.concat([data["trades"][c][w].assign(coin=c) for c in data["trades"] for w in data["trades"][c] if len(data["trades"][c][w])])
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(p), "mean": p.mean(), "median": p.median(), "win_share": (p>0).mean(), "top10_share_of_sum": p.head(10).sum()/p.sum(), "top5pct_share": p.head(int(len(p)*0.05)).sum()/p.sum(), "mean_days": T.duration_minutes.mean()/1440})
    # ---- grid analysis at several horizons
    res = []
    for h in [7, 14, 28]:
        G = []
        for c in bars:
            cm = []
            for w in bars[c]:
                b = bars[c][w].reset_index(drop=True)
                cl = b["close"]; v = b["volume"]
                sma = cl.rolling(50).mean()
                fr = cl.shift(-h)/cl - 1
                r60 = cl/cl.shift(60) - 1
                vr = v.rolling(14).mean()/v.rolling(30).mean() - 1
                idx = np.arange(0, len(b), h)
                g = pd.DataFrame({"fr": fr.iloc[idx].values, "fc": b["forecast"].iloc[idx].values,
                                  "reg": b["regime"].iloc[idx].values, "dist": (cl/sma-1).iloc[idx].values,
                                  "r60": r60.iloc[idx].values, "vr": vr.iloc[idx].values,
                                  "day": pd.to_datetime(b["timestamp"].iloc[idx]).dt.floor("D").values})
                g["coin"] = c
                G.append(g)
        G = pd.concat(G).dropna(subset=["fr"])
        G["ex"] = G["fr"] - G.groupby("coin")["fr"].transform("mean")
        def tm(x):
            x = x.dropna(); return pd.Series({"mean_ex": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, "n": len(x)})
        for name, m in [("trend_fc>0", (G.reg=="trending")&(G.fc>0)), ("trend_fc=0", (G.reg=="trending")&(G.fc<=0)), ("unknown", G.reg!="trending")]:
            s = tm(G.loc[m,"ex"]); s["h"]=h; s["group"]=name; s["mean_raw"]=G.loc[m,"fr"].mean(); res.append(s)
        # correlations with ex across all grid
        for var in ["dist", "r60", "vr"]:
            sub = G[["ex", var]].dropna()
            r, pv = stats.spearmanr(sub[var], sub["ex"])
            res.append(pd.Series({"h": h, "group": "rank corr ex~"+var+" all", "mean_ex": r, "t": r*np.sqrt((len(sub)-2)/(1-r*r)), "n": len(sub)}))
            subt = G.loc[G.reg=="trending", ["ex", var]].dropna()
            r = stats.spearmanr(subt[var], subt["ex"])[0]
            res.append(pd.Series({"h": h, "group": "rank corr ex~"+var+" trending", "mean_ex": r, "t": r*np.sqrt((len(subt)-2)/(1-r*r)), "n": len(subt)}))
    out["grid by group and horizon"] = pd.DataFrame(res)[["h","group","mean_ex","t","n","mean_raw"]]
    return out
