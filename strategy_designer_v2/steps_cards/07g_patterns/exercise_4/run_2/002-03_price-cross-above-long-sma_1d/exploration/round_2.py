def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        cr = pd.concat([data["days"][coin][w]["coin_return"] for w in wins]).dropna()
        mu = cr.mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(df)
            ts = pd.to_datetime(df["timestamp"])
            dist = df.get("debug_info.components.above_ma.last_history_value")
            dist = dist.values if dist is not None else np.full(n, np.nan)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vol = pd.Series(r1).rolling(20).std().shift(1).values
            for i in range(21, n - 3):
                rows.append(dict(coin=coin, w=w, yr=ts.iloc[i].year, wd=ts.iloc[i].weekday(),
                                 prev=r1[i], z=r1[i] / vol[i] if vol[i] > 0 else np.nan,
                                 f1=c[i+1]/c[i]-1-mu, f3=c[i+3]/c[i]-1-3*mu,
                                 above=dist[i] > 0 if not np.isnan(dist[i]) else np.nan,
                                 grid3=(i % 3 == 0)))
    D = pd.DataFrame(rows).dropna(subset=["z"])
    out = {}
    def tab(g, col="f1"):
        a = g[col].agg(["size", "mean", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["size"]))
        a["hit"] = g[col].apply(lambda x: (x > 0).mean())
        return a.drop(columns="std")
    D["zq"] = pd.qcut(D["z"], 10, labels=False)
    out["f1_by_zdecile"] = tab(D.groupby("zq"))
    G = D[D["grid3"]]
    out["f3_by_zdecile_grid"] = tab(G.groupby("zq"), "f3")
    out["slope_f1_on_z"] = pd.Series(stats.linregress(D["z"].clip(-5,5), D["f1"])[:4],
                                     index=["slope","int","r","p"])
    D["low"] = D["zq"] <= 1
    out["lowz_by_coin"] = tab(D[D["low"]].groupby("coin"))
    out["lowz_by_year"] = tab(D[D["low"]].groupby("yr"))
    out["lowz_by_above"] = tab(D[D["low"]].dropna(subset=["above"]).groupby("above"))
    out["topz_by_above"] = tab(D[D["zq"] >= 8].dropna(subset=["above"]).groupby("above"))
    # weekday robustness
    out["fri_by_year"] = tab(D[D["wd"] == 4].groupby("yr"))
    out["wed_by_year"] = tab(D[D["wd"] == 2].groupby("yr"))
    out["fri_by_coin"] = tab(D[D["wd"] == 4].groupby("coin"))
    # weekday controlling for prior move: weekday means among non-extreme prev
    mid = D[(D["zq"] >= 2) & (D["zq"] <= 7)]
    out["weekday_mid_moves"] = tab(mid.groupby("wd"))
    # is low-z drop concentrated on a weekday?
    out["lowz_share_by_wd"] = D.groupby("wd")["low"].mean()
    return out
