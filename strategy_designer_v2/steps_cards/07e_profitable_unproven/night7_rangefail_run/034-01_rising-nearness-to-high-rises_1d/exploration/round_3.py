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
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            pos = b["postRebalance_current_allocation"].fillna(0)
            dr = cl.pct_change()
            hi = cl.shift(1).rolling(20, min_periods=20).max()
            vs = dr.rolling(20, min_periods=20).std()
            raw = (cl / hi - 1) / vs
            v30 = dr.rolling(30, min_periods=20).std()
            vmed = v30.expanding(min_periods=60).median()
            d = pd.DataFrame({"coin": c, "win": w, "i": np.arange(len(b)),
                              "day": pd.to_datetime(b["timestamp"]).dt.floor("D").astype(str),
                              "pos": pos, "ret": cl.shift(-1) / cl - 1, "fc": b["forecast"],
                              "regime": b["regime"].astype(str), "raw": raw,
                              "agit": (v30 > vmed).where(vmed.notna())})
            for h in [1, 2, 3, 5, 10]:
                d[f"f{h}"] = cl.shift(-h) / cl - 1
            d["gain"] = d.pos * d.ret
            d["drift"] = d.pos * cm[c]
            d["side"] = np.sign(d.pos)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    Dr = D.dropna(subset=["ret"])
    tot = Dr.gain.sum()
    out["by_side"] = Dr.groupby("side").agg(gain_sum=("gain", "sum"), gain_mean=("gain", "mean"),
                                            drift_mean=("drift", "mean"), n=("gain", "size"))
    out["by_side"]["share_of_gain"] = out["by_side"].gain_sum / tot
    Dr2 = Dr[Dr.side != 0].copy()
    Dr2["rb"] = pd.cut(Dr2.raw, [-99, -2, -1, 0, 99], labels=["<-2", "-2..-1", "-1..0", ">0"])
    a = Dr2.groupby(["side", "rb"]).agg(gain_sum=("gain", "sum"), gain_mean=("gain", "mean"),
                                         drift_mean=("drift", "mean"), n=("gain", "size"))
    a["share_of_gain"] = a.gain_sum / tot
    out["gain_by_side_rawbin"] = a
    b2 = Dr[Dr.side != 0].groupby(["agit", "side"]).agg(gain_sum=("gain", "sum"), n=("gain", "size"))
    b2["share_of_gain"] = b2.gain_sum / tot
    out["gain_by_agit_side"] = b2
    out["share_gain_w10_w11"] = float(Dr[Dr.win.isin(["w10", "w11"])].gain.sum() / tot)

    def ct(G):
        m = G.y.mean()
        s = G.groupby("day").y.apply(lambda v: (v - m).sum())
        se = np.sqrt((s ** 2).sum()) / len(G)
        return m / se, G.day.nunique()
    res = []; sl = []
    for h in [1, 3, 5, 10]:
        g = []
        for (c, w), d in D.groupby(["coin", "win"]):
            dd = d[d.i % h == 0].copy()
            dd["y"] = dd[f"f{h}"] - cm[c] * h
            g.append(dd)
        G = pd.concat(g).dropna(subset=["raw", "y"])
        for inp, GG in [("in", G[G.regime == "unknown"]), ("out", G[G.regime != "unknown"])]:
            GG = GG.copy()
            GG["rb"] = pd.cut(GG.raw, [-99, -2, -1, -0.3, 0.0001, 99],
                              labels=["<-2", "-2..-1", "-1..-0.3", "-0.3..0", ">0"])
            for k, gg in GG.groupby("rb", observed=True):
                if len(gg) < 15: continue
                t, nd = ct(gg)
                res.append({"h": h, "prof": inp, "bin": str(k), "n": len(gg), "days": nd,
                            "mean_ex": gg.y.mean(), "t": t})
            up = GG[GG.raw > 0]
            if len(up) > 20:
                r = stats.linregress(up.raw, up.y)
                sl.append({"h": h, "prof": inp, "set": "raw>0", "n": len(up), "slope": r.slope,
                           "t": r.slope / r.stderr})
            dn = GG[GG.raw <= 0]
            r = stats.linregress(dn.raw, dn.y)
            sl.append({"h": h, "prof": inp, "set": "raw<=0", "n": len(dn), "slope": r.slope,
                       "t": r.slope / r.stderr})
    out["raw_bins"] = pd.DataFrame(res)
    out["slopes_split"] = pd.DataFrame(sl)
    T = pd.concat([data["trades"][c][w].assign(coin=c) for c in data["trades"] for w in data["trades"][c]])
    out["trades_by_side"] = T.groupby("side").net_profit_loss_percent.agg(["sum", "mean", "median", "count"])
    return out
