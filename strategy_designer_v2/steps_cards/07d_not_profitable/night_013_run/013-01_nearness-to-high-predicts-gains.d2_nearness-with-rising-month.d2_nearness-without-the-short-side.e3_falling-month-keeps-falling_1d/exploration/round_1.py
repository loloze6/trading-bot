def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily stats, decomposition into drift and timing
    rows = []
    coin_mean = {}
    for c, ws in data["days"].items():
        allr = pd.concat([d["coin_return"] for d in ws.values()]).dropna()
        coin_mean[c] = allr.mean()
    day_frames = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            b = data["bars"][c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos = b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            dd = d.copy()
            dd["day"] = pd.to_datetime(dd["day"])
            dd = dd.set_index("day")
            dd["pos"] = pos.reindex(dd.index).values
            dd["coin"] = c; dd["win"] = w
            dd["year"] = dd.index.year
            day_frames.append(dd.reset_index())
    D = pd.concat(day_frames)
    D = D.dropna(subset=["book_return", "coin_return"])
    D["drift"] = D["pos"] * D["coin"].map(coin_mean)
    D["timing"] = D["pos"] * (D["coin_return"] - D["coin"].map(coin_mean))
    D["fee_gap"] = D["book_return"] - D["pos"] * D["coin_return"]
    out["book_decomp_by_coin"] = D.groupby("coin")[["book_return", "drift", "timing", "fee_gap", "pos"]].mean()
    out["book_decomp_all"] = D[["book_return", "drift", "timing", "fee_gap", "pos"]].mean().to_frame("mean")
    out["by_year"] = D.groupby("year")[["book_return", "coin_return", "drift", "timing", "fee_gap"]].mean()
    out["share_days_short"] = float((D["pos"] < 0).mean())
    # 3-bar grid analysis: excess return by 30d-return quintile, with trend regimes
    G = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r30 = cl / cl.shift(30) - 1
            r90 = cl / cl.shift(90) - 1
            vol = cl.pct_change().rolling(30).std()
            fwd = cl.shift(-3) / cl - 1
            idx = np.arange(0, len(b), 3)
            g = pd.DataFrame({"fc": b["forecast"].values[idx], "fwd": fwd.values[idx],
                              "r30": r30.values[idx], "r90": r90.values[idx], "vol": vol.values[idx],
                              "pos": b["postRebalance_current_allocation"].values[idx]})
            g["coin"] = c
            G.append(g)
    G = pd.concat(G).dropna(subset=["fwd"])
    G["exc"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    act = G[G["fc"] < 0].copy()
    act["q"] = pd.qcut(act["fc"], 5, labels=False)
    out["exc_by_fc_quintile(0=deepest)"] = act.groupby("q").agg(n=("exc", "size"), exc=("exc", "mean"), fwd=("fwd", "mean"), fc=("fc", "mean"))
    G2 = G.dropna(subset=["r30"]).copy()
    G2["q30"] = pd.qcut(G2["r30"], 5, labels=False)
    out["exc_by_r30_quintile_all"] = G2.groupby("q30").agg(n=("exc", "size"), exc=("exc", "mean"), r30=("r30", "mean"))
    a2 = act.dropna(subset=["r90"]).copy()
    a2["long_up"] = a2["r90"] > 0
    a2["gain"] = a2["pos"] * a2["exc"]
    out["active_by_90d_sign"] = a2.groupby("long_up").agg(n=("exc", "size"), exc=("exc", "mean"), gain=("gain", "mean"),
                                                          t=("exc", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    a3 = act.dropna(subset=["vol"]).copy()
    a3["vq"] = pd.qcut(a3["vol"], 3, labels=False)
    out["active_by_vol_tercile"] = a3.groupby("vq").agg(n=("exc", "size"), exc=("exc", "mean"),
                                                         t=("exc", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    tr = pd.concat([t for ws in data["trades"].values() for t in ws.values()])
    out["trades"] = pd.Series({"n": len(tr), "mean_pl": tr["profit_loss_percent"].mean(),
                               "mean_net": tr["net_profit_loss_percent"].mean(),
                               "win_share": (tr["profit_loss_percent"] > 0).mean()})
    return out
