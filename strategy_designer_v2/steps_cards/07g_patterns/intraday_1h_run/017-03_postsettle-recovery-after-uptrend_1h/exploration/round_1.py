def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            d = df[["timestamp","open","close","volume","postRebalance_current_allocation","total_portfolio_value","postRebalance_total_value"]].copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d["hour"] = d["ts"].dt.hour
            d["wd"] = d["ts"].dt.weekday
            d["r1"] = d["close"].shift(-1)/d["close"]-1
            d["r2"] = d["close"].shift(-2)/d["close"]-1
            d["r4"] = d["close"].shift(-4)/d["close"]-1
            d["r24"] = d["close"].shift(-24)/d["close"]-1
            d["rise72"] = d["close"]/d["close"].shift(72)-1
            d["past1"] = d["close"]/d["close"].shift(1)-1
            d["past24"] = d["close"]/d["close"].shift(24)-1
            d["vol24"] = d["past1"].rolling(24).std()
            d["vol720"] = d["past1"].rolling(720).std()
            d["lv"] = np.log(d["volume"].replace(0,np.nan))
            d["lv_rel"] = d["lv"] - d["lv"].rolling(168).mean()
            d["pos"] = d["postRebalance_current_allocation"]
            d["gain"] = d["pos"]*d["r1"]
            d["fee"] = (d["total_portfolio_value"]-d["postRebalance_total_value"])/d["total_portfolio_value"]
            d["i"] = np.arange(len(d))
            d["coin"]=c; d["w"]=w
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    # coin mean returns
    m1 = A.groupby("coin")["r1"].mean()
    A["x1"] = A["r1"]-A["coin"].map(m1)
    # hourly excess return by hour, t
    g = A.groupby("hour")["x1"]
    out["x1_by_hour_bp_t"] = pd.DataFrame({"bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # volume relative by hour
    out["lvrel_by_hour"] = A.groupby("hour")["lv_rel"].mean()
    # interaction: 1h excess return x sign of 72-bar rise by hour (trend-signed)
    A["sgn"] = np.sign(A["rise72"])
    A["tx1"] = A["x1"]*A["sgn"]
    g = A.groupby("hour")["tx1"]
    out["trendsigned_x1_by_hour"] = pd.DataFrame({"bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count()))})
    # reversal after large 1h moves, grid h=1 is all bars; by past1 decile
    A["q1"] = A.groupby("coin")["past1"].transform(lambda s: pd.qcut(s,10,labels=False,duplicates="drop"))
    g = A.groupby("q1")["x1"]
    out["x1_by_past1_decile"] = pd.DataFrame({"bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # next 24h on non-overlapping grid by past24 decile
    G = A[A["i"]%24==0].copy()
    m24 = G.groupby("coin")["r24"].mean()
    G["x24"] = G["r24"]-G["coin"].map(m24)
    G["q24"] = G.groupby("coin")["past24"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    g = G.groupby("q24")["x24"]
    out["x24_by_past24_quint"] = pd.DataFrame({"bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    G["qr72"] = G.groupby("coin")["rise72"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    g = G.groupby("qr72")["x24"]
    out["x24_by_rise72_quint"] = pd.DataFrame({"bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # vol regime: |r1| by vol720 tercile and x1 sign
    # book: gross gain vs fee
    act = A[A["pos"].abs()>0]
    out["book_gross_vs_fee"] = pd.Series({"mean_gain_per_bar_bp": A["gain"].mean()*1e4, "mean_fee_per_bar_bp": A["fee"].mean()*1e4,
        "active_share": len(act)/len(A), "gain_active_bp": act["gain"].mean()*1e4, "fee_sum_per_coin_window_pct": A.groupby(["coin","w"])["fee"].sum().mean()*100,
        "gain_sum_per_coin_window_pct": A.groupby(["coin","w"])["gain"].sum().mean()*100})
    out["gain_by_hour_active_bp"] = act.groupby("hour")["gain"].agg(["mean","count"]).assign(mean=lambda x:x["mean"]*1e4)
    # book daily by weekday
    D = pd.concat([days[c][w].assign(coin=c,w=w) for c in days for w in days[c]])
    D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    g = D.groupby("wd")[["book_return","coin_return"]].mean()*1e4
    out["daily_bp_by_weekday"]=g
    # weekday x hour excess? per coin x1 by weekday
    g = A.groupby("wd")["x1"]
    out["x1_by_weekday"] = pd.DataFrame({"bp":g.mean()*1e4,"t":g.mean()/(g.std()/np.sqrt(g.count()))})
    return out
