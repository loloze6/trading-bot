def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    FC = "forecast"
    # grid cases at several horizons
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; f = df[FC].values
            n = len(df)
            r1 = pd.Series(c).pct_change().values
            ret20 = pd.Series(c).pct_change(20).values
            vol20 = pd.Series(r1).rolling(20).std().values
            for h in (5, 10, 20):
                for i in range(0, n - h, h):
                    rows.append((coin, w, h, f[i], c[i+h]/c[i]-1, ret20[i], vol20[i]))
    g = pd.DataFrame(rows, columns=["coin","w","h","f","r","ret20","vol20"])
    drift = g.groupby(["coin","h"])["r"].transform("mean")
    sd = g.groupby(["coin","h"])["r"].transform("std")
    g["s"] = np.sign(g["f"])
    g["unus"] = g["s"]*(g["r"]-drift)
    g["tot"] = g["s"]*g["r"]
    g["strength"] = g["unus"]/sd
    a = g[g["f"]!=0].copy()
    a["fq"] = a.groupby("h")["f"].transform(lambda x: pd.qcut(x.abs(), 5, labels=False, duplicates="drop"))
    def summ(x):
        return pd.Series({"n": len(x), "unus%": 100*x["unus"].mean(), "tot%": 100*x["tot"].mean(),
                          "t": stats.ttest_1samp(x["unus"], 0).statistic if len(x)>2 else np.nan,
                          "str": x["strength"].mean(), "absf": x["f"].abs().mean()})
    out["by_h_absf_quintile"] = a.groupby(["h","fq"]).apply(summ)
    out["by_h_side"] = a.groupby(["h","s"]).apply(summ)
    a["trend"] = np.sign(a["ret20"])
    out["h5_side_trend"] = a[a.h==5].groupby(["s","trend"]).apply(summ)
    a["vq"] = a.groupby("h")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["h5_volq"] = a[a.h==5].groupby(["vq"]).apply(summ)
    out["h20_volq"] = a[a.h==20].groupby(["vq"]).apply(summ)
    # book: daily per window, mean across coins
    bk = []
    for coin, ws in days.items():
        for w, d in ws.items():
            d = d.copy(); d["coin"]=coin; d["w"]=w; bk.append(d)
    bk = pd.concat(bk)
    br = bk.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book_by_window"] = br.groupby(level=0).agg(["mean","count"]).sort_values(("book_return","mean")).head(10)
    # gains split by side and fees
    rows=[]
    for coin, ws in bars.items():
        for w, df in ws.items():
            al = df["postRebalance_current_allocation"].values
            c = df["close"].values
            r = np.r_[c[1:]/c[:-1]-1, np.nan]
            fee = (df["total_portfolio_value"]-df["postRebalance_total_value"]).values/df["total_portfolio_value"].values
            for i in range(len(df)):
                rows.append((np.sign(al[i]), al[i]*r[i] if not np.isnan(r[i]) else np.nan, fee[i], abs(al[i])))
    p = pd.DataFrame(rows, columns=["side","gain","fee","absal"])
    out["bar_gain_by_side"] = p.groupby("side").agg(n=("gain","size"), gain_mean=("gain","mean"), fee_mean=("fee","mean"), absal=("absal","mean"))
    out["overall_fee_vs_gain"] = pd.Series({"gain_mean": p["gain"].mean(), "fee_mean": p["fee"].mean()})
    return out
