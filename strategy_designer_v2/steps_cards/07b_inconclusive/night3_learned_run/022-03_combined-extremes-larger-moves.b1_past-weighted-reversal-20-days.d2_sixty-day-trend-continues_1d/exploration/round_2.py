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
            d["sd"] = d["r"].std()
            d["volrank"] = d["vol"].rank(pct=True)
            rows.append(d)
        d = pd.concat(rows, ignore_index=True)
        d = d[d["f"] != 0].copy()
        d["u"] = np.sign(d["f"]) * (d["r"] - d["drift"])
        d["tot"] = np.sign(d["f"]) * d["r"]
        d["s"] = d["u"] / d["sd"]
        d["m"] = d["f"]/10 * (d["r"] - d["drift"])
        d["vt"] = pd.cut(d["volrank"], [0, 1/3, 2/3, 1], labels=["lowvol","midvol","highvol"])
        d["side"] = np.where(d["f"] > 0, "long", "short")
        return d
    def summ(g):
        g = g.dropna(subset=["u"])
        n = len(g)
        if n < 3: return pd.Series({"n": n})
        return pd.Series({"n": n, "mean_u": g["u"].mean(), "mean_tot": g["tot"].mean(), "strength": g["s"].mean(),
                          "t_u": g["u"].mean()/(g["u"].std()/np.sqrt(n)),
                          "t_m": g["m"].mean()/(g["m"].std()/np.sqrt(n)),
                          "spear_f_excess": stats.spearmanr(g["f"], g["r"]-g["drift"])[0]})
    for h in [10, 20]:
        d = cases(h)
        out[f"h{h}_all"] = summ(d).to_frame().T
        out[f"h{h}_by_vol"] = d.groupby("vt").apply(summ)
        d["fq"] = pd.qcut(d["f"].abs(), 4, labels=False)
        out[f"h{h}_by_absf_quart"] = d.groupby("fq").apply(summ)
        d["rq"] = pd.qcut(d["r60"].abs(), 4, labels=False)
        out[f"h{h}_by_abs_raw_r60_quart"] = d.groupby("rq").apply(summ)
        dv = d[d["vt"] != "lowvol"]
        out[f"h{h}_notlow_by_absf_quart"] = dv.groupby("fq").apply(summ)
        out[f"h{h}_notlow_by_year"] = dv.groupby("year").apply(summ)
        out[f"h{h}_low_by_year"] = d[d["vt"]=="lowvol"].groupby("year").apply(summ)
    return out
