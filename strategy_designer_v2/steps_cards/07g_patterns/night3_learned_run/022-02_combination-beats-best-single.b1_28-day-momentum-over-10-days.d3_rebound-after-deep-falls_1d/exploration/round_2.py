import numpy as np, pandas as pd
from scipy import stats

def tt(s):
    s = s.dropna()
    return s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float); n = len(df)
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            vol20 = pd.Series(r1).rolling(20, min_periods=15).std().values
            ret28 = df["debug_info.components.fall28.last_history_value"].values
            hi60 = pd.Series(c).rolling(60, min_periods=20).max().values
            lo60 = pd.Series(c).rolling(60, min_periods=20).min().values
            rng = (c-lo60)/(hi60-lo60)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for i in range(n):
                rows.append(dict(coin=coin, win=w, wn=int(w[1:]), pos=i, yr=yr[i],
                    r28=ret28[i], rng=rng[i], r1=r1[i], vol20=vol20[i],
                    f1=(c[i+1]/c[i]-1) if i+1<n else np.nan,
                    f2=(c[i+2]/c[i]-1) if i+2<n else np.nan,
                    f10=(c[i+10]/c[i]-1) if i+10<n else np.nan))
    d = pd.DataFrame(rows)
    out = {}
    g = d[d["pos"] % 10 == 0].dropna(subset=["f10"]).copy()
    g["u"] = g["f10"] - g.groupby("coin")["f10"].transform("mean")
    g["sd"] = g.groupby("coin")["f10"].transform("std")
    g["s"] = g["u"]/g["sd"]
    g["z28"] = g.groupby("coin")["r28"].transform(lambda s: (s-s.mean())/s.std())
    g["q28"] = g.groupby("coin")["r28"].transform(lambda s: pd.qcut(s.rank(method="first"),10,labels=False))
    out["f10_by_decile28"] = g.groupby("q28").agg(r28=("r28","mean"), u=("u","mean"), strength=("s","mean"), n=("u","size"), t=("u", tt))
    g["half"] = np.where(g["wn"] <= 12, "w1-12", "w13-24")
    res = []
    for (h, coin), gg in g.groupby(["half","coin"]):
        s = stats.linregress(gg["z28"], gg["u"])
        res.append(dict(half=h, coin=coin, n=len(gg), slope=s.slope, t=s.slope/s.stderr))
    out["slope28_by_half_coin"] = pd.DataFrame(res)
    res = []
    for y, gg in g.groupby("yr"):
        s = stats.linregress(gg["z28"], gg["u"])
        res.append(dict(yr=y, n=len(gg), slope=s.slope, t=s.slope/s.stderr))
    out["slope28_by_year"] = pd.DataFrame(res)
    s = stats.linregress(g["z28"], g["u"])
    out["slope28_pooled"] = pd.Series(dict(slope=s.slope, t=s.slope/s.stderr, n=len(g)))
    gr = g.dropna(subset=["rng"]).copy()
    gr["qr"] = gr.groupby("coin")["rng"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["f10_by_range60"] = gr.groupby("qr").agg(rng=("rng","mean"), u=("u","mean"), strength=("s","mean"), n=("u","size"), t=("u", tt))
    # 1-day reversal after large down days
    g1 = d.dropna(subset=["f1","r1","vol20"]).copy()
    g1["u1"] = g1["f1"] - g1.groupby("coin")["f1"].transform("mean")
    g1["z"] = g1["r1"]/g1["vol20"]
    g1["qz"] = pd.qcut(g1["z"].rank(method="first"), 10, labels=False)
    out["next1_by_r1z_decile"] = g1.groupby("qz").agg(z=("z","mean"), u=("u1","mean"), raw=("f1","mean"), n=("u1","size"), t=("u1", tt))
    low = g1[g1["qz"] <= 1]
    out["next1_lowz_by_coin"] = low.groupby("coin").agg(u=("u1","mean"), n=("u1","size"), t=("u1", tt))
    out["next1_lowz_by_year"] = low.groupby("yr").agg(u=("u1","mean"), n=("u1","size"), t=("u1", tt))
    res = []
    for coin, gg in g1.groupby("coin"):
        s = stats.linregress(gg["z"], gg["u1"])
        res.append(dict(coin=coin, n=len(gg), slope=s.slope, t=s.slope/s.stderr))
    out["next1_slope_on_z_by_coin"] = pd.DataFrame(res)
    g2 = d[d["pos"] % 2 == 0].dropna(subset=["f2","r1","vol20"]).copy()
    g2["u2"] = g2["f2"] - g2.groupby("coin")["f2"].transform("mean")
    g2["z"] = g2["r1"]/g2["vol20"]
    g2["qz"] = pd.qcut(g2["z"].rank(method="first"), 10, labels=False)
    out["next2_by_r1z_decile"] = g2.groupby("qz").agg(z=("z","mean"), u=("u2","mean"), n=("u2","size"), t=("u2", tt))
    return out
