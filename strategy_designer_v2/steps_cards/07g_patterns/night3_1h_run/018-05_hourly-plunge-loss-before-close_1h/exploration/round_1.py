def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    H = [24, 72, 168]
    rows = []
    hour_rows = []
    for coin, wins in bars.items():
        # coin drift per horizon over all windows (non-overlapping)
        drift = {}; usual = {}
        for h in H:
            allr = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                allr.append(c[idx + h] / c[idx] - 1)
            allr = np.concatenate(allr)
            drift[h] = allr.mean(); usual[h] = allr.std()
        for w, b in wins.items():
            c = b["close"].astype(float)
            r24 = c / c.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=120).mean().shift(1)
            z = r24 / mabs
            rv = np.log(c).diff().rolling(168).std()
            rvq = rv / rv.rolling(720, min_periods=120).median().shift(1)
            r7 = c / c.shift(168) - 1
            m7 = r7.abs().rolling(720, min_periods=120).mean().shift(1)
            z7 = r7 / m7
            ts = pd.to_datetime(b["timestamp"])
            hr = np.log(c).diff()
            hour_rows.append(pd.DataFrame({"hour": ts.dt.hour.values, "wd": ts.dt.weekday.values, "r": hr.values, "coin": coin}))
            cv = c.values
            for h in H:
                idx = np.arange(0, len(cv) - h, h)
                fr = cv[idx + h] / cv[idx] - 1
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "z": z.values[idx], "z7": z7.values[idx],
                                          "rvq": rvq.values[idx], "ex": fr - drift[h], "tot": fr,
                                          "st": (fr - drift[h]) / usual[h]}))
    df = pd.concat(rows).dropna()
    df["zb"] = pd.cut(df["z"], [-99, -3, -2, -1, 0, 1, 2, 3, 99])
    df["z7b"] = pd.cut(df["z7"], [-99, -2, -1, 0, 1, 2, 99])
    def agg(g):
        return pd.Series({"n": len(g), "ex_bps": g.ex.mean() * 1e4, "tot_bps": g.tot.mean() * 1e4,
                          "strength": g.st.mean(), "t": g.ex.mean() / (g.ex.std() / np.sqrt(len(g)))})
    out["z24 bin x horizon"] = df.groupby(["h", "zb"]).apply(agg).reset_index()
    out["z7 bin x horizon"] = df.groupby(["h", "z7b"]).apply(agg).reset_index()
    df["rvb"] = pd.qcut(df["rvq"], 5, labels=False)
    out["vol quintile x horizon"] = df.groupby(["h", "rvb"]).apply(agg).reset_index()
    # correlation of z with forward excess by coin, 72h
    cc = []
    for (coin, h), g in df.groupby(["coin", "h"]):
        r, p = stats.spearmanr(g.z, g.ex); r7, p7 = stats.spearmanr(g.z7, g.ex)
        cc.append({"coin": coin, "h": h, "n": len(g), "rho_z24": r, "rho_z7": r7})
    out["spearman by coin"] = pd.DataFrame(cc)
    hrs = pd.concat(hour_rows).dropna()
    hh = hrs.groupby("hour").r.agg(["mean", "std", "count"])
    hh["t"] = hh["mean"] / (hh["std"] / np.sqrt(hh["count"])); hh["mean_bps"] = hh["mean"] * 1e4
    out["hour"] = hh[["mean_bps", "t", "count"]]
    # book: daily returns, largest losses context
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, w=w))
    dd = pd.concat(dd).dropna(subset=["book_return"])
    out["book by window"] = dd.groupby("w").agg(book=("book_return", "mean"), coin=("coin_return", "mean")).T
    return out
