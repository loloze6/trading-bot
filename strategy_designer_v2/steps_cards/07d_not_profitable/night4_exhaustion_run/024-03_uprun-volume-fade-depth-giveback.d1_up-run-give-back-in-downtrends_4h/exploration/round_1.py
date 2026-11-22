def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 18
    # drift per coin
    rows = []; fc_rows = []
    for coin, ws in data["bars"].items():
        rets = []
        for w, b in ws.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            rets += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(rets); usual = np.std(rets)
        for w, b in ws.items():
            c = b["close"].values
            f = b["forecast"].values
            raw = b.get("debug_info.components.relief_rally.last_history_value")
            raw = raw.values if raw is not None else np.full(len(c), np.nan)
            al = b["postRebalance_current_allocation"].values
            fc_rows.append(pd.DataFrame({"coin": coin, "f": f, "al": al, "raw": raw}))
            ma = pd.Series(c).rolling(180, min_periods=1).mean().values
            depth = (ma - c) / ma
            for s in range(0, len(c) - H, H):
                seg = f[s:s + H]
                nz = np.where(seg < 0)[0]
                if len(nz) == 0: continue
                t = s + nz[0]
                if t + H >= len(c): continue
                r = c[t + H] / c[t] - 1
                rows.append({"coin": coin, "w": w, "f": f[t], "raw": raw[t], "depth": depth[t],
                             "tot": -r, "unu": -(r - drift), "usual": usual})
    cs = pd.DataFrame(rows)
    fc = pd.concat(fc_rows)
    out["forecast dist"] = fc["f"].describe(percentiles=[.01, .05, .1, .25, .5]).to_frame()
    out["share bars f<0"] = float((fc["f"] < 0).mean())
    out["share bars al<0"] = float((fc["al"] < -1e-9).mean())
    out["abs alloc when short"] = fc.loc[fc["al"] < -1e-9, "al"].describe().to_frame()
    out["case f value counts"] = cs["f"].round(2).value_counts().head(10).to_frame()
    cs["fq"] = pd.qcut(cs["f"].rank(method="first"), 4, labels=False)
    out["by forecast quartile (0=most neg)"] = cs.groupby("fq").agg(n=("tot", "size"), f=("f", "mean"), tot=("tot", "mean"), unu=("unu", "mean"), depth=("depth", "mean"))
    cs["dq"] = pd.qcut(cs["depth"].rank(method="first"), 4, labels=False)
    out["by depth quartile"] = cs.groupby("dq").agg(n=("tot", "size"), depth=("depth", "mean"), tot=("tot", "mean"), unu=("unu", "mean"))
    out["by coin cases"] = cs.groupby("coin").agg(n=("tot", "size"), tot=("tot", "mean"), unu=("unu", "mean"))
    # book
    d = []
    for coin, ws in data["days"].items():
        for w, x in ws.items():
            d.append(x.assign(coin=coin, w=w))
    d = pd.concat(d)
    out["book by window"] = d.groupby("w").agg(book=("book_return", "mean"), coin=("coin_return", "mean")).T
    tr = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            tr.append(t.assign(coin=coin))
    tr = pd.concat(tr)
    out["trades"] = tr.groupby("side").agg(n=("net_profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"),
                                           net=("net_profit_loss_percent", "mean"), dur_h=("duration_minutes", lambda x: x.mean() / 60),
                                           win=("profit_loss_percent", lambda x: (x > 0).mean()))
    tr["durq"] = pd.qcut(tr["duration_minutes"].rank(method="first"), 4, labels=False)
    out["trades by duration q"] = tr.groupby("durq").agg(dur_h=("duration_minutes", lambda x: x.mean() / 60), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    return out
