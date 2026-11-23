def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"])
            b["hour"] = ts.dt.hour.values
            b["year"] = ts.dt.year.values
            c = b["close"].astype(float)
            r1 = c.pct_change()
            b["r1"] = r1
            b["fwd1"] = c.shift(-1) / c - 1
            b["fwd24"] = c.shift(-24) / c - 1
            b["ret24"] = c / c.shift(24) - 1
            vol24 = r1.rolling(24).std()
            m720 = vol24.rolling(720, min_periods=240).mean()
            b["z1"] = r1 / m720
            b["volratio"] = vol24 / m720
            b["z24"] = b["ret24"] / (vol24 * np.sqrt(24))
            b["z24m"] = b["ret24"] / (m720 * np.sqrt(24))
            b["pos"] = np.arange(len(b))
            b["coin"] = coin; b["w"] = w
            rows.append(b[["coin","w","year","hour","r1","fwd1","fwd24","ret24","z1","volratio","z24","z24m","pos"]])
    df = pd.concat(rows, ignore_index=True)
    g24 = df[df.pos % 24 == 0].dropna(subset=["fwd24"])
    drift24 = g24.groupby("coin")["fwd24"].mean()
    drift1 = df.groupby("coin")["fwd1"].mean()
    df["ex1"] = df["fwd1"] - df["coin"].map(drift1)
    df["ex24"] = df["fwd24"] - df["coin"].map(drift24)
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean_bp": x.mean()*1e4, "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    g = df[df.pos % 24 == 0].dropna(subset=["ex24","z1","volratio","z24m"]).copy()
    # volratio quintile x 24h scaled-return tercile
    g["vq"] = pd.qcut(g["volratio"], 5, labels=False)
    g["zq"] = pd.qcut(g["z24m"], 5, labels=False)
    out["ex24_mean_bp_vq_x_z24m_q"] = g.pivot_table(index="vq", columns="zq", values="ex24", aggfunc="mean")*1e4
    out["ex24_n_vq_x_z24m_q"] = g.pivot_table(index="vq", columns="zq", values="ex24", aggfunc="count")
    hv = g[g.vq == 4]
    out["highvol_by_coin"] = hv.groupby("coin")["ex24"].apply(tt).unstack()
    out["highvol_by_year"] = hv.groupby("year")["ex24"].apply(tt).unstack()
    # within high vol, graded by volratio deciles of top
    hv2 = g[g.volratio >= g.volratio.quantile(0.8)].copy()
    hv2["vd"] = pd.qcut(hv2["volratio"], 4, labels=False)
    out["highvol_graded"] = hv2.groupby("vd")["ex24"].apply(tt).unstack()
    # correlation of ex24 with -z24m within high vol: slope
    x = hv.dropna(subset=["z24m"])
    out["highvol_corr_ex24_z24m"] = pd.Series({"corr": np.corrcoef(x["z24m"], x["ex24"])[0,1], "n": len(x)})
    # hours 20-21 effect by year and coin
    h = df[df.hour.isin([20, 21])]
    out["h2021_by_year"] = h.groupby("year")["ex1"].apply(tt).unstack()
    out["h2021_by_coin"] = h.groupby("coin")["ex1"].apply(tt).unstack()
    h13 = df[df.hour == 13]
    out["h13_by_year"] = h13.groupby("year")["ex1"].apply(tt).unstack()
    # hour 20-21 graded by volratio
    h = h.dropna(subset=["volratio"]).copy()
    h["vq"] = pd.qcut(h["volratio"], 5, labels=False)
    out["h2021_by_volq"] = h.groupby("vq")["ex1"].apply(tt).unstack()
    # hour 22 with-trend effect by year
    h22 = df[df.hour == 22].dropna(subset=["ret24"]).copy()
    h22["with"] = np.sign(h22["ret24"]) * h22["ex1"]
    out["h22_withtrend_by_year"] = h22.groupby("year")["with"].apply(tt).unstack()
    return out
