import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        g = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            d = pd.DataFrame(index=b.index)
            d["coin"] = coin; d["win"] = w
            d["wd"] = ts.dt.weekday; d["year"] = ts.dt.year
            r1 = c.pct_change(); v = r1.rolling(20).std()
            d["z"] = r1 / v
            d["zsat"] = d["z"].shift(1)
            d["z20"] = (c.shift(1) / c.shift(21) - 1) / (v * np.sqrt(20))
            d["vrel"] = v / v.rolling(120, min_periods=40).median()
            vol = b["volume"].astype(float)
            d["volrel"] = np.log(vol / vol.rolling(20).mean().shift(1))
            for h in (1, 2, 3, 5):
                d[f"f{h}"] = c.shift(-h) / c - 1
            d["pos"] = np.arange(len(d))
            g.append(d)
        g = pd.concat(g)
        for h in (1, 2, 3, 5):
            grid = g[g.pos % h == 0][f"f{h}"].dropna()
            g[f"s{h}"] = (g[f"f{h}"] - grid.mean()) / grid.std()
        rows.append(g)
    A = pd.concat(rows)
    out = {}

    def slope(s, x="z", y="s3"):
        s = s.dropna(subset=[x, y])
        if len(s) < 30: return pd.Series({"slope": np.nan, "t": np.nan, "n": len(s)})
        lr = stats.linregress(s[x], s[y])
        return pd.Series({"slope": lr.slope, "t": lr.slope / lr.stderr, "n": len(s)})

    S = A[A.wd == 6].copy()
    out["sun_slope_by_horizon"] = pd.DataFrame({h: slope(S, y=f"s{h}") for h in ("s1", "s2", "s3", "s5")}).T
    out["sun_slope_by_year"] = S.groupby("year").apply(slope).round(4)
    out["sun_slope_by_coin"] = S.groupby("coin").apply(slope).round(4)
    Sc = S.copy(); Sc["zc"] = Sc.z.clip(-2, 2)
    out["sun_slope_clipped_z2"] = str(slope(Sc, x="zc").round(4).to_dict())
    Sm = S[S.z.abs() <= 1.5]
    out["sun_slope_absz_le_1.5"] = str(slope(Sm).round(4).to_dict())
    Sl = S[S.z.abs() > 1.5]
    out["sun_slope_absz_gt_1.5"] = str(slope(Sl).round(4).to_dict())
    S["tq"] = pd.qcut(S.z20, 3, labels=["down20", "mid", "up20"])
    out["sun_slope_by_trend20"] = S.groupby("tq", observed=True).apply(slope)
    S["vq"] = pd.qcut(S.vrel, 3, labels=["calm", "mid", "turbulent"])
    out["sun_slope_by_volregime"] = S.groupby("vq", observed=True).apply(slope)
    S["lq"] = pd.qcut(S.volrel, 3, labels=["lowvolume", "mid", "highvolume"])
    out["sun_slope_by_sunvolume"] = S.groupby("lq", observed=True).apply(slope)
    # multiple regression: sunday z and saturday z
    M = S.dropna(subset=["z", "zsat", "s3"])
    X = np.column_stack([np.ones(len(M)), M.z, M.zsat]); y = M.s3.values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta; s2 = res @ res / (len(y) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["sun_multi_z_zsat"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "z_sun", "z_sat"])
    # Friday continuation check
    Fr = A[A.wd == 4]
    out["fri_slope_by_horizon"] = pd.DataFrame({h: slope(Fr, y=f"s{h}") for h in ("s1", "s2", "s3")}).T
    out["fri_slope_by_year"] = Fr.groupby("year").apply(slope).round(4)
    out["volrel_by_weekday"] = A.groupby("wd").volrel.mean()
    # sunday rise side and fall side bucket means of s3 (sign)
    S["side"] = np.where(S.z > 0, "rise", "fall")
    out["sun_side_mean_s3"] = S.groupby("side").s3.agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(x.count()))])
    return out
