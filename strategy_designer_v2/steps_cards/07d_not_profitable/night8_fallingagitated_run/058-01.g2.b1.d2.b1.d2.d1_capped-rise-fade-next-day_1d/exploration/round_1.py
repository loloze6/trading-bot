def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    drift = {}
    for c, ws in data["bars"].items():
        allr = []
        for w, b in ws.items():
            r = b["close"].pct_change()
            allr.append(r.dropna())
        drift[c] = pd.concat(allr).mean()
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r = cl.pct_change()
            sd = r.rolling(30).std()
            z = r / sd
            f = {h: cl.shift(-h) / cl - 1 for h in (1, 2, 3, 5)}
            reg = b["regime"].astype(str)
            inprof = reg.isin(["mean_reversion", "unknown"])
            alloc = b["postRebalance_current_allocation"]
            ret5 = cl / cl.shift(5) - 1
            sd5 = sd * np.sqrt(5)
            z5 = ret5 / sd5
            df = pd.DataFrame({"coin": c, "win": w, "z": z, "z5": z5, "inprof": inprof,
                               "active": reg == "mean_reversion", "alloc": alloc,
                               "pos": b.index % 1 == 0, "idx": b.index})
            for h in (1, 2, 3, 5):
                df[f"f{h}"] = f[h] - h * drift[c]
                df[f"g{h}"] = df["idx"] % h == 0
            df["tot1"] = f[1]
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    bins = [-np.inf, -1, 0, 0.5, 1, 1.5, 2, np.inf]
    d["zb"] = pd.cut(d["z"], bins)

    def tab(sub, col, grid):
        s = sub[sub[grid]]
        g = s.groupby("zb", observed=True)[col]
        m = -g.mean(); n = g.count(); sdv = g.std()
        return pd.DataFrame({"short_mean": m, "n": n, "t": m / (sdv / np.sqrt(n))})
    for h in (1, 2, 3, 5):
        out[f"in profile: short unusual move h={h}d by 1d z"] = tab(d[d.inprof], f"f{h}", f"g{h}")
    out["outside profile: short unusual h=1 by z"] = tab(d[~d.inprof], "f1", "g1")
    out["outside profile: short unusual h=3 by z"] = tab(d[~d.inprof], "f3", "g3")
    # 5-day rise (brief's multi-day) in profile
    d["z5b"] = pd.cut(d["z5"], [-np.inf, 0, 0.5, 1, 1.5, 2, np.inf])
    for h in (1, 3, 5):
        s = d[d.inprof & d[f"g{h}"]]
        g = s.groupby("z5b", observed=True)[f"f{h}"]
        m = -g.mean(); n = g.count()
        out[f"in profile: short unusual h={h}d by 5d z"] = pd.DataFrame({"short_mean": m, "n": n, "t": m / (g.std() / np.sqrt(n))})
    a = d[d.active]
    out["active: alloc stats"] = a["alloc"].abs().describe()
    out["share of profile bars"] = float(d.inprof.mean())
    out["share active bars"] = float(d.active.mean())
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)], ignore_index=True)
    out["trades"] = pd.DataFrame({"n": [len(tr)], "gross_mean": [tr.profit_loss_percent.mean()],
                                  "net_mean": [tr.net_profit_loss_percent.mean()],
                                  "dur_days_mean": [tr.duration_minutes.mean() / 1440]})
    # book by window
    dd = pd.concat([x.assign(coin=c, win=w) for c, ws in data["days"].items() for w, x in ws.items()])
    bw = dd.groupby("win").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"))
    out["book by window"] = bw
    return out
