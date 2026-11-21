import numpy as np, pandas as pd
from scipy import stats

def qc(s, k):
    s = pd.Series(s)
    out = pd.Series(np.nan, index=s.index)
    m = s.notna()
    if m.sum() >= k:
        out[m] = pd.qcut(s[m].rank(method="first"), k, labels=False)
    return out

def summ(x):
    n = len(x)
    sd = x["ex"].std()
    return pd.Series(dict(n=n, mean_ex=x["ex"].mean(),
                          t=x["ex"].mean() / (sd / np.sqrt(n)) if n > 2 and sd > 0 else np.nan))

def explore(data):
    out = {}
    H = 72
    rows = []
    hr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            cs = b["close"].astype(float)
            c = cs.values
            n = len(c)
            r1 = cs.pct_change()
            ret72 = cs / cs.shift(72) - 1
            ret24 = cs / cs.shift(24) - 1
            vol72 = r1.rolling(72).std()
            lc = np.log(cs)
            lr = lc.diff()
            eff = (lc - lc.shift(72)).abs() / lr.abs().rolling(72).sum()
            vol = b["volume"].astype(float)
            vshare = vol.rolling(72).max() / vol.rolling(72).sum()
            ts = pd.to_datetime(b["timestamp"])
            fc = b["forecast"].values
            pos = b["postRebalance_current_allocation"].values
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, fwd=c[i+H]/c[i]-1, ret72=ret72[i], ret24=ret24[i],
                                 vol=vol72[i], eff=eff[i], vshare=vshare[i], fc=fc[i], pos=pos[i],
                                 year=ts.iloc[i].year))
            nxt = cs.shift(-1) / cs - 1
            hr.append(pd.DataFrame(dict(coin=coin, w=w, hour=ts.dt.hour, wd=ts.dt.weekday, r=nxt,
                                        pos=b["postRebalance_current_allocation"])))
    g = pd.DataFrame(rows).dropna(subset=["fwd"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    for nm, col in [("past 72h return", "ret72"), ("past 24h return", "ret24"), ("72h vol", "vol")]:
        try:
            gg = g.dropna(subset=[col]).copy()
            gg["q"] = qc(gg[col], 5)
            out["fwd72 excess by " + nm + " quintile"] = gg.groupby("q").apply(summ)
        except Exception as e:
            out["err " + nm] = str(e)[:80]
    try:
        gg = g.dropna(subset=["eff", "ret72", "vshare"]).copy()
        gg["dir"] = np.sign(gg["ret72"])
        gg["qe"] = gg.groupby("dir")["eff"].transform(lambda s: qc(s, 3))
        out["fwd72 ex by dir x efficiency tercile (2=grind)"] = gg.groupby(["dir", "qe"]).apply(summ)
        gg["qs"] = gg.groupby("dir")["vshare"].transform(lambda s: qc(s, 3))
        out["fwd72 ex by dir x vol-burst tercile (2=burst)"] = gg.groupby(["dir", "qs"]).apply(summ)
        gg["qv"] = qc(gg["vol"], 3)
        out["fwd72 ex by dir x vol tercile"] = gg.groupby(["dir", "qv"]).apply(summ)
    except Exception as e:
        out["err shape"] = str(e)[:80]
    try:
        a = g[g["fc"] > 0].copy()
        a["qf"] = qc(a["fc"], 5)
        out["active: ex by forecast quintile"] = a.groupby("qf").apply(summ)
        out["active vs inactive"] = g.groupby(g["fc"] > 0).apply(summ)
        out["active by coin"] = a.groupby("coin").apply(summ)
        out["active by year"] = a.groupby("year").apply(summ)
        out["mean position active/inactive"] = g.groupby(g["fc"] > 0)["pos"].mean()
    except Exception as e:
        out["err active"] = str(e)[:80]
    try:
        d = []
        for coin, wins in data["days"].items():
            for w, x in wins.items():
                x = x.copy(); x["coin"] = coin; x["w"] = w; d.append(x)
        d = pd.concat(d)
        bk = d.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
        out["book daily"] = pd.Series(dict(mean=bk["book_return"].mean(), hold=bk["coin_return"].mean(),
                                           sharpe=bk["book_return"].mean()/bk["book_return"].std()*np.sqrt(365),
                                           corr_with_hold=bk["book_return"].corr(bk["coin_return"]), n=len(bk)))
        bk2 = bk.reset_index()
        bk2["wnum"] = bk2["w"].str[1:].astype(int)
        out["book by window"] = bk2.groupby("wnum").agg(book=("book_return", "mean"), hold=("coin_return", "mean"), n=("book_return", "size"))
    except Exception as e:
        out["err book"] = str(e)[:80]
    try:
        h = pd.concat(hr).dropna()
        h["gain"] = h["pos"] * h["r"]
        hm = h.groupby("hour").agg(r=("r", "mean"), gain=("gain", "mean"), n=("r", "size"))
        hm["t_r"] = h.groupby("hour")["r"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s))))
        out["by hour"] = hm
        wm = h.groupby("wd").agg(r=("r", "mean"), gain=("gain", "mean"))
        wm["t_r"] = h.groupby("wd")["r"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s))))
        out["by weekday"] = wm
        mu = h.groupby("coin")["r"].transform("mean")
        out["hourly gain: total vs market part"] = pd.Series(dict(gain=h["gain"].mean(), market=(h["pos"]*mu).mean(),
                                                                  mean_pos=h["pos"].mean()))
    except Exception as e:
        out["err hour"] = str(e)[:80]
    try:
        t = pd.concat([x.assign(coin=c) for c, ws in data["trades"].items() for x in ws.values()])
        out["trades"] = pd.Series(dict(n=len(t), mean_gross=t["profit_loss_percent"].mean(), mean_net=t["net_profit_loss_percent"].mean(),
                                       med_dur_h=t["duration_minutes"].median()/60, win=(t["net_profit_loss_percent"]>0).mean(),
                                       mean_comm=t["total_commission"].mean()))
    except Exception as e:
        out["err trades"] = str(e)[:80]
    return out
