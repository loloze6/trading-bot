def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            b["clv"] = (b["close"] - b["low"]) / rng
            b["dayret"] = b["close"] / b["open"] - 1
            b["ret1d"] = b["close"] / b["close"].shift(1) - 1
            for h in (1, 2, 3, 5):
                b[f"r{h}"] = b["close"].shift(-h) / b["close"] - 1
            b["pos"] = np.arange(len(b))
            b["inprof"] = (b["regime"] != "chop")
            b["coin"] = coin; b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["fc"] = b["forecast"]
            b["zc"] = b.get("debug_info.components.close_loc.post_pipeline_value")
            rows.append(b[["coin","win","year","pos","clv","dayret","ret1d","r1","r2","r3","r5","inprof","fc","day"]])
    d = pd.concat(rows, ignore_index=True)
    for h in (1,2,3,5):
        dm = {c: d[(d.coin==c) & (d.pos % h == 0)][f"r{h}"].mean() for c in d.coin.unique()}
        d[f"ex{h}"] = d[f"r{h}"] - d["coin"].map(dm)
    p = d[d.inprof & d.clv.notna()].copy()
    out = {}
    def ct(x, col, wcol=None):
        x = x.dropna(subset=[col])
        if len(x) < 5: return pd.Series({"n": len(x)})
        w = x[wcol] if wcol else pd.Series(1.0, index=x.index)
        m = (x[col]*w).sum()/w.sum()
        dev = ((x[col]-m)*w).groupby(x["day"]).sum()
        se = np.sqrt((dev**2).sum()*len(dev)/(len(dev)-1))/w.sum()
        return pd.Series({"n": len(x), "days": x.day.nunique(), "mean_%": 100*m, "t": m/se})
    # short-direction, graded by forecast size, per horizon
    for h in (1,2,3,5):
        sub = p[(p.pos % h == 0) & (p.fc < 0)].copy()
        sub["s"] = -sub[f"ex{h}"]; sub["w"] = -sub["fc"]
        out[f"short_w_fc_h{h}"] = ct(sub, "s", "w")
        # short graded by clv on up days only
        u = sub[sub.dayret > 0].copy(); u["w2"] = u["clv"]
        out[f"short_updays_wclv_h{h}"] = ct(u, "s", "w2")
        # short graded by day return size on up days
        u["w3"] = u["dayret"]
        out[f"short_updays_wdayret_h{h}"] = ct(u, "s", "w3")
        u2 = sub[sub.ret1d > 0].copy(); u2["w4"] = u2["ret1d"]
        out[f"short_uprets_wret1d_h{h}"] = ct(u2, "s", "w4")
    # cross: up/down day x clv half, 1 and 3 day short excess
    p["up"] = p.dayret > 0; p["hi"] = p.clv > 0.5
    for h in (1,3):
        sub = p[p.pos % h == 0].copy(); sub["s"] = -sub[f"ex{h}"]
        out[f"cross_short_h{h}"] = sub.groupby(["up","hi"]).apply(lambda g: ct(g, "s"))
    # by coin, up-day short weighted by dayret, h3
    sub = p[(p.pos % 3 == 0) & (p.dayret > 0)].copy(); sub["s"] = -sub["ex3"]; sub["w"] = sub["dayret"]
    out["updays_short_h3_by_coin"] = sub.groupby("coin").apply(lambda g: ct(g, "s", "w"))
    out["updays_short_h3_by_year"] = sub.groupby("year").apply(lambda g: ct(g, "s", "w"))
    sub = p[(p.pos % 1 == 0) & (p.dayret > 0)].copy(); sub["s"] = -sub["ex1"]; sub["w"] = sub["clv"]
    out["updays_short_h1_wclv_by_coin"] = sub.groupby("coin").apply(lambda g: ct(g, "s", "w"))
    return out
