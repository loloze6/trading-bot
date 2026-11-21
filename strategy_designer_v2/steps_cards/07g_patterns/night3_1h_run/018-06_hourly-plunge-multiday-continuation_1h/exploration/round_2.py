import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        fw = {}
        for h in (12, 24, 48, 72):
            allr = []
            for w, df in wins.items():
                c = df["close"].values.astype(float)
                idx = np.arange(0, len(c) - h, h)
                allr.append(c[idx + h] / c[idx] - 1)
            allr = np.concatenate(allr)
            fw[h] = (allr.mean(), allr.std(ddof=1))
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            z = r24 / r24.abs().rolling(720, min_periods=120).mean().shift(1)
            n = len(c)
            for h in (12, 24, 48, 72):
                idx = np.arange(0, n - h, h)
                fr = c.values[idx + h] / c.values[idx] - 1
                rows.append(pd.DataFrame({"coin": coin, "win": w, "h": h, "z": z.values[idx],
                                          "year": ts.dt.year.values[idx], "hour": ts.dt.hour.values[idx],
                                          "tot_bps": fr * 1e4, "unus_bps": (fr - fw[h][0]) * 1e4,
                                          "s": (fr - fw[h][0]) / fw[h][1]}))
    D = pd.concat(rows).dropna(subset=["s", "z"])
    out = {}
    def agg(g):
        return pd.Series({"n": len(g), "tot_bps": g["tot_bps"].mean(), "unus_bps": g["unus_bps"].mean(),
                          "s": g["s"].mean(), "t": g["s"].mean() / (g["s"].std() / np.sqrt(len(g)))})
    D["zb"] = pd.cut(D["z"], [-np.inf, -3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 3, np.inf])
    out["z_bins_by_h"] = D.groupby(["h", "zb"], observed=True).apply(agg).reset_index()
    d24 = D[D.h == 24]
    neg = d24[d24.z < -1]
    out["drop_gt1_by_coin"] = neg.groupby("coin").apply(agg)
    out["drop_gt1_by_year"] = neg.groupby("year").apply(agg)
    out["drop_gt1_wins_pos_share"] = pd.Series({"wins": neg.groupby(["coin", "win"])["s"].mean().shape[0],
                                                "share_pos": (neg.groupby(["coin", "win"])["s"].mean() > 0).mean()})
    rho = []
    for h in (12, 24, 48, 72):
        g = D[(D.h == h) & (D.z < 0)]
        r, p = stats.spearmanr(-g["z"], g["s"])
        rho.append({"h": h, "n": len(g), "rho_dropsize_vs_s": r, "p": p})
    out["spearman_downside"] = pd.DataFrame(rho)
    # book by year
    days = data["days"]
    bk = []
    for coin, wins in days.items():
        for w, df in wins.items():
            bk.append(pd.DataFrame({"year": pd.to_datetime(df["day"]).dt.year, "b": df["book_return"], "c": df["coin_return"]}))
    B = pd.concat(bk).dropna()
    out["book_by_year_bps"] = (B.groupby("year")[["b", "c"]].mean() * 1e4).round(2)
    return out
