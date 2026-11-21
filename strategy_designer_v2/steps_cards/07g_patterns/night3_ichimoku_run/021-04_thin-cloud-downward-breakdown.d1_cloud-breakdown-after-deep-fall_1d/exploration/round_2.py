import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            df["wd"] = ts.dt.dayofweek; df["year"] = ts.dt.year
            r1 = c.pct_change()
            df["f1"] = c.shift(-1) / c - 1
            df["ret5"] = c / c.shift(5) - 1
            df["ret26"] = c / c.shift(26) - 1
            df["vol20"] = r1.rolling(20).std()
            ten = (hi.rolling(9).max() + lo.rolling(9).min()) / 2
            kij = (hi.rolling(26).max() + lo.rolling(26).min()) / 2
            sa = ((ten + kij) / 2).shift(26)
            sb = ((hi.rolling(52).max() + lo.rolling(52).min()) / 2).shift(26)
            top = np.maximum(sa, sb); bot = np.minimum(sa, sb)
            df["cloud_pos"] = np.where(c > top, 1, np.where(c < bot, -1, 0))
            df.loc[top.isna(), "cloud_pos"] = np.nan
            df["cloud_dist"] = np.where(c > top, c / top - 1, np.where(c < bot, c / bot - 1, 0.0))
            df.loc[top.isna(), "cloud_dist"] = np.nan
            df["f26"] = c.shift(-26) / c - 1
            df["f10"] = c.shift(-10) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)

    # 26-day continuation: size and robustness
    G = D[D["pos"] % 26 == 0].copy()
    G["drift"] = G.groupby("coin")["f26"].transform("mean")
    G["usd"] = G.groupby("coin")["f26"].transform("std")
    G["u"] = G["f26"] - G["drift"]
    res = []
    for feat in ["ret26", "ret5", "cloud_dist"]:
        g = G.dropna(subset=[feat, "u"]).copy()
        g["s"] = np.sign(g[feat])
        g["dir_u"] = g["s"] * g["u"]; g["dir_tot"] = g["s"] * g["f26"]
        g["strength"] = g["dir_u"] / g["usd"]
        t = g["dir_u"].mean() / (g["dir_u"].std() / np.sqrt(len(g)))
        res.append({"feat": feat, "n": len(g), "unusual_mean": g["dir_u"].mean(), "t": t,
                    "total_mean": g["dir_tot"].mean(), "strength": g["strength"].mean(),
                    "up_unusual": g.loc[g.s > 0, "u"].mean(), "n_up": int((g.s > 0).sum()),
                    "down_unusual_shortdir": -g.loc[g.s < 0, "u"].mean(), "n_down": int((g.s < 0).sum())})
    out["sign_bet_26d"] = pd.DataFrame(res)
    g = G.dropna(subset=["ret26", "u"]).copy()
    g["q"] = g.groupby("coin")["ret26"].transform(lambda x: pd.qcut(x, 4, labels=False))
    q = g.groupby("q")["u"].agg(["mean", "std", "count"]); q["t"] = q["mean"] / (q["std"] / np.sqrt(q["count"]))
    out["u26_by_ret26_quartile"] = q
    g["dir_u"] = np.sign(g["ret26"]) * g["u"]
    out["ret26_signbet_by_year"] = g.groupby("year")["dir_u"].agg(["mean", "count"])
    out["ret26_signbet_by_coin"] = g.groupby("coin")["dir_u"].agg(["mean", "count"])
    g2 = G.dropna(subset=["cloud_pos", "u"])
    cp = g2.groupby("cloud_pos")["u"].agg(["mean", "std", "count"]); cp["t"] = cp["mean"] / (cp["std"] / np.sqrt(cp["count"]))
    out["u26_by_cloud_pos"] = cp

    # weekday robustness
    W = D.dropna(subset=["f1"]).copy()
    W["u1"] = W["f1"] - W.groupby("coin")["f1"].transform("mean")
    W["thufri"] = W["wd"].isin([3, 4])
    def tt(x):
        a = x.loc[x.thufri, "u1"]; b = x.loc[~x.thufri, "u1"]
        return pd.Series({"diff": a.mean() - b.mean(), "t": stats.ttest_ind(a, b, equal_var=False).statistic, "n_thufri": len(a)})
    out["thufri_minus_rest_by_coin"] = W.groupby("coin").apply(tt)
    out["thufri_minus_rest_by_year"] = W.groupby("year").apply(tt)
    fr = W.groupby(["coin"]).apply(lambda x: x.loc[x.wd == 4, "u1"].mean())
    out["friday_unusual_by_coin"] = fr
    out["friday_unusual_by_year"] = W[W.wd == 4].groupby("year")["u1"].agg(["mean", "count"])
    # Monday/Wednesday weak?
    out["wd_unusual"] = W.groupby("wd")["u1"].agg(["mean", "count"])
    return out
