def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"]
            r = c.pct_change()
            sd24 = r.rolling(24).std()
            vol_avg = sd24.rolling(720, min_periods=200).mean()
            df = pd.DataFrame({"coin": coin, "win": w, "hour": ts.dt.hour, "year": ts.dt.year,
                               "pos_in_win": np.arange(len(b)), "r1": r, "sd": sd24,
                               "vr": sd24 / vol_avg})
            for h in [1, 4, 8, 24]:
                df[f"f{h}"] = c.shift(-h) / c - 1
            for k in [4, 24]:
                df[f"r{k}"] = c / c.shift(k) - 1
            df["z1"] = r / sd24
            df["z4"] = df["r4"] / (sd24 * 2)
            df["z24"] = df["r24"] / (sd24 * np.sqrt(24))
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for h in [1, 4, 8, 24]:
        d[f"a{h}"] = d[f"f{h}"] - d.groupby("coin")[f"f{h}"].transform("mean") * 1.0
    def tstat(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(n)) if n > 1 else np.nan, "n": n})
    out = {}
    # non-overlapping grids: down vs up z1, horizons
    res = []
    for h in [1, 4, 8, 24]:
        g = d[d["pos_in_win"] % h == 0].copy()
        g["zq"] = pd.qcut(g["z1"], 5, labels=False)
        s = g.groupby("zq")[f"a{h}"].apply(tstat).unstack()
        s["h"] = h; res.append(s.reset_index())
    out["z1_quintile_excess_fwd_by_h_nonoverlap"] = pd.concat(res).set_index(["h", "zq"])
    # 24h move z quintile, 24h fwd non-overlap
    for k in ["z4", "z24"]:
        res = []
        for h in [4, 24]:
            g = d[d["pos_in_win"] % h == 0].copy()
            g["q"] = pd.qcut(g[k], 5, labels=False)
            s = g.groupby("q")[f"a{h}"].apply(tstat).unstack(); s["h"] = h; res.append(s.reset_index())
        out[f"{k}_quintile_excess_fwd"] = pd.concat(res).set_index(["h", "q"])
    # down vs up reversal in high vol quintile
    d["vq"] = pd.qcut(d["vr"], 5, labels=False)
    d["side"] = np.where(d["r1"] < 0, "down", "up")
    d["rev"] = -np.sign(d["r1"]) * d["a1"]
    out["rev_by_vq_side"] = d.groupby(["vq", "side"])["rev"].apply(tstat).unstack()
    # slope of excess fwd on z1 within vq (per-unit z)
    out["slope_by_vq"] = d.dropna(subset=["z1", "a1"]).groupby("vq").apply(
        lambda g: pd.Series({"beta_per_z": np.polyfit(g["z1"].clip(-5, 5), g["a1"], 1)[0]}))
    # hour block stability across years
    d["hb"] = pd.cut(d["hour"], [-1, 2, 10, 13, 16, 23], labels=["0-2", "3-10", "11-13", "14-16", "17-23"])
    out["rev_hourblock_by_year_t"] = d.groupby(["year", "hb"])["rev"].apply(
        lambda x: x.mean()/(x.std()/np.sqrt(x.notna().sum()))).unstack()
    # plain hourly mean excess return by hour (drift, not reversal)
    out["excess_ret_by_hour"] = d.groupby("hour")["a1"].apply(tstat).unstack()
    # book daily: largest gains/losses vs coin
    dl = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dl.append(x.assign(coin=coin))
    dd = pd.concat(dl)
    dd["cabs"] = dd["coin_return"].abs()
    dd["cq"] = pd.qcut(dd["cabs"], 5, labels=False)
    out["book_by_coin_absmove_q"] = dd.groupby("cq").agg(book=("book_return", "mean"), coin_abs=("cabs", "mean"), n=("book_return", "count"))
    return out
