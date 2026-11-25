def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    cm = {}
    for c in bars:
        r = pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        cm[c] = r.mean()
    rows = []
    for c in bars:
        allr = pd.concat([b["close"].pct_change() for b in bars[c].values()]).dropna()
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            pos = b["postRebalance_current_allocation"].fillna(0)
            nxt = b["close"].shift(-1) / b["close"] - 1
            dr = b["close"].pct_change()
            vol30 = dr.rolling(30, min_periods=20).std()
            d = pd.DataFrame({"coin": c, "win": w, "i": np.arange(len(b)),
                              "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                              "pos": pos, "ret": nxt, "fc": b["forecast"], "regime": b["regime"],
                              "close": b["close"],
                              "raw": b["debug_info.components.near_high.last_history_value"],
                              "vol30": vol30})
            d["gain"] = d.pos * d.ret
            d["drift"] = d.pos * cm[c]
            d["side"] = np.sign(d.pos)
            d["agit"] = d.vol30 > allr.rolling(30).std().median()
            # forward returns
            for h in [1, 2, 3, 5]:
                d[f"f{h}"] = b["close"].shift(-h) / b["close"] - 1
            rows.append(d)
    D = pd.concat(rows)
    Dr = D.dropna(subset=["ret"])
    # gain by side
    out["by_side"] = Dr.groupby("side").agg(gain_sum=("gain", "sum"), gain_mean=("gain", "mean"),
                                            drift_mean=("drift", "mean"), n=("gain", "size"),
                                            ret=("ret", "mean"))
    # gain by agitation (proxy) and side
    out["by_agit_side"] = Dr[Dr.side != 0].groupby(["agit", "side"]).agg(gain_sum=("gain", "sum"),
                                                     gain_mean=("gain", "mean"), n=("gain", "size"))
    # raw distance bins (in-regime), excess forward returns on non-overlapping grids, day-clustered t
    def grid(h):
        g = []
        for (c, w), d in D.groupby(["coin", "win"]):
            dd = d[d.i % h == 0].copy()
            dd["y"] = dd[f"f{h}"] - cm[c] * h
            g.append(dd)
        G = pd.concat(g)
        G = G[(G.regime == "unknown") & G.raw.notna() & G.y.notna()]
        return G
    def ct(G, col="y"):
        s = G.groupby("day")[col].apply(lambda v: (v - G[col].mean()).sum())
        se = np.sqrt((s ** 2).sum()) / len(G)
        return G[col].mean() / se, G.day.nunique()
    res = []
    for h in [1, 2, 3, 5]:
        G = grid(h)
        G["rb"] = pd.cut(G.raw, [-99, -3, -2, -1, -0.5, -0.001, 0.001, 99],
                         labels=["<-3", "-3..-2", "-2..-1", "-1..-0.5", "-0.5..0", "at0", ">0"])
        for k, gg in G.groupby("rb"):
            if len(gg) < 10: continue
            t, nd = ct(gg)
            res.append({"h": h, "bin": k, "n": len(gg), "days": nd, "mean_ex": gg.y.mean(), "t": t})
    out["raw_bins"] = pd.DataFrame(res)
    # raw distribution
    G5 = grid(5)
    out["raw_desc"] = G5.raw.describe()
    out["share_raw_ge0"] = float((G5.raw >= -1e-9).mean())
    # graded slope above high only (raw>0) at h=3,5
    sl = []
    for h in [1, 3, 5]:
        G = grid(h)
        for name, gg in [("raw>0", G[G.raw > 0]), ("raw<=0", G[G.raw <= 0])]:
            r = stats.linregress(gg.raw, gg.y)
            sl.append({"h": h, "set": name, "n": len(gg), "slope": r.slope, "t": r.slope / r.stderr})
    out["slopes_split"] = pd.DataFrame(sl)
    # outside the profile (chop regime): same bins at 3d, raw recomputed
    res = []
    for h in [3]:
        g = []
        for (c, w), d in D.groupby(["coin", "win"]):
            dd = d[d.i % h == 0].copy()
            hi = d.close.shift(1).rolling(20).max()
            vs = d.close.pct_change().rolling(20).std()
            dd["raw2"] = ((d.close - hi) / d.close / vs)[dd.index] if False else ((d.close / hi - 1) / vs).loc[dd.index]
            dd["y"] = dd[f"f{h}"] - cm[c] * h
            g.append(dd)
        G = pd.concat(g).dropna(subset=["raw2", "y"])
        G["in"] = G.regime == "unknown"
        G["rb"] = pd.cut(G.raw2, [-99, -2, -0.5, 0, 99], labels=["<-2", "-2..-0.5", "-0.5..0", ">0"])
        out["profile_vs_out_3d"] = G.groupby(["in", "rb"]).y.agg(["mean", "count"])
    # long-trade concentration
    T = pd.concat([data["trades"][c][w].assign(coin=c) for c in data["trades"] for w in data["trades"][c]])
    out["trades_by_side"] = T.groupby("side").net_profit_loss_percent.agg(["sum", "mean", "median", "count"])
    return out
