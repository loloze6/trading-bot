def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    out = {}
    feats = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            rng = (b["high"]-b["low"])
            cl = (b["close"]-b["low"])/rng.replace(0,np.nan)
            r1 = b["close"].pct_change()
            vol20 = r1.rolling(20, min_periods=10).std()
            f = pd.DataFrame({"coin":c,"w":w,"ts":b["timestamp"],"cl":cl,"r1v":r1/vol20,
                              "r5p": b["close"]/b["close"].shift(5)-1,
                              "r10p": b["close"]/b["close"].shift(10)-1,
                              "fwd2": b["close"].shift(-2)/b["close"]-1,
                              "fwd5": b["close"].shift(-5)/b["close"]-1,
                              "fwd10": b["close"].shift(-10)/b["close"]-1,
                              "regime": b["regime"], "alloc": b["postRebalance_current_allocation"],
                              "pos": np.arange(len(b)), "nb": len(b)})
            feats.append(f)
    F = pd.concat(feats, ignore_index=True)
    for h in [2,5,10]:
        dr = F[F["pos"]%h==0].groupby("coin")[f"fwd{h}"].mean()
        F[f"un{h}"] = -(F[f"fwd{h}"] - F["coin"].map(dr))
    inprof = F[F["regime"].isin(["mean_reversion","unknown"])].copy()
    inprof["sig"] = inprof["regime"]=="mean_reversion"
    inprof["r5neg"] = inprof["r5p"]<0
    inprof["r1low"] = inprof["r1v"]<inprof.loc[inprof["sig"],"r1v"].quantile(0.75)
    def summ(g, h=5):
        x = g[f"un{h}"].dropna()
        return pd.Series({"n":len(x),"mean_un":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out["condition check r5<0 (signal x cond), 5d"] = inprof.groupby(["sig","r5neg"]).apply(summ)
    out["condition check r1v below sig q75, 5d"] = inprof.groupby(["sig","r1low"]).apply(summ)
    sig = inprof[inprof["sig"]]
    out["signal horizon 2/5/10"] = pd.DataFrame({h: summ(sig,h) for h in [2,5,10]})
    out["signal r5neg horizons"] = pd.DataFrame({h: summ(sig[sig["r5neg"]],h) for h in [2,5,10]})
    sig = sig.copy()
    sig["cl_b"] = pd.cut(sig["cl"],[0.79,0.9,0.97,1.01])
    out["signal by cl bin"] = sig.groupby("cl_b").apply(summ)
    # trades
    T = pd.concat([t.assign(coin=c, w=w) for c in trades for w, t in trades[c].items() if len(t)], ignore_index=True)
    T["dur_d"] = (T["duration_minutes"]/1440).round()
    # window end?
    last = {(c,w): b["timestamp"].iloc[-1] for c in bars for w,b in bars[c].items()}
    T["at_end"] = [pd.Timestamp(e)==pd.Timestamp(last[(c,w)]) for e,c,w in zip(T["exit_time"],T["coin"],T["w"])]
    T["short_d"] = T["dur_d"]<=4
    out["trades short dur vs end"] = T.groupby(["short_d","at_end"]).agg(n=("net_profit_loss_percent","size"),mean_net=("net_profit_loss_percent","mean"))
    out["short trades exit regime fcst"] = T[T["short_d"]].agg({"exit_forecast":"mean","entry_forecast":"mean"})
    # entry features of trades
    Fi = F.set_index(["coin","w","ts"])
    keys = list(zip(T["coin"],T["w"],pd.to_datetime(T["entry_time"])))
    Fi.index = pd.MultiIndex.from_arrays([Fi.index.get_level_values(0),Fi.index.get_level_values(1),pd.to_datetime(Fi.index.get_level_values(2))])
    ent = Fi.reindex(keys)
    T["r5p"] = ent["r5p"].values; T["r1v"] = ent["r1v"].values
    out["trades by entry r5p sign"] = T.groupby(T["r5p"]<0).agg(n=("net_profit_loss_percent","size"),mean_net=("net_profit_loss_percent","mean"),worst=("net_profit_loss_percent","min"))
    out["worst 10 trades"] = T.nsmallest(10,"net_profit_loss_percent")[["w","dur_d","net_profit_loss_percent","r5p","r1v","at_end"]].reset_index(drop=True)
    # book: adverse after 2 days among signals
    s2 = sig.dropna(subset=["fwd2","fwd5"]).copy()
    s2["adverse2"] = s2["fwd2"]>0
    s2["rest"] = -((1+s2["fwd5"])/(1+s2["fwd2"])-1)
    out["after 2d up vs down: remaining 3d short"] = s2.groupby("adverse2")["rest"].agg(["size","mean"])
    return out
