def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily returns, chained in window order
    wins = sorted({w for c in data["days"] for w in data["days"][c]}, key=lambda s: int(s[1:]))
    rows = []
    for w in wins:
        frames = []
        for c in data["days"]:
            if w in data["days"][c]:
                d = data["days"][c][w][["day","book_return","coin_return"]].copy()
                d["coin"] = c; frames.append(d)
        f = pd.concat(frames)
        g = f.groupby("day")[["book_return","coin_return"]].mean().sort_index()
        g["window"] = w
        rows.append(g.dropna())
    P = pd.concat(rows)
    P["idx"] = np.arange(len(P))
    eq = (1+P["book_return"]).cumprod(); dd = eq/eq.cummax()-1
    heq = (1+P["coin_return"]).cumprod(); hdd = heq/heq.cummax()-1
    P["dd"] = dd.values
    yr = eq.iloc[-1]**(365/len(P))-1
    out["summary"] = pd.Series({"yearly": yr, "maxdd": dd.min(), "calmar": yr/abs(dd.min()),
        "hold_yearly": heq.iloc[-1]**(365/len(P))-1, "hold_maxdd": hdd.min(), "days": len(P)})
    # drawdown episodes
    trough = dd.values.argmin()
    peak = eq.values[:trough+1].argmax()
    out["deepest_fall"] = pd.Series({"peak_pos": peak, "trough_pos": trough, "len_days": trough-peak,
        "windows": ",".join(sorted(set(P["window"].iloc[peak:trough+1]), key=lambda s:int(s[1:]))),
        "book_fall": dd.min(), "hold_fall_same_days": (1+P["coin_return"].iloc[peak+1:trough+1]).prod()-1})
    out["dd_by_window"] = P.groupby("window").agg(book_mean=("book_return","mean"), coin_mean=("coin_return","mean"),
        min_dd=("dd","min"), n=("book_return","size")).reindex(wins)
    # bar-level analysis
    B = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            cl = b["close"]; r1 = cl.pct_change()
            df = pd.DataFrame({"coin": c, "window": w, "r1": r1,
                "z": r1/ r1.abs().rolling(60, min_periods=20).mean().shift(1),
                "tr20": cl/cl.shift(20)-1, "tr60": cl/cl.shift(60)-1,
                "vol20": r1.rolling(20).std(),
                "alloc": b["postRebalance_current_allocation"], "fc": b["forecast"],
                "next1": cl.shift(-1)/cl-1, "f5": cl.shift(-5)/cl-1})
            df["gain"] = df["alloc"]*df["next1"]
            df["pos"] = np.arange(len(df))
            B.append(df)
    B = pd.concat(B, ignore_index=True)
    drift = B[B.pos%5==0].groupby("coin")["f5"].mean()
    B["ex5"] = B["f5"] - B["coin"].map(drift)
    G = B[(B.pos%5==0)].dropna(subset=["ex5","z","tr20"])
    G["side"] = np.where(G.r1>0,"up","down")
    G["mag"] = pd.qcut(G.z.abs(), 3, labels=["small","mid","large"])
    G["trend"] = np.where(G.tr20>0,"tr20+","tr20-")
    def agg(x):
        return pd.Series({"n": len(x), "ex5": x.ex5.mean(), "t": x.ex5.mean()/(x.ex5.std()/np.sqrt(len(x))), "f5": x.f5.mean()})
    out["ex5_by_side_mag"] = G.groupby(["side","mag"]).apply(agg)
    out["ex5_by_trend_side_mag"] = G.groupby(["trend","side","mag"]).apply(agg)
    # where the book's gain is lost: bar gains by trend and state
    B["trend"] = np.where(B.tr20>0,"tr20+","tr20-")
    B["volq"] = pd.qcut(B.vol20, 3, labels=["lowvol","midvol","highvol"])
    H = B.dropna(subset=["gain","tr20","vol20"])
    out["gain_by_trend_vol"] = H.groupby(["trend","volq"]).agg(n=("gain","size"), mean_alloc=("alloc","mean"),
        mean_gain=("gain","mean"), sum_gain=("gain","sum"), coin_next1=("next1","mean"))
    return out
