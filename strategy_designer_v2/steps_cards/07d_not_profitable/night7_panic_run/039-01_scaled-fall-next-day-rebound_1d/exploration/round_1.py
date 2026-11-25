def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    # coin mean daily return over all windows
    cmean = {}
    for c, ws in data["bars"].items():
        rr = []
        for w, b in ws.items():
            r = b["close"].pct_change().shift(-1)
            rr.append(r.dropna())
        cmean[c] = pd.concat(rr).mean()
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r = cl.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd.shift(0)
            nxt = cl.shift(-1) / cl - 1
            tr = cl / cl.shift(30) - 1  # 30-bar trend (window short)
            r5 = cl / cl.shift(5) - 1
            alloc = b["postRebalance_current_allocation"]
            gain = alloc * nxt
            fc = b["forecast"]
            df = pd.DataFrame({"coin": c, "w": w, "pos": np.arange(len(b)), "z": z, "nxt": nxt,
                               "ex": nxt - cmean[c], "tr": tr, "r5": r5, "alloc": alloc,
                               "gain": gain, "fc": fc, "r": r,
                               "dayid": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d = d.dropna(subset=["nxt"])
    # exposure by forecast state
    d["state"] = np.where(d["r"] < 0, "down", "up/flat")
    out["exposure"] = d.groupby("state").agg(n=("nxt", "size"), inpos=("alloc", lambda x: (x > 0.01).mean()),
                                              alloc=("alloc", "mean"), gain=("gain", "mean"), ex=("ex", "mean"))
    # z buckets
    d["zb"] = pd.cut(d["z"], [-99, -2.5, -1.5, -1, -0.5, 0, 0.5, 1, 99])
    g = d.groupby("zb", observed=True)
    out["by_z"] = g.agg(n=("ex", "size"), ex=("ex", "mean"), nxt=("nxt", "mean"), sd=("nxt", "std"),
                        alloc=("alloc", "mean"), gain=("gain", "mean"))
    # book gain share by alloc>0 & state
    d["held"] = d["alloc"] > 0.01
    tot = d["gain"].sum()
    out["gain_share"] = d.groupby(["held", "zb"], observed=True)["gain"].sum() / tot
    # trend condition
    d["trb"] = pd.cut(d["tr"], [-9, -0.1, 0.1, 9], labels=["falling", "choppy", "rising"])
    d["big"] = d["z"] < -1.5
    t = d.dropna(subset=["trb"]).groupby(["trb", "big"], observed=True)
    out["trend_x_bigfall"] = t.agg(n=("ex", "size"), ex=("ex", "mean"), sd=("ex", "std"),
                                   gain=("gain", "mean"), alloc=("alloc", "mean"))
    # book daily returns pooled
    days = []
    for c, ws in data["days"].items():
        for w, dd in ws.items():
            x = dd[["day", "book_return", "coin_return"]].copy(); x["w"] = w; days.append(x)
    D = pd.concat(days)
    B = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    order = sorted(B["w"].unique(), key=lambda s: int(s[1:]))
    B["wi"] = B["w"].map({w: i for i, w in enumerate(order)})
    B = B.sort_values(["wi", "day"]).dropna()
    v = (1 + B["book_return"]).cumprod().values
    peak = np.maximum.accumulate(v); dd_ = v / peak - 1
    B["dd"] = dd_
    out["deepest_dd"] = float(dd_.min())
    out["dd_by_window"] = B.groupby("w").agg(book=("book_return", lambda x: (1 + x).prod() - 1),
                                            coin=("coin_return", lambda x: (1 + x).prod() - 1),
                                            mindd=("dd", "min"), sd=("book_return", "std"))
    # worst book days: coin return then
    B["bq"] = pd.qcut(B["book_return"], 10, labels=False)
    out["book_decile_vs_coin"] = B.groupby("bq")[["book_return", "coin_return"]].mean()
    # after big fall, also previous 5-day return
    bigd = d[d["z"] < -1.5].copy()
    bigd["r5b"] = pd.cut(bigd["r5"], [-9, -0.15, -0.05, 9])
    out["big_by_r5"] = bigd.groupby("r5b", observed=True).agg(n=("ex", "size"), ex=("ex", "mean"), sd=("ex", "std"))
    out["by_year_big"] = bigd.groupby("year").agg(n=("ex", "size"), ex=("ex", "mean"))
    out["by_year_all_held"] = d[d["held"]].groupby("year").agg(n=("ex", "size"), gain=("gain", "mean"), ex=("ex","mean"))
    return out
