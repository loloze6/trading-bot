def explore(data):
    import numpy as np, pandas as pd
    H = 18
    drift = {}; usual = {}
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr.append(c[idx + H] / c[idx] - 1)
        allr = np.concatenate(allr); drift[coin] = allr.mean(); usual[coin] = allr.std()
    def build(off):
        rows = []
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"]; v = b["volume"]; n = len(b)
                fwd = c.shift(-H) / c - 1
                r1d = c / c.shift(6) - 1
                lv = np.log(v.replace(0, np.nan))
                v1d = v.rolling(6).sum()
                vrel1d = v1d / v.rolling(180, min_periods=60).mean() / 6
                vrel = v / v.rolling(180, min_periods=60).mean()
                sdv = np.log(c).diff().rolling(180, min_periods=60).std() * np.sqrt(6)
                idx = np.arange(off, n - H, H)
                df = pd.DataFrame({"coin": coin, "win": w, "fwd": fwd.values[idx], "r1d": r1d.values[idx],
                                   "z1d": (r1d / sdv).values[idx], "vrel": vrel.values[idx], "vrel1d": vrel1d.values[idx],
                                   "flat": (c == c.shift(1)).values[idx], "v0": (v == 0).values[idx],
                                   "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values[idx],
                                   "yr": pd.to_datetime(b["timestamp"]).dt.year.values[idx]})
                df["ex"] = df["fwd"] - drift[coin]
                rows.append(df)
        G = pd.concat(rows).dropna(subset=["fwd", "vrel1d", "z1d"])
        G["qv"] = G.groupby("coin")["vrel1d"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        G["qz"] = G.groupby("coin")["z1d"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
        return G
    def summ(g):
        x = g["ex"].dropna()
        return pd.Series({"n": len(x), "mean_ex%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    for off in [0, 6, 12]:
        G = build(off)
        out[f"off{off}_by_1dvolume_q"] = G.groupby("qv").apply(summ)
        if off == 0:
            out["off0_vol_x_1dmove_tercile"] = G.groupby(["qv", "qz"]).apply(summ).unstack("qz")["mean_ex%"]
            out["off0_vol_x_1dmove_t"] = G.groupby(["qv", "qz"]).apply(summ).unstack("qz")["t"]
            top = G[G["qv"] == 4]
            out["off0_topvol_by_coin"] = top.groupby("coin").apply(summ)
            out["off0_topvol_by_year"] = top.groupby("yr").apply(summ)
            out["off0_flat_bars"] = G.groupby("flat").apply(summ)
            out["off0_zero_volume_share"] = float(G["v0"].mean())
            # graded: signed by 1d move, high vol
            G["sgn_ex"] = np.where(G["r1d"] < 0, G["ex"], -G["ex"])
            hv = G[G["qv"] >= 3]
            out["off0_highvol_reversal_signed"] = pd.Series({"n": len(hv), "mean%": 100*hv.sgn_ex.mean(),
                "t": hv.sgn_ex.mean()/(hv.sgn_ex.std()/np.sqrt(len(hv)))})
            out["off0_corr_ex_vrel1d_spearman"] = float(G["ex"].corr(G["vrel1d"], method="spearman"))
        out[f"off{off}_by_weekday"] = G.groupby("wd").apply(summ)["t"]
    # weekday on daily coin returns (all days)
    D = pd.concat([d.assign(coin=c) for c, ws in data["days"].items() for d in ws.values()]).dropna(subset=["coin_return"])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["daily_coin_by_weekday"] = D.groupby("wd")["coin_return"].agg(lambda x: x.mean()/(x.std()/np.sqrt(len(x))))
    return out
