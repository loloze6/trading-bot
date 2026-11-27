def explore(data):
    import numpy as np, pandas as pd
    out = {}
    T = []
    feats = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            b = data["bars"][c][w].reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"]; hi = b["high"]; lo = b["low"]
            loc = (cl - lo) / (hi - lo).replace(0, np.nan)
            r1 = cl.pct_change(); r5 = cl.pct_change(5); r60 = cl.pct_change(60)
            rng = (hi - lo) / cl
            vol30 = r1.rolling(30).std()
            for _, tr in t.iterrows():
                et = pd.to_datetime(tr["entry_time"]); xt = pd.to_datetime(tr["exit_time"])
                ie = ts.searchsorted(et, side="right") - 1
                ix = ts.searchsorted(xt, side="right") - 1
                ie = max(ie, 0); ix = min(max(ix, 0), len(b) - 1)
                seg = cl.iloc[ie:ix + 1]
                mae = (seg.max() / cl.iloc[ie] - 1) if len(seg) else np.nan
                feats.append(dict(coin=c, w=w, days=tr["duration_minutes"] / 1440,
                                  net=tr["net_profit_loss_percent"], ef=tr["entry_forecast"],
                                  r1e=r1.iloc[ie], r5e=r5.iloc[ie], loce=loc.iloc[ie], rnge=rng.iloc[ie] / vol30.iloc[ie] if vol30.iloc[ie] > 0 else np.nan,
                                  r60e=r60.iloc[ie], r60x=r60.iloc[ix], regx=b["regime"].iloc[ix],
                                  lastbar=(ix == len(b) - 1), maxup=mae,
                                  r1_after=(cl.iloc[min(ie + 1, len(b) - 1)] / cl.iloc[ie] - 1)))
    F = pd.DataFrame(feats)
    F["db"] = pd.cut(F["days"], [0, 3, 5.5, 400])
    out["exit_regime_by_dur"] = F.groupby(["db", "regx"]).agg(n=("net", "size"), mean=("net", "mean"), r60x=("r60x", "mean")).dropna()
    F["r60xb"] = pd.cut(F["r60x"], [-5, -0.1, 0.1, 5], labels=["falling", "choppy", "rising"])
    out["by_exit_trend"] = F.groupby("r60xb").agg(n=("net", "size"), mean=("net", "mean"), sum=("net", "sum"), days=("days", "mean"))
    for col in ["r1e", "r5e", "loce", "rnge", "r60e", "ef", "r1_after"]:
        F[col + "_q"] = pd.qcut(F[col], 3, labels=["lo", "mid", "hi"], duplicates="drop")
        out["by_" + col] = F.groupby(col + "_q").agg(n=("net", "size"), mean=("net", "mean"), sum=("net", "sum"), med=("net", "median"), x=(col, "mean"))
    F["maxupb"] = pd.cut(F["maxup"], [-1, 0, 0.05, 0.1, 0.2, 5])
    out["by_maxup"] = F.groupby("maxupb").agg(n=("net", "size"), mean=("net", "mean"), sum=("net", "sum"))
    out["by_coin"] = F.groupby("coin").agg(n=("net", "size"), mean=("net", "mean"), sum=("net", "sum"))
    out["worst10"] = F.nsmallest(10, "net")[["coin", "w", "days", "net", "r1e", "r5e", "loce", "r60e", "r60x", "regx", "r1_after"]].reset_index(drop=True)
    # grid check: in-profile deep 5d fall without high close vs with
    g = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; hi = b["high"].values; lo = b["low"].values
            loc = (cl - lo) / np.where(hi - lo > 0, hi - lo, np.nan)
            r5 = pd.Series(cl).pct_change(5).values
            r1 = pd.Series(cl).pct_change().values
            sd = pd.Series(cl).pct_change().rolling(30).std().values
            inp = (b["regime"] != "chop").values
            for i in range(0, len(b) - 5, 5):
                g.append(dict(coin=c, inp=inp[i], loc=loc[i], r5z=r5[i] / (sd[i] * np.sqrt(5)) if sd[i] > 0 else np.nan, r1=r1[i], fwd=cl[i + 5] / cl[i] - 1))
    G = pd.DataFrame(g).dropna()
    G["unus"] = -(G["fwd"] - G.groupby("coin")["fwd"].transform("mean"))
    G = G[G.inp]
    G["depth"] = pd.cut(G["r5z"], [-99, -1, 0, 1, 99], labels=["deep<-1sd", "neg", "pos", ">1sd"])
    G["hc"] = G["loc"] > 0.5
    out["inprof_depth_x_hiclose"] = G.groupby(["depth", "hc"])["unus"].agg(["count", "mean", "std"])
    return out
