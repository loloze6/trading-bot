def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    hr = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float); v = df["volume"].values.astype(float)
            n = len(c)
            r = np.r_[c[1:]/c[:-1]-1, np.nan]
            ts = pd.to_datetime(df["timestamp"])
            ret180 = pd.Series(c).pct_change(180).values
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            vol = pd.Series(r1).rolling(180, min_periods=60).std().values
            hr.append(pd.DataFrame({"coin": coin, "w": w, "yr": ts.dt.year, "h": ts.dt.hour, "wd": ts.dt.weekday,
                                    "r": r, "ret180": ret180, "vol": vol, "rprev": r1}))
    H = pd.concat(hr).dropna(subset=["r"])
    def tt(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean_bp": 1e4*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x)))})
    h16 = H[H.h == 16]; h20 = H[H.h == 20]
    out["h16_by_coin"] = h16.groupby("coin")["r"].apply(tt).unstack()
    out["h16_by_year"] = h16.groupby("yr")["r"].apply(tt).unstack()
    out["h20_by_coin"] = h20.groupby("coin")["r"].apply(tt).unstack()
    out["h20_by_year"] = h20.groupby("yr")["r"].apply(tt).unstack()
    H["z"] = H["r"]/H["vol"]
    out["h16_z_by_vol_tercile"] = h16.assign(z=h16.r/h16.vol, q=h16.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))).groupby("q")["r"].apply(tt).unstack()
    out["h16_by_30d_sign"] = h16.groupby(h16.ret180 > 0)["r"].apply(tt).unstack()
    out["h16_by_weekday"] = h16.groupby("wd")["r"].apply(tt).unstack()
    sat = H[H.wd == 5]
    out["sat_by_year"] = sat.groupby("yr")["r"].apply(tt).unstack()
    out["sat_by_coin"] = sat.groupby("coin")["r"].apply(tt).unstack()
    # 1-bar reversal / continuation by size of previous bar (z-score) quintile
    H["zp"] = H["rprev"]/H["vol"]
    H["qz"] = pd.cut(H["zp"], [-99, -2, -1, 0, 1, 2, 99])
    out["next_bar_after_prev_z"] = H.groupby("qz")["r"].apply(tt).unstack()
    # up streak length with forward 3 days (18 bars), non-overlapping grid, plus volume slope sign
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float); v = df["volume"].values.astype(float); n = len(c)
            sgn = np.sign(np.r_[0, np.diff(c)])
            st = np.zeros(n)
            for i in range(1, n):
                st[i] = st[i-1]+sgn[i] if (sgn[i] == np.sign(st[i-1]) and sgn[i] != 0) else sgn[i]
            ret18 = pd.Series(c).pct_change(18).values
            sd18 = pd.Series(ret18).rolling(360, min_periods=90).std().values
            for i in range(0, n-18, 18):
                k = int(abs(st[i]))
                slope = np.nan
                if k >= 2:
                    y = v[i-k+1:i+1]; x = np.arange(k)
                    slope = np.polyfit(x, y, 1)[0]/max(y.mean(), 1e-12)
                rows.append(dict(coin=coin, st=st[i], fwd=c[i+18]/c[i]-1, slope=slope, z18=ret18[i]/sd18[i]))
    G = pd.DataFrame(rows)
    G["ex"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    G["stb"] = pd.cut(G["st"], [-99, -5, -3, -1, 0, 2, 4, 99])
    out["fwd3d_by_streak"] = G.groupby("stb")["ex"].apply(tt).unstack()
    up = G[G.st >= 3]
    out["fwd3d_upstreak3plus_by_volslope_sign"] = up.groupby(up.slope > 0)["ex"].apply(tt).unstack()
    G["qz18"] = pd.cut(G["z18"], [-99, -1.5, -0.5, 0.5, 1.5, 99])
    out["fwd3d_by_3d_ret_z"] = G.groupby("qz18")["ex"].apply(tt).unstack()
    return out
