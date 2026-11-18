def explore(data):
    import numpy as np, pandas as pd
    out = {}
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    # book daily returns: mean over coins per (window, day)
    rows = []
    for c in coins:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    book = D.groupby(["wn","day"]).agg(b=("book_return","mean"), h=("coin_return","mean")).reset_index().sort_values(["wn","day"])
    book = book.dropna()
    def stats(x):
        return pd.Series({"mean": x.mean(), "sd": x.std(), "sharpe": x.mean()/x.std()*np.sqrt(365), "n": len(x)})
    out["book_vs_hold"] = pd.DataFrame({"book": stats(book["b"]), "hold": stats(book["h"])})
    book["year"] = pd.to_datetime(book["day"]).dt.year
    out["by_year"] = book.groupby("year").agg(b_mean=("b","mean"), h_mean=("h","mean"), n=("b","size"))
    out["by_window"] = book.groupby("wn").agg(b_sum=("b","sum"), h_sum=("h","sum"), n=("b","size"))
    # drawdown of chained book
    v = (1+book["b"]).cumprod(); dd = v/v.cummax()-1
    out["max_dd"] = float(dd.min())
    # bar-level: position, gain, by regime and volratio terciles, and trend state
    R = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.copy()
            b["ret1"] = b["close"].shift(-1)/b["close"]-1
            b["gain"] = b["postRebalance_current_allocation"]*b["ret1"]
            b["r5"] = b["close"]/b["close"].shift(5)-1
            b["r30"] = b["close"]/b["close"].shift(30)-1
            b["r60"] = b["close"]/b["close"].shift(60)-1
            b["sma"] = b["close"]/b["close"].rolling(50).mean()-1
            b["coin"]=c; b["w"]=w
            R.append(b)
    B = pd.concat(R)
    cm = B.groupby("coin")["ret1"].mean()
    B["cm"] = B["coin"].map(cm)
    B["mkt"] = B["postRebalance_current_allocation"]*B["cm"]
    B["timing"] = B["gain"]-B["mkt"]
    act = B[B["postRebalance_current_allocation"].abs()>1e-9]
    out["gain_decomp"] = pd.Series({"gain_mean_allbars": B["gain"].mean(), "mkt": B["mkt"].mean(), "timing": B["timing"].mean(), "share_active": len(act)/len(B), "mean_alloc_active": act["postRebalance_current_allocation"].mean()})
    act = act.dropna(subset=["ret1"])
    act["r30s"] = np.sign(act["r30"])
    out["active_by_r30sign"] = act.groupby("r30s").agg(n=("gain","size"), gain=("gain","mean"), ret1=("ret1","mean"), t=("gain", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    act["smas"] = np.sign(act["sma"])
    out["active_by_sma50sign"] = act.groupby("smas").agg(n=("gain","size"), gain=("gain","mean"), ret1=("ret1","mean"), t=("gain", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    act["fq"] = pd.qcut(act["forecast"], 3, labels=False, duplicates="drop")
    out["active_by_fc_tercile"] = act.groupby("fq").agg(n=("gain","size"), fc=("forecast","mean"), gain=("gain","mean"), ret1=("ret1","mean"))
    act["r5q"] = pd.qcut(act["r5"], 4, labels=False)
    out["active_by_r5_quart"] = act.groupby("r5q").agg(n=("gain","size"), r5=("r5","mean"), gain=("gain","mean"), ret1=("ret1","mean"))
    out["by_coin"] = act.groupby("coin").agg(gain=("gain","mean"), ret1=("ret1","mean"), n=("gain","size"))
    T = pd.concat([t.assign(coin=c) for c in coins for w,t in data["trades"][c].items() if len(t)])
    out["trades"] = pd.Series({"n": len(T), "mean_pl": T["profit_loss_percent"].mean(), "mean_net": T["net_profit_loss_percent"].mean(), "mean_dur_days": T["duration_minutes"].mean()/1440, "win": (T["net_profit_loss_percent"]>0).mean()})
    return out
