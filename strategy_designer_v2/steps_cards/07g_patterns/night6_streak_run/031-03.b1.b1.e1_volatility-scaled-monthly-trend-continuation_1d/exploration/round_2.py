def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            r1 = pd.Series(c).pct_change().values
            vol60 = pd.Series(r1).rolling(60, min_periods=20).std().shift(0).values
            ts = pd.to_datetime(b["timestamp"])
            raw = b.get("debug_info.components.vol_scaled_mom.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            alloc = b["postRebalance_current_allocation"].values
            for i in range(1, n):
                volp = vol60[i-1] if i-1 >= 0 else np.nan
                rows.append(dict(coin=coin, w=w, i=i, day=ts[i].normalize(), wd=ts[i].dayofweek, yr=ts[i].year,
                                 z=r1[i]/volp if volp and volp > 0 else np.nan,
                                 n1=c[i+1]/c[i]-1 if i+1 < n else np.nan,
                                 n3=c[i+3]/c[i]-1 if (i+3 < n and i % 3 == 0) else np.nan,
                                 n5=c[i+5]/c[i]-1 if (i+5 < n and i % 5 == 0) else np.nan,
                                 vol=vol60[i], raw=raw[i], alloc=alloc[i]))
    d = pd.DataFrame(rows)
    for h in ["n1", "n3", "n5"]:
        d["x" + h] = d[h] - d.groupby("coin")[h].transform("mean")

    def ct(df, col):
        dd = df.dropna(subset=[col])
        if len(dd) < 3: return (len(dd), np.nan, np.nan, 0)
        m = dd[col].mean()
        per = (dd[col] - m).groupby(dd["day"]).sum()
        se = np.sqrt((per**2).sum()) / len(dd)
        return (len(dd), m, m/se if se > 0 else np.nan, dd["day"].nunique())

    def table(df, key, cols):
        out = []
        for k, g in df.groupby(key, observed=True):
            r = dict(key=str(k))
            for col in cols:
                nn, m, t, days = ct(g, col)
                r[col+"_n"] = nn; r[col+"_mean"] = m; r[col+"_t"] = t
            out.append(r)
        return pd.DataFrame(out)

    res = {}
    d["zb"] = pd.cut(d["z"], [-99, -3, -2, -1, 0, 1, 2, 3, 99])
    res["z bucket -> excess 1/3/5d, day-clustered"] = table(d.dropna(subset=["z"]), "zb", ["xn1", "xn3", "xn5"])
    res["weekday -> excess next day, clustered"] = table(d, "wd", ["xn1"])
    # weekday stability by year: sign of mean for wd 1 and 4
    st = []
    for y, g in d.groupby("yr"):
        r = dict(yr=y)
        for wd in [1, 4, 0, 2]:
            nn, m, t, _ = ct(g[g.wd == wd], "xn1")
            r[f"wd{wd}_mean"] = m; r[f"wd{wd}_t"] = t
        st.append(r)
    res["weekday by year"] = pd.DataFrame(st)
    # large down day stability by year
    dd = d[d.z <= -2]
    res["z<=-2 by year next-day excess"] = table(dd, "yr", ["xn1", "xn3"])
    # by |z| magnitude: does move size scale (absolute, graded)
    d["az"] = d["z"].abs()
    d["azb"] = pd.cut(d["az"], [0, 0.5, 1, 1.5, 2, 3, 99])
    res["|z| bucket -> excess 3d by sign"] = table(d.dropna(subset=["z"]).assign(k=lambda x: x["azb"].astype(str) + np.where(x["z"] < 0, "_dn", "_up")), "k", ["xn3", "xn5"])
    # vol tercile x raw positive slope
    sl = []
    d["vt"] = d.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    g10 = d[(d.i % 10 == 0)].copy()
    return res
