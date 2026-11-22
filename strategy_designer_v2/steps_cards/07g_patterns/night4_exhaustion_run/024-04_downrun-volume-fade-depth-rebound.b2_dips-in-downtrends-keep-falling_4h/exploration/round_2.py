import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        grids = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            v = b["volume"].astype(float).values
            n = len(c)
            ts = pd.to_datetime(b["timestamp"])
            vs = pd.Series(v)
            v6 = vs.rolling(6).mean().values
            v180 = vs.rolling(180, min_periods=90).mean().values
            v36 = vs.rolling(36).mean().values
            v18 = vs.rolling(18).mean().values
            # same-weekday-hour baseline: mean of the volume 42 bars apart (7 days), last 4 weeks
            lagged = np.nanmean(np.vstack([np.r_[np.full(42*k, np.nan), v[:-42*k]] if n > 42*k else np.full(n, np.nan) for k in range(1, 5)]), axis=0)
            v6_same = pd.Series(lagged).rolling(6).mean().values
            ret1d = np.full(n, np.nan); ret1d[6:] = c[6:] / c[:-6] - 1
            ret3d = np.full(n, np.nan); ret3d[18:] = c[18:] / c[:-18] - 1
            for t in range(0, n - H, H):
                grids.append(dict(coin=coin, w=w, year=ts.iloc[t].year, wd=ts.iloc[t].weekday(),
                                  fwd=c[t+H]/c[t]-1, fwd1=c[min(t+6, n-1)]/c[t]-1,
                                  vr6=v6[t]/v180[t], vr18=v18[t]/v180[t], vr36=v36[t]/v180[t],
                                  vr_same=v6[t]/v6_same[t], ret1d=ret1d[t], ret3d=ret3d[t]))
        g = pd.DataFrame(grids)
        g["s"] = (g["fwd"] - g["fwd"].mean()) / g["fwd"].std()
        g["s1"] = (g["fwd1"] - g["fwd1"].mean()) / g["fwd1"].std()
        g["usual"] = g["fwd"].std()
        g["ret3d_z"] = g["ret3d"] / g["usual"]
        for col in ["vr6", "vr18", "vr36", "vr_same"]:
            g["l" + col] = np.log(g[col].replace([np.inf, 0], np.nan))
        rows.append(g)
    G = pd.concat(rows, ignore_index=True).replace([np.inf, -np.inf], np.nan)
    out = {}
    def slope(col, d, y="s", by="coin"):
        d = d.dropna(subset=[col, y])
        res = []
        for k, x in list(d.groupby(by)) + [("ALL", d)]:
            if len(x) < 20: continue
            lr = stats.linregress(x[col], x[y])
            res.append(dict(key=k, n=len(x), slope=lr.slope, t=lr.slope / lr.stderr))
        return pd.DataFrame(res).set_index("key").round(4)
    out["lvr6_by_coin"] = slope("lvr6", G)
    out["lvr6_by_year"] = slope("lvr6", G, by="year")
    out["lvr6_by_weekday"] = slope("lvr6", G, by="wd")
    out["lvr18_by_coin"] = slope("lvr18", G)
    out["lvr36_by_coin"] = slope("lvr36", G)
    out["lvr_same_by_coin"] = slope("lvr_same", G)
    out["lvr6_1day_ahead"] = slope("lvr6", G, y="s1")
    out["lvr6_after_up3d"] = slope("lvr6", G[G["ret3d"] > 0])
    out["lvr6_after_down3d"] = slope("lvr6", G[G["ret3d"] <= 0])
    # interaction: signed: vr * sign of 3d move
    G["lvr6_x_dir"] = G["lvr6"] * np.sign(G["ret3d"])
    out["lvr6_x_dir"] = slope("lvr6_x_dir", G)
    # multiple regression: s on lvr6 + weekday dummies + ret3d_z
    d = G.dropna(subset=["lvr6", "s", "ret3d_z"])
    X = pd.get_dummies(d["wd"], prefix="wd", drop_first=True).astype(float)
    X["lvr6"] = d["lvr6"]; X["ret3d_z"] = d["ret3d_z"]; X["const"] = 1.0
    beta, *_ = np.linalg.lstsq(X.values, d["s"].values, rcond=None)
    resid = d["s"].values - X.values @ beta
    s2 = resid @ resid / (len(d) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.values.T @ X.values)))
    out["multireg"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=X.columns).round(4)
    # Sunday effect by coin and year
    G["sun"] = (G["wd"] == 6).astype(float)
    sw = []
    for k, x in list(G.groupby("coin")) + list(G.groupby("year")):
        a = x.loc[x["sun"] == 1, "s"]; b_ = x.loc[x["sun"] == 0, "s"]
        tt = stats.ttest_ind(a, b_, equal_var=False)
        sw.append(dict(key=k, n_sun=len(a), diff=a.mean() - b_.mean(), t=tt.statistic))
    out["sunday_minus_rest"] = pd.DataFrame(sw).set_index("key").round(4)
    out["vr6_mean_by_weekday"] = G.groupby("wd")["vr6"].mean().round(4)
    # windows with positive lvr6 slope share
    ws = G.dropna(subset=["lvr6", "s"]).groupby("w").apply(lambda x: stats.linregress(x["lvr6"], x["s"]).slope)
    out["share_windows_pos_slope"] = float((ws > 0).mean())
    out["n_windows"] = int(len(ws))
    return out
