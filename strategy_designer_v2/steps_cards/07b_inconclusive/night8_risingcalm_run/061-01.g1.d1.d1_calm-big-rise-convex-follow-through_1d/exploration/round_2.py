import numpy as np, pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            r = c.pct_change()
            vsr = r / r.rolling(30, min_periods=20).std()
            reg = df["regime"].astype(str)
            fc = df["forecast"].astype(float).fillna(0)
            fcp = fc.shift(1).fillna(0)
            n = len(df)
            for i in range(n):
                f5 = c.iloc[i + 5] / c.iloc[i] - 1 if i + 5 < n else np.nan
                f10 = c.iloc[i + 10] / c.iloc[i] - 1 if i + 10 < n else np.nan
                f1 = c.iloc[i + 1] / c.iloc[i] - 1 if i + 1 < n else np.nan
                rows.append(dict(coin=coin, w=w, i=i, day=str(df["timestamp"].iloc[i])[:10],
                                 year=str(df["timestamp"].iloc[i])[:4], vsr=vsr.iloc[i], reg=reg.iloc[i],
                                 fc=fc.iloc[i], fcp=fcp.iloc[i], f1=f1, f5=f5, f10=f10,
                                 grid=(i % 5 == 0)))
    d = pd.DataFrame(rows)
    allg = d[d.grid].dropna(subset=["f5"])
    drift5 = allg.groupby("coin")["f5"].mean()
    d["ex5"] = d["f5"] - d["coin"].map(drift5)
    g10 = d[d.i % 10 == 0].dropna(subset=["f10"]).groupby("coin")["f10"].mean()
    d["ex10"] = d["f10"] - d["coin"].map(g10)

    def ct(x, g):
        x = np.asarray(x, float); m = x.mean(); n = len(x)
        s = pd.Series(x - m).groupby(np.asarray(g)).sum(); G = len(s)
        if G < 3: return np.nan
        return m / (np.sqrt(G / (G - 1) * (s ** 2).sum()) / n)

    def summ(sub, col="ex5"):
        sub = sub.dropna(subset=[col])
        return pd.Series(dict(n=len(sub), mean=sub[col].mean(), t=ct(sub[col], sub["day"]) if len(sub) > 2 else np.nan))

    out = {}
    tr = d[d.reg == "trending"]
    out["trending_all_bars_ex5"] = summ(tr)
    out["trending_all_bars_ex10"] = summ(tr, "ex10")
    out["trending_by_vsr"] = tr.groupby(pd.cut(tr.vsr, [1, 1.5, 2, 3, np.inf]).astype(str)).apply(summ)
    out["trending_fc_pos_vs_zero"] = tr.groupby(tr.fc > 0).apply(summ)
    out["trending_by_year"] = tr.groupby("year").apply(summ)
    out["trending_by_coin"] = tr.groupby("coin").apply(summ)
    # entries: forecast rises from <=0
    ent = d[(d.fc > 0) & (d.fcp <= 0)]
    out["entries_ex5"] = summ(ent)
    out["entries_regime"] = ent["reg"].value_counts()
    pos = d[d.fc > 0]
    out["fcpos_bars_regime"] = pos["reg"].value_counts()
    out["fcpos_bars_ex5"] = summ(pos)
    # big up days in choppy calm proxy = not chop: compare trending vs big up in chop
    bigchop = d[(d.reg == "chop") & (d.vsr >= 1)]
    out["bigup_outside_profile_ex5"] = summ(bigchop)
    # trades
    t = []
    for coin, wins in data["trades"].items():
        for w, tdf in wins.items():
            if len(tdf): t.append(tdf.assign(coin=coin))
    T = pd.concat(t)
    out["trades"] = pd.Series(dict(n=len(T), mean_pl=T.profit_loss_percent.mean(),
                                   mean_net=T.net_profit_loss_percent.mean(),
                                   mean_dur_days=T.duration_minutes.mean() / 1440,
                                   win=(T.profit_loss_percent > 0).mean()))
    out["trades_by_entry_regime"] = T.groupby("entry_regime")["profit_loss_percent"].agg(["count", "mean"])
    return out
