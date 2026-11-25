def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            f = df["forecast"].fillna(0).values
            reg = df["regime"].astype(str).values
            r1 = pd.Series(c).pct_change()
            sd30 = r1.rolling(30).std()
            r7 = pd.Series(c).pct_change(7)
            sc = (r7 / (sd30 * np.sqrt(7))).values
            for h in [7, 14]:
                for i in range(0, n - h, 7):
                    rows.append(dict(coin=coin, w=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                     day=pd.Timestamp(df["timestamp"].iloc[i]).floor("D"),
                                     h=h, f=f[i], inprof=(reg[i] == "unknown"), sc=sc[i],
                                     ret=c[i + h] / c[i] - 1))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby(["coin", "h"])["ret"].transform("mean")
    R["ex"] = R["ret"] - R["drift"]

    def summ(g):
        if len(g) < 3:
            return pd.Series(dict(n=len(g), days=np.nan, mean_ex=np.nan, t_day=np.nan, mean_tot=np.nan))
        m = g["ex"].mean()
        dev = (g["ex"] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(g) * np.sqrt(len(dev) / max(len(dev) - 1, 1))
        return pd.Series(dict(n=len(g), days=len(dev), mean_ex=m, t_day=m / se if se > 0 else np.nan,
                              mean_tot=g["ret"].mean()))
    out = {}
    P = R[R.inprof].dropna(subset=["sc"]).copy()
    P["bin"] = pd.cut(P["sc"], [-np.inf, 0, 0.5, 1.0, 1.5, np.inf], labels=["<=0", "0-0.5", "0.5-1", "1-1.5", ">1.5"])
    out["inprof_by_scaled_bin_h"] = P.groupby(["h", "bin"]).apply(summ)
    P7 = P[P.h == 7]
    top = P7[P7.sc > P7.sc.quantile(0.8)]
    out["top20_by_year"] = top.groupby("year").apply(summ)
    out["top20_by_coin_mean"] = top.groupby("coin")["ex"].agg(["count", "mean"])
    pos = P7[P7.sc > 0]
    out["pos_slope_ex_on_sc"] = float(np.polyfit(pos.sc, pos.ex, 1)[0])
    out["pos_n"] = int(len(pos))
    return out
