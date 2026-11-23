def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["bars"].keys())
    def tt(x):
        x = pd.Series(x).dropna()
        return x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 and x.std() > 0 else np.nan
    def rq(x, k):
        return pd.qcut(x.rank(method="first"), k, labels=False)
    wi = {f"w{i}": i for i in range(1, 25)}
    cs = []; grid = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b.close.values.astype(float); vo = b.volume.values.astype(float)
            n = len(b); ts = pd.to_datetime(b.timestamp)
            lr = np.diff(np.log(cl))
            fc = b.forecast.fillna(0).values
            sig = (fc != 0) & (b.regime.values == "trending")
            for t in np.where(sig)[0]:
                if t + 48 >= n or t < 720: continue
                s = np.sign(fc[t])
                vol = np.std(lr[t - 720:t]) * np.sqrt(48)
                p30 = cl[t - 48] / cl[t - 720] - 1
                vr = vo[t - 47:t + 1].mean() / max(vo[t - 167:t - 47].mean(), 1e-12)
                r48 = cl[t + 48] / cl[t] - 1
                cs.append(dict(coin=c, w=w, wn=wi[w], t=t, year=ts[t].year, s=s, vr=vr, vol=vol,
                               trend=s * np.sign(p30), d48=s * r48,
                               pnl=abs(b.postRebalance_current_allocation.values[t]) * s * r48))
            for t in range(720, n - 48, 48):
                vol = np.std(lr[t - 720:t]) * np.sqrt(48)
                wk = cl[t] / cl[t - 48] - 1
                s = np.sign(wk)
                if s == 0: continue
                grid.append(dict(coin=c, vol=vol, d48=s * (cl[t + 48] / cl[t] - 1)))
    cs = pd.DataFrame(cs); grid = pd.DataFrame(grid)
    cs["volq"] = cs.groupby("coin").vol.transform(lambda x: rq(x, 3))
    cs["vrq"] = rq(cs.vr, 2)
    grid["volq"] = grid.groupby("coin").vol.transform(lambda x: rq(x, 3))
    out["grid_follow48h_by_volq_condition_alone"] = grid.groupby("volq").agg(n=("d48", "size"), d48=("d48", "mean"), t=("d48", tt))
    fall = cs[cs.wn >= 22]
    out["fall_by_vrq"] = fall.groupby("vrq").agg(n=("d48", "size"), d48=("d48", "mean"), t=("d48", tt), pnl=("pnl", "sum"))
    out["fall_by_volq"] = fall.groupby("volq").agg(n=("d48", "size"), d48=("d48", "mean"), t=("d48", tt), pnl=("pnl", "sum"))
    out["w13_by_vrq"] = cs[cs.wn.between(11, 13)].groupby("vrq").agg(n=("d48", "size"), d48=("d48", "mean"), pnl=("pnl", "sum"))
    cs = cs.sort_values(["wn", "t"])
    def chain(sub):
        # weekly case pnl averaged over the 6 coins (zero if no case), chained in time order
        p = sub.groupby(["wn", "t"]).pnl.sum() / 6.0
        v = (1 + p).cumprod()
        mdd = (v / v.cummax() - 1).min()
        return pd.Series({"n": len(sub), "total": v.iloc[-1] - 1, "maxdd": mdd,
                          "ratio": (v.iloc[-1] - 1) / abs(mdd) if mdd < 0 else np.nan, "d48": sub.d48.mean(), "t": tt(sub.d48)})
    out["chains"] = pd.DataFrame({
        "all": chain(cs),
        "vr_top_half": chain(cs[cs.vrq == 1]),
        "vol_low_mid": chain(cs[cs.volq <= 1]),
        "trend_aligned": chain(cs[cs.trend == 1]),
        "no_XMR": chain(cs[cs.coin != "XMRUSD"]),
        "vr_top_and_aligned": chain(cs[(cs.vrq == 1) & (cs.trend == 1)]),
    }).T
    return out
