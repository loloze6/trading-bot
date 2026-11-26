def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            z = r1 / sd
            tr60 = c / c.shift(60) - 1
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            rng = (b["high"] - b["low"]) / c
            clv = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            vol = b["volume"].astype(float)
            vz = vol / vol.rolling(30, min_periods=20).mean()
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                              "z": z, "fwd": fwd, "fwd1": fwd1, "tr60": tr60,
                              "calm": (b["regime"] == "unknown"), "clv": clv, "vz": vz,
                              "year": pd.to_datetime(b["timestamp"]).dt.year,
                              "wd": pd.to_datetime(b["timestamp"]).dt.weekday})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.pos % H == 0].groupby("coin")["fwd"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    G = A[(A.pos % H == 0)].dropna(subset=["z", "ex"])
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    G["zb"] = pd.cut(G.z, [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
    out = {}
    out["ex5_by_zbin_calm"] = G.groupby(["calm", "zb"])["ex"].apply(tt).unstack()
    G["trend"] = np.where(G.tr60 > 0.1, "rising", np.where(G.tr60 < -0.1, "falling", "choppy"))
    G.loc[G.tr60.isna(), "trend"] = "na"
    def slope(g):
        if len(g) < 30: return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        s = stats.linregress(g.z, g.ex)
        return pd.Series({"n": len(g), "slope": s.slope, "t": s.slope / s.stderr})
    out["slope_ex5_on_z_by_calm_trend"] = G.groupby(["calm", "trend"]).apply(slope)
    out["slope_by_calm_year"] = G.groupby(["calm", "year"]).apply(slope)
    out["slope_by_coin_calm"] = G.groupby(["coin", "calm"]).apply(slope)
    # down days only vs up days only
    out["slope_up_only"] = G[G.z > 0].groupby("calm").apply(slope)
    out["slope_down_only"] = G[G.z < 0].groupby("calm").apply(slope)
    # close location on big days
    big = G[G.z.abs() > 1.5].copy()
    big["sgn_ex"] = big.ex * np.sign(big.z)
    big["clvb"] = pd.cut(big.clv, [0, 0.33, 0.67, 1.0001])
    out["big_day_signed_ex_by_dir_clv"] = big.groupby([np.sign(big.z), "clvb"])["sgn_ex"].apply(tt).unstack()
    big["vb"] = pd.qcut(big.vz, 3, labels=["lowvol", "mid", "highvol"])
    out["big_day_signed_ex_by_volume"] = big.groupby(["calm", "vb"])["sgn_ex"].apply(tt).unstack()
    # weekday of 1-day returns, all bars
    A["ex1"] = A.fwd1 - A.groupby("coin").fwd1.transform("mean")
    out["ex1_by_weekday"] = A.groupby("wd")["ex1"].apply(tt).unstack()
    # book: days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, w=w))
    D = pd.concat(dd)
    D["d"] = pd.to_datetime(D["day"])
    bk = D.groupby("d").agg(br=("book_return", "mean"), cr=("coin_return", "mean")).dropna()
    out["book_vs_hold"] = pd.Series({"book_mean": bk.br.mean(), "hold_mean": bk.cr.mean(),
                                     "corr": bk.br.corr(bk.cr), "n": len(bk)})
    bk["y"] = bk.index.year
    out["book_by_year"] = bk.groupby("y")[["br", "cr"]].mean()
    return out
