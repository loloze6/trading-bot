def explore(data):
    import numpy as np, pandas as pd
    res = {}
    daily = []
    gridrows = []
    for coin, wins in data["bars"].items():
        fr = {}
        for H in (7, 14, 28):
            xs = []
            for w, b in wins.items():
                c = b["close"].values
                for i in range(0, len(c) - H, H):
                    xs.append(c[i + H] / c[i] - 1)
            fr[H] = (np.mean(xs), np.std(xs, ddof=1))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; v = b["volume"]
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            feats = dict(
                vr14_30=v.rolling(14).mean() / v.rolling(30).mean() - 1,
                vr7_30=v.rolling(7).mean() / v.rolling(30).mean() - 1,
                vr7_60=v.rolling(7).mean() / v.rolling(60).mean() - 1,
                lvr14_60=np.log(v.rolling(14).mean() / v.rolling(60).mean()),
                vol_ratio=r1.rolling(7).std() / r1.rolling(60).std() - 1,
                vol30=vol30,
                ret14=c / c.shift(14) - 1,
                dhi=c / c.rolling(30).max() - 1,
                r1z=r1 / vol30.shift(1),
            )
            for H in (7, 14, 28):
                dr, sd = fr[H]
                for i in range(0, len(c) - H, H):
                    row = dict(coin=coin, H=H, day=ts.iloc[i].normalize(), year=ts.iloc[i].year,
                               fwdz=(c.iloc[i + H] / c.iloc[i] - 1 - dr) / sd)
                    for k, f in feats.items():
                        row[k] = f.iloc[i]
                    gridrows.append(row)
            dd = data["days"][coin][w]
            daily.append(pd.DataFrame(dict(coin=coin, day=ts.dt.normalize(), year=ts.dt.year,
                                           wd=ts.dt.weekday, nxt=r1.shift(-1), z=r1 / vol30.shift(1))))
    g = pd.DataFrame(gridrows)
    d = pd.concat(daily).dropna()

    def slope(df, x, y="fwdz"):
        df = df.dropna(subset=[x, y])
        if len(df) < 30: return pd.Series(dict(b=np.nan, t=np.nan, n=len(df), days=0))
        X = (df[x] - df[x].mean()) / df[x].std()
        e = df[y] - df[y].mean()
        b = (X * e).sum() / (X ** 2).sum()
        res_ = e - b * X
        sc = (X * res_).groupby(df["day"]).sum()
        se = np.sqrt((sc ** 2).sum()) / (X ** 2).sum()
        return pd.Series(dict(b=b, t=b / se, n=len(df), days=df["day"].nunique()))

    feats_l = ["vr14_30", "vr7_30", "vr7_60", "lvr14_60", "vol_ratio", "vol30", "ret14", "dhi"]
    out = {}
    for H in (7, 14, 28):
        s = g[g.H == H]
        for k in feats_l:
            r = slope(s, k); out[(H, k)] = r
    res["slopes_by_H"] = pd.DataFrame(out).T
    s14 = g[g.H == 14].copy()
    # multivariate check: vr14_30 residual after ret14 and dhi
    s = s14.dropna(subset=["vr14_30", "ret14", "dhi", "vol30", "fwdz"]).copy()
    X = s[["ret14", "dhi", "vol30"]].apply(lambda x: (x - x.mean()) / x.std())
    X["c"] = 1
    beta = np.linalg.lstsq(X.values, s["vr14_30"].values, rcond=None)[0]
    s["vr_res"] = s["vr14_30"] - X.values @ beta
    res["vr_resid_slope"] = slope(s, "vr_res")
    res["corr_feats"] = s14[["vr14_30", "vr7_60", "vol_ratio", "ret14", "dhi", "vol30"]].corr()
    # vol30 slope by year
    res["vol30_by_year"] = pd.DataFrame({str(k): slope(x, "vol30") for k, x in s14.groupby("year")}).T
    # daily clustered
    def cl_mean(x):
        m = x["nxt"].mean(); dev = (x["nxt"] - m).groupby(x["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(x)
        return pd.Series(dict(n=len(x), days=x["day"].nunique(), mean=m, t=m / se))
    d["zb"] = pd.cut(d["z"], [-np.inf, -2, -1, 0, 1, 2, np.inf]).astype(str)
    res["nextday_by_z_clustered"] = d.groupby("zb").apply(cl_mean)
    res["weekday_clustered"] = d.groupby("wd").apply(cl_mean)
    res["weekday_by_year_mean"] = d.pivot_table(index="year", columns="wd", values="nxt", aggfunc="mean")
    # per coin daily reversal slope (next-day on z), coin-level
    pc = {}
    for coin, x in d.groupby("coin"):
        b = np.polyfit(x["z"].clip(-5, 5), x["nxt"], 1)[0]
        r = np.corrcoef(x["z"].clip(-5, 5), x["nxt"])[0, 1]
        pc[coin] = dict(b=b, t=r * np.sqrt(len(x) - 2) / np.sqrt(1 - r * r), n=len(x))
    res["nextday_on_z_per_coin"] = pd.DataFrame(pc).T
    return res
