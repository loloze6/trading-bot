def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [7, 14, 21]
    drift, usual = {}, {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = np.mean(rs) if rs else np.nan
            usual[(coin, h)] = np.std(rs, ddof=1) if len(rs) > 1 else np.nan
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r7 = c / c.shift(7) - 1
            sr = r7 / r7.abs().rolling(30, min_periods=30).mean()
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            reg = df["regime"].values
            for i in range(0, n, 14):
                rec = dict(coin=coin, w=w, year=ts.iloc[i].year, day=ts.iloc[i].normalize(),
                           prof=reg[i] != "chop", act=reg[i] == "trending", sr=sr.iloc[i])
                for h in H:
                    rec[f"r{h}"] = c.iloc[i + h] / c.iloc[i] - 1 if i + h < n else np.nan
                    rec[f"u{h}"] = rec[f"r{h}"] - drift[(coin, h)] if i + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows).dropna(subset=["sr"])
    # same coin-year mean of grid returns (market's own move that year)
    for h in H:
        d[f"y{h}"] = d[f"r{h}"] - d.groupby(["coin", "year"])[f"r{h}"].transform("mean")

    def clus_t(x, col):
        x = x.dropna(subset=[col])
        if len(x) < 3:
            return (len(x), np.nan, np.nan, 0)
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(x)
        return (len(x), m, m / se if se > 0 else np.nan, x["day"].nunique())

    def grp(df, key, col):
        res = []
        for k, x in df.groupby(key):
            n, m, t, nd = clus_t(x, col)
            res.append(dict(key=k, n=n, mean=m, t=t, days=nd))
        return pd.DataFrame(res)

    out = {}
    p = d[d["prof"]].copy()
    out["profile_share_of_grid"] = float(d["prof"].mean())
    p["srbin"] = pd.cut(p["sr"], [-100, -1, 0, 1, 2, 100]).astype(str)
    for col in ["u14", "y14", "y21"]:
        out[f"profile_srbin_{col}"] = grp(p, "srbin", col)
    # slopes of forward move on scaled rise inside profile
    sl = []
    for col in ["u7", "u14", "u21", "y14", "y21"]:
        x = p.dropna(subset=[col])
        b = np.polyfit(x["sr"], x[col], 1)[0]
        cc = np.corrcoef(x["sr"], x[col])[0, 1]
        sl.append(dict(col=col, n=len(x), slope=b, corr=cc, t=cc * np.sqrt((len(x) - 2) / (1 - cc ** 2))))
    out["profile_slopes"] = pd.DataFrame(sl)
    # active cases (sr>=1 in profile) year-demeaned
    a = p[p["sr"] >= 1]
    out["profile_rise_by_year_y14"] = grp(a, "year", "y14")
    out["profile_rise_by_year_u14"] = grp(a, "year", "u14")
    # outside profile, same bins, for comparison
    q = d[~d["prof"]].copy()
    q["srbin"] = pd.cut(q["sr"], [-100, -1, 0, 1, 2, 100]).astype(str)
    out["outside_srbin_y14"] = grp(q, "srbin", "y14")
    return out
