def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(df)
            r60 = pd.Series(c).pct_change(60).values
            for h in [3, 7]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=yr[i], f=f[i],
                                     r=c[i + h] / c[i] - 1, r60=r60[i]))
    R = pd.DataFrame(rows)
    R["rd"] = R["r"] - R.groupby(["coin", "h"])["r"].transform("mean")
    R = R[R["f"] != 0].dropna(subset=["f", "rd"])

    def reg(d):
        if len(d) < 8 or d["f"].std() == 0:
            return pd.Series(dict(n=len(d), slope=np.nan, t=np.nan))
        s = stats.linregress(d["f"], d["rd"])
        return pd.Series(dict(n=len(d), slope=s.slope, t=s.slope / s.stderr))

    out = {}
    for h in [3, 7]:
        D = R[R.h == h].copy()
        out[f"coin_h{h}"] = D.groupby("coin").apply(reg)
        out[f"year_h{h}"] = D.groupby("year").apply(reg)
        out[f"sign_h{h}"] = D.groupby(np.sign(D["f"])).apply(reg)
        Dm = D.dropna(subset=["r60"])
        out[f"trend60_h{h}"] = Dm.groupby(np.sign(Dm["r60"])).apply(reg)
        D["q"] = pd.qcut(D["f"], 5, labels=False, duplicates="drop")
        out[f"quint_h{h}"] = D.groupby("q").agg(n=("rd", "size"), fmean=("f", "mean"),
                                                rd_mean=("rd", "mean"),
                                                rd_t=("rd", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    return out
