def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; out = {}
    H = 7
    rows = []
    drift = {}
    for coin, ws in bars.items():
        allr = []
        for w, b in ws.items():
            c = b["close"].values
            n = len(c)
            for i in range(0, n - H, H):
                allr.append(c[i+H]/c[i]-1)
        drift[coin] = np.mean(allr) if allr else np.nan
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; hi = b["high"]; lo = b["low"]
            rr = (hi-lo)/c
            f = pd.DataFrame({
                "coin": coin, "w": w,
                "inprof": (b["regime"]=="unknown").values,
                "fc": b["forecast"].values,
                "raw": b.get("debug_info.components.scaled_rise.last_history_value", pd.Series(np.nan,index=b.index)).values,
                "r1": c.pct_change().values,
                "r3": c.pct_change(3).values,
                "r7": c.pct_change(7).values,
                "r14": c.pct_change(14).values,
                "r30": c.pct_change(30).values,
                "clv": ((c-lo)/(hi-lo)).values,
                "rng": (rr/rr.rolling(30).mean()).values,
                "vol": (b["volume"]/b["volume"].rolling(30).mean()).values,
                "dhi20": (c/hi.rolling(20).max()-1).values,
                "dlo20": (c/lo.rolling(20).min()-1).values,
                "sd30": c.pct_change().rolling(30).std().values,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values,
            })
            f["pos"] = np.arange(len(f))
            f["fwd"] = c.shift(-H)/c - 1
            f["fwd"] = f["fwd"].values
            f["exc"] = f["fwd"] - drift[coin]
            f["grid"] = (f["pos"] % H == 0)
            rows.append(f)
    df = pd.concat(rows, ignore_index=True)
    g = df[df.grid & df.fwd.notna()]
    p = g[g.inprof]
    out["counts"] = pd.Series({"grid_all": len(g), "grid_prof": len(p), "prof_share_bars": df.inprof.mean()})
    out["prof_mean_exc"] = pd.Series({"mean": p.exc.mean(), "t": stats.ttest_1samp(p.exc,0).statistic, "n": len(p),
                                      "outside_mean": g[~g.inprof].exc.mean()})
    def quint(col, d=p):
        d = d.dropna(subset=[col, "exc"])
        q = pd.qcut(d[col].rank(method="first"), 5, labels=False)
        a = d.groupby(q)["exc"].agg(["mean","count","std"])
        a["t"] = a["mean"]/(a["std"]/np.sqrt(a["count"]))
        a["colmean"] = d.groupby(q)[col].mean()
        return a.drop(columns="std")
    for col in ["r1","r3","r7","r14","r30","clv","rng","vol","dhi20","dlo20","sd30"]:
        out["q_"+col] = quint(col)
    a = p.groupby("wd")["exc"].agg(["mean","count"]); out["weekday"] = a
    out["by_window_prof"] = p.groupby("w")["exc"].agg(["mean","count"])
    out["by_coin_prof"] = p.groupby("coin")["exc"].agg(["mean","count"])
    out["fc_pos_vs_zero"] = p.groupby(p.fc>0)["exc"].agg(["mean","count"])
    # book days
    dd = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            x = d.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    dd = pd.concat(dd)
    br = dd.groupby(["w","day"])["book_return"].mean().dropna()
    out["book_daily"] = pd.Series({"mean": br.mean(), "sd": br.std(), "n": len(br),
                                   "top10_share_of_sum": br.sort_values().iloc[-10:].sum()/br.sum(),
                                   "bottom10_sum": br.sort_values().iloc[:10].sum()})
    tr = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t): tt=t.copy(); tt["coin"]=coin; tr.append(tt)
    if tr:
        tr = pd.concat(tr)
        out["trades"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["mean","count","median"])
        tr["ef"] = pd.qcut(tr["entry_forecast"].rank(method="first"),3,labels=False)
        out["trades_by_entry_fc"] = tr.groupby("ef")["net_profit_loss_percent"].agg(["mean","count"])
    return out
