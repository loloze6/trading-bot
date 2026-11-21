def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            n = len(c)
            rp = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vol = pd.Series(rp).rolling(20, min_periods=15).std().shift(1).values
            ts = pd.to_datetime(b["timestamp"])
            for h in [1, 3, 7]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, fwd=c[i + h] / c[i] - 1, rp=rp[i], vol=vol[i],
                                     year=ts.iloc[i].year, wd=ts.iloc[i].dayofweek,
                                     wnum=int(w[1:])))
    D = pd.DataFrame(rows).dropna(subset=["rp", "vol", "fwd"])
    D["ex"] = D["fwd"] - D.groupby(["coin", "h"])["fwd"].transform("mean")
    D["z"] = D["rp"] / D["vol"]
    D["usual"] = D.groupby(["coin", "h"])["fwd"].transform("std")
    D["str"] = D["ex"] / D["usual"]

    def summ(df, key, col="ex"):
        a = df.groupby(key)[col].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.drop(columns="std")

    for h in [1, 3, 7]:
        q = D[D.h == h].copy()
        q["zq"] = pd.cut(q["z"], [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
        out[f"h{h}_by_z_band"] = summ(q, "zq")
    q = D[D.h == 1].copy()
    down = q[q.z < -1]
    out["h1_down_by_coin"] = summ(down, "coin")
    out["h1_down_by_year"] = summ(down, "year")
    down["half"] = np.where(down.wnum <= 12, "w1-12", "w13-24")
    out["h1_down_by_half"] = summ(down, "half")
    # graded: regression of ex on z within down days
    from scipy import stats
    for h in [1, 3]:
        dd = D[(D.h == h) & (D.z < 0)]
        r = stats.linregress(dd["z"], dd["ex"])
        out[f"h{h}_slope_on_z_downdays"] = f"slope {r.slope:.5f} t {r.slope / r.stderr:.2f} n {len(dd)}"
        uu = D[(D.h == h) & (D.z > 0)]
        r = stats.linregress(uu["z"], uu["ex"])
        out[f"h{h}_slope_on_z_updays"] = f"slope {r.slope:.5f} t {r.slope / r.stderr:.2f} n {len(uu)}"
    # size of the down-day bounce vs cost
    dd = q[q.z < -1]
    out["h1_down_size"] = pd.Series({"ex_mean": dd["ex"].mean(), "total_mean": dd["fwd"].mean(),
                                     "strength": dd["str"].mean(), "n": len(dd)})
    # weekday robustness
    q["half"] = np.where(q.wnum <= 12, "a", "b")
    wk = q.groupby(["wd", "half"])["ex"].mean().unstack()
    out["h1_weekday_by_half"] = wk
    return out
