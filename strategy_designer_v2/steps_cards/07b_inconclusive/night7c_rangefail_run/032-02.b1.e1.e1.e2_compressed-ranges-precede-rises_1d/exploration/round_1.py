def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change().abs()
            hi = c.shift(1).rolling(60).max(); lo = c.shift(1).rolling(60).min()
            mad = r1.rolling(60).mean()
            W = (hi - lo) / c / mad
            pos = (c - (hi + lo) / 2) / (hi - lo)          # position vs range mid
            ret60 = c / c.shift(60) - 1
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for h in (5, 10, 20, 40):
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(b) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=yr[i], fc=b["forecast"].iloc[i],
                                     W=W.iloc[i], pos=pos.iloc[i], ret60=ret60.iloc[i], fwd=fwd.iloc[i]))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby(["coin", "h"])["fwd"].transform("mean")
    out = {}
    def slope(g, x):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 10: return pd.Series({"n": len(g), "corr": np.nan, "t": np.nan})
        r, p = stats.pearsonr(g[x], g["ex"])
        t = r * np.sqrt((len(g) - 2) / (1 - r * r))
        return pd.Series({"n": len(g), "corr": r, "t": t})
    out["by_h_forecast"] = d.groupby("h").apply(lambda g: slope(g, "fc"))
    d["negW"] = -d["W"]
    out["by_h_negW"] = d.groupby("h").apply(lambda g: slope(g, "negW"))
    d20 = d[d.h == 20].copy()
    out["h20_by_coin_fc"] = d20.groupby("coin").apply(lambda g: slope(g, "fc"))
    out["h20_by_year_fc"] = d20.groupby("year").apply(lambda g: slope(g, "fc"))
    d20["q"] = pd.qcut(d20["fc"], 5, labels=False, duplicates="drop")
    out["h20_quint_fc"] = d20.groupby("q").agg(n=("ex", "size"), ex=("ex", "mean"), absfwd=("fwd", lambda s: s.abs().mean()), fc=("fc", "mean"))
    # direction by position in range interacted with compression
    for h in (10, 20):
        g = d[d.h == h].dropna(subset=["W", "pos"]).copy()
        g["comp_pos"] = g["pos"] / g["W"]
        g["comp_trend"] = np.sign(g["ret60"]) / g["W"]
        g["negpos"] = -g["pos"]
        out[f"h{h}_signals"] = pd.DataFrame({k: slope(g, k) for k in ["pos", "negpos", "comp_pos", "comp_trend", "ret60"]}).T
        g["qW"] = pd.qcut(g["W"], 3, labels=["tight", "mid", "wide"])
        out[f"h{h}_pos_slope_by_W"] = g.groupby("qW").apply(lambda x: slope(x, "pos"))
        out[f"h{h}_absmove_by_W"] = g.groupby("qW").agg(n=("fwd", "size"), absfwd=("fwd", lambda s: s.abs().mean()), ex=("ex", "mean"))
    return out
