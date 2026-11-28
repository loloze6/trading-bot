def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.shift(1).rolling(30, min_periods=20).std()
            z = r / sd
            inprof = (b["regime"] == "unknown")
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for h in [1, 3, 5, 10]:
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(b), h)
                for i in idx:
                    rows.append(dict(coin=coin, w=w, h=h, z=z.iloc[i], fwd=fwd.iloc[i],
                                     prof=bool(inprof.iloc[i]), yr=yr.iloc[i],
                                     fc=b["forecast"].iloc[i]))
    d = pd.DataFrame(rows).dropna(subset=["fwd"])
    drift = d.groupby(["coin", "h"])["fwd"].mean().rename("drift")
    d = d.join(drift, on=["coin", "h"])
    d["unu"] = d["fwd"] - d["drift"]
    p = d[d.prof].dropna(subset=["z"])
    p["zb"] = pd.cut(p["z"], [-99, -1.5, -0.5, 0, 0.5, 1, 1.5, 2, 99])
    tab = p.groupby(["h", "zb"])["unu"].agg(["mean", "count", "std"])
    tab["t"] = tab["mean"] / (tab["std"] / np.sqrt(tab["count"]))
    out["in profile: unusual fwd move by z bucket and horizon"] = tab.reset_index()
    reg = []
    for h, g in p.groupby("h"):
        up = g[g.z > 0]
        s = stats.linregress(up.z, up.unu)
        sa = stats.linregress(g.z, g.unu)
        reg.append(dict(h=h, n_up=len(up), slope_up=s.slope, t_up=s.slope / s.stderr,
                        n_all=len(g), slope_all=sa.slope, t_all=sa.slope / sa.stderr))
    out["slope of unusual move on z (in profile)"] = pd.DataFrame(reg)
    big = p[(p.z > 1)]
    gc = big.groupby(["h", "coin"])["unu"].agg(["mean", "count"])
    out["z>1 in profile: by coin"] = gc.reset_index()
    gy = big[big.h == 3].groupby("yr")["unu"].agg(["mean", "count"])
    out["z>1 h3 by year"] = gy.reset_index()
    o = d[~d.prof].dropna(subset=["z"])
    ob = o[o.z > 1].groupby("h")["unu"].agg(["mean", "count", "std"])
    ob["t"] = ob["mean"] / (ob["std"] / np.sqrt(ob["count"]))
    out["outside profile z>1"] = ob.reset_index()
    out["share in profile by coin"] = d[d.h == 1].groupby("coin")["prof"].mean()
    return out
