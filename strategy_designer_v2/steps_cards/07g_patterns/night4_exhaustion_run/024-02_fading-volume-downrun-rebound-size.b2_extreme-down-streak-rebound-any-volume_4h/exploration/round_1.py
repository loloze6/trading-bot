def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        recs = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            mad = r1.abs().rolling(180, min_periods=45).mean()
            sd = r1.rolling(180, min_periods=45).std()
            past6 = c / c.shift(6) - 1
            past18 = c / c.shift(18) - 1
            past42 = c / c.shift(42) - 1
            # signed streak sum
            sgn = np.sign(r1.fillna(0)).values
            st = np.zeros(len(b)); ln = np.zeros(len(b))
            for i in range(1, len(b)):
                if sgn[i] != 0 and sgn[i] == sgn[i-1]:
                    st[i] = st[i-1] + r1.iloc[i]; ln[i] = ln[i-1] + 1
                elif sgn[i] != 0:
                    st[i] = r1.iloc[i]; ln[i] = 1
            volr = v.rolling(6).mean() / v.rolling(180, min_periods=45).mean()
            volsl = v.rolling(3).mean() / v.shift(3).rolling(3).mean()
            vollvl = sd / sd.rolling(540, min_periods=90).median()
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "fwd": fwd,
                "z6": past6 / (sd * np.sqrt(6)), "z18": past18 / (sd * np.sqrt(18)),
                "z42": past42 / (sd * np.sqrt(42)),
                "streak": st / mad, "len": ln * np.sign(st), "volr": volr, "volsl": volsl,
                "vollvl": vollvl, "fc": b["forecast"].astype(float),
                "hour": ts.dt.hour, "wd": ts.dt.weekday, "year": ts.dt.year,
            })
            df = df.iloc[::H]
            recs.append(df)
        d = pd.concat(recs)
        d = d.dropna(subset=["fwd"])
        usual = d["fwd"].std(); drift = d["fwd"].mean()
        d["u"] = (d["fwd"] - drift) / usual
        rows.append(d)
    D = pd.concat(rows)

    def tab(col, q=5, cond=None):
        x = D if cond is None else D[cond]
        x = x.dropna(subset=[col, "u"])
        g = pd.qcut(x[col].rank(method="first"), q, labels=False)
        o = x.groupby(g)["u"].agg(["mean", "count", "std"])
        o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
        o["xmean"] = x.groupby(g)[col].mean()
        return o[["xmean", "mean", "t", "count"]].round(4)

    out = {}
    out["z6 quintiles"] = tab("z6")
    out["z18 quintiles"] = tab("z18")
    out["z42 quintiles"] = tab("z42")
    out["streak quintiles nonzero"] = tab("streak", 5, D["streak"].abs() > 0)
    out["volr quintiles"] = tab("volr")
    out["vollvl quintiles"] = tab("vollvl")
    def grp(col):
        o = D.groupby(col)["u"].agg(["mean", "count", "std"])
        o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
        return o[["mean", "t", "count"]].round(4)
    out["by hour"] = grp("hour"); out["by weekday"] = grp("wd"); out["by year"] = grp("year")
    out["by coin"] = grp("coin")
    # z18 slope per coin
    sl = []
    for coin, x in D.dropna(subset=["z18", "u"]).groupby("coin"):
        r = stats.linregress(x["z18"], x["u"]); sl.append([coin, r.slope, r.slope / r.stderr, len(x)])
    out["z18 slope by coin"] = pd.DataFrame(sl, columns=["coin", "slope", "t", "n"]).round(4)
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin, win=w))
    Dd = pd.concat(dd)
    Dd["wd"] = pd.to_datetime(Dd["day"]).dt.weekday
    o = Dd.groupby("wd")[["book_return", "coin_return"]].mean() * 100
    out["book by weekday %"] = o.round(4)
    return out
