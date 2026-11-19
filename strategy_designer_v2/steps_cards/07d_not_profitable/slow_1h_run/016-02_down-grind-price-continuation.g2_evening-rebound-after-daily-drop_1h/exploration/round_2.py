def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    parts = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            ts = pd.to_datetime(b["timestamp"], utc=True)
            cl = b["close"]
            r1 = np.log(cl).diff()
            vol = r1.rolling(24*20, min_periods=200).std()
            g = pd.DataFrame({"coin": c, "win": w, "hour": ts.dt.hour, "fc": b["forecast"],
                              "pos": b["postRebalance_current_allocation"].fillna(0),
                              "f2": cl.shift(-2)/cl - 1, "f6": cl.shift(-6)/cl - 1,
                              "f12": cl.shift(-12)/cl - 1, "f24": cl.shift(-24)/cl - 1,
                              "f48": cl.shift(-48)/cl - 1,
                              "ret24": cl/cl.shift(24) - 1, "vol": vol})
            parts.append(g[g.hour == 20])
    D = pd.concat(parts)
    D["fb"] = pd.cut(D.fc, [-0.01, 0.0001, 5, 10, 21])
    out["fwd_by_fc"] = D.groupby("fb", observed=True)[["f2", "f6", "f12", "f24", "f48"]].mean()
    out["n_by_fc"] = D.groupby("fb", observed=True).size()
    P = D[D.fc > 0].copy()
    # graded with horizon: slope t of each horizon on fc
    res = {}
    for h in ["f2", "f6", "f12", "f24", "f48"]:
        x = D.dropna(subset=[h])
        s = stats.linregress(x.fc, x[h])
        res[h] = pd.Series({"slope": s.slope, "t": s.slope/s.stderr, "n": len(x)})
    out["slope_by_h"] = pd.DataFrame(res)
    # edge vs vol: positive forecast cases by vol tercile; gross 2h return vs a 0.1% fee
    P["vq"] = pd.qcut(P.vol, 3, labels=["lowvol", "midvol", "highvol"])
    out["pos_by_vol"] = P.groupby("vq", observed=True).agg(n=("f2", "size"), f2=("f2", "mean"),
                                                            f24=("f24", "mean"), pos=("pos", "mean"))
    # raw 24h return size (in own vol) tercile among positive forecasts
    P["z"] = P.ret24 / (P.vol * np.sqrt(24))
    P["zq"] = pd.qcut(P.z, 4)
    out["pos_by_z"] = P.groupby("zq", observed=True).agg(n=("f2", "size"), f2=("f2", "mean"),
                                                          f6=("f6", "mean"), f24=("f24", "mean"))
    # unconditional 20:00 2h return vs all-bars 2h mean
    out["zero_fc_f2"] = D[D.fc <= 0].f2.agg(["size", "mean"])
    return out
