def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    allbars = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["coin"] = coin; b["win"] = w
            b["r1"] = b["close"].shift(-1)/b["close"] - 1
            for h in [1,2,3,5,10]:
                b[f"f{h}"] = b["close"].shift(-h)/b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"]*b["r1"]
            b["fee"] = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["ret20"] = b["close"]/b["close"].shift(20)-1
            allbars.append(b)
    B = pd.concat(allbars, ignore_index=True)
    # coin mean daily
    cm = B.groupby("coin")["r1"].mean()
    B["mkt"] = B["pos"]*B["coin"].map(cm)
    g = B.groupby("coin").agg(exposure=("pos", lambda x: (x.abs()>0).mean()), meanpos=("pos","mean"),
                              gain=("gain","mean"), mkt=("mkt","mean"), fee=("fee","mean"), coinmean=("r1","mean"))
    g["timing"] = g["gain"]-g["mkt"]
    out["per_coin"] = g
    # days-level
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"]=coin; d["win"]=w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    dd = D.groupby("coin").agg(book=("book_return","mean"), bsd=("book_return","std"), hold=("coin_return","mean"), hsd=("coin_return","std"))
    dd["bookSh"] = dd.book/dd.bsd*np.sqrt(365); dd["holdSh"]=dd.hold/dd.hsd*np.sqrt(365)
    out["days_coin"] = dd
    # forward returns by forecast bucket (all bars, overlapping ok for profile; also excess)
    B["fb"] = pd.cut(B["forecast"], [-0.01,0.0001,0.5,2,5,10,20.1], labels=["0","0-.5",".5-2","2-5","5-10","10-20"])
    prof = {}
    for h in [1,2,3,5,10]:
        cmh = B.groupby("coin")[f"f{h}"].mean()
        B[f"x{h}"] = B[f"f{h}"]-B["coin"].map(cmh)
        prof[f"x{h}"] = B.groupby("fb")[f"x{h}"].mean()
    p = pd.DataFrame(prof); p["n"] = B.groupby("fb").size(); p["meanpos"]=B.groupby("fb")["pos"].mean()
    p["gain_sum_share"] = B.groupby("fb")["gain"].sum()/B["gain"].sum()
    out["by_fc"] = p
    # gain by window
    wg = B.groupby("win").agg(gain=("gain","mean"), mkt=("mkt","mean"), r=("r1","mean"), exp=("pos",lambda x:(x>0).mean()))
    out["by_win"] = wg
    # trades
    T = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            t = t.copy(); t["coin"]=coin; T.append(t)
    T = pd.concat(T, ignore_index=True)
    out["trades"] = pd.Series({"n":len(T), "dur_days_mean":T.duration_minutes.mean()/1440, "dur_med":T.duration_minutes.median()/1440,
        "pl_mean":T.profit_loss_percent.mean(), "net_mean":T.net_profit_loss_percent.mean(), "win":(T.profit_loss_percent>0).mean()})
    # regime: prior 20d return
    B["rb"] = pd.qcut(B["ret20"], 4, labels=["q1","q2","q3","q4"])
    act = B[B.forecast>=2]
    out["active_by_ret20"] = act.groupby("rb").agg(n=("x5","size"), x5=("x5","mean"), x1=("x1","mean"), gain=("gain","mean"))
    return out
