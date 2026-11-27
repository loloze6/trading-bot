def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            r1 = c.pct_change()
            hi = c.rolling(20, min_periods=20).max()
            sd = r1.rolling(20, min_periods=20).std()
            depth = (c / hi - 1) / sd
            tr20 = c / c.shift(20) - 1
            tr60 = c / c.shift(60) - 1
            vol30 = r1.rolling(30, min_periods=30).std()
            fwd5 = c.shift(-5) / c - 1
            fwd10 = c.shift(-10) / c - 1
            fc = b["forecast"].astype(float)
            al = b["postRebalance_current_allocation"].astype(float)
            for i in range(0, n, 5):
                if i + 5 >= n:
                    break
                rows.append(dict(coin=coin, w=w, day=str(b["timestamp"].iloc[i])[:10], up=r1.iloc[i] > 0,
                                 depth=depth.iloc[i], tr20=tr20.iloc[i], tr60=tr60.iloc[i], vol30=vol30.iloc[i],
                                 fwd5=fwd5.iloc[i], fwd10=fwd10.iloc[i] if i + 10 < n else np.nan,
                                 fc=fc.iloc[i], al=al.iloc[i]))
    d = pd.DataFrame(rows)
    d["drift5"] = d["coin"].map(d.groupby("coin")["fwd5"].mean())
    d["drift10"] = d["coin"].map(d.groupby("coin")["fwd10"].mean())
    d["u5"] = -(d["fwd5"] - d["drift5"])
    d["u10"] = -(d["fwd10"] - d["drift10"])
    d["tot5"] = -d["fwd5"]
    d["sig"] = d["up"] & (d["depth"] < 0)
    def ct(g, col):
        x = g[[col, "day"]].dropna()
        if len(x) < 5:
            return np.nan
        s = x.groupby("day")[col].apply(lambda v: (v - x[col].mean()).sum())
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / len(x)
        return x[col].mean() / se
    def summ(g):
        return pd.Series(dict(n=len(g), days=g["day"].nunique(), tot5=g["tot5"].mean(), u5=g["u5"].mean(),
                              t_u5=ct(g, "u5"), u10=g["u10"].mean(), t_u10=ct(g, "u10")))
    d["dbin"] = pd.cut(d["depth"], [-np.inf, -4, -3, -2, -1, -0.0001, np.inf],
                       labels=["<-4", "-4..-3", "-3..-2", "-2..-1", "-1..0", "0"])
    d["t20"] = pd.cut(d["tr20"], [-np.inf, -0.1, 0.0, np.inf], labels=["<-10", "-10..0", ">0"])
    out = {}
    out["sig_by_rawdepth"] = d[d.sig].groupby("dbin").apply(summ)
    out["down_by_rawdepth"] = d[~d.up].groupby("dbin").apply(summ)
    out["sig_t20_x_depth"] = d[d.sig].groupby(["t20", pd.cut(d["depth"], [-np.inf, -2.5, 0])]).apply(summ)
    out["corr_fc_depth"] = pd.Series(dict(corr=d.loc[d.sig, ["fc", "depth"]].corr().iloc[0, 1],
                                          share_fc_neg=(d.loc[d.sig, "fc"] < 0).mean(),
                                          share_alloc_neg_all=(d["al"] < 0).mean()))
    d["fcq"] = pd.qcut(d["fc"].where(d.sig), 3, labels=["strong", "mid", "weak"], duplicates="drop")
    out["sig_by_fc_tercile"] = d[d.sig].groupby("fcq").apply(summ)
    # deep cases outside any signal: book holding on non-signal bars
    d["held_nosig"] = (~d.sig) & (d["al"] < 0)
    out["held_without_signal"] = d.groupby("held_nosig").apply(summ)
    tr = pd.concat([t.assign(coin=c, w=w) for c, ws in data["trades"].items() for w, t in ws.items()])
    tr["dur"] = tr["duration_minutes"] / 1440
    tr["durb"] = pd.cut(tr["dur"], [0, 5.5, 10, 20, np.inf])
    out["trades_by_duration"] = tr.groupby("durb").agg(n=("net_profit_loss_percent", "size"),
                                                      gross=("profit_loss_percent", "mean"),
                                                      net=("net_profit_loss_percent", "mean"))
    return out
