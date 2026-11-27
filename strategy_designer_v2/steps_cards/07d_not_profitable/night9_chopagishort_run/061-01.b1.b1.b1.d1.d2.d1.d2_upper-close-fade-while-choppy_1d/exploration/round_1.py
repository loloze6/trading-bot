def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # ---- book daily returns
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna().reset_index()
    B["wn"] = B["w"].str[1:].astype(int)
    B = B.sort_values(["wn", "day"])
    def dd_stats(s):
        v = (1 + s).cumprod(); peak = v.cummax(); dd = v / peak - 1
        return dd.min()
    per_w = B.groupby("w").agg(book_sum=("book_return", "sum"), coin_sum=("coin_return", "sum"),
                               book_sd=("book_return", "std"), n=("book_return", "size"))
    per_w["book_mdd"] = B.groupby("w")["book_return"].apply(dd_stats)
    out["per_window"] = per_w
    v = (1 + B["book_return"]).cumprod().values
    peak = np.maximum.accumulate(v); ddv = v / peak - 1
    out["overall"] = pd.Series({"mean": B.book_return.mean(), "sd": B.book_return.std(),
                                "sharpe": B.book_return.mean() / B.book_return.std() * np.sqrt(365),
                                "hold_sharpe": B.coin_return.mean() / B.coin_return.std() * np.sqrt(365),
                                "mdd_chain": ddv.min(), "days": len(B)})
    # ---- bars-level: grid analysis
    g = []
    alloc = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; hi = b["high"].values; lo = b["low"].values
            n = len(b)
            loc = (cl - lo) / np.where(hi - lo > 0, hi - lo, np.nan)
            r5 = pd.Series(cl).pct_change(5).values
            r60 = pd.Series(cl).pct_change(60).values
            vol30 = pd.Series(cl).pct_change().rolling(30).std().values
            inprof = (b["regime"] != "chop").values
            a = b["postRebalance_current_allocation"].values
            alloc.append(pd.DataFrame({"a": a[a != 0]}))
            for h in (2, 5, 10):
                for i in range(0, n - h, 5 if h <= 5 else h):
                    g.append(dict(coin=c, w=w, h=h, inprof=inprof[i], loc=loc[i], r5=r5[i],
                                  r60=r60[i], vol=vol30[i], fwd=cl[i + h] / cl[i] - 1,
                                  pos=a[i]))
    G = pd.DataFrame(g)
    drift = G.groupby(["coin", "h"])["fwd"].mean().rename("drift")
    G = G.join(drift, on=["coin", "h"])
    G["unus_short"] = -(G["fwd"] - G["drift"])
    G["tot_short"] = -G["fwd"]
    G["sig"] = (G["loc"] > 0.5) & (G["r5"] < 0)
    G["grp"] = np.where(G["loc"] > 0.5, "hiC", "loC") + np.where(G["r5"] < 0, "_neg5", "_pos5")
    def summ(x):
        return pd.Series({"n": len(x), "unus": x.unus_short.mean(), "tot": x.tot_short.mean(),
                          "t": x.unus_short.mean() / (x.unus_short.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["grid_groups"] = G.dropna(subset=["loc", "r5"]).groupby(["h", "inprof", "grp"]).apply(summ)
    S = G[(G.h == 5) & G.inprof & G.sig].copy()
    S["r5q"] = pd.qcut(S["r5"], 3, labels=["deep", "mid", "shallow"])
    out["sig_by_depth"] = S.groupby("r5q").apply(summ)
    S["r60b"] = pd.cut(S["r60"], [-1, -0.03, 0.03, 1])
    out["sig_by_r60"] = S.groupby("r60b").apply(summ)
    S["locb"] = pd.cut(S["loc"], [0.5, 0.75, 1.0])
    out["sig_by_loc"] = S.groupby("locb").apply(summ)
    S["held"] = S["pos"] < 0
    out["sig_held_or_not"] = S.groupby("held").apply(summ)
    A = pd.concat(alloc)
    out["alloc_abs"] = A["a"].abs().describe()
    # ---- trades
    T = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            t = t.copy(); t["coin"] = c; t["w"] = w; T.append(t)
    T = pd.concat(T)
    T["days"] = T["duration_minutes"] / 1440
    out["trades"] = pd.Series({"n": len(T), "mean_net": T.net_profit_loss_percent.mean(),
                               "mean_gross": T.profit_loss_percent.mean(), "win": (T.net_profit_loss_percent > 0).mean(),
                               "mean_days": T.days.mean(), "median_days": T.days.median()})
    T["db"] = pd.cut(T["days"], [0, 3, 5.5, 8, 15, 400])
    out["trades_by_days"] = T.groupby("db")["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    out["trades_worst"] = T.nsmallest(8, "net_profit_loss_percent")[["coin", "w", "days", "entry_forecast", "net_profit_loss_percent"]].reset_index(drop=True)
    return out
