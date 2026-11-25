def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in (3, 7, 14)}
        for w, df in wins.items():
            c = df["close"].reset_index(drop=True)
            for h in (3, 7, 14):
                idx = np.arange(0, len(c) - h, h)
                allr[h] += list(c.values[idx + h] / c.values[idx] - 1)
        for h in (3, 7, 14):
            drift[(coin, h)] = np.mean(allr[h]); usual[(coin, h)] = np.std(allr[h], ddof=1)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            lr = np.log(df["close"]).diff()
            ret7 = df["close"] / df["close"].shift(7) - 1
            ret30 = df["close"] / df["close"].shift(30) - 1
            er = (df["close"] - df["close"].shift(30)).abs() / df["close"].diff().abs().rolling(30).sum()
            vol30 = lr.rolling(30).std()
            year = pd.to_datetime(df["timestamp"]).dt.year
            n = len(df)
            for i in range(0, n - 7, 7):
                rec = dict(coin=coin, win=w, year=int(year.iloc[i]),
                           sit=df["regime"].iloc[i] == "mean_reversion",
                           ret7=ret7.iloc[i], ret30=ret30.iloc[i], er=er.iloc[i],
                           z7=ret7.iloc[i] / (vol30.iloc[i] * np.sqrt(7)) if vol30.iloc[i] > 0 else np.nan,
                           fc=df["forecast"].iloc[i], day=str(df["timestamp"].iloc[i])[:10])
                for h in (3, 7, 14):
                    if i + h < n:
                        r = c[i + h] / c[i] - 1
                        rec[f"tot{h}"] = -r
                        rec[f"unu{h}"] = -(r - drift[(coin, h)])
                        rec[f"str{h}"] = rec[f"unu{h}"] / usual[(coin, h)]
                rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="unu7"):
        x = g[col].dropna()
        if len(x) < 3: return pd.Series(dict(n=len(x)))
        dd = g.groupby("day")[col].sum()
        t = x.mean() / (np.sqrt((dd - dd.mean() * 0).pow(2).sum()) / len(x)) if False else x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
        return pd.Series(dict(n=len(x), mean=x.mean(), t=t, hit=(x > 0).mean()))
    s = d[d.sit]
    out = {}
    out["situation_short_by_h"] = pd.DataFrame({h: summ(s, f"unu{h}") for h in (3, 7, 14)}).T
    out["nonsit_falls_short"] = pd.DataFrame({h: summ(d[(~d.sit) & (d.ret7 < 0)], f"unu{h}") for h in (3, 7, 14)}).T
    out["by_coin"] = s.groupby("coin").apply(summ)
    out["by_window"] = s.groupby("win").apply(summ)
    out["by_year"] = s.groupby("year").apply(summ)
    s = s.copy()
    s["er_q"] = pd.qcut(s.er, 3, labels=["lowER", "midER", "highER"])
    s["z_q"] = pd.qcut(s.z7, 3, labels=["bigfall", "midfall", "smallfall"])
    s["r30_q"] = pd.qcut(s.ret30, 3, labels=["r30low", "r30mid", "r30high"])
    out["by_er"] = s.groupby("er_q").apply(summ)
    out["by_z7"] = s.groupby("z_q").apply(summ)
    out["by_ret30"] = s.groupby("r30_q").apply(summ)
    out["corr_unu7"] = pd.Series({k: s[[k, "unu7"]].dropna().corr().iloc[0, 1] for k in ["er", "z7", "ret30", "ret7"]})
    out["fc_nonzero_share"] = float((s.fc < 0).mean())
    return out
