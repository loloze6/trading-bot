def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    def tstat(x):
        x = np.asarray(x, float); x = x[~np.isnan(x)]
        if len(x) < 3: return np.nan
        return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sc7 = (c / c.shift(7) - 1) / (c / c.shift(7) - 1).abs().rolling(30).mean()
            vol30 = r1.rolling(30).std()
            ret60 = c / c.shift(60) - 1
            for h in (1, 3, 7, 21):
                fr = c.shift(-h) / c - 1
                grid = (np.arange(len(b)) % h) == 0
                d = pd.DataFrame({"coin": coin, "w": w, "h": h, "pos": np.arange(len(b)),
                                  "fr": fr, "grid": grid, "sc7": sc7, "r1": r1,
                                  "r1z": r1 / vol30.shift(1), "vol30": vol30, "ret60": ret60,
                                  "regime": b["regime"].values, "fc": b["forecast"].values,
                                  "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                                  "alloc": b["postRebalance_current_allocation"].values})
                rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    G = D[D.grid & D.fr.notna()].copy()
    drift = G.groupby(["coin", "h"]).fr.mean().rename("drift")
    G = G.join(drift, on=["coin", "h"]); G["ex"] = G.fr - G.drift
    G["inprof"] = G.regime == "unknown"
    # 1. scaled 7d return bins, by profile, horizons 7 and 21
    res = []
    for h in (7, 21):
        g = G[(G.h == h) & G.sc7.notna()].copy()
        g["bin"] = pd.cut(g.sc7, [-99, -1.5, -0.5, 0.5, 1.5, 99])
        for (ip, bn), s in g.groupby(["inprof", "bin"], observed=True):
            res.append({"h": h, "inprof": ip, "bin": str(bn), "n": len(s), "mean_ex": s.ex.mean(), "t": tstat(s.ex)})
    out["sc7_bins_by_profile"] = pd.DataFrame(res)
    # 2. after large daily moves (r1z), next 1 and 3 days, by profile
    res = []
    for h in (1, 3):
        g = G[(G.h == h) & G.r1z.notna()].copy()
        g["bin"] = pd.cut(g.r1z, [-99, -2, -1, 1, 2, 99])
        for (ip, bn), s in g.groupby(["inprof", "bin"], observed=True):
            res.append({"h": h, "inprof": ip, "bin": str(bn), "n": len(s), "mean_ex": s.ex.mean(), "t": tstat(s.ex)})
    out["bigmove_bins"] = pd.DataFrame(res)
    # 3. weekday
    g = G[G.h == 1]
    out["weekday"] = g.groupby("wd").ex.agg(["count", "mean", tstat])
    # 4. 60d trend bins and vol tercile, 21d
    g = G[(G.h == 21) & G.ret60.notna()].copy()
    g["tr"] = pd.cut(g.ret60, [-9, -0.3, -0.1, 0.1, 0.3, 9])
    out["trend60_21d"] = g.groupby("tr", observed=True).ex.agg(["count", "mean", tstat])
    # 5. in-profile forecast quintile, 21d
    g = G[(G.h == 21) & G.inprof & (G.fc > 0)].copy()
    g["q"] = pd.qcut(g.fc, 4, labels=False, duplicates="drop")
    out["fc_quart_21d"] = g.groupby("q").agg(n=("ex", "size"), mean_ex=("ex", "mean"), t=("ex", tstat), fc=("fc", "mean"))
    # 6. book days: by window, and largest days
    dd = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            dd.append(d.assign(coin=coin, w=w))
    DD = pd.concat(dd)
    out["book_by_window"] = DD.groupby("w").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    # 7. trades
    tr = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            tr.append(t.assign(coin=coin))
    T = pd.concat(tr)
    T["ef"] = pd.qcut(T.entry_forecast, 3, labels=False, duplicates="drop")
    out["trades_by_entryfc"] = T.groupby("ef").agg(n=("net_profit_loss_percent", "size"),
        mean=("net_profit_loss_percent", "mean"), med=("net_profit_loss_percent", "median"),
        dur=("duration_minutes", "mean"))
    out["share_inprof"] = float(D[D.h == 1].regime.eq("unknown").mean())
    return out
