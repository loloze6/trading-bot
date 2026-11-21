def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 26
    def cloud(b):
        hi = b["high"]; lo = b["low"]
        ten = (hi.rolling(9).max() + lo.rolling(9).min()) / 2
        kij = (hi.rolling(26).max() + lo.rolling(26).min()) / 2
        sa = ((ten + kij) / 2).shift(26)
        sb = ((hi.rolling(52).max() + lo.rolling(52).min()) / 2).shift(26)
        top = np.maximum(sa, sb); bot = np.minimum(sa, sb)
        mid = (sa + sb) / 2
        return top, bot, mid
    # daily book by coin, with regime age of the held position
    rows = []
    cases = []
    for c, ws in data["bars"].items():
        allr = []
        for w, b in ws.items():
            cl = b["close"].values
            for i in range(0, len(cl) - H, H):
                allr.append(cl[i + H] / cl[i] - 1)
        mu = np.mean(allr) if allr else np.nan
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            top, bot, mid = cloud(b)
            cl = b["close"].values
            n = len(cl)
            bir = pd.to_numeric(b["debug_info.bars_in_regime"], errors="coerce").values
            reg = b["regime"].values
            alloc = b["postRebalance_current_allocation"].values
            pv = b["postRebalance_total_value"].values
            # streak of trending regime (own count)
            streak = np.zeros(n)
            for i in range(n):
                streak[i] = (streak[i - 1] + 1) if (reg[i] == "trending" and i > 0) else (1 if reg[i] == "trending" else 0)
            ret1 = np.r_[cl[1:] / cl[:-1] - 1, np.nan]
            gain = alloc * ret1
            dist = cl / top.values - 1
            thick = (top.values - bot.values) / cl
            slope = mid.values / np.r_[np.full(26, np.nan), mid.values[:-26]] - 1
            r26p = cl / np.r_[np.full(26, np.nan), cl[:-26]] - 1
            for i in range(n - 1):
                if abs(alloc[i]) > 0.01:
                    rows.append(dict(coin=c, w=int(w[1:]), streak=streak[i], dist=dist[i], gain=gain[i],
                                     r=ret1[i], alloc=alloc[i]))
            for i in range(0, n - H, H):
                if b["forecast"].values[i] > 0:
                    r = cl[i + H] / cl[i] - 1
                    cases.append(dict(coin=c, w=int(w[1:]), ex=r - mu, r=r, streak=streak[i], dist=dist[i],
                                      thick=thick[i], slope=slope[i], r26=r26p[i],
                                      fc=b["forecast"].values[i]))
    G = pd.DataFrame(rows)
    C = pd.DataFrame(cases)
    def summ(g, col="ex"):
        s = g[col].dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / s.std() * np.sqrt(len(s)) if len(s) > 2 else np.nan,
                          "share_up": (g["r"] > 0).mean()})
    for col in ["streak", "dist", "thick", "slope", "r26"]:
        X = C.dropna(subset=[col]).copy()
        X["q"] = pd.qcut(X[col].rank(method="first"), 4, labels=False)
        t = X.groupby("q").apply(summ); t["feat"] = X.groupby("q")[col].mean()
        t["spearman_all"] = stats.spearmanr(X[col], X.ex).correlation
        out["case_by_" + col] = t.round(4)
    # held-day gains by regime age and distance
    G["sq"] = pd.cut(G.streak, [-1, 0, 13, 26, 52, 104, 10000])
    out["held_by_streak"] = G.groupby("sq").agg(n=("gain", "size"), mean_gain=("gain", "mean"),
                                                mean_r=("r", "mean"), alloc=("alloc", "mean")).round(5)
    G2 = G.dropna(subset=["dist"]).copy()
    G2["dq"] = pd.qcut(G2.dist.rank(method="first"), 5, labels=False)
    t = G2.groupby("dq").agg(n=("gain", "size"), mean_gain=("gain", "mean"), mean_r=("r", "mean"))
    t["dist"] = G2.groupby("dq").dist.mean()
    out["held_by_dist"] = t.round(5)
    # windows 12-18: where losses are
    out["held_by_wgroup"] = G.assign(g=pd.cut(G.w, [0, 6, 12, 18, 24])).groupby("g").agg(
        n=("gain", "size"), mean_gain=("gain", "mean"), mean_streak=("streak", "mean")).round(5)
    out["held_loss_by_coin_w13_18"] = G[(G.w >= 13) & (G.w <= 18)].groupby("coin").gain.agg(["size", "sum"]).sort_values("sum").head(10).round(3)
    return out
