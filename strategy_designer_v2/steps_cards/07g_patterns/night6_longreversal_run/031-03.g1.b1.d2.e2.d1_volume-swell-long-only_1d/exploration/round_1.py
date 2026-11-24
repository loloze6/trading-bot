import numpy as np, pandas as pd

def explore(data):
    H = 14
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            vr = v.rolling(14, min_periods=14).mean() / v.rolling(30, min_periods=30).mean() - 1
            ret60 = c / c.shift(60) - 1
            ret28 = c / c.shift(28) - 1
            ret14 = c / c.shift(14) - 1
            vol20 = r1.rolling(20, min_periods=15).std()
            ma50 = c.rolling(50, min_periods=40).mean()
            dist = c / ma50 - 1
            fwd = c.shift(-H) / c - 1
            idx = np.arange(0, len(b), H)
            for i in idx:
                if i + H < len(b):
                    rows.append(dict(coin=coin, win=w, ts=b["timestamp"].iloc[i],
                                     fwd=fwd.iloc[i], fc=b["forecast"].iloc[i], vr=vr.iloc[i],
                                     ret60=ret60.iloc[i], ret28=ret28.iloc[i], ret14=ret14.iloc[i],
                                     vol20=vol20.iloc[i], dist=dist.iloc[i],
                                     vol60z=ret60.iloc[i] / (vol20.iloc[i] * np.sqrt(60)) if vol20.iloc[i] > 0 else np.nan))
            z = r1 / vol20.shift(1)
            nxt = r1.shift(-1)
            d = pd.DataFrame(dict(coin=coin, ts=b["timestamp"], z=z, nxt=nxt, r=r1,
                                  wd=pd.to_datetime(b["timestamp"]).dt.weekday,
                                  yr=pd.to_datetime(b["timestamp"]).dt.year))
            daily.append(d)
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby("coin")["fwd"].transform("mean")
    g["ex"] = g["fwd"] - g["drift"]
    g["day"] = pd.to_datetime(g["ts"]).dt.floor("D")
    g["yr"] = pd.to_datetime(g["ts"]).dt.year

    def summ(df, col):
        out = []
        for k, s in df.groupby(col, observed=True):
            s = s.dropna(subset=["ex"])
            ds = s.groupby("day")["ex"].sum()
            D = len(ds)
            t = ds.sum() / np.sqrt((ds ** 2).sum() * D / max(D - 1, 1)) if D > 1 else np.nan
            out.append(dict(bucket=str(k), n=len(s), days=D, mean_ex=s["ex"].mean(), mean_fwd=s["fwd"].mean(), t=t))
        return pd.DataFrame(out)

    res = {}
    for col in ["vr", "ret60", "vol60z", "ret28", "ret14", "vol20", "dist"]:
        sub = g.dropna(subset=[col]).copy()
        sub["q"] = pd.qcut(sub[col], 5, labels=False, duplicates="drop")
        res["q5_" + col] = summ(sub, "q")
    pos = g[g["fc"] > 0].copy()
    pos["q"] = pd.qcut(pos["fc"], 4, labels=False, duplicates="drop")
    res["fc_pos_q4"] = summ(pos, "q")
    res["fc_zero"] = summ(g[g["fc"] <= 0].assign(k="zero"), "k")
    res["by_year"] = summ(g, "yr")
    # interaction: vr high vs ret60 sign
    sub = g.dropna(subset=["vr", "ret60"]).copy()
    sub["k"] = (sub["vr"] > sub["vr"].median()).map({True: "vrHi", False: "vrLo"}) + "_" + (sub["ret60"] > 0).map({True: "up60", False: "dn60"})
    res["vr_x_ret60"] = summ(sub, "k")
    dd = pd.concat(daily).dropna(subset=["z", "nxt"])
    dd["zq"] = pd.cut(dd["z"], [-99, -3, -2, -1, 0, 1, 2, 3, 99])
    a = dd.groupby("zq", observed=True)["nxt"].agg(["count", "mean", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    res["nextday_after_z"] = a
    b = dd.groupby("wd")["r"].agg(["count", "mean", "std"]); b["t"] = b["mean"] / (b["std"] / np.sqrt(b["count"]))
    res["weekday_ret"] = b
    return res
