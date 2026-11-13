def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []; ev = []
    allbars = {}
    for c, ws in data["bars"].items():
        lst = []
        for w, b in ws.items():
            b = b.copy()
            b["day"] = pd.to_datetime(b.timestamp).dt.floor("D")
            b["r1"] = b.close.pct_change()
            b["tr50"] = b.close / b.close.shift(50) - 1
            b["vol20"] = b.r1.rolling(20).std()
            b["pos20"] = (b.close - b.close.rolling(20).min()) / (b.close.rolling(20).max() - b.close.rolling(20).min())
            b["f10"] = b.close.shift(-10) / b.close - 1
            b["w"] = w; b["coin"] = c
            lst.append(b)
        allbars[c] = pd.concat(lst)
    # coin mean 10-bar return over all windows
    vq = pd.concat([allbars[c].vol20 for c in allbars]).quantile([1/3, 2/3]).values
    for c, A in allbars.items():
        mu10 = A.f10.mean()
        for w, b in A.groupby("w"):
            b = b.reset_index(drop=True)
            sh = b["debug_info.components.since_high.last_history_value"] if "debug_info.components.since_high.last_history_value" in b else pd.Series(np.nan, index=b.index)
            newhi = (b.close >= b.close.rolling(20).max()) & (b.close.shift(1) < b.close.rolling(20).max().shift(1))
            last = -100
            for i in np.where(newhi.values)[0]:
                if i - last >= 10 and not np.isnan(b.f10[i]):
                    ev.append({"coin": c, "x": b.f10[i] - mu10, "tr_up": b.tr50[i] > 0 if not np.isnan(b.tr50[i]) else np.nan,
                               "vol": np.digitize(b.vol20[i], vq) if not np.isnan(b.vol20[i]) else np.nan})
                    last = i
        # book per coin per day with prior-bar features
        d = []
        for w, dd in data["days"][c].items():
            dd = dd.copy(); dd["day"] = pd.to_datetime(dd["day"]).dt.tz_localize(None).dt.floor("D"); dd["w"] = w; d.append(dd)
        d = pd.concat(d)
        f = A[["w", "day", "tr50", "vol20", "postRebalance_current_allocation", "forecast"]].copy()
        f["day"] = f["day"].dt.tz_localize(None) if f["day"].dt.tz is not None else f["day"]
        f = f.sort_values(["w", "day"])
        for col in ["tr50", "vol20", "postRebalance_current_allocation", "forecast"]:
            f[col] = f.groupby("w")[col].shift(1)
        m = d.merge(f, on=["w", "day"], how="left"); m["coin"] = c
        rows.append(m)
    M = pd.concat(rows).dropna(subset=["book_return"])
    M["exposed"] = M.forecast.fillna(0) > 0
    M["trend"] = np.where(M.tr50 > 0, "up50", np.where(M.tr50 <= 0, "down50", "na"))
    M["volb"] = pd.Series(np.digitize(M.vol20.fillna(-1), vq), index=M.index).where(M.vol20.notna())
    ncoin = 6
    def bookby(key):
        g = M.groupby(["w", "day", key])["book_return"].sum().reset_index()
        tot = M.groupby(["w", "day"]).size().rename("n").reset_index()
        g = g.merge(tot, on=["w", "day"]); g["contrib"] = g.book_return / g.n
        r = g.groupby(key)["contrib"].agg(["sum", "mean"]); return r.round(4)
    out["book_contrib_by_trend"] = bookby("trend")
    out["book_contrib_by_vol"] = bookby("volb")
    M["tv"] = M.trend + "_v" + M.volb.astype(str)
    out["book_contrib_by_trend_vol"] = bookby("tv")
    # exposed coin-days stats by trend
    E = M[M.exposed]
    out["exposed_daily_by_trend"] = E.groupby("trend")["book_return"].agg(["mean", "std", "size", lambda s: s.mean()/s.std()*np.sqrt(len(s))]).round(5)
    out["exposed_daily_by_vol"] = E.groupby("volb")["book_return"].agg(["mean", "std", "size"]).round(5)
    out["exposure_share_by_trend"] = M.groupby("trend")["exposed"].mean().round(3)
    # events
    V = pd.DataFrame(ev)
    def tt(s): return pd.Series({"mean": s.mean(), "t": s.mean()/s.std()*np.sqrt(len(s)), "n": len(s)})
    out["events_all"] = tt(V.x).round(4)
    out["events_by_trend"] = V.dropna(subset=["tr_up"]).groupby("tr_up")["x"].apply(tt).unstack().round(4)
    out["events_by_vol"] = V.dropna(subset=["vol"]).groupby("vol")["x"].apply(tt).unstack().round(4)
    # book falls: worst 5% book days, share of exposed coins and coin return
    bk = M.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"), ex=("exposed", "mean"),
                                    up=("tr50", lambda s: (s > 0).mean())).reset_index()
    q = bk.br.quantile(0.05)
    out["worst5pct_days"] = bk[bk.br <= q][["br", "cr", "ex", "up"]].mean().round(4)
    out["all_days"] = bk[["br", "cr", "ex", "up"]].mean().round(4)
    bk["upb"] = pd.cut(bk.up, [-0.01, 0.34, 0.67, 1.0])
    out["book_by_share_up50"] = bk.groupby("upb").agg(mean=("br", "mean"), sd=("br", "std"), n=("br", "size"), cr=("cr", "mean"), ex=("ex", "mean")).round(5)
    return out
