def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = (6, 18, 36, 72)
    rows = []
    for coin, wins in bars.items():
        per_h = {}
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            rs = np.array(rs)
            per_h[h] = (rs.mean(), rs.std())
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; hi = df["high"]; lo = df["low"]
            r1 = np.log(c).diff()
            vol42 = r1.rolling(42).std()
            minl12 = lo.shift(1).rolling(12).min()
            maxh12 = hi.shift(1).rolling(12).max()
            depth = (minl12 / c - 1) / vol42          # how far below the 2-day low, in bar vols
            dn = (c < minl12)
            ret6z = (c / c.shift(6) - 1) / (vol42 * np.sqrt(6))
            ret42z = (c / c.shift(42) - 1) / (vol42 * np.sqrt(42))
            vol_rel = vol42 / vol42.rolling(360, min_periods=120).median()
            ts = pd.to_datetime(df["timestamp"])
            for h in H:
                d, u = per_h[h]
                idx = np.arange(0, len(c) - h, h)
                fwd = c.values[idx + h] / c.values[idx] - 1
                rows.append(pd.DataFrame({
                    "coin": coin, "w": w, "h": h, "fwd": fwd, "unus": fwd - d,
                    "str": (fwd - d) / u, "dn": dn.values[idx], "depth": depth.values[idx],
                    "ret6z": ret6z.values[idx], "ret42z": ret42z.values[idx],
                    "vol_rel": vol_rel.values[idx], "year": ts.dt.year.values[idx],
                    "wd": ts.dt.weekday.values[idx], "hr": ts.dt.hour.values[idx]}))
    A = pd.concat(rows, ignore_index=True)

    def summ(g, val="str"):
        o = g[val].agg(["mean", "std", "count"])
        o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
        return o.drop(columns="std").round(4)

    out = {}
    # breakdown: by horizon, with total and unusual move in %
    B = A[A.dn == True]
    o = B.groupby("h").agg(str=("str", "mean"), unus=("unus", "mean"), fwd=("fwd", "mean"), n=("str", "count"),
                           sd=("str", "std"))
    o["t"] = o["str"] / (o["sd"] / np.sqrt(o["n"]))
    out["dn_by_h"] = o.drop(columns="sd").round(4)
    B18 = B[B.h == 18]
    out["dn18_by_year"] = summ(B18.groupby("year"))
    cc = B18.groupby("coin")["str"].mean()
    out["dn18_coins_pos_share"] = float((cc > 0).mean())
    out["dn18_coins_n"] = int(len(cc))
    # graded: depth terciles within breakdowns
    d = B18.dropna(subset=["depth"]).copy()
    d["q"] = pd.qcut(d["depth"].rank(method="first"), 3, labels=False)
    out["dn18_by_depth_tercile"] = summ(d.groupby("q"))
    # graded over all bars: 1-day return z quintiles, by horizon 6/18/36
    for h in (6, 18, 36):
        D = A[A.h == h].dropna(subset=["ret6z"]).copy()
        D["q"] = D.groupby("coin")["ret6z"].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
        out[f"h{h}_ret6z_decile"] = summ(D.groupby("q"))
    # 1-day fall bottom decile by year (h18) and in high vs low vol
    D = A[A.h == 18].dropna(subset=["ret6z", "vol_rel"]).copy()
    D["q"] = D.groupby("coin")["ret6z"].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
    D["vh"] = D.groupby("coin")["vol_rel"].transform(lambda s: s > s.median())
    low = D[D.q == 0]
    out["h18_fall_decile_by_year"] = summ(low.groupby("year"))
    out["h18_fall_decile_by_vol_half"] = summ(low.groupby("vh"))
    # slope of str on ret6z among negative ret6z (h18)
    neg = D[D.ret6z < 0]
    x = neg["ret6z"].values; y = neg["str"].values
    b = np.polyfit(x, y, 1)[0]
    res = y - np.polyval(np.polyfit(x, y, 1), x)
    se = np.sqrt((res ** 2).sum() / (len(x) - 2) / ((x - x.mean()) ** 2).sum())
    out["h18_slope_on_negative_ret6z"] = pd.Series({"slope": b, "t": b / se, "n": len(x)}).round(4)
    # Sunday effect by year
    S = A[(A.h == 18)]
    out["h18_sunday_by_year"] = summ(S[S.wd == 6].groupby("year"))
    # 7-day strength top quintile by year (h72)
    D72 = A[A.h == 72].dropna(subset=["ret42z"]).copy()
    D72["q"] = D72.groupby("coin")["ret42z"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["h72_top7d_by_year"] = summ(D72[D72.q == 4].groupby("year"))
    return out
