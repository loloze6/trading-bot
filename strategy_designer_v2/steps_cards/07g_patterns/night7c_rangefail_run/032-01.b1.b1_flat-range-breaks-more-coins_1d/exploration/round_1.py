def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for H in (5, 10, 20):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    rs.append(c[i + H] / c[i] - 1)
            drift[(coin, H)] = (np.mean(rs) if rs else np.nan, np.std(rs, ddof=1) if len(rs) > 1 else np.nan)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; h = df["high"]; l = df["low"]
            r1 = c.pct_change()
            ret20 = c / c.shift(20) - 1
            ret5 = c / c.shift(5) - 1
            ret60 = c / c.shift(60) - 1
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60).std()
            er20 = (c - c.shift(20)).abs() / c.diff().abs().rolling(20).sum()
            er60 = (c - c.shift(60)).abs() / c.diff().abs().rolling(60).sum()
            hi20 = h.shift(1).rolling(20).max(); lo20 = l.shift(1).rolling(20).min()
            hi60 = h.shift(1).rolling(60).max(); lo60 = l.shift(1).rolling(60).min()
            pos20 = (c - lo20) / (hi20 - lo20)
            rng = (h - l) / c
            rngz = rng / rng.rolling(20).mean()
            volz = df["volume"] / df["volume"].rolling(20).mean()
            wd = pd.to_datetime(df["timestamp"]).dt.weekday
            for H in (5, 10, 20):
                d, sd = drift[(coin, H)]
                for i in range(0, len(c) - H, H):
                    fr = c.iloc[i + H] / c.iloc[i] - 1
                    rows.append(dict(coin=coin, win=w, H=H, i=i, fr=fr, un=fr - d, st=(fr - d) / sd,
                        ret5=ret5.iloc[i], ret20=ret20.iloc[i], ret60=ret60.iloc[i], vol20=vol20.iloc[i],
                        volratio=vol20.iloc[i] / vol60.iloc[i] if vol60.iloc[i] else np.nan,
                        er20=er20.iloc[i], er60=er60.iloc[i], pos20=pos20.iloc[i],
                        brk60=c.iloc[i] / hi60.iloc[i] - 1, brkd60=c.iloc[i] / lo60.iloc[i] - 1,
                        rngz=rngz.iloc[i], volz=volz.iloc[i], r1=r1.iloc[i], wd=wd.iloc[i],
                        fc=df["forecast"].iloc[i]))
    S = pd.DataFrame(rows)
    out = {}
    def qtab(H, col, q=5):
        s = S[(S.H == H)].dropna(subset=[col, "un"]).copy()
        s["q"] = pd.qcut(s[col].rank(method="first"), q, labels=False)
        g = s.groupby("q").agg(n=("un", "size"), lo=(col, "min"), hi=(col, "max"), un=("un", "mean"), st=("st", "mean"),
                               t=("un", lambda x: x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))))
        return g.round(4)
    for col in ["ret20", "ret5", "r1", "vol20", "volratio", "er20", "pos20", "rngz", "volz"]:
        for H in (5, 20):
            out[f"{col}_H{H}"] = qtab(H, col)
    for col in ["ret60", "er60", "brk60", "brkd60"]:
        out[f"{col}_H20"] = qtab(20, col, 4)
    s = S[S.H == 5]
    out["wd_H5"] = s.groupby("wd").agg(n=("un", "size"), un=("un", "mean")).round(4)
    # book days
    D = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df.copy(); x["coin"] = coin; x["win"] = w; D.append(x)
    D = pd.concat(D)
    bk = D.groupby(["win", "day"]).agg(b=("book_return", "mean"), c=("coin_return", "mean")).dropna()
    out["book_by_win"] = bk.groupby(level=0).agg(n=("b", "size"), b=("b", "mean"), c=("c", "mean")).round(5)
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, df in wins.items():
            x = df.copy(); x["coin"] = coin; T.append(x)
    T = pd.concat(T)
    out["trades_by_coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"), m=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda x: (x > 0).mean())).round(3)
    T["fq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades_by_fq"] = T.groupby("fq").agg(n=("net_profit_loss_percent", "size"), lo=("entry_forecast", "min"), m=("net_profit_loss_percent", "mean"), med=("net_profit_loss_percent", "median")).round(3)
    return out
