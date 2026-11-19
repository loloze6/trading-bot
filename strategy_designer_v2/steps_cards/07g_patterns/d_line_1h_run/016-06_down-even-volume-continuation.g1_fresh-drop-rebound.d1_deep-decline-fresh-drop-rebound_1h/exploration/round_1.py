import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    H = 72
    rows = []
    hr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            r1 = pd.Series(c).pct_change()
            ret72 = pd.Series(c) / pd.Series(c).shift(72) - 1
            ret24 = pd.Series(c) / pd.Series(c).shift(24) - 1
            vol72 = r1.rolling(72).std()
            maxabs = r1.abs().rolling(72).max()
            # path efficiency: |net log move| / sum |log steps|
            lr = np.log(pd.Series(c)).diff()
            eff = (np.log(pd.Series(c)) - np.log(pd.Series(c)).shift(72)).abs() / lr.abs().rolling(72).sum()
            vshare = b["volume"].rolling(72).max() / b["volume"].rolling(72).sum()
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, fwd=c[i+H]/c[i]-1, ret72=ret72[i], ret24=ret24[i],
                                 vol=vol72[i], eff=eff[i], vshare=vshare[i], fc=b["forecast"].iloc[i],
                                 reg=b["regime"].iloc[i], year=ts.iloc[i].year))
            nxt = pd.Series(c).shift(-1) / pd.Series(c) - 1
            hr.append(pd.DataFrame(dict(coin=coin, hour=ts.dt.hour, wd=ts.dt.weekday, r=nxt,
                                        pos=b["postRebalance_current_allocation"], absr1=r1.abs())))
    g = pd.DataFrame(rows).dropna(subset=["fwd", "ret72"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    def summ(x):
        return pd.Series(dict(n=len(x), mean_ex=x["ex"].mean(), t=x["ex"].mean()/(x["ex"].std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    g["q72"] = pd.qcut(g["ret72"], 5, labels=False)
    out["fwd72 excess by past 72h return quintile"] = g.groupby("q72").apply(summ)
    g["q24"] = pd.qcut(g["ret24"], 5, labels=False)
    out["fwd72 excess by past 24h return quintile"] = g.groupby("q24").apply(summ)
    g["qv"] = pd.qcut(g["vol"], 5, labels=False)
    out["fwd72 excess by vol quintile"] = g.groupby("qv").apply(summ)
    gg = g.dropna(subset=["eff"]).copy()
    gg["dir"] = np.sign(gg["ret72"])
    gg["qe"] = gg.groupby("dir")["eff"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["fwd72 excess by direction x efficiency tercile (2=grind)"] = gg.groupby(["dir", "qe"]).apply(summ)
    gg["qs"] = gg.groupby("dir")["vshare"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["fwd72 excess by direction x volume-burst tercile (2=burst)"] = gg.groupby(["dir", "qs"]).apply(summ)
    a = g[g["fc"] > 0].copy()
    a["qf"] = pd.qcut(a["fc"], 5, labels=False, duplicates="drop")
    out["active: excess by forecast quintile"] = a.groupby("qf").apply(summ)
    out["active vs inactive"] = g.groupby(g["fc"] > 0).apply(summ)
    out["active by coin"] = a.groupby("coin").apply(summ)
    out["active by year"] = a.groupby("year").apply(summ)
    # book
    d = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; d.append(x)
    d = pd.concat(d)
    bk = d.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book daily"] = pd.Series(dict(mean=bk["book_return"].mean(), hold=bk["coin_return"].mean(),
                                       sharpe=bk["book_return"].mean()/bk["book_return"].std()*np.sqrt(365), n=len(bk)))
    h = pd.concat(hr).dropna()
    h["gain"] = h["pos"] * h["r"]
    hm = h.groupby("hour").agg(r=("r", "mean"), gain=("gain", "mean"), n=("r", "size"))
    hm["t_r"] = h.groupby("hour")["r"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s))))
    out["by hour"] = hm
    wm = h.groupby("wd").agg(r=("r", "mean"), gain=("gain", "mean"))
    wm["t_r"] = h.groupby("wd")["r"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s))))
    out["by weekday"] = wm
    # trades
    t = pd.concat([x.assign(coin=c) for c, ws in data["trades"].items() for x in ws.values()])
    out["trades"] = pd.Series(dict(n=len(t), mean_gross=t["profit_loss_percent"].mean(), mean_net=t["net_profit_loss_percent"].mean(),
                                   med_dur_h=t["duration_minutes"].median()/60, win=(t["net_profit_loss_percent"]>0).mean()))
    return out
