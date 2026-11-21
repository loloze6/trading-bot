import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    H = 5
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(30, min_periods=20).std()
            z = r1 / vol
            r20 = c / c.shift(20) - 1
            hi30 = c / c.rolling(30, min_periods=20).max() - 1
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for i in range(0, n, H):
                if i + H >= n: break
                rows.append(dict(coin=coin, win=w, z=z[i], r1=r1[i], vol=vol[i], r20=r20[i],
                                 hi30=hi30[i], fwd=fwd[i], wd=ts[i].weekday(),
                                 fc=b["forecast"].iloc[i], year=ts[i].year))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby("coin")["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["drift"]
    d["volrank"] = d.groupby("coin")["vol"].rank(pct=True)
    out = {}
    def summ(g):
        x = g["ex"].dropna()
        return pd.Series({"n": len(x), "mean_ex_%": 100*x.mean(),
                          "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "mean_fwd_%": 100*g["fwd"].mean()})
    dz = d.dropna(subset=["z", "ex"])
    dz["zq"] = pd.qcut(dz["z"], 10, labels=False)
    out["by_z_decile"] = dz.groupby("zq").apply(summ)
    dr = d.dropna(subset=["r20", "ex"]).copy()
    dr["q"] = pd.qcut(dr["r20"], 5, labels=False)
    out["by_r20_quint"] = dr.groupby("q").apply(summ)
    dh = d.dropna(subset=["hi30", "ex"]).copy()
    dh["q"] = pd.qcut(dh["hi30"].rank(method="first"), 5, labels=False)
    out["by_hi30_quint"] = dh.groupby("q").apply(summ)
    dv = d.dropna(subset=["volrank", "ex"]).copy()
    dv["q"] = pd.qcut(dv["volrank"], 5, labels=False)
    out["by_vol_quint"] = dv.groupby("q").apply(summ)
    out["by_weekday"] = d.dropna(subset=["ex"]).groupby("wd").apply(summ)
    out["by_coin"] = d.dropna(subset=["ex"]).groupby("coin").apply(summ)
    out["by_year"] = d.dropna(subset=["ex"]).groupby("year").apply(summ)
    # z slope within up / down days, and within high/low vol
    res = {}
    for name, g in [("up", dz[dz.z > 0]), ("down", dz[dz.z < 0]), ("all", dz)]:
        s = stats.linregress(g["z"], g["ex"])
        res[name] = (len(g), s.slope*100, s.slope/s.stderr)
    out["z_slope"] = pd.DataFrame(res, index=["n", "slope_%", "t"]).T
    # interaction: z by vol regime and by r20 sign
    dz2 = dz.dropna(subset=["r20", "volrank"]).copy()
    dz2["trend"] = np.where(dz2["r20"] > 0, "up20", "down20")
    dz2["vh"] = np.where(dz2["volrank"] > 0.5, "hivol", "lovol")
    dz2["zs"] = np.where(dz2["z"] > 0, "zpos", "zneg")
    out["z_sign_x_trend"] = dz2.groupby(["trend", "zs"]).apply(summ)
    out["z_sign_x_vol"] = dz2.groupby(["vh", "zs"]).apply(summ)
    # book
    br = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd[["book_return", "coin_return"]].copy(); x["coin"] = coin; x["win"] = w
            x["day"] = range(len(x)); br.append(x)
    B = pd.concat(br)
    pb = B.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    pb["wdq"] = None
    out["book_vs_coin"] = pd.Series({"book_mean_%": 100*pb.book_return.mean(),
        "coin_mean_%": 100*pb.coin_return.mean(),
        "corr": pb.book_return.corr(pb.coin_return),
        "book_sharpe": pb.book_return.mean()/pb.book_return.std()*np.sqrt(365),
        "beta": np.cov(pb.book_return, pb.coin_return)[0,1]/pb.coin_return.var()})
    bw = pb.groupby("win")["book_return"].agg(lambda s: (1+s).prod()-1)
    cw = pb.groupby("win")["coin_return"].agg(lambda s: (1+s).prod()-1)
    out["by_window_%"] = pd.DataFrame({"book": 100*bw, "coin": 100*cw})
    return out
