def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 5
    rows = []
    win_rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            b["fwd"] = c.shift(-H) / c - 1
            b["past5"] = c / c.shift(5) - 1
            b["past20"] = c / c.shift(20) - 1
            r = c.pct_change()
            b["vol20"] = r.rolling(20).std()
            b["volz"] = b["volume"] / b["volume"].rolling(5).mean().shift(1)
            b["inprof"] = (b["regime"] == "unknown")
            b["raw"] = b.get("debug_info.components.vol_shrink.last_history_value")
            b["coin"] = coin; b["win"] = w
            b["pos"] = np.arange(len(b))
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            g = b[(b["pos"] % H == 0) & b["fwd"].notna()]
            rows.append(g[["coin","win","year","timestamp","fwd","forecast","inprof","past5","past20","vol20","raw","volz","postRebalance_current_allocation"]])
            d = data["days"][coin][w]
            win_rows.append(pd.DataFrame({"coin":[coin],"win":[w],
                "book":[d["book_return"].sum()],"coin_ret":[d["coin_return"].sum()],
                "inprof_share":[b["inprof"].mean()],
                "held_share":[(b["postRebalance_current_allocation"].abs()>1e-9).mean()]}))
    G = pd.concat(rows, ignore_index=True)
    drift = G.groupby("coin")["fwd"].mean()
    G["ex"] = G["fwd"] - G["coin"].map(drift)
    P = G[G["inprof"]].copy()
    P["case"] = P["forecast"] <= -2
    def summ(df, by):
        return df.groupby(by).agg(n=("ex","size"), mean_fwd=("fwd","mean"), mean_ex=("ex","mean"),
                                  t=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out["by_case"] = summ(P, "case")
    P["fbin"] = pd.cut(P["forecast"], [-21,-15,-10,-5,-2,-0.01,0.01], labels=["<-15","-15..-10","-10..-5","-5..-2","-2..0","0"])
    out["by_forecast_bin"] = summ(P, "fbin")
    P["rawbin"] = pd.qcut(P["raw"], 5, duplicates="drop")
    out["by_raw_quintile"] = summ(P, "rawbin")
    P["p5bin"] = pd.qcut(P["past5"], 3, labels=["fell","mid","rose"])
    out["case_x_past5"] = summ(P, ["p5bin","case"])
    P["p20bin"] = pd.qcut(P["past20"], 3, labels=["deep","mid","shallow"])
    out["case_x_past20"] = summ(P, ["p20bin","case"])
    P["v20bin"] = pd.qcut(P["vol20"], 2, labels=["calm","agit"])
    out["case_x_vol20"] = summ(P, ["v20bin","case"])
    out["case_x_year"] = summ(P, ["year","case"])
    out["case_x_coin"] = summ(P, ["coin","case"])
    W = pd.concat(win_rows, ignore_index=True)
    out["by_window"] = W.groupby("win")[["book","coin_ret","inprof_share","held_share"]].mean()
    T = pd.concat([t.assign(coin=c, win=w) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)], ignore_index=True)
    T["days"] = T["duration_minutes"]/1440
    T["dbin"] = pd.cut(T["days"], [0,5.5,10,20,40,400])
    out["trades_by_duration"] = T.groupby("dbin").agg(n=("net_profit_loss_percent","size"), mean_net=("net_profit_loss_percent","mean"), mean_gross=("profit_loss_percent","mean"))
    return out
