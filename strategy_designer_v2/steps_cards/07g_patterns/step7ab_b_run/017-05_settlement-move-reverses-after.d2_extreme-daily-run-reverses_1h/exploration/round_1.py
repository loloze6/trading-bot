import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    out = {}
    # 1. forecast-signed forward returns by forecast bucket, several horizons (non-overlapping)
    rows = []
    hz = [24, 72, 120, 240]
    for coin, wins in bars.items():
        for w, b in wins.items():
            c = b["close"].values; f = b["forecast"].values
            r1 = np.log(c[1:]/c[:-1])
            vol = pd.Series(np.r_[np.nan, r1]).rolling(168, min_periods=84).std().values
            ret24 = np.r_[np.full(24, np.nan), c[24:]/c[:-24]-1]
            z = ret24/(vol*np.sqrt(24))
            for h in hz:
                idx = np.arange(0, len(c)-h, h)
                fr = c[idx+h]/c[idx]-1
                for i, v in zip(idx, fr):
                    rows.append((coin, w, h, z[i], f[i], v, vol[i]))
    df = pd.DataFrame(rows, columns=["coin","w","h","z","f","fr","vol"]).dropna()
    df["drift"] = df.groupby(["coin","h"])["fr"].transform("mean")
    df["ex"] = df["fr"]-df["drift"]
    res = []
    for h in hz:
        d = df[df.h==h].copy()
        d["zb"] = pd.qcut(d["z"], 10, labels=False)
        g = d.groupby("zb")["ex"]
        t = g.mean()/(g.std()/np.sqrt(g.count()))
        for k in g.mean().index:
            res.append((h, k, round(d[d.zb==k]["z"].mean(),2), g.count()[k], round(g.mean()[k]*1e4,1), round(t[k],2)))
    out["excess fwd ret (bps) by z24 decile, horizon h"] = pd.DataFrame(res, columns=["h","dec","zmean","n","ex_bps","t"])
    # vol level: 24h fwd return by vol tercile per coin
    d = df[df.h==24].copy()
    d["vb"] = d.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
    d["s_ex"] = -np.sign(d["z"])*d["ex"]*(d["z"].abs()>1.5)
    g = d[d.z.abs()>1.5].groupby("vb")["s_ex"]
    out["reversal of |z|>1.5 by vol tercile (bps,t,n)"] = pd.DataFrame({"bps": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count()})
    # 2. hour of day: mean 1h return, t, volume ratio
    hr = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            ts = pd.to_datetime(b["timestamp"])
            r = b["close"].pct_change()
            v = b["volume"]/b["volume"].rolling(24, min_periods=12).mean()
            hr.append(pd.DataFrame({"hour": ts.dt.hour, "wd": ts.dt.weekday, "r": r, "v": v, "coin": coin}))
    H = pd.concat(hr).dropna()
    H["r"] = H["r"] - H.groupby("coin")["r"].transform("mean")
    g = H.groupby("hour")
    out["hour of day: excess 1h ret bps, t, rel volume"] = pd.DataFrame({"bps": g["r"].mean()*1e4, "t": g["r"].mean()/(g["r"].std()/np.sqrt(g["r"].count())), "relvol": g["v"].mean()})
    g = H.groupby("wd")
    out["weekday: excess 1h ret bps, t, rel vol"] = pd.DataFrame({"bps": g["r"].mean()*1e4, "t": g["r"].mean()/(g["r"].std()/np.sqrt(g["r"].count())), "relvol": g["v"].mean()})
    # 3. book: daily returns by coin, by window, timing vs market
    D = []
    for coin, wins in days.items():
        for w, dd in wins.items():
            D.append(dd.assign(coin=coin, w=w))
    D = pd.concat(D).dropna(subset=["book_return"])
    g = D.groupby("coin")
    out["book by coin"] = pd.DataFrame({"book_mean_bps": g["book_return"].mean()*1e4, "coin_mean_bps": g["coin_return"].mean()*1e4,
                                        "sharpe": g["book_return"].mean()/g["book_return"].std()*np.sqrt(365), "corr": g.apply(lambda x: x["book_return"].corr(x["coin_return"]))})
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()])
    out["trades by side"] = T.groupby("side").agg(n=("net_profit_loss_percent","size"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"), dur_h=("duration_minutes", lambda s: s.mean()/60))
    return out
