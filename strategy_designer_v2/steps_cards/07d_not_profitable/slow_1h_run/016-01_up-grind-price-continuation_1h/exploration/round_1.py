def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily returns, coin daily returns, market part vs timing
    rows = []
    coinmean = {}
    for c in data["days"]:
        cr = pd.concat([d["coin_return"] for d in data["days"][c].values()]).dropna()
        coinmean[c] = cr.mean()
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            pos = b["postRebalance_current_allocation"]
            b["gain"] = pos * b["r1"]
            dd = data["days"][c][w]
            g = b.groupby("day").agg(pos=("postRebalance_current_allocation", "mean"))
            rows.append(pd.DataFrame({"coin": c, "w": w, "book": dd["book_return"].values,
                                      "coinr": dd["coin_return"].values,
                                      "pos": g["pos"].reindex(pd.to_datetime(dd["day"]).dt.floor("D")).values}))
    D = pd.concat(rows).dropna()
    D["mkt"] = D["pos"] * D["coin"].map(coinmean)
    out["book summary"] = pd.Series({"mean book": D.book.mean(), "mean mkt part": D.mkt.mean(),
                                     "timing": D.book.mean() - D.mkt.mean(), "mean pos": D.pos.mean(),
                                     "share days in": (D.pos > 0.01).mean(), "n": len(D)})
    out["by coin"] = D.groupby("coin").agg(book=("book", "mean"), coinr=("coinr", "mean"), pos=("pos", "mean"))
    # fees
    fees = []
    for c in data["trades"]:
        for w, t in data["trades"][c].items():
            if len(t): fees.append(t[["profit_loss_percent", "net_profit_loss_percent", "total_commission", "duration_minutes"]])
    T = pd.concat(fees)
    out["trades"] = T.describe().T[["count", "mean", "50%"]]
    # grid analysis: raw share, forecast vs forward 72h return, plus past return and vol
    G = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            cl = b["close"].values
            r = np.r_[np.nan, cl[1:] / cl[:-1] - 1]
            idx = np.arange(0, len(b), 72)
            for i in idx:
                if i < 72 or i + 72 >= len(b): continue
                past = cl[i] / cl[i - 72] - 1
                hr = r[i - 71:i + 1]
                vol = np.nanstd(hr)
                G.append((c, w, b["forecast"].iloc[i], b["debug_info.components.grind_share.last_history_value"].iloc[i],
                          past, vol, cl[i + 72] / cl[i] - 1, b["postRebalance_current_allocation"].iloc[i]))
    G = pd.DataFrame(G, columns=["coin", "w", "fc", "raw", "past", "vol", "fwd", "pos"])
    G["up"] = G.past > 0
    out["fwd by up"] = G.groupby("up").fwd.agg(["mean", "count"])
    U = G[G.past > 0].copy()
    U["rawq"] = pd.qcut(U.raw.rank(method="first"), 3, labels=False)
    U["fcq"] = pd.qcut(U.fc.rank(method="first"), 3, labels=False)
    U["pastq"] = pd.qcut(U.past.rank(method="first"), 3, labels=False)
    U["volq"] = pd.qcut(U.vol.rank(method="first"), 3, labels=False)
    out["up: fwd by raw share third"] = U.groupby("rawq").agg(fwd=("fwd", "mean"), n=("fwd", "size"), raw=("raw", "mean"), fc=("fc", "mean"))
    out["up: fwd by forecast third"] = U.groupby("fcq").agg(fwd=("fwd", "mean"), n=("fwd", "size"), raw=("raw", "mean"))
    out["up: fwd by past third x raw third"] = U.pivot_table(index="pastq", columns="rawq", values="fwd", aggfunc="mean")
    out["up: fwd by vol third x raw third"] = U.pivot_table(index="volq", columns="rawq", values="fwd", aggfunc="mean")
    out["corr fc raw"] = U[["fc", "raw"]].corr().iloc[0, 1]
    out["holding mean 72h"] = G.fwd.mean()
    return out
