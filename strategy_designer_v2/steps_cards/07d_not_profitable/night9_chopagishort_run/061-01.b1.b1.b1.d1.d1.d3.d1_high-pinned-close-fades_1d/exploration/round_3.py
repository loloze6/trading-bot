def explore(data):
    import numpy as np, pandas as pd
    out = {}
    feats = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            b["r5"] = c / c.shift(5) - 1
            b["r60"] = c / c.shift(60) - 1
            b["f5"] = c.shift(-5) / c - 1
            b["f10"] = c.shift(-10) / c - 1
            b["coin"] = coin; b["w"] = w
            b["ts"] = pd.to_datetime(b["timestamp"])
            feats.append(b[["coin","w","ts","r5","r60","f5","f10","regime","forecast"]])
    F = pd.concat(feats, ignore_index=True)
    key = F.set_index(["coin","w","ts"])
    T = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; t["w"] = w; T.append(t)
    T = pd.concat(T, ignore_index=True)
    T["days"] = T["duration_minutes"]/1440
    T["early"] = T["days"] < 4.5
    T["et"] = pd.to_datetime(T["entry_time"])
    def look(r, col):
        try: return key.loc[(r.coin, r.w, r.et), col]
        except Exception: return np.nan
    for col in ["r5","r60","f5","f10"]:
        T["e_"+col] = T.apply(lambda r: look(r, col), axis=1)
    T["fix5_short"] = -T["e_f5"]*100 - 0.22
    T["fix10_short"] = -T["e_f10"]*100 - 0.22
    out["trades actual vs fixed hold"] = T.groupby("early").agg(n=("side","size"),
        actual=("net_profit_loss_percent","mean"), fix5=("fix5_short","mean"), fix10=("fix10_short","mean"),
        found=("e_f5", lambda x: x.notna().sum()))
    out["trades by entry r5 depth"] = T.groupby(T.e_r5 < -0.05).agg(n=("side","size"),
        actual=("net_profit_loss_percent","mean"), fix5=("fix5_short","mean"),
        worst=("net_profit_loss_percent","min"), win=("net_profit_loss_percent", lambda x: (x>0).mean()))
    out["trades by r5 depth and window"] = T[T.e_r5 < -0.05].groupby("w").agg(n=("side","size"),
        actual=("net_profit_loss_percent","mean"))
    out["shallow trades by window"] = T[T.e_r5 >= -0.05].groupby("w").agg(n=("side","size"),
        actual=("net_profit_loss_percent","mean"))
    return out
