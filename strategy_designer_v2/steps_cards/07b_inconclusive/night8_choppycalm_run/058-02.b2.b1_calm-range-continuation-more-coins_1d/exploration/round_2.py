def explore(data):
    import numpy as np, pandas as pd
    rows = []
    H = [5, 10]
    coinmean = {}
    for coin, wins in data["bars"].items():
        for h in H:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            coinmean[(coin, h)] = np.mean(rs) if rs else np.nan
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            hi = b["high"].rolling(20).max(); lo = b["low"].rolling(20).min()
            rp = 2 * (c - lo) / (hi - lo) - 1
            ts = pd.to_datetime(b["timestamp"])
            for h in H:
                for i in np.arange(0, len(b) - h, h):
                    if np.isnan(rp[i]): continue
                    r = c[i + h] / c[i] - 1
                    rows.append(dict(coin=coin, w=w, year=ts[i].year, h=h, rp=rp[i],
                                     inprof=(b.loc[i, "regime"] == "unknown"),
                                     f=b.loc[i, "forecast"], ex=r - coinmean[(coin, h)],
                                     day=ts[i].normalize()))
    d = pd.DataFrame(rows)

    def slope(g, x="rp"):
        if len(g) < 10: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        X = g[x] - g[x].mean(); y = g["ex"]
        bta = (X * y).sum() / (X ** 2).sum()
        res = y - y.mean() - bta * X
        s = (X * res).groupby(g["day"]).sum()
        G = len(s); se = np.sqrt((s ** 2).sum() * G / (G - 1)) / (X ** 2).sum()
        return pd.Series(dict(n=len(g), slope=bta, t=bta / se))
    out = {}
    out["rp_slope_in_vs_out_profile"] = d.groupby(["h", "inprof"]).apply(slope)
    out["rp_slope_out_profile_by_year_h5"] = d[(d.h == 5) & (~d.inprof)].groupby("year").apply(slope)
    di = d[d.inprof & (d.f != 0)].copy()
    di["side"] = np.sign(di["rp"])
    di["sx"] = di.ex * di.side
    out["in_signed_by_h_year_side"] = di.groupby(["h", "side", "year"]).agg(
        n=("sx", "size"), signed_ex=("sx", "mean"),
        t=("sx", lambda x: x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan))
    di["edge"] = pd.cut(di.rp.abs(), [0, 0.33, 0.66, 1.01], labels=["mid", "near", "edge"])
    out["in_signed_by_h_edge_side"] = di.groupby(["h", "edge", "side"]).agg(
        n=("sx", "size"), signed_ex=("sx", "mean"),
        t=("sx", lambda x: x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan))
    out["in_h5_slope_excl_2021"] = slope(di[(di.h == 5) & (di.year != 2021)])
    return out
