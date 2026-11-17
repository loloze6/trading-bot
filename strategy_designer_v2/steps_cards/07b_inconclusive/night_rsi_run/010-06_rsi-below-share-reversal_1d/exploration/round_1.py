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
            for h in [3, 7, 14, 28]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=yr[i], f=f[i],
                                     r=c[i + h] / c[i] - 1))
    R = pd.DataFrame(rows)
    R["rd"] = R["r"] - R.groupby(["coin", "h"])["r"].transform("mean")
    R = R[R["f"] != 0].dropna(subset=["f", "rd"])

    def reg(d):
        if len(d) < 8 or d["f"].std() == 0:
            return pd.Series(dict(n=len(d), slope=np.nan, t=np.nan))
        s = stats.linregress(d["f"], d["rd"])
        return pd.Series(dict(n=len(d), slope=s.slope, t=s.slope / s.stderr))

    out = {}
    out["by_h"] = R.groupby("h").apply(reg)
    R14 = R[R.h == 14].copy()
    out["by_coin_h14"] = R14.groupby("coin").apply(reg)
    out["by_year_h14"] = R14.groupby("year").apply(reg)
    out["by_sign_h14"] = R14.groupby(np.sign(R14["f"])).apply(reg)
    R14["q"] = pd.qcut(R14["f"], 5, labels=False, duplicates="drop")
    out["quint_h14"] = R14.groupby("q").agg(n=("rd", "size"), fmean=("f", "mean"),
                                            rd_mean=("rd", "mean"),
                                            rd_t=("rd", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    R28 = R[R.h == 28]
    out["by_year_h28"] = R28.groupby("year").apply(reg)
    return out
