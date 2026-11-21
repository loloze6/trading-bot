def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    def cases(h):
        rows = []
        for coin, ws in bars.items():
            tmp = []
            for w, df in ws.items():
                c = df["close"].values; f = df["forecast"].values
                ts = pd.to_datetime(df["timestamp"])
                lr = np.log(df["close"]).diff()
                vol = lr.rolling(30, min_periods=20).std().values
                r60 = df["close"].pct_change(60).values
                for i in range(0, len(df) - h, h):
                    tmp.append((coin, w, ts.iloc[i].year, f[i], c[i+h]/c[i]-1, vol[i], r60[i]))
            d = pd.DataFrame(tmp, columns=["coin","w","year","f","r","vol","r60"])
            d["drift"] = d["r"].mean()
            d["volrank"] = d["vol"].rank(pct=True)
            rows.append(d)
        d = pd.concat(rows, ignore_index=True)
        d["u"] = np.sign(d["f"]) * (d["r"] - d["drift"])
        d["m"] = d["f"]/10 * (d["r"] - d["drift"])
        return d
    def summ(g):
        g = g.dropna(subset=["u"])
        g = g[g["f"] != 0]
        n = len(g)
        if n < 3: return pd.Series({"n": n})
        return pd.Series({"n": n, "mean_u": g["u"].mean(), "t_u": g["u"].mean()/(g["u"].std()/np.sqrt(n)),
                          "mean_m": g["m"].mean(), "t_m": g["m"].mean()/(g["m"].std()/np.sqrt(n))})
    hz = {}
    for h in [5, 10, 20, 40, 60]:
        d = cases(h)
        hz[h] = summ(d)
        if h == 20: d20 = d
    out["by_horizon"] = pd.DataFrame(hz).T
    d = d20[d20["f"] != 0].copy()
    d["side"] = np.where(d["f"] > 0, "long", "short")
    out["by_side"] = d.groupby("side").apply(summ)
    d["fq"] = pd.qcut(d["f"].abs(), 5, labels=False)
    out["by_absf_quintile"] = d.groupby("fq").apply(summ)
    d["fq_signed"] = pd.qcut(d["f"], 6, labels=False)
    out["by_signed_f_sextile"] = d.groupby("fq_signed").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    out["by_coin"] = d.groupby("coin").apply(summ)
    d["vt"] = pd.cut(d["volrank"], [0, 1/3, 2/3, 1], labels=["lowvol","midvol","highvol"])
    out["by_vol_tercile"] = d.groupby("vt").apply(summ)
    out["by_vol_side"] = d.groupby(["vt","side"]).apply(summ)
    return out
