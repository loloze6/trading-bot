def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    def tstat(x):
        x = np.asarray(x, float); x = x[~np.isnan(x)]
        if len(x) < 3: return np.nan
        return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
    rows = []
    for h in [1, 5, 10, 20, 30]:
        for coin, wins in bars.items():
            # coin mean return over h, all windows
            allr = []
            cells = []
            for w, df in wins.items():
                c = df["close"].values; f = df["forecast"].values
                vol = pd.Series(c).pct_change().rolling(30).std().values
                ts = pd.to_datetime(df["timestamp"])
                for i in range(0, len(c) - h, h):
                    r = c[i + h] / c[i] - 1
                    allr.append(r)
                    cells.append((w, ts.iloc[i].year, f[i], r, vol[i]))
            mu = np.mean(allr) if allr else np.nan
            for (w, y, f, r, v) in cells:
                rows.append(dict(h=h, coin=coin, w=w, year=y, f=f, r=r, ex=r - mu, vol=v))
    D = pd.DataFrame(rows)
    D["g"] = D["f"] / 10 * D["ex"]
    D = D[D["f"] != 0]
    out["by_horizon"] = D.groupby("h")["g"].agg(["mean", "count", tstat])
    D5 = D[D.h == 5].copy()
    out["h5_by_coin"] = D5.groupby("coin")["g"].agg(["mean", "count", tstat])
    out["h5_by_year"] = D5.groupby("year")["g"].agg(["mean", "count", tstat])
    out["h5_by_side"] = D5.groupby(np.sign(D5["f"]))["g"].agg(["mean", "count", tstat])
    D5["absq"] = pd.qcut(D5["f"].abs(), 5, labels=False)
    out["h5_by_absf_quint"] = D5.groupby("absq")["g"].agg(["mean", "count", tstat])
    D5["volq"] = D5.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["h5_by_vol_tercile"] = D5.groupby("volq")["g"].agg(["mean", "count", tstat])
    out["corr_f_ex_by_h"] = D.groupby("h").apply(lambda g: pd.Series({"rho": stats.spearmanr(g.f, g.ex)[0], "n": len(g)}))
    # plain volatility signal: -vol z vs future ex, h=5
    D5["vz"] = D5.groupby("coin")["vol"].transform(lambda s: (s - s.mean()) / s.std())
    D5["gv"] = -D5["vz"] * D5["ex"]
    out["plain_lowvol_signal_h5_by_coin"] = D5.groupby("coin")["gv"].agg(["mean", "count", tstat])
    out["plain_lowvol_signal_h5_by_year"] = D5.groupby("year")["gv"].agg(["mean", "count", tstat])
    return out
